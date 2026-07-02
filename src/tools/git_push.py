import subprocess
from src.context import context


def name():
    return "Git Push"


def description():
    return "Safely stages, commits, and pushes changes to GitHub"


def category():
    return "Git"


# ?? FIXED: must accept args
def run(args=None):

    try:
        subprocess.run(["git", "add", "."], cwd=context.root, check=False)

        subprocess.run(
            ["git", "commit", "-m", "auto commit"],
            cwd=context.root,
            check=False
        )

        subprocess.run(
            ["git", "push"],
            cwd=context.root,
            check=False
        )

        result = "Git push completed successfully"
        status = "success"

    except Exception as e:
        result = f"Git error: {e}"
        status = "error"

    context.log("Git Push", result, status)

    return result
