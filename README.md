# Master In Prompts using Python

## Overview

This repository provides a comprehensive guide on mastering prompt engineering using Python. It covers various techniques and styles of prompting, including zero-shot, few-shot, chain-of-thought, self-consistency, persona-based, and role-playing prompting. The examples demonstrate how to interact with language models like OpenAI's GPT and Gemini.

## Features

- **Alpaca Prompting**: Learn how to structure prompts for effective communication with language models.
- **INST Format (LLaMA-2)**: Understand the use of special tokens to guide model responses.
- **ChatML (OpenAI)**: Explore OpenAI's format for structuring conversations.
- **Zero-shot and Few-shot Prompting**: Discover techniques for providing context to models with minimal examples.
- **Chain of Thought**: Encourage models to break down problems into logical steps.
- **Self-consistency Prompting**: Generate multiple responses and select the most consistent one.
- **Persona-based and Role-playing Prompting**: Instruct models to respond as specific characters or professionals.

## Getting Started

### Prerequisites

- Python 3.x
- OpenAI API key
- Gemini API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/imhbm/masterinprompting.git
   cd masterinprompting
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. Configure your API keys in the script:
   ```python
   openai_api_key = 'your_openai_api_key'
   gemini_api_key = 'your_gemini_api_key'
   ```

2. Run the examples:
   ```bash
   python example_script.py
   ```

## Examples

- **Zero-shot Prompting**: Ask a question without providing examples.
- **Few-shot Prompting**: Provide a few examples to guide the model.
- **Chain of Thought**: Encourage step-by-step reasoning.
- **Persona-based Prompting**: Simulate responses from a specific character.

## Contributing

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the advancements in AI and prompt engineering.
- Special thanks to the contributors and the open-source community.

For more information, visit the [project repository](https://github.com/imhbm/masterinprompting).
