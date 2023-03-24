import os

def load_vars():
    global root_path, auto_models_path, auto_config_path, auto_global_path, auto_lark_config, auto_merge_model_path, ckpt_dir, auto_tasks_path
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    auto_models_path = os.path.join(root_path, "models")
    auto_config_path = os.path.join(auto_models_path, "AutoTool")
    auto_tasks_path = os.path.join(auto_config_path, "tasks")
    auto_global_path = os.path.join(auto_config_path, "global")
    auto_lark_config = os.path.join(auto_global_path, "lark.json")
    ckpt_dir = os.path.join(auto_models_path, "Stable-diffusion")
    auto_merge_model_path = os.path.join(ckpt_dir, "AutoTool")

    # models/AutoTool
    if not os.path.exists(auto_config_path):
        os.mkdir(auto_config_path)
    # models/AutoTool/tasks
    if not os.path.exists(auto_tasks_path):
        os.mkdir(auto_tasks_path)
    # models/AutoTool/global
    if not os.path.exists(auto_global_path):
        os.mkdir(auto_global_path)

root_path = ""
auto_models_path = ""
auto_config_path = ""
auto_tasks_path = ""
auto_global_path = ""
auto_lark_config = ""
auto_merge_model_path = ""
ckpt_dir = ""

load_vars()
