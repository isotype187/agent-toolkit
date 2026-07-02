import time
from flask import Flask, render_template_string, redirect, url_for
from src.tool_loader import load_tools
from src.context import context

app = Flask(__name__)

_last_run = {}


HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Agent Toolkit</title>

<style>
body {
    background:#111;
    color:white;
    font-family:Arial;
    padding:30px;
}

.tool {
    background:#222;
    padding:15px;
    margin:15px 0;
    border-radius:10px;
}

button {
    padding:10px 15px;
    cursor:pointer;
}
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

</body>
</html>
"""


@app.route("/")
def home():
    tools = load_tools()

    return render_template_string(
        HTML,
        tools=tools,
        history=context.events
    )


@app.route("/run/<tool_name>", methods=["POST"])
def run_tool(tool_name):

    # debounce lock (prevents double-click / browser spam)
    now = time.time()
    if tool_name in _last_run:
        if now - _last_run[tool_name] < 1.0:
            return redirect(url_for("home"))

    _last_run[tool_name] = now

    tools = load_tools()

    for tool in tools:
        if tool["name"] == tool_name:
            try:
                result = tool["run"]()
                context.log(tool_name, result, "success")
            except Exception as e:
                context.log(tool_name, str(e), "error")
            break

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )
