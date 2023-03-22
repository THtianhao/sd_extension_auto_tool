import json
import os

from extensions.sd_extension_auto_tool.utils.share import auto_tool_models_path

task_list = []

def set_task_list():
    global task_list
    for root, dirs, files in os.walk(auto_tool_models_path):
        for file in files:
            task_name = file.split('.')[0]
            task_list.append(task_name)
    return task_list

def refresh_task_list():
    global task_list
    task_list.clear()
    return set_task_list()

def read_task_json(task_name):
    with open(os.path.join(auto_tool_models_path, f"{task_name}.json"), 'r') as f:
        task_json = json.load(f)
        return task_json

set_task_list()
