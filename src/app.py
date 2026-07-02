import time
import uuid
from flask import Flask, render_template_string, redirect, url_for, request
from src.tool_loader import load_tools
from src.context import context

app = Flask(__name__)

DEBUG_RUNS = []


HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Agent Toolkit</title>

<style>
body { background:#111; color:white; font-family:Arial; padding:30px; }
.tool { background:#222; padding:15px; margin:15px 0; border-radius:10px; }
button { padding:10px 15px; cursor:pointer; }
</style>
</head>

<body>

<h1>?? Agent Toolkit</h1>

{% for tool in tools %}
<div class="tool">
    <h2>{{ tool.name }}</h2>
    <p>{{ tool.description }}</p>
    <p><b>Category:</b> {{ tool.category }}</p>

    <form action="/run/{{ tool.name }}" method="post">
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

<hr>

<h2>?? DEBUG RUN TRACE</h2>

{% for d in debug %}
<div class="tool">
    {{ d }}
</div>
{% endfor %}

</body>
</html>
"""


@app.route("/")
def home():
    tools = load_tools()

    return render_template_string(
        HTML,
        tools=tools,
        history=context.events,
        debug=DEBUG_RUNS
    )


@app.route("/run/<tool_name>", methods=["POST"])
def run_tool(tool_name):

    req_id = str(uuid.uuid4())

    DEBUG_RUNS.append(f"ENTER run_tool | tool={tool_name} | req={req_id}")

    tools = load_tools()

    matches = 0

    for tool in tools:
        if tool["name"] == tool_name:
            matches += 1

            try:
                result = tool["run"]()
                context.log(tool_name, result, "success")
            except Exception as e:
                context.log(tool_name, str(e), "error")

    DEBUG_RUNS.append(
        f"EXIT run_tool | tool={tool_name} | req={req_id} | matches={matches}"
    )

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )
