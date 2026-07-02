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

        # ?? CLEAN OUTPUT (no duplication, no raw spam)
        output_parts = []

        if commit.stdout:
            output_parts.append(commit.stdout.strip())

        if push.stdout:
            output_parts.append(push.stdout.strip())

        if commit.stderr:
            output_parts.append(commit.stderr.strip())

        if push.stderr:
            output_parts.append(push.stderr.strip())

        result = "\n".join([p for p in output_parts if p])

        # fallback if empty
        if not result:
            result = "Git push completed"

        status = "success"

    except Exception as e:
        result = f"Git error: {e}"
        status = "error"

    context.log("Git Push", result, status)

    return result
