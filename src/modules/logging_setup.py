import logging
import sys
from pathlib import Path

print(f"Python version: {sys.version}")
print(f"sys.path: {sys.path}")

shared_config_dir = Path.home() / "ollama-agents-data"
sys.path.insert(0, str(shared_config_dir))
print(f"Inserted {shared_config_dir} into sys.path")

try:
    from config import LOG_FILE, LOG_LEVEL
    print(f"Imported from config: LOG_FILE={LOG_FILE}, LOG_LEVEL={LOG_LEVEL}")
except ImportError as e:
    print(f"Error importing config: {e}")
    raise

def setup_logging():
    print(f"Setting up logging with LOG_FILE: {LOG_FILE}")
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename=str(LOG_FILE),
        filemode='a'
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(console_handler)

    print(f"Logging setup complete. Log file: {LOG_FILE}")
    return logger

logger = setup_logging()

def get_logger(name):
    return logging.getLogger(name)

if __name__ == "__main__":
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

    module_logger = get_logger("test_module")
    module_logger.info("This is a module-specific log message")
