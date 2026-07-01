import importlib
import os
import sys


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


TOOLS_DIR = os.path.join(PROJECT_ROOT, "src", "tools")

_loaded_modules = {}


def load_tools():

    tools = []

    for file in os.listdir(TOOLS_DIR):

        if file.endswith(".py") and file != "__init__.py":

            module_name = file[:-3]

            # FORCE RELOAD (hot reload)
            if module_name in _loaded_modules:
                importlib.reload(_loaded_modules[module_name])
                module = _loaded_modules[module_name]
            else:
                module = importlib.import_module(f"src.tools.{module_name}")
                _loaded_modules[module_name] = module

            tools.append({
                "name": getattr(module, "name", lambda: module_name)(),
                "description": getattr(module, "description", lambda: "")(),
                "category": getattr(module, "category", lambda: "Uncategorized")(),
                "run": getattr(module, "run", lambda: lambda: "No run()")()
            })

    return tools
