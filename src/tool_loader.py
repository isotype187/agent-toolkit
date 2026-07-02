import importlib
import os

TOOLS = {}


def load_tools():
    global TOOLS

    if TOOLS:
        return list(TOOLS.values())

    tools_path = os.path.join(os.path.dirname(__file__), "tools")

    for file in os.listdir(tools_path):
        if file.endswith(".py") and file != "__init__.py":
            module_name = f"src.tools.{file[:-3]}"

            module = importlib.import_module(module_name)

            tool_name = module.name()

            # ?? CRITICAL FIX: prevent duplicate registration
            if tool_name in TOOLS:
                continue

            TOOLS[tool_name] = {
                "name": tool_name,
                "description": module.description(),
                "category": module.category(),
                "run": module.run
            }

    return list(TOOLS.values())
