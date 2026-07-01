import os

TOOLS_PATH = os.path.join(
    os.path.dirname(__file__),
    "tools"
)


def create_tool(name, description, category, action_code):

    safe_name = name.lower().replace(" ", "_")

    file_path = os.path.join(TOOLS_PATH, f"{safe_name}.py")

    code = f'''
def name():
    return "{name}"

def description():
    return "{description}"

def category():
    return "{category}"

def run():
{action_code}
'''

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    return f"Tool '{name}' created."
