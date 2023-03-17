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
    obj = AutoTaskConfig(data)
    print(obj)
