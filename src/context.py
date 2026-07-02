from datetime import datetime

class Context:
    def __init__(self):
        self.root = r"C:\Users\isoty\dev\repos\agent-toolkit"
        self.events = []
        self.tool_outputs = {}
        self._locks = {}

    def log(self, tool, result, status="success"):
        self.events.append({
            "tool": tool,
            "result": str(result),
            "status": status,
            "time": datetime.now().strftime("%H:%M:%S")
        })

    def lock_tool(self, tool):
        if self._locks.get(tool):
            return False
        self._locks[tool] = True
        return True

    def unlock_tool(self, tool):
        self._locks[tool] = False


context = Context()
