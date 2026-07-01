import os
import re

TOOLS_PATH = os.path.join(
    os.path.dirname(__file__),
    "tools"
)


def sanitize(name: str):
    return re.sub(r"[^a-zA-Z0-9_ ]", "", name).strip()


def to_filename(name: str):
    return name.lower().replace(" ", "_") + ".py"


def create_tool_from_prompt(prompt: str):

    prompt = sanitize(prompt)

    # --- VERY SIMPLE INTENT PARSER (v2 baseline brain)
    name = prompt.title()

    description = f"Auto-generated tool: {prompt}"

    category = "Generated"

    # crude behavior mapping (we improve later with real AI)
    if "git" in prompt.lower():
        action = '''
    import subprocess
    result = subprocess.run(["git", "--version"], capture_output=True, text=True)
    return result.stdout
'''
    elif "system" in prompt.lower():
        action = '''
    import platform
    return platform.platform()
'''
    else:
        action = '''
    return "Tool executed (no behavior defined yet)"
'''

    code = f'''
def name():
    return "{name}"

def description():
    return "{description}"

def category():
    return "{category}"

def run():
{action}
'''

    file_path = os.path.join(TOOLS_PATH, to_filename(prompt))

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    return f"Tool created: {name}"
