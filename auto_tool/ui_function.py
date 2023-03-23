import json
import os.path

import gradio as gr

from extensions.sd_extension_auto_tool.auto_tool.auto_tasks_file import refresh_task_list, task_list
from extensions.sd_extension_auto_tool.bean.task_config import AutoTaskConfig
from extensions.sd_extension_auto_tool.utils.share import auto_tool_tasks_path

def choose_task_fn(task_name):
    with open(os.path.join(auto_tool_tasks_path, f"{task_name}.json"), 'r') as f:
        task_json = json.load(f)
        task_config = AutoTaskConfig.parse_obj(task_json)
        return [task_config.task_name,
                task_config.task_merge.human_model_dir_flag,
                task_config.task_merge.style_model,
                task_config.task_merge.base_model_flag,
                task_config.task_merge.delete_after_merge,
                task_config.task_merge.multiplier,
                task_config.task_txt2img.use_txt2img,
                task_config.task_txt2img.prompt,
                task_config.task_txt2img.negative_prompt,
                task_config.task_txt2img.human_weight,
                task_config.task_txt2img.seed,
                task_config.task_txt2img.cfg_scale,
                task_config.task_txt2img.sampler_index,
                task_config.task_txt2img.steps,
                task_config.task_txt2img.batch_size,
                task_config.task_lark.use_lark,
                task_config.task_lark.at_user, ]

def save_config(task_name: str,
                human_model_dir_flag: str,
                style_model: str,
                base_model_flag: str,
                delete_after_merge: bool,
                multiplier: float,
                use_txt2img: bool,
                prompt: str,
                negative_prompt: str,
                human_weight: float,
                seed: int,
                cfg_scale: int,
                sampler_index: str,
                steps: int,
                batch_size: int,
                use_lark: bool,
                at_user: str,
                ):
    if not len(task_name):
        return gr.update(value="Please input task name", visible=True)
    if not len(human_model_dir_flag):
        return gr.update(value="Please input human flag ", visible=True)
    if not len(style_model):
        return gr.update(value="Please select style model", visible=True)
    if not len(base_model_flag):
        return gr.update(value="Please select tertiary model", visible=True)
    if use_txt2img:
        if not len(prompt):
            return gr.update(value="please input prompt", visible=True)
        if not len(negative_prompt):
            return gr.update(value="please input negative prompt", visible=True)
    if use_lark:
        return gr.update(value="please input user lark", visible=True)
    task_config = AutoTaskConfig()
    task_config.task_name = task_name
    task_config.task_merge.human_model_dir_flag = human_model_dir_flag
    task_config.task_merge.style_model = style_model
    task_config.task_merge.base_model_flag = base_model_flag
    task_config.task_merge.delete_after_merge = delete_after_merge
    task_config.task_merge.interp_method = "Add difference"
    task_config.task_merge.multiplier = multiplier
    task_config.task_merge.checkpoint_format = "ckpt"
    task_config.task_txt2img.use_txt2img = use_txt2img
    task_config.task_txt2img.prompt = prompt
    task_config.task_txt2img.negative_prompt = negative_prompt
    task_config.task_txt2img.human_weight = human_weight
    task_config.task_txt2img.seed = seed
    task_config.task_txt2img.cfg_scale = cfg_scale
    task_config.task_txt2img.sampler_index = sampler_index
    task_config.task_txt2img.steps = steps
    task_config.task_txt2img.batch_size = batch_size
    task_config.task_lark.use_lark = use_lark
    task_config.task_lark.at_user = at_user
    task_config.save()
    return gr.update(value="Save success", visible=True)

def auto_delete_task(task_name):
    if len(task_name):
        os.remove(os.path.join(auto_tool_tasks_path, f"{task_name}.json"))
        refresh_task_list()
        return gr.update(value="Delete success", visible=True)

def fill():
    return ', '.join(task_list) if task_list else gr.update()

def fill_choose_task():
    refresh_task_list()
    return fill()
