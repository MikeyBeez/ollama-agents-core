# Ollama Agents Core

This package contains the core functionality for Ollama Agents, including the Ollama client, input handling, and other essential modules.

## Installation

To install for development:

```
pip install -e .[dev]
```

## Running Tests

To run tests:

```
pytest tests/
```
EOF
```

5. Set up a virtual environment and install the package:

```bash
cd ollama-agents-core
python3 -m venv venv
source venv/bin/activate
pip install -e .[dev]
```

6. Run the tests:

```bash
pytest tests/
```

If you encounter any import errors or missing dependencies, you may need to adjust the `setup.py` file or install additional packages.

This setup should give you a working `ollama-agents-core` package that you can run tests on. It includes the essential modules needed for the Ollama client and input handling.

Remember that you might need to adjust some imports in the test files or modules if they were referencing modules in a different structure in the original Ollama_Agents project. Also, ensure that the `config.py` file has all the necessary configurations for the tests to run successfully.
