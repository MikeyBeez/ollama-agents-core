# agents/simple_agent.py

import logging
from config import USER_NAME, AGENT_NAME, LOG_FILE, LOG_LEVEL, DEFAULT_MODEL
from utils.initialize_db import initialize_database
from src.modules.ollama_client import generate_response

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
        return generate_response(user_input, self.model, self.user_name)

def main():
    initialize_database()
    agent = SimpleAgent()
    print(f"{agent.agent_name}: Hello! I'm an AI assistant. How can I help you today?")

    while True:
        user_input = input(f"{agent.user_name}> ").strip()

        if user_input.startswith('/'):
            command = user_input[1:].lower()
            if command in ['q', 'quit', 'exit']:
                print(f"{agent.agent_name}: Goodbye! Have a great day!")
                break
            elif command == 'help':
                print("Available commands:")
                print("/q, /quit, /exit - Exit the program")
                print("/help - Display this help message")
                continue
            else:
                print(f"Unknown command: {command}")
        else:
            response = agent.respond(user_input)
            print(response)

if __name__ == "__main__":
    main()
