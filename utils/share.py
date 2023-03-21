import os

def load_vars():
    global root_path, models_path, auto_tool_models_path, ckpt_dir
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    models_path = os.path.join(root_path, "models")
    auto_tool_models_path = os.path.join(models_path, "auto_tool")
    ckpt_dir = os.path.join(models_path, "Stable-diffusion")
    if not os.path.exists(auto_tool_models_path):
        os.mkdir(auto_tool_models_path)


root_path = ""
models_path = ""
auto_tool_models_path = ""
ckpt_dir = ""

load_vars()
