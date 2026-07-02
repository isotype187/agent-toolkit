import subprocess
from src.context import context


def name():
    return "Git Push"


def description():
    return "Stages, commits, and pushes changes to GitHub"


def category():
    return "Git"


def run():

    try:
        subprocess.run(["git", "add", "."], cwd=context.root, check=False)

        commit = subprocess.run(
            ["git", "commit", "-m", "auto commit"],
            cwd=context.root,
            capture_output=True,
            text=True,
            check=False
        )

        push = subprocess.run(
            ["git", "push"],
            cwd=context.root,
            capture_output=True,
            text=True,
            check=False
        )

        # ?? ONLY KEEP MEANINGFUL INFO
        result = "Git push completed successfully"

        if commit.returncode != 0:
            result += "\nCommit had warnings/errors"

        if push.returncode != 0:
            result += "\nPush had warnings/errors"

        status = "success"

    except Exception as e:
        result = f"Git error: {e}"
        status = "error"

    context.log("Git Push", result, status)

    return result
