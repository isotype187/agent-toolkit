import subprocess
from src.context import context


def name():
    return "Git Push"


def description():
    return "Stages, commits, and pushes all changes to GitHub"


def category():
    return "Git"


def run():

    root = context.root

    try:
        subprocess.run(["git", "add", "."], cwd=root, check=False)

        subprocess.run(
            ["git", "commit", "-m", "auto commit"],
            cwd=root,
            check=False
        )

        subprocess.run(["git", "push"], cwd=root, check=False)

        result = "Git push complete"

    except Exception as e:
        result = f"Git error: {e}"

    context.tool_outputs["Git Push"] = result
    context.tool_history.append({"tool": "Git Push", "result": result})

    return result
