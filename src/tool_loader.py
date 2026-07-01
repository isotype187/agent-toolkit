import importlib
import os


TOOLS_DIR = os.path.join(
    os.path.dirname(__file__),
    "tools"
)


def load_tools():

    tools = []

    for file in os.listdir(TOOLS_DIR):

        if file.endswith(".py") and file != "__init__.py":

            module_name = file[:-3]

            module = importlib.import_module(f"tools.{module_name}")

            # REQUIRED contract with fallbacks
            tool = {
                "name": getattr(module, "name", lambda: module_name)(),
                "description": getattr(module, "description", lambda: "")(),
                "category": getattr(module, "category", lambda: "Uncategorized")(),
                "run": getattr(module, "run", lambda: lambda: "No run() defined")()
            }

            tools.append(tool)

    return tools
