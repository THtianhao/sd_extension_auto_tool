import os

from extensions.sd_extension_auto_tool.auto_tool.auto_task_console import stop_console_task
from extensions.sd_extension_auto_tool.auto_tool.auto_tasks_file import task_list, refresh_task_list, read_task_json
from extensions.sd_extension_auto_tool.auto_tool.ui_function import choose_task_fn, save_config, auto_delete_task, fill_choose_task
from extensions.sd_extension_auto_tool.bean.task_config import AutoTaskConfig, AutoTaskMerge, AutoTaskTxt2Img
from extensions.sd_extension_auto_tool.utils.share import auto_tool_root_path
from modules import script_callbacks, extras, sd_samplers, shared
import gradio as gr

from modules.processing import StableDiffusionProcessingTxt2Img, process_images
from modules.scripts import scripts_txt2img
from modules.sd_models import list_models, checkpoints_list
from modules.sd_samplers import samplers
from modules.shared import opts
from modules.ui import create_refresh_button
import modules
from modules.ui_components import ToolButton

refresh_symbol = '\U0001f504'  # 🔄
fill_values_symbol = "\U0001f4d2"  # 📒

def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as auto_tool_interface:
        with gr.Tab(label="Console"):
            with gr.Row():
                with gr.Column():
                    with gr.Row():
                        start_task = gr.Button(value="Start")
                        stop_task = gr.Button(value="Stop")
                    task_log = gr.Label(value="aaa", visible=False)
                    with gr.Row():
                        choose_task = gr.Textbox(label="Choose Task", lines=3)
                        fill_task_button = ToolButton(value=fill_values_symbol, elem_id="Fill task button")
                        fill_task_button.click(fn=fill_choose_task, outputs=choose_task)
                with gr.Column():
                    gr.Button(value="Get lark code")
                    gr.Textbox(label="Lark code")
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
                    save_model_name = f"{style_model_cut}_{human_model_cut}_{str(config.task_merge.multiplier).replace('.', '_')}"
                    merge_task(human_model, style_model_cut, save_model_name, config.task_merge)
                    txt2img_task(human_model, config.task_txt2img)
                    # lark_task(human_model, config)

        def filter_human_models(filter):
            list_models()
            result = [checkpoint.title for checkpoint in checkpoints_list.values() if filter in checkpoint.title.split('/')]
            return result

        def merge_task(human_model, style_dir, file_name, merge: AutoTaskMerge):
            auto_style_dir = os.path.join(auto_tool_root_path, style_dir)
            if not os.path.exists(auto_style_dir):
                os.makedirs(auto_style_dir)
            file = os.path.join(auto_style_dir, f"{file_name}.ckpt")
            filter_model = [model.title for model in checkpoints_list.values() if f"{file_name}.ckpt" in model.title]
            if len(filter_model):
                print(f"File {os.path.join(style_dir, file_name)} already exist")
                return
            result = extras.run_modelmerger(0,
                                            human_model,
                                            merge.style_model,
                                            merge.base_model_flag,
                                            merge.interp_method,
                                            merge.multiplier,
                                            False,
                                            file,
                                            merge.checkpoint_format,
                                            0,
                                            None,
                                            "")
            print(f"Merge result = {result}")

        def txt2img_task(human_name, auto_para: AutoTaskTxt2Img):
            if not auto_para.use_txt2img: return

            def validate_sampler_name(name):
                config = sd_samplers.all_samplers_map.get(name, None)
                if config is None:
                    print(f"toto error sampler_name{name}")
                return name

            def init_script_args(replace_argu, selectable_scripts, selectable_idx, script_runner):
                # find max idx from the scripts in runner and generate a none array to init script_args
                last_arg_index = 1
                for script in script_runner.scripts:
                    if last_arg_index < script.args_to:
                        last_arg_index = script.args_to
                # None everywhere except position 0 to initialize script args
                script_args = [None] * last_arg_index
                # position 0 in script_arg is the idx+1 of the selectable script that is going to be run when using scripts.scripts_*2img.run()
                if selectable_scripts:
                    script_args[selectable_scripts.args_from:selectable_scripts.args_to] = replace_argu
                    script_args[0] = selectable_idx + 1
                else:
                    # when [0] = 0 no selectable script to run
                    script_args[0] = 0

                # # Now check for always on scripts
                # if request.alwayson_scripts and (len(request.alwayson_scripts) > 0):
                #     for alwayson_script_name in request.alwayson_scripts.keys():
                #         alwayson_script = self.get_script(alwayson_script_name, script_runner)
                #         if alwayson_script == None:
                #             print(f"always on script {alwayson_script_name} not found")
                #         # Selectable script in always on script param check
                #         if alwayson_script.alwayson == False:
                #             print(f"Cannot have a selectable script in the always on scripts params")
                #         # always on script with no arg should always run so you don't really need to add them to the requests
                #         if "args" in request.alwayson_scripts[alwayson_script_name]:
                #             script_args[alwayson_script.args_from:alwayson_script.args_to] = request.alwayson_scripts[alwayson_script_name]["args"]
                return script_args

            def get_selectable_script(script_name, script_runner):
                if script_name is None or script_name == "":
                    return None, None
                script_idx = script_name_to_index(script_name, script_runner.selectable_scripts)
                script = script_runner.selectable_scripts[script_idx]
                return script, script_idx

            def script_name_to_index(name, scripts):
                try:
                    return [script.title().lower() for script in scripts].index(name.lower())
                except:
                    print(f"Script '{name}' not found")

            script_runner = scripts_txt2img
            if not script_runner.scripts:
                script_runner.initialize_scripts(False)
            script_name = None
            selectable_scripts, selectable_script_idx = get_selectable_script(script_name, script_runner)
            script_args = init_script_args([], selectable_scripts, selectable_script_idx, script_runner)
            auto_prompt = f"({human_name}:{auto_para.human_weight}), {auto_para.prompt}"
            p = StableDiffusionProcessingTxt2Img(sd_model=shared.sd_model,
                                                 enable_hr=False,
                                                 denoising_strength=0.0,
                                                 seed=auto_para.seed,
                                                 cfg_scale=auto_para.cfg_scale,
                                                 prompt=auto_prompt,
                                                 negative_prompt=auto_para.negative_prompt,
                                                 sampler_name=sd_samplers.samplers[auto_para.sampler_index].name,
                                                 steps=auto_para.steps,
                                                 batch_size=auto_para.batch_size,
                                                 n_iter=auto_para.batch_count,
                                                 subseed=-1,
                                                 subseed_strength=0.0,
                                                 seed_resize_from_h=1,
                                                 seed_resize_from_w=1,
                                                 styles=['anime'],
                                                 hr_scale=2.0,
                                                 hr_upscaler='Latent',
                                                 hr_second_pass_steps=0,
                                                 hr_resize_x=0,
                                                 hr_resize_y=0,
                                                 )
            p.scripts = script_runner
            p.outpath_grids = opts.outdir_txt2img_grids
            p.outpath_samples = opts.outdir_txt2img_samples
            shared.state.begin()

            if selectable_scripts != None:
                p.script_args = script_args
                processed = scripts_txt2img.run(p, *p.script_args)  # Need to pass args as list here
            else:
                p.script_args = tuple(script_args)  # Need to pass args as tuple here
                processed = process_images(p)
            shared.state.end()
            images = processed.images
            print(images)

        start_task.click(fn=start_console_task, inputs=choose_task, outputs=task_log)
        stop_task.click(fn=stop_console_task, outputs=task_log)
        use_lark.change(fn=is_show_lark, inputs=use_lark, outputs=use_lark_group)
        create_task.click(fn=save_config, inputs=all_para, outputs=create_hint)
        load_task.click(fn=choose_task_fn, inputs=select_task, outputs=all_para)
        delete_task.click(fn=auto_delete_task, inputs=select_task, outputs=create_hint)
    return (auto_tool_interface, 'Auto Tool', 'auto_tool_tab'),

script_callbacks.on_ui_tabs(on_ui_tabs)
