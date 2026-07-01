import importlib
import os
import sys


# FORCE project root into Python path
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


TOOLS_DIR = os.path.join(PROJECT_ROOT, "src", "tools")


def load_tools():

    tools = []

    for file in os.listdir(TOOLS_DIR):

        if file.endswith(".py") and file != "__init__.py":

            module_name = file[:-3]

            module = importlib.import_module(f"src.tools.{module_name}")

            tools.append({
                "name": getattr(module, "name", lambda: module_name)(),
                "description": getattr(module, "description", lambda: "")(),
                "category": getattr(module, "category", lambda: "Uncategorized")(),
                "run": getattr(module, "run", lambda: lambda: "No run()")()
            })

    return tools
