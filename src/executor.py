import threading
import time

class Executor:
    def __init__(self):
        self.running = {}
        self.cooldowns = {}

    def can_run(self, tool, cooldown=2):
        now = time.time()

        # cooldown check
        last = self.cooldowns.get(tool, 0)
        if now - last < cooldown:
            return False

        # already running check
        if self.running.get(tool):
            return False

        return True

    def start(self, tool):
        self.running[tool] = True
        self.cooldowns[tool] = time.time()

    def stop(self, tool):
        self.running[tool] = False


executor = Executor()
