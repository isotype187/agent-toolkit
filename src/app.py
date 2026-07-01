from flask import Flask, render_template_string, request
from tool_loader import load_tools
from src.context import tool_outputs, tool_history

app = Flask(__name__)


HTML = '''
<!DOCTYPE html>
<html>
<head>
<title>Agent Toolkit</title>

<style>
body {
    font-family: Arial;
    margin: 30px;
    background: #0f0f0f;
    color: white;
}

.category {
    margin-top: 20px;
    padding: 15px;
    border-radius: 10px;
    background: #1c1c1c;
}

button {
    width: 220px;
    height: 40px;
    margin: 6px;
    border-radius: 6px;
    border: none;
    cursor: pointer;
    background: #2b2b2b;
    color: white;
}

button:hover {
    background: #3a3a3a;
}

.output-box {
    margin-top: 30px;
    padding: 15px;
    background: #111;
    border-radius: 10px;
}
</style>

</head>

<body>

<h1>?? Agent Toolkit</h1>

<h2>Tools</h2>

{% for category, tools in grouped.items() %}

<div class="category">
<h3>{{category}}</h3>

{% for tool in tools %}
<form method="post" action="/run/{{tool['name']}}">
    <button title="{{tool['description']}}">
        {{tool['name']}}
    </button>
</form>
{% endfor %}

</div>

{% endfor %}

<div class="output-box">
<h2>Output</h2>

{% for item in history %}
<p><b>{{item['tool']}}</b> ? {{item['result']}}</p>
{% endfor %}

</div>

</body>
</html>
'''


def group_tools(tools):
    grouped = {}
    for t in tools:
        cat = t["category"]
        grouped.setdefault(cat, []).append(t)
    return grouped


@app.route("/")
def home():
    tools = load_tools()
    grouped = group_tools(tools)

    return render_template_string(
        HTML,
        grouped=grouped,
        history=tool_history
    )


@app.route("/run/<tool_name>", methods=["POST"])
def run_tool(tool_name):

    tools = load_tools()

    for tool in tools:
        if tool["name"] == tool_name:

            try:
                result = tool["run"]()

            except Exception as e:
                result = f"Error: {e}"

            tool_outputs[tool_name] = result

            tool_history.append({
                "tool": tool_name,
                "result": result
            })

    return home()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
