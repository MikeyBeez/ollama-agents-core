from setuptools import setup, find_packages

setup(
    name="ollama_agents_core",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "rich",
        "prompt_toolkit",
        "requests",
        # Add other dependencies as needed
    ],
    extras_require={
        "dev": [
            "pytest",
            # Other development dependencies
        ],
    },
)
