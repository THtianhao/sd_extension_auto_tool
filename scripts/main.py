import os

from extensions.sd_extension_auto_tool.auto_tool.auto_task_console import stop_console_task
from extensions.sd_extension_auto_tool.auto_tool.auto_tasks_file import task_list, refresh_task_list, read_task_json
from extensions.sd_extension_auto_tool.auto_tool.ui_function import choose_task_fn, save_config, auto_delete_task, fill_choose_task
from extensions.sd_extension_auto_tool.bean.task_config import AutoTaskConfig, AutoTaskMerge, AutoTaskTxt2Img
from extensions.sd_extension_auto_tool.utils.share import ckpt_dir
from modules import script_callbacks, extras
import gradio as gr

from modules.sd_models import list_models, checkpoints_list
from modules.sd_samplers import samplers
from modules.txt2img import txt2img
from modules.ui import create_refresh_button
import modules
from modules.ui_components import ToolButton

refresh_symbol = '\U0001f504'  # 🔄
fill_values_symbol = "\U0001f4d2"  # 📒

def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as auto_tool_interface:
        with gr.Tab(label="Console"):
            with gr.Row():
                start_task = gr.Button(value="Start")
                stop_task = gr.Button(value="Stop")
            with gr.Column():
                task_log = gr.Label(value="aaa", visible=False)
                with gr.Row():
                    choose_task = gr.Textbox(label="Choose Task", lines=3)
                    fill_task_button = ToolButton(value=fill_values_symbol, elem_id="Fill task button")
                    fill_task_button.click(fn=fill_choose_task, outputs=choose_task)
        with gr.Tab(label="Task"):
            with gr.Row():
                with gr.Column():
                    gr.HTML(value="<span class='hh'>Task choose</span>")
                    with gr.Row():
                        select_task = gr.Dropdown(label="Choose Task", choices=task_list)
                        create_refresh_button(select_task, refresh_task_list, lambda: {"choices": task_list}, "refresh_select_task")
                    with gr.Row():
                        load_task = gr.Button(value="Load task")
                        delete_task = gr.Button(value="Delete task")
                with gr.Column():
                    gr.HTML(value="<span class='hh'>Task config</span>")
                    create_hint = gr.Label(lable="notice", value="hint", visible=False)
                    create_task = gr.Button(value="Create task")
                    # Merge config
                    task_name = gr.Textbox(label="Task name")
                    with gr.Box():
                        with gr.Column():
                            gr.HTML(value="<span>merge config</span>")
                            with gr.Row():
                                human_folder_flag = gr.Textbox(label="Human folder flag")
                                secondary_model_name = gr.Dropdown(modules.sd_models.checkpoint_tiles(), label="Style model")
                                create_refresh_button(secondary_model_name, modules.sd_models.list_models, lambda: {"choices": modules.sd_models.checkpoint_tiles()}, "refresh_checkpoint_B")
                                tertiary_model_name = gr.Dropdown(modules.sd_models.checkpoint_tiles(), label="Tertiary model")
                                create_refresh_button(tertiary_model_name, modules.sd_models.list_models, lambda: {"choices": modules.sd_models.checkpoint_tiles()}, "refresh_checkpoint_C")
                            multiplier = gr.Slider(minimum=0.0, maximum=1.0, step=0.05, label='Multiplier (M) - set to 0 to get model A', value=0.3, elem_id="modelmerger_interp_amount")
                    # Merge txt2img
                    with gr.Box():
                        use_txt2img = gr.Checkbox(label="Use txt2img")
                        delete_model_after_txt2img = gr.Checkbox(label="Delete model after merge", visible=False)
                        prompt = gr.Textbox(label="Prompt", lines=3, visible=False)
                        negative_prompt = gr.Textbox(label="Negative prompt", lines=3, visible=False)
                        human_weight = gr.Slider(minimum=0.0, maximum=2.0, step=0.1, label='human weight', value=1.0, elem_id="human_wight", visible=False)
                        seed = gr.Number(label="Seed", value=-1, visible=False)
                        cfg_scale = gr.Slider(minimum=1.0, maximum=30.0, step=0.5, label='CFG Scale', value=7.0, elem_id="cfg_scale", visible=False)
                        batch_size = gr.Slider(minimum=1.0, maximum=8.0, step=1.0, label='Batch Size', value=1.0, elem_id="batch_size", visible=False)
                        sample_method = gr.Dropdown(label='Sampling method', choices=[x.name for x in samplers], value=samplers[0].name, type="index")
                        sample_steps = gr.Slider(minimum=1.0, maximum=150.0, step=1.0, label='Sampling steps', value=20.0, elem_id="sample_step", visible=False)
                        group_txt2img = [delete_model_after_txt2img, prompt, negative_prompt, human_weight, seed, cfg_scale, batch_size, sample_method, sample_steps, sample_steps]

                        def is_show_txt2img(enable):
                            result = {}
                            for i in group_txt2img:
                                result[i] = gr.update(visible=enable)
                            return result

                        use_txt2img.change(fn=is_show_txt2img, inputs=use_txt2img, outputs=group_txt2img)
                    # Feishu
                    with gr.Box():
                        use_lark = gr.Checkbox(label="Use lark")
                        at_after_finish = gr.Textbox(label="@ someone after finish", visible=False)
                        use_lark_group = [at_after_finish]

                        def is_show_lark(enable):
                            result = {}
                            for i in use_lark_group:
                                result[i] = gr.update(visible=enable)
                            return result
        all_para = [task_name,
                    human_folder_flag,
                    secondary_model_name,
                    tertiary_model_name,
                    delete_model_after_txt2img,
                    multiplier,
                    use_txt2img,
                    prompt,
                    negative_prompt,
                    human_weight,
                    seed,
                    cfg_scale,
                    sample_method,
                    sample_steps,
                    batch_size,
                    use_lark,
                    at_after_finish]

        def start_console_task(tasks_name):
            tasks_split = tasks_name.split(', ')
            for task_name in tasks_split:
                task_json = read_task_json(task_name)
                config: AutoTaskConfig = AutoTaskConfig.parse_obj(task_json)
                id_task = 0
                style_model_cut = config.task_merge.style_model.split('/')[-1].split('.')[0]
                human_models = filter_human_models(config.task_merge.human_model_dir_flag)
                if not human_models:
                    return gr.update(value=f"human models {config.task_merge.human_model_dir_flag} not exist", visible=True)
                for human_index, human_model in enumerate(human_models):
                    human_model_cut = human_model.split('/')[-1].split('.')[0]
                    save_model_name = f"AutoTool/{style_model_cut}/{style_model_cut}_{human_model_cut}_{config.task_merge.multiplier}"
                    merge_task(human_model, save_model_name, config.task_merge)
                    txt2img_task(human_model, config.task_txt2img)
                    # lark_task(human_model, config)

        def filter_human_models(filter):
            list_models()
            result = [checkpoint.title for checkpoint in checkpoints_list.values() if filter in checkpoint.title.split('/')]
            return result

        def merge_task(human_model, name, merge: AutoTaskMerge):
            auto_dir = os.path.join(ckpt_dir, name)
            if not os.path.exists(auto_dir):
                os.makedirs(auto_dir)
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

        start_task.click(fn=start_console_task, inputs=choose_task, outputs=task_log)
        stop_task.click(fn=stop_console_task, outputs=task_log)
        use_lark.change(fn=is_show_lark, inputs=use_lark, outputs=use_lark_group)
        create_task.click(fn=save_config, inputs=all_para, outputs=create_hint)
        load_task.click(fn=choose_task_fn, inputs=select_task, outputs=all_para)
        delete_task.click(fn=auto_delete_task, inputs=select_task, outputs=create_hint)
    return (auto_tool_interface, 'Auto Tool', 'auto_tool_tab'),

script_callbacks.on_ui_tabs(on_ui_tabs)
