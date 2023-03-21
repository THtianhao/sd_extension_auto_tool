import json
import os
from extensions.sd_extension_auto_tool.utils.share import auto_tool_models_path

class AutoTaskConfig:
    def __init__(self, data):
        self.task_name = data["task_name"]
        self.task_merge = AutoTaskMerge(data["task_merge"])
        self.task_txt2img = AutoTaskTxt2Img(data["task_txt2img"])
        self.task_lark = AutoTaskLark(data["task_lark"])

    def save(self):
        if self.task_name is not None and len(self.task_name):
            data = self.get_config(self.task_name)
            if data is None:
                with open(os.path.join(auto_tool_models_path, f"{self.task_name}.json"), 'w') as f:
                    json.dump(data, f)

    def get_config(self, task_name):
        if os.path.exists(os.path.join(auto_tool_models_path, f"{task_name}.json")):
            with open(f"{task_name}.json", 'r') as f:
                data = f.read()
                if data is not None and len(data):
                    return json.loads(data)
        else:
            print("file not exist")

class AutoTaskMerge:
    def __init__(self, data):
        self.human_model_dir_flag = data['human_model_dir_flag']
        self.style_model = data['style_model']
        self.base_model_flag = data['base_model_flag']
        self.delete_after_merge = data['delete_after_merge']
        self.interp_method = data['interp_method']
        self.multiplier = data['multiplier']
        self.checkpoint_format = data['checkpoint_format']

class AutoTaskTxt2Img:
    def __init__(self, data):
        self.prompt = data['prompt']
        self.negative_prompt = data['negative_prompt']
        self.human_weight = data['human_weight']
        self.seed = data['seed']
        self.cfg_scale = data['cfg_scale']
        self.sampler_index = data['sampler_index']
        self.steps = data['steps']
        self.batch_size = data['batch_size']

class AutoTaskLark:
    def __init__(self, data):
        # self.user_access_token = data['user_access_token']
        self.at_user = data['at_user']
