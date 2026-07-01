from flask import Flask, render_template_string, request
from src.tool_loader import load_tools

app = Flask(__name__)

HTML = """
<h1>Agent Toolkit</h1>
{% for t in tools %}
    <form method="post" action="/run/{{t['name']}}">
        <button>{{t['name']}}</button>
    </form>
{% endfor %}
"""

@app.route("/")
def home():
    tools = load_tools()
    return render_template_string(HTML, tools=tools)

@app.route("/run/<tool_name>", methods=["POST"])
def run_tool(tool_name):
    tools = load_tools()

    for t in tools:
        if t["name"] == tool_name:
            return t["run"]()

    return "Tool not found"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
