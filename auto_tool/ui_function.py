# import gr
#
# from extensions.sd_extension_auto_tool.bean.task_config import AutoTaskConfig
#
# def save_config(task_name: str,
#                 human_model_dir_flag: str,
#                 style_model: str,
#                 base_model_flag: str,
#                 delete_after_merge: bool,
#                 multiplier: int,
#                 user_txt2img: bool,
#                 prompt: str,
#                 negative_prompt: str,
#                 human_weight: int,
#                 seed: int,
#                 cfg_scale: int,
#                 sampler_index: int,
#                 step: int,
#                 batch_size: int,
#                 user_lark: bool,
#                 at_user: str
#                 ):
#     if task_name is None:
#         return {create_hint: gr.update(value="Enter valid age", visible=True)}
#     json_data = {
#         "task_name": task_name,
#         "task_merge": {
#             "human_model_dir_flag": human_model_dir_flag,
#             "style_model": style_model,
#             "base_model_flag": base_model_flag,
#             "delete_after_merge": delete_after_merge,
#             "interp_method": "Add difference",
#             "multiplier": multiplier,
#             "checkpoint_format": "ckpt"
#         }
#     }
#     if user_txt2img:
#         json_data["task_txt2img"] = {
#             "prompt": prompt,
#             "negative_prompt": negative_prompt,
#             "human_weight": human_weight,
#             "seed": seed,
#             "cfg_scale": cfg_scale,
#             "sampler_index": sampler_index,
#             "steps": step,
#             "batch_size": batch_size
#         }
#     if user_lark:
#         json_data["task_lark"] = {
#             "at_user": at_user
#         }
#     task = AutoTaskConfig(json_data)
#     result = task.save()
#     if result is None:
#         return "json save error"
#     return "success"
