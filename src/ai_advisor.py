def suggest_tool(tools, history):

    if not history:
        return "Try running Git Push to sync your repo."

    last = history[-1]["tool"].lower()

    if "git" in last:
        return "Next step: check project status or run a build tool (if added)."

    return "No strong suggestion yet. Try Git Push or check tools."
