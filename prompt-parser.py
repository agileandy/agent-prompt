import json
import re
import os

def parse_agent_prompt(text):
    """
    Parses a block of text representing a single agent's prompt
    and returns a dictionary in the rooCode format.
    """
    header_pattern = r"\n\n\*\*(?:Core Directives|Task Completion Criteria|Constraints|Protocols):\*\*"
    role_match = re.search(r"### \d+\. (.*?)\n(.*?)(?=" + header_pattern + "|$)", text, re.DOTALL)
    
    if not role_match:
        simple_role_match = re.search(r"### \d+\. (.*)", text)
        if not simple_role_match:
            return None
        role_name = simple_role_match.group(1).strip()
        role_description = ""
    else:
        role_name = role_match.group(1).strip()
        role_description = role_match.group(2).strip()

    def get_section(name, text_block):
        pattern = r"\*\*" + re.escape(name) + r":\*\*\n(.*?)(?=\n\n\*\*|$)"
        match = re.search(pattern, text_block, re.DOTALL)
        return match.group(1).strip() if match else ""

    def get_yaml_section(name, text_block):
        pattern = r"\*\*" + re.escape(name) + r":\*\*\n```yaml\n(.*?)\n```"
        match = re.search(pattern, text_block, re.DOTALL)
        return match.group(1).strip() if match else ""

    main_tasks = get_section("Core Directives", text)
    definition_of_done = get_yaml_section("Task Completion Criteria", text)
    constraints = get_section("Constraints", text)
    protocols = get_section("Protocols", text)

    slug_base = role_name.split('(')[0].strip().lower()
    slug = re.sub(r'[^a-z0-9]', '', slug_base)

    custom_instructions_parts = [main_tasks, definition_of_done, constraints, protocols]
    custom_instructions = "\n\n".join(part for part in custom_instructions_parts if part)

    roo_format = {
        "slug": slug,
        "name": role_name,
        "roleDefinition": f"Role: {role_name}\n{role_description}".strip(),
        "customInstructions": custom_instructions,
        "groups": ["read", "edit", "browser", "command", "mcp"],
        "source": "global"
    }
    return roo_format

def main():
    """
    Main function to read the input file, parse it, and write the output JSON.
    """
    input_filename = 'agentPrompt.txt'
    output_filename = 'output.json'

    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_filepath = os.path.join(script_dir, input_filename)
    output_filepath = os.path.join(script_dir, output_filename)

    try:
        with open(input_filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_filepath}")
        return

    prompts_start_marker = "## Agent System Prompts"
    prompts_start_index = content.find(prompts_start_marker)
    if prompts_start_index == -1:
        print("Error: '## Agent System Prompts' marker not found.")
        return
    
    agent_content = content[prompts_start_index + len(prompts_start_marker):]
    agent_blocks = agent_content.split('---')

    all_agents_json = []
    for block in agent_blocks:
        if block.strip():
            parsed_data = parse_agent_prompt(block)
            if parsed_data:
                all_agents_json.append(parsed_data)

    with open(output_filepath, 'w', encoding='utf-8') as f:
        json.dump(all_agents_json, f, indent=2)

    print(f"Successfully converted {len(all_agents_json)} agent prompts.")
    print(f"Output saved to {output_filepath}")

if __name__ == "__main__":
    main()
