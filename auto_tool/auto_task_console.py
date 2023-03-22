from extensions.sd_extension_auto_tool.auto_tool.auto_tasks_file import read_task_json
from extensions.sd_extension_auto_tool.bean.task_config import AutoTaskConfig, AutoTaskMerge, AutoTaskTxt2Img
from modules import extras, sd_samplers, shared
from modules.call_queue import wrap_gradio_gpu_call
from modules.processing import StableDiffusionProcessingTxt2Img
from modules.sd_models import list_models, checkpoints_list
from modules.txt2img import txt2img

def start_task(tasks_name):
    tasks_split = tasks_name.split(', ')
    for task_name in tasks_split:
        task_json = read_task_json(task_name)
        config: AutoTaskConfig = AutoTaskConfig.parse_obj(task_json)
        id_task = 0
        human_models = filter_human_models(config.task_merge.human_model_dir_flag)
        for human_model in human_models:
            name = ""
            merge_task(human_model, name, config.task_merge)
            txt2img_task(human_model, config.task_txt2img)
            lark_task(human_model, config)

def filter_human_models(filter):
    list_models()
    result = [checkpoint['title'] for checkpoint in checkpoints_list.values() if filter in checkpoint['title']]
    return result

def merge_task(human_model, name, merge: AutoTaskMerge):
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

def txt2img_task(human_name, para: AutoTaskTxt2Img):
    txt2img_prompt_styles = []
    restore_faces = False,
    tiling = False,
    subseed = -1,
    subseed_strength = 0.0,
    seed_resize_from_h = -1,
    seed_resize_from_w = -1,
    seed_checkbox = False,
    width = 512,
    height = 512,
    denoising_strength = 0.0
    enable_hr = False,
    hr_scale = 2,
    hr_upscaler = "Latent",
    hr_second_pass_steps = 0,
    hr_resize_x = 0,
    hr_resize_y = 0,
    override_settings = {}
    result = txt2img("",
                     f"({human_name}:{para.human_weight}){para.prompt}",
                     para.negative_prompt,
                     txt2img_prompt_styles,
                     para.steps,
                     para.sampler_index,
                     False,
                     False,
                     para.batch_count,
                     para.batch_size,
                     para.cfg_scale,

                     para.seed,
                     -1, 0.0, -1, -1, False,
                     512,
                     512,
                     False,

                     denoising_strength,
                     2,
                     "Latent",
                     0,
                     0,
                     0,
                     override_settings)

def validate_sampler_name(name):
    config = sd_samplers.all_samplers_map.get(name, None)
    if config is None:
        pass
    return name

def lark_task(human_model, config):
    pass
