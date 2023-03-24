from pydantic import BaseModel

class LarkConfig(BaseModel):
    lark_user_token: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
