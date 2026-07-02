import importlib
import os

TOOLS = {}

def load_tools(force=False):
    global TOOLS

    if TOOLS and not force:
        return list(TOOLS.values())

    TOOLS.clear()

    tools_path = os.path.join(os.path.dirname(__file__), "tools")

    for file in os.listdir(tools_path):
        if file.endswith(".py") and file != "__init__.py":

            module_name = f"src.tools.{file[:-3]}"
            module = importlib.import_module(module_name)

            name = module.name()

            TOOLS[name] = {
                "name": name,
                "description": module.description(),
                "category": module.category(),
                "run": module.run
            }

    return list(TOOLS.values())
