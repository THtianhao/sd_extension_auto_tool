import os
from extensions.sd_extension_auto_tool.utils.share import auto_merge_model_path

if __name__ == "__main__":
    # task_config = AutoTaskConfig()
    # task_config.task_name = "asd"
    # task_config.task_merge.human_model_dir_flag = "asdasd"
    # task_config.task_merge.style_model = "asdasd"
    # task_config.task_merge.base_model_flag = "asdasd"
    # task_config.task_merge.delete_after_merge = "asdasd"
    # task_config.task_merge.interp_method = "Add difference"
    # task_config.task_merge.multiplier = 0.1
    # task_config.task_merge.checkpoint_format = "ckpt"
    # task_config.task_txt2img.use_txt2img = True
    # task_config.task_txt2img.prompt = "asdasd"
    # task_config.task_txt2img.negative_prompt = "asdasd"
    # task_config.task_txt2img.human_weight = 1.1
    # task_config.task_txt2img.seed = 1
    # task_config.task_txt2img.cfg_scale = 1
    # task_config.task_txt2img.sampler_index = "asdasd"
    # task_config.task_txt2img.steps = 1
    # task_config.task_txt2img.batch_size = 1
    # task_config.task_lark.use_lark = True
    # task_config.task_lark.at_user = "asdasd"
    # task_config.save()
    def set_task_list():
        global task_list
        for root, dirs, files in os.walk(auto_merge_model_path):
            for file in files:
                print(os.path.join(root, file))
    set_task_list()

