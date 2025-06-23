# Prompt Parser README

This repository contains a prompt parser that converts `agentPrompt.txt` into a structured JSON format stored in `output.json`. The parser is implemented in `prompt_parser.py`.

## Files Overview
- `agentPrompt.txt`: The input file containing the raw prompt data.
- `prompt_parser.py`: The Python script that parses `agentPrompt.txt` and generates `output.json`.
- `output.json`: The generated JSON file containing the parsed data.
- `README.md`: This file, explaining the conversion process.

## Conversion Process
1. The parser reads `agentPrompt.txt` line by line.
2. It processes each line to extract relevant information (like system prompts, user messages, etc.).
3. The extracted data is structured into a JSON format.
4. The structured data is written to `output.json`.

## Usage
To run the parser, execute the following command in the terminal:
```python
python prompt_parser.py
```
This will read `agentPrompt.txt` and update `output.json` with the parsed data.

## Note
Ensure that any changes to `agentPrompt.txt` are correctly formatted to avoid parsing errors.
