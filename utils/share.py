import os

def load_vars():
    global root_path, auto_models_path, auto_tool_root_path, ckpt_dir, auto_tool_tasks_path
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    auto_models_path = os.path.join(root_path, "models")
    ckpt_dir = os.path.join(auto_models_path, "Stable-diffusion")
    auto_tool_root_path = os.path.join(ckpt_dir, "AutoTool")
    auto_tool_tasks_path = os.path.join(auto_tool_root_path, "tasks")
    if not os.path.exists(auto_tool_tasks_path):
        os.mkdir(auto_tool_tasks_path)


root_path = ""
auto_models_path = ""
auto_tool_root_path = ""
auto_tool_tasks_path = ""
ckpt_dir = ""

load_vars()
