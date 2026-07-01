import importlib
import os

def load_tools():
    tools = []
    tool_dir = os.path.join(os.path.dirname(__file__), "tools")

    for file in os.listdir(tool_dir):
        if file.endswith(".py") and file != "__init__.py":
            module_name = file[:-3]
            module = importlib.import_module(f"src.tools.{module_name}")

            tools.append({
                "name": module.name(),
                "description": module.description(),
                "category": module.category(),
                "run": module.run
            })

    return tools
