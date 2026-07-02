from src.tool_loader import load_tools

print("=== TOOL TEST START ===")

tools = load_tools()

print(f"Found {len(tools)} tools")

for tool in tools:
    print("----------------")
    print("Name:", tool["name"])
    print("Description:", tool["description"])
    print("Category:", tool["category"])

print("=== TOOL TEST END ===")
