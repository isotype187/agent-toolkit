def suggest_tool(tools, context):

    history = context.events if hasattr(context, "events") else []

    if not history:
        return {
            "type": "starter",
            "message": "Run Git Push or generate a system info tool to begin.",
            "generate_suggestion": "system info tool"
        }

    last = history[-1]["tool"].lower()

    # --- PATTERN: git usage
    if "git" in last:
        return {
            "type": "workflow",
            "message": "You just used Git. Next logical tools: build tool, test runner, or system status.",
            "generate_suggestion": "create build status tool"
        }

    # --- PATTERN: tool generator usage
    if "generator" in last.lower():
        return {
            "type": "meta",
            "message": "You are creating tools. Next: safety validator or tool tester.",
            "generate_suggestion": "tool validation checker"
        }

    # --- PATTERN: repeated behavior
    tool_counts = {}
    for h in history:
        t = h["tool"]
        tool_counts[t] = tool_counts.get(t, 0) + 1

    most_used = max(tool_counts, key=tool_counts.get)

    if tool_counts[most_used] > 2:
        return {
            "type": "optimization",
            "message": f"You are heavily using '{most_used}'. You should automate it further.",
            "generate_suggestion": f"auto wrapper for {most_used}"
        }

    return {
        "type": "neutral",
        "message": "System stable. Consider expanding automation coverage.",
        "generate_suggestion": "system health dashboard"
    }
