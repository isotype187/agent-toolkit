import time

_last_request = {}

def is_duplicate(tool_name):
    now = time.time()
    last = _last_request.get(tool_name, 0)

    if now - last < 0.8:
        return True

    _last_request[tool_name] = now
    return False

import time
import threading
from flask import Flask, render_template_string, redirect, url_for, request

from src.tool_loader import load_tools
from src.context import context
from src.tool_safety import check_tool, parse_args
from src.auth import get_user_role, can_run
from src.executor import executor

app = Flask(__name__)

# =========================
# DUPLICATE REQUEST GUARD
# =========================



HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Agent Toolkit</title>

<style>
body { background:#111; color:white; font-family:Arial; padding:30px; }
.tool { background:#222; padding:15px; margin:15px 0; border-radius:10px; }
input { padding:8px; width:90%; }
button { padding:10px 15px; cursor:pointer; margin-top:5px; }
</style>
</head>

<body>

<h1>?? Agent Toolkit</h1>

{% for tool in tools %}
<div class="tool">
    <h2>{{ tool.name }}</h2>
    <p>{{ tool.description }}</p>

    <form action="/run/{{ tool.name }}" method="post">
        <input name="args" placeholder='JSON args'>
        <button type="submit">Run Tool</button>
    </form>
</div>
{% endfor %}

<hr>

<h2>?? Event Log</h2>

{% for event in history %}
<div class="tool">
    <b>{{ event.time }}</b><br>
    <b>{{ event.tool }}</b><br>
    {{ event.result }}<br>
    <i>Status: {{ event.status }}</i>
</div>
{% endfor %}

</body>
</html>
"""


def execute(tool_name, fn, args):
    try:
        result = fn(args)
        context.log(tool_name, result, "success")
    except Exception as e:
        context.log(tool_name, str(e), "error")
    finally:
        executor.stop(tool_name)


@app.route("/")
def home():
    return render_template_string(
        HTML,
        tools=load_tools(),
        history=list(context.events)
    )


@app.route("/run/<tool_name>", methods=["POST"])
def run_tool(tool_name):

    # prevent browser double-submit spam
    if is_duplicate(tool_name):
        return redirect(url_for("home"))

    role = get_user_role()
    args = parse_args(request.form.get("args", ""))

    if not can_run(tool_name, role):
        context.log(tool_name, "BLOCKED (role)", "blocked")
        return redirect(url_for("home"))

    policy = check_tool(tool_name)

    if not policy["allowed"]:
        context.log(tool_name, "BLOCKED (policy)", "blocked")
        return redirect(url_for("home"))

    if not executor.can_run(tool_name, args, cooldown=2):
        context.log(tool_name, "BLOCKED (cooldown)", "blocked")
        return redirect(url_for("home"))

    executor.start(tool_name, args)

    tools = load_tools()
    target = next((t for t in tools if t["name"] == tool_name), None)

    if not target:
        context.log(tool_name, "TOOL NOT FOUND", "error")
        executor.stop(tool_name)
        return redirect(url_for("home"))

    thread = threading.Thread(
        target=execute,
        args=(tool_name, target["run"], args)
    )
    thread.start()

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        threaded=True,
        use_reloader=False
    )



