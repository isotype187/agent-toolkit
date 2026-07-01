from flask import Flask, render_template_string, request
from tool_loader import load_tools

app = Flask(__name__)

last_output = "Ready."


HTML = '''
<!DOCTYPE html>
<html>
<head>
<title>Agent Toolkit</title>
<style>
body {
    font-family: Arial;
    margin: 30px;
}

.category {
    margin-top: 20px;
    padding: 10px;
    border: 1px solid #ddd;
}

button {
    width: 200px;
    height: 35px;
    margin: 5px;
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

<h2>Output</h2>
<pre>{{output}}</pre>

</body>
</html>
'''


def group_tools(tools):

    grouped = {}

    for t in tools:

        cat = t["category"]

        if cat not in grouped:
            grouped[cat] = []

        grouped[cat].append(t)

    return grouped


@app.route("/")
def home():

    tools = load_tools()

    grouped = group_tools(tools)

    return render_template_string(
        HTML,
        grouped=grouped,
        output=last_output
    )


@app.route("/run/<tool_name>", methods=["POST"])
def run_tool(tool_name):

    global last_output

    tools = load_tools()

    for tool in tools:

        if tool["name"] == tool_name:

            try:
                last_output = tool["run"]()

            except Exception as e:
                last_output = f"Error: {e}"

    return home()


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
