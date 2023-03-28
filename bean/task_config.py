import json
import os

from pydantic import BaseModel

from extensions.sd_extension_auto_tool.utils.share import  auto_tasks_path

class AutoTaskMerge(BaseModel):
    human_model_dir_flag: str = ""
    style_model: str = ""
    base_model_flag: str = ""
    interp_method: str = ""
    multiplier: float = 1.0
    checkpoint_format: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class AutoTaskTxt2Img(BaseModel):
    use_txt2img: bool = False
    delete_after_txt2img: bool = False
    prompt: str = ""
    negative_prompt: str = ""
    seed: int = -1
    cfg_scale: float = 1.0
    sampler_index: int = 0
    steps: int = 20
    batch_size: int = 1
    batch_count: int = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class AutoTaskLark(BaseModel):
    use_lark: bool = False
    at_user: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class AutoTaskConfig(BaseModel):
    task_name = ""
    task_merge: AutoTaskMerge = AutoTaskMerge()
    task_txt2img: AutoTaskTxt2Img = AutoTaskTxt2Img()
    task_lark: AutoTaskLark = AutoTaskLark()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def save(self):
        with open(os.path.join(auto_tasks_path, f"{self.task_name}.json"), 'w') as f:
            json.dump(self.dict(), f, indent=4)
            return "success"

    def get_config(self, task_name):
        if os.path.exists(os.path.join(auto_tasks_path, f"{task_name}.json")):
            with open(f"{task_name}.json", 'r') as f:
                data = f.read()
                if data is not None and len(data):
                    return json.loads(data)
        else:
            print("file not exist")
