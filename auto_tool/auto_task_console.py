import os

import gradio as gr

from extensions.sd_extension_auto_tool.auto_tool.auto_tasks_file import read_task_json
from extensions.sd_extension_auto_tool.bean.task_config import AutoTaskConfig, AutoTaskMerge, AutoTaskTxt2Img, AutoTaskLark
from extensions.sd_extension_auto_tool.utils.share import ckpt_dir
from modules import extras, sd_samplers
from modules.sd_models import list_models, checkpoints_list
from modules.txt2img import txt2img

stop_task = False

def set_stop_task(stop):
    global stop_task
    stop_task = stop

def get_stop_task():
    global stop_task
    return stop_task

def stop_console_task():
    set_stop_task(True)


def start_console_task(tasks_name):
    tasks_split = tasks_name.split(', ')
    for task_name in tasks_split:
        task_json = read_task_json(task_name)
        config: AutoTaskConfig = AutoTaskConfig.parse_obj(task_json)
        id_task = 0
        style_model_cut = config.task_merge.style_model.split('/')[-1].split('.')[0]
        human_models = filter_human_models(config.task_merge.human_model_dir_flag)
        if not human_models:
            return gr.update(value="human models not exist", visible=True)
        for human_index, human_model in enumerate(human_models):
            human_model_cut = human_model.split('/')[-1].split('.')[0]
            save_model_name = f"AutoTool/{style_model_cut}/{style_model_cut}_{human_model_cut}"
            merge_task(human_model, save_model_name, config.task_merge)
            # lark_task(human_model, config)

def filter_human_models(filter):
    list_models()
    result = [checkpoint for checkpoint in checkpoints_list.values() if filter in checkpoint.split('/')]
    return result

def merge_task(human_model, name, merge: AutoTaskMerge):
    models_path = os.path.join(ckpt_dir, name)
    if not os.path.exists(models_path):
        os.makedirs(models_path)
    else:
        print(f"{name} already had")
        return
    result = extras.run_modelmerger(0,
                                    human_model,
                                    merge.style_model,
                                    merge.base_model_flag,
                                    merge.interp_method,
                                    merge.multiplier,
                                    False,
                                    name,
                                    merge.checkpoint_format,
                                    0,
                                    None,
                                    "")
    print(f"Merge {name} success")

def validate_sampler_name(name):
    config = sd_samplers.all_samplers_map.get(name, None)
    if config is None:
        pass
    return name

def lark_task(human_model, lark_config: AutoTaskLark):
    if not lark_config.at_user: return
