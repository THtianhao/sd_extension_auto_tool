from extensions.sd_extension_auto_tool.auto_tool.ui_function import save_config
from modules import script_callbacks

import gradio as gr
from modules.ui import create_refresh_button
import modules
import extensions.sd_extension_auto_tool.utils.share

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
                    create_hint = gr.Label(label="label",value="aaaa")
                    create_hint2 = gr.Text(label="text",value="bbbb")
                    create_hint3 = gr.Textbox(label="textbox",value="ccccc")
                    gr.Button(value="Create task")
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
                        delete_model_after_txt2img = gr.Checkbox(label="Delete model after merge")
                        use_txt2img.change(fn=aa, inputs=use_txt2img, outputs=None)
                        prompt = gr.Textbox(label="Prompt", lines=3)
                        negative_prompt = gr.Textbox(label="Negative prompt", lines=3)
                        human_weight = gr.Slider(minimum=0.0, maximum=2.0, step=0.1, label='human weight', value=1.0, elem_id="human_wight")
                        seed = gr.Textbox(label="Seed")
                        cfg_scale = gr.Slider(minimum=1.0, maximum=30.0, step=0.5, label='CFG Scale', value=7.0, elem_id="cfg_scale")
                        batch_size = gr.Slider(minimum=1.0, maximum=8.0, step=1.0, label='Batch Size', value=1.0, elem_id="batch_size")
                        sample_method = gr.Text(lable="Sampling method")
                        sample_step = gr.Slider(minimum=1.0, maximum=150.0, step=1.0, label='Sampling steps', value=20.0, elem_id="sample_step")
                    # Feishu
                    with gr.Box():
                        use_lark = gr.Checkbox(label="Use lark")
                        use_lark.change(fn=aa, inputs=use_lark, outputs=None)
                        at_after_finish = gr.Textbox(label="@ someone after finish")
                    save_config_button = gr.Button(label="Save")
                    save_config_button.click(fn=save_config, inputs=[task_name,
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
                                                                     sample_step,
                                                                     batch_size,
                                                                     use_lark,
                                                                     at_after_finish
                                                                     ], outputs=create_hint)

    return (auto_tool_interface, 'Auto Tool', 'auto_tool_tab'),

def aa(radio):
    print(radio)
    pass

script_callbacks.on_ui_tabs(on_ui_tabs)
