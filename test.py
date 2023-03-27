import os
from extensions.sd_extension_auto_tool.utils.share import auto_merge_model_path, ckpt_dir

if __name__ == "__main__":

    def set_task_list():
        list_dir = []
        for root, dirs, files in os.walk(ckpt_dir):
            for dir in dirs:
                list_dir.append(dir)
        return list_dir
    set_task_list()
