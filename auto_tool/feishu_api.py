import io
import json

import requests

from extensions.sd_extension_auto_tool.bean.feishu_response import TokenResponse
from extensions.sd_extension_auto_tool.bean.feishu_user_response import UserResponseData

feishu_base_url = "https://open.feishu.cn"
get_access_token = f"{feishu_base_url}/open-apis/auth/v3/tenant_access_token/internal"
get_user_token = f"{feishu_base_url}/open-apis/authen/v1/access_token"
get_pre_code = f"{feishu_base_url}/open-apis/authen/v1/index"
get_refresh_token = f"{feishu_base_url}/open-apis/authen/v1/refresh_access_token"
get_root_token = f"{feishu_base_url}/open-apis/drive/explorer/v2/root_folder/meta"
create_sheet = f"{feishu_base_url}/open-apis/sheets/v3/spreadsheets"

class FeishuApi:
    def __init__(self):
        self.tenant_access_token = ""
        self.user_access_token = ""
        self.session = requests.session()
        self.upload = False
        self.session_success = False

    def set_upload(self, upload):
        self.upload = upload

    def can_upload(self) -> bool:
        if not self.upload:
            return False
        if not self.session_success:
            return False
        return True

    def getToken(self, app_id, app_secret):
        payload = {"app_id": app_id, "app_secret": app_secret}
        response = self.session.post(url=get_access_token, json=payload)
        if response.status_code == 200:
            dict = json.loads(response.content)
            bean = TokenResponse(**dict)
            if bean.code == 0:
                self.tenant_access_token = bean.tenant_access_token
                print(f"access token = {self.tenant_access_token}")
                return bean
            else:
                print(f"get access token fail")

    def get_tenant_headers(self):
        return {
            "Authorization": f"Bearer {self.tenant_access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }

    def get_user_headers(self):
        return {
            "Authorization": f"Bearer {self.user_access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }

    def get_user_access_token(self, code):
        payload = {
            "grant_type": "authorization_code",
            "code": code
        }
        response = self.session.post(url=get_user_token, headers=self.get_tenant_headers(), json=payload)
        if response.status_code == 200:
            dict = json.loads(response.content)
            if dict['code'] == 0:
                bean = UserResponseData(**dict['data'])
                self.user_access_token = bean.access_token
                self.session_success = True
                return bean

    def refresh_user_access_token(self, user_refresh_token):
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": user_refresh_token
        }
        response = self.session.post(url=get_refresh_token, headers=self.get_tenant_headers(), json=payload)
        if response.status_code == 200:
            dict = json.loads(response.content)
            if dict['code'] == 0:
                bean = UserResponseData(**dict['data'])
                self.user_access_token = bean.access_token
                self.session_success = True
                return bean

    def get_root_token(self):
        response = self.session.get(url=get_root_token, headers=self.get_user_headers())
        if response.status_code == 200:
            content = json.loads(response.content)
            if content['code'] == 0:
                root_token = content['data']['token']
                return root_token

    def create_sheet(self, name, root_token):
        payload = {
            "title": name,
            "folder_token": root_token
        }
        response = self.session.post(url=create_sheet, headers=self.get_user_headers(), json=payload)
        if response.status_code == 200:
            content = json.loads(response.content)
            if content['code'] == 0:
                return content['data']['spreadsheet']

    def query_sheetId(self, sheet_token):
        response = self.session.get(url=f"{feishu_base_url}/open-apis/sheets/v3/spreadsheets/{sheet_token}/sheets/query", headers=self.get_user_headers())
        if response.status_code == 200:
            content = json.loads(response.content)
            if content['code'] == 0:
                return content['data']['sheets'][0]['sheet_id']

    def qut_sheet(self, sheet_token, value):
        response = self.session.put(url=f"{feishu_base_url}/open-apis/sheets/v2/spreadsheets/{sheet_token}/values", headers=self.get_user_headers(), json=value)
        print(f"qut_sheet = {response.content}")

    def post_image(self, sheet_token, range, image):
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
        response = self.session.post(url=f"{feishu_base_url}/open-apis/sheets/v2/spreadsheets/{sheet_token}/values_image",
                                     headers=self.get_user_headers(),
                                     data=json.dumps(payload))
        print(f"post_image = {response.content}")

    def set_token(self, user_token):
        self.user_access_token = user_token

def getPreCodeUrl(self):
    return "https://open.feishu.cn/open-apis/authen/v1/index?app_id=cli_a483ea8b94e3100e&redirect_uri=http://127.0.0.1"
