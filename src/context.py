from datetime import datetime

class Context:
    def __init__(self):
        self.root = r"C:\Users\isoty\dev\repos\agent-toolkit"
        self.events = []
        self.tool_outputs = {}

    def log(self, tool, result, status="success"):

        self.events.append({
            "tool": tool,
            "result": result,
            "status": status,
            "time": datetime.now().strftime("%H:%M:%S")
        })

        self.tool_outputs[tool] = result


context = Context()

tool_outputs = []
tool_history = []

