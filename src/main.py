import tkinter as tk
from tool_loader import load_tools

def run_tool(tool):
    result = tool["run"]()
    output.insert(tk.END, f"{tool['name']}: {result}\n")

root = tk.Tk()
root.title("Dev Helper Tool")
root.geometry("600x400")

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

output = tk.Text(root, height=10)
output.pack(fill=tk.BOTH, expand=True)

tools = load_tools()

for tool in tools:
    btn = tk.Button(frame, text=tool["name"], command=lambda t=tool: run_tool(t))
    btn.pack(fill=tk.X)

root.mainloop()
