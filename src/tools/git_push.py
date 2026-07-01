import subprocess
import sys
import os

# ensure src is visible
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from context import context


def name():
    return "Git Push"


def description():
    return "Pushes current project using context-aware root"


def run():

    root = context.root

    status = context.git_status()

    if not status:
        return "Nothing to commit"


    subprocess.run(["git", "add", "."], cwd=root)
    subprocess.run(["git", "commit", "-m", "auto commit"], cwd=root)
    subprocess.run(["git", "push"], cwd=root)

    return "Push complete"
