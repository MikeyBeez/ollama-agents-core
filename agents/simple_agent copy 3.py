# agents/simple_agent.py

import sys
from pathlib import Path

# Add necessary directories to Python path
project_root = Path(__file__).resolve().parent.parent
ollama_agents_data_dir = Path.home() / "ollama-agents-data"
sys.path.insert(0, str(ollama_agents_data_dir))  # Prioritize ollama-agents-data for imports
sys.path.append(str(project_root))

print(f"Python path in simple_agent.py: {sys.path}")

import logging
from config import USER_NAME, AGENT_NAME, LOG_FILE, LOG_LEVEL, DEFAULT_MODEL
from utils.initialize_db import initialize_database
from src.modules.input import get_user_input
from src.modules.ollama_client import generate_response
from src.modules.save_history import save_interaction

print(f"Config loaded from: {ollama_agents_data_dir / 'config.py'}")
print(f"USER_NAME: {USER_NAME}")
print(f"AGENT_NAME: {AGENT_NAME}")
print(f"LOG_FILE: {LOG_FILE}")
print(f"DEFAULT_MODEL: {DEFAULT_MODEL}")

# Try to import ollama_agents_knowledge
try:
    import ollama_agents_knowledge as oak
    print("Successfully imported ollama_agents_knowledge")
except ImportError as e:
    print(f"Failed to import ollama_agents_knowledge: {e}")
    oak = None

# Set up logging
logging.basicConfig(filename=LOG_FILE, level=LOG_LEVEL,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

print(f"Logging setup complete. Log file: {LOG_FILE}")

class SimpleAgent:
    def __init__(self):
        self.user_name = USER_NAME
        self.agent_name = AGENT_NAME
        self.model = DEFAULT_MODEL

    def respond(self, user_input):
        response = generate_response(user_input, self.model, self.user_name)
        save_interaction(user_input, response, self.user_name, self.model)

        if oak:
            try:
                extracted_knowledge = oak.knowledge_extraction.extract_knowledge(user_input)
                logger.info(f"Extracted knowledge: {extracted_knowledge}")

                prompt_id = oak.kb_graph.create_node(user_input)
                response_id = oak.kb_graph.create_node(response)
                oak.kb_graph.create_edge(prompt_id, response_id, "RESPONSE_TO", 1.0)

                oak.memory_search.save_memory("interaction", {"prompt": user_input, "response": response}, self.user_name, self.model)
            except Exception as e:
                logger.error(f"Error in ollama_agents_knowledge operations: {e}")

        return response

def main():
    initialize_database()
    agent = SimpleAgent()
    print(f"{agent.agent_name}: Hello! I'm an AI assistant. How can I help you today?")
    print("Type /h or /help for available commands.")

    while True:
        user_input = get_user_input()

        if user_input is None:
            print(f"{agent.agent_name}: Goodbye! Have a great day!")
            break
        elif user_input == 'CONTINUE':
            continue
        else:
            response = agent.respond(user_input)
            print(response)

            if oak:
                try:
                    related_memories = oak.memory_search.search_memories(user_input, top_k=3, similarity_threshold=0.5)
                    if related_memories:
                        print("Related memories:")
                        for memory in related_memories:
                            print(f"- {memory['content']}")
                except Exception as e:
                    logger.error(f"Error searching memories: {e}")

if __name__ == "__main__":
    main()
