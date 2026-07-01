import subprocess
import os


def check_git_repo(path):
    return os.path.isdir(os.path.join(path, ".git"))


def check_git_remote(path):
    try:
        result = subprocess.run(
            ["git", "remote"],
            cwd=path,
            capture_output=True,
            text=True
        )
        return bool(result.stdout.strip())
    except:
        return False


def validate_git_ready(path):
    issues = []

    if not check_git_repo(path):
        issues.append("Not a git repository (.git missing)")

    if not check_git_remote(path):
        issues.append("No git remote configured")

    return {
        "ok": len(issues) == 0,
        "issues": issues
    }
