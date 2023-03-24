import io
import json
import os

import requests

from extensions.sd_extension_auto_tool.bean.lark_config import LarkConfig
from extensions.sd_extension_auto_tool.bean.lark_response import TokenResponse
from extensions.sd_extension_auto_tool.bean.lark_user_response import UserResponseData
from extensions.sd_extension_auto_tool.utils.share import auto_lark_config

url_lark_base = r"https://open.feishu.cn"
url_access_token = f"{url_lark_base}/open-apis/auth/v3/tenant_access_token/internal"
url_user_token = f"{url_lark_base}/open-apis/authen/v1/access_token"
url_pre_code = f"{url_lark_base}/open-apis/authen/v1/index"
url_refresh_token = f"{url_lark_base}/open-apis/authen/v1/refresh_access_token"
url_lark_root_token = f"{url_lark_base}/open-apis/drive/explorer/v2/root_folder/meta"
url_lark_create_sheet = f"{url_lark_base}/open-apis/sheets/v3/spreadsheets"

tenant_access_token = ""
user_access_token = ""
user_lark_token_key = "lark_user_token"

def get_access_token():
    global user_access_token
    return user_access_token

def read_lark_config():
    global user_access_token
    if os.path.exists(auto_lark_config):
        with open(auto_lark_config, 'r') as f:
            task_json = json.load(f)
            if task_json is not None:
                user_access_token = task_json[user_lark_token_key]
            return task_json

def save_lark_config(token=""):
    with open(auto_lark_config, 'w') as f:
        config = LarkConfig()
        config.lark_user_token = token
        lark_config_json = config.dict()
        json.dump(lark_config_json, f)

def get_or_refresh_save_user_token(lark_code: str):
    if not len(lark_code): return
    global user_access_token
    response = get_token('cli_a483ea8b94e3100e', 'UhJeWk7YxAgzhbc6mOz6xh7Gkfwu6eGS')
    if response is not None:
        if len(user_access_token):
            return refresh_user_access_token(user_access_token)
        else:
            return get_user_access_token(lark_code)
    else:
        return "Get token fail"

def get_token(app_id, app_secret):
    print("accesstoken")
    print("accesstokenx")
    print("accesstokeny")
    payload = {"app_id": app_id, "app_secret": app_secret}
    response = requests.session().post(url="https://open.feishu.cn", json=payload)
    if response.status_code == 200:
        dict = json.loads(response.content)
        bean = TokenResponse(**dict)
        if bean.code == 0:
            tenant_access_token = bean.tenant_access_token
            return bean

def get_tenant_headers():
    global tenant_access_token
    return {
        "Authorization": f"Bearer {tenant_access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }

def get_user_headers():
    global user_access_token
    return {
        "Authorization": f"Bearer {user_access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }

def get_user_access_token(code):
    global user_access_token, url_user_token
    payload = {
        "grant_type": "authorization_code",
        "code": code
    }
    response = requests.session().post(url=url_user_token, headers=get_tenant_headers(), json=payload)
    if response.status_code == 200:
        dict = json.loads(response.content)
        if dict['code'] == 0:
            bean = UserResponseData(**dict['data'])
            user_access_token = bean.access_token
            save_lark_config(user_access_token)
            return "Lark verify success"
    user_access_token = ""
    save_lark_config()
    return "Lark code expired, please get lark code again"

def refresh_user_access_token(user_refresh_token):
    global user_access_token, url_refresh_token
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": user_refresh_token
    }
    response = requests.session().post(url=url_refresh_token, headers=get_tenant_headers(), json=payload)
    if response.status_code == 200:
        dict = json.loads(response.content)
        if dict['code'] == 0:
            bean = UserResponseData(**dict['data'])
            user_access_token = bean.access_token
            save_lark_config(user_access_token)
            return "Refresh token success"
    user_access_token = ""
    save_lark_config()
    return "Lark code expired,please get lark code again"

def get_root_token():
    global user_access_token
    response = requests.session().get(url=url_lark_root_token, headers=get_user_headers())
    if response.status_code == 200:
        content = json.loads(response.content)
        if content['code'] == 0:
            root_token = content['data']['token']
            return root_token
    elif response.status_code == 400:
        user_access_token = ""
        save_lark_config(user_access_token)
        return ""

def create_sheet(name, root_token):
    payload = {
        "title": name,
        "folder_token": root_token
    }
    response = requests.session().post(url=url_lark_create_sheet, headers=get_user_headers(), json=payload)
    if response.status_code == 200:
        content = json.loads(response.content)
        if content['code'] == 0:
            return content['data']['spreadsheet']

def query_sheetId(sheet_token):
    response = requests.session().get(url=f"{url_lark_base}/open-apis/sheets/v3/spreadsheets/{sheet_token}/sheets/query", headers=get_user_headers())
    if response.status_code == 200:
        content = json.loads(response.content)
        if content['code'] == 0:
            return content['data']['sheets'][0]['sheet_id']

def put_sheet(sheet_token, value):
    response = requests.session().put(url=f"{url_lark_base}/open-apis/sheets/v2/spreadsheets/{sheet_token}/values", headers=get_user_headers(), json=value)
    print(f"qut_sheet = {response.content}")

def post_image(sheet_token, range, image):
    img_bytes = io.BytesIO()
    # 把PNG格式转换成的四通道转成RGB的三通道，然后再保存成jpg格式
    image = image.convert("RGB")
    # 将图片数据存入字节流管道， format可以按照具体文件的格式填写
    image.save(img_bytes, format="JPEG")
    # 从字节流管道中获取二进制
    image_bytes = list(img_bytes.getvalue())
    payload = {
        "range": range,
        "image": image_bytes,
        "name": "demo.png"
    }
    response = requests.session().post(url=f"{url_lark_base}/open-apis/sheets/v2/spreadsheets/{sheet_token}/values_image",
                                       headers=get_user_headers(),
                                       data=json.dumps(payload))
    print(f"post_image = {response.content}")

def set_token(user_token):
    global user_access_token
    user_access_token = user_token

def getPreCodeUrl():
    return "https://open.feishu.cn/open-apis/authen/v1/index?app_id=cli_a483ea8b94e3100e&redirect_uri=http://127.0.0.1"

read_lark_config()
