import json

from extensions.sd_extension_auto_tool.bean.task_config import AutoTaskConfig

if __name__ == "__main__":
    data = {
        "task_merge": {
            "human_model_dir_flag": "male",
            "style_model": "style/elldrethsLucidMix_v10.ckpt",
            "base_model_flag": "v1-5-pruned.ckpt",
            "delete_after_merge": False,
            "interp_method": "Add difference",
            "multiplier": 0.8,
            "checkpoint_format": "ckpt"
        },
        "task_txt2img": {
            "prompt": "portrait,delicate eyes,beautiful eyes, by ((Alice Pasquini)) and ((alena aenami)), (punk boy), purple hair,painting style,Hand Painted, wild hair, leather jacket, concert lights, 2D style, character portrait, avatar, art by cardstylev3",
            "negative_prompt": "bags under the eyes,upper body, worst quality, low quality, medium quality, deleted, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, jpeg artifacts, signature, watermark, username, blurry, 3D,real people",
            "human_weight": 1,
            "seed": -1,
            "cfg_scale": 9,
            "sampler_index": "DPM++ 2S a Karras",
            "steps": 20,
            "batch_size": 4
        },
        "task_lark": {
            "user_access_token": "asd",
            "at_user": "bbb"
        }
    }

    task_config = AutoTaskConfig()
    task_config.task_name = "asd"
    task_config.task_merge.human_model_dir_flag = "asdasd"
    task_config.task_merge.style_model = "asdasd"
    task_config.task_merge.base_model_flag = "asdasd"
    task_config.task_merge.delete_after_merge = "asdasd"
    task_config.task_merge.interp_method = "Add difference"
    task_config.task_merge.multiplier = 0.1
    task_config.task_merge.checkpoint_format = "ckpt"
    task_config.task_txt2img.use_txt2img = True
    task_config.task_txt2img.prompt = "asdasd"
    task_config.task_txt2img.negative_prompt = "asdasd"
    task_config.task_txt2img.human_weight = 1.1
    task_config.task_txt2img.seed = 1
    task_config.task_txt2img.cfg_scale = 1
    task_config.task_txt2img.sampler_index = "asdasd"
    task_config.task_txt2img.steps = 1
    task_config.task_txt2img.batch_size = 1
    task_config.task_lark.use_lark = True
    task_config.task_lark.at_user = "asdasd"
    task_config.save()

    print("asdasd")

