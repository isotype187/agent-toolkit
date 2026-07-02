def get_user_role():
    # ?? simple placeholder (upgrade later to real auth)
    return "admin"


def can_run(tool_name: str, role: str) -> bool:

    rules = {
        "Git Push": ["admin"],
        "Hello Tool": ["admin", "user"]
    }

    allowed_roles = rules.get(tool_name, ["admin"])

    return role in allowed_roles
