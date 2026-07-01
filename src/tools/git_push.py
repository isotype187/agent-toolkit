import subprocess
from src.context import context
from src.tool_safety import validate_git_ready


def name():
    return "Git Push"


def description():
    return "Safely stages, commits, and pushes changes to GitHub"


def category():
    return "Git"


def run():

    safety = validate_git_ready(context.root)

    if not safety["ok"]:
        return "BLOCKED:\n" + "\n".join(safety["issues"])

    try:
        add = subprocess.run(["git", "add", "."], cwd=context.root, capture_output=True, text=True)
        commit = subprocess.run(["git", "commit", "-m", "auto commit"], cwd=context.root, capture_output=True, text=True)
        push = subprocess.run(["git", "push"], cwd=context.root, capture_output=True, text=True)

        output = "\n".join([
            add.stdout or add.stderr,
            commit.stdout or commit.stderr,
            push.stdout or push.stderr
        ])

        context.log("Git Push", output, "success")

        return output

    except Exception as e:
        context.log("Git Push", str(e), "error")
        return f"Git error: {e}"
