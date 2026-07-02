import json

def get_policy(tool_name: str):
    policies = {
        "Git Push": {
            "allowed": True,
            "requires_confirm": True,
            "async": False
        },
        "Hello Tool": {
            "allowed": True,
            "requires_confirm": False,
            "async": False
        }
    }

    return policies.get(tool_name, {
        "allowed": True,
        "requires_confirm": False,
        "async": False
    })


def parse_args(raw: str):
    if not raw:
        return None

    try:
        return json.loads(raw)
    except:
        return {"raw": raw}


def check_tool(tool_name: str):
    return get_policy(tool_name)
