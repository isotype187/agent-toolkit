import time

class Executor:
    def __init__(self):
        self.running = {}
        self.cooldowns = {}
        self.last_signature = {}

    def _signature(self, tool, args):
        return f"{tool}:{str(args)}"

    def can_run(self, tool, args, cooldown=2):
        now = time.time()

        sig = self._signature(tool, args)

        # ?? block duplicate identical calls instantly
        if self.last_signature.get(tool) == sig:
            return False

        # cooldown protection
        if now - self.cooldowns.get(tool, 0) < cooldown:
            return False

        # running lock
        if self.running.get(tool):
            return False

        return True

    def start(self, tool, args):
        self.running[tool] = True
        self.cooldowns[tool] = time.time()
        self.last_signature[tool] = self._signature(tool, args)

    def stop(self, tool):
        self.running[tool] = False


executor = Executor()
