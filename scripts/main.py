from extensions.sd_extension_auto_tool.bean.task_config import AutoTaskConfig, AutoTaskTxt2Img
from modules import script_callbacks
import gradio as gr
from modules.ui import create_refresh_button
import modules

refresh_symbol = '\U0001f504'  # 🔄

def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as auto_tool_interface:
        with gr.Tab(label="Console"):
            with gr.Row():
                gr.Button(value="Start")
                gr.Button(value="Stop")
                pass
            with gr.Column():
                gr.Dropdown(label="Choose Task")
        with gr.Tab(label="Task"):
            with gr.Row():
                with gr.Column():
                    gr.HTML(value="<span class='hh'>Task choose</span>")
                    gr.Dropdown(label="Choose Task")
                    with gr.Row():
                        gr.Button(value="Load task")
                with gr.Column():
                    gr.HTML(value="<span class='hh'>Task config</span>")
                    create_hint = gr.Label(lable="notice", value="", visible=False)
                    create_task = gr.Button(value="Create task")
                    # Merge config
                    task_name = gr.Textbox(label="Task name")
                    with gr.Box():
                        with gr.Column():
                            gr.HTML(value="<span>merge config</span>")
                            with gr.Row():
                                human_folder_flag = gr.Textbox(label="Human model folder flag")
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
                        sample_method = gr.Text(lable="Sampling method", visible=False)
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

                        use_lark.change(fn=is_show_lark, inputs=use_lark, outputs=use_lark_group)

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
                                    at_user: str
                                    ):
                        if not len(task_name):
                            return {create_hint: gr.update(value="Please input task name", visible=True)}
                        if not len(human_model_dir_flag):
                            return {create_hint: gr.update(value="Please input human flag ", visible=True)}
                        if not len(style_model):
                            return {create_hint: gr.update(value="Please select style model", visible=True)}
                        if not len(base_model_flag):
                            return {create_hint: gr.update(value="Please select tertiary model", visible=True)}
                        if use_txt2img:
                            if not len(prompt):
                                return {create_hint: gr.update(value="please input prompt", visible=True)}
                            if not len(negative_prompt):
                                return {create_hint: gr.update(value="please input negative prompt", visible=True)}
                        if use_lark:
                            return {create_hint: gr.update(value="please input user lark", visible=True)}
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
                        return {create_hint: gr.update(value="Save success", visible=True)}

                    create_task.click(fn=save_config, inputs=[task_name,
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
                                                              at_after_finish
                                                              ], outputs=create_hint)

    return (auto_tool_interface, 'Auto Tool', 'auto_tool_tab'),

script_callbacks.on_ui_tabs(on_ui_tabs)
