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
        subprocess.run(["git", "add", "."], cwd=root)

        subprocess.run(
            ["git", "commit", "-m", "auto commit"],
            cwd=root
        )

        subprocess.run(["git", "push"], cwd=root)

        return "Git push complete"

    except Exception as e:
        return f"Git error: {e}"
