from datetime import datetime

class Context:
    def __init__(self):
        self.root = r"C:\Users\isoty\dev\repos\agent-toolkit"
        self.events = []
        self.tool_outputs = {}
        self._last_event_hash = None

    def log(self, tool, result, status="success"):

        event = {
            "tool": tool,
            "result": result,
            "status": status,
            "time": datetime.now().strftime("%H:%M:%S")
        }

        # ?? HARD DEDUPE (prevents identical double logs)
        event_hash = f"{tool}:{result}:{status}"

        if event_hash == self._last_event_hash:
            return

        self._last_event_hash = event_hash

        self.events.append(event)
        self.tool_outputs[tool] = result


context = Context()
