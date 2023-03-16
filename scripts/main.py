from modules import script_callbacks

import gradio as gr
import extensions.sd_extension_auto_tool

def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as auto_tool_interface:
        with gr.Tab("Check point merge"):
            with gr.Row():
                with gr.Column(variant="panel"):
                    # db_model_name = gr.Dropdown(label='Config', choices=sorted(get_db_models()))
                    gr.Textbox(label="Last")
        with gr.Tab("Txt2Img"):
            pass
        with gr.Tab("Feishu"):
            pass
        return (auto_tool_interface, 'Auto Tool', 'auto_tool_tab'),

script_callbacks.on_ui_tabs(on_ui_tabs)
