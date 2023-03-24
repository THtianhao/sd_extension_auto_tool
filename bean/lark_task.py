from pydantic import BaseModel

class LarkTask(BaseModel):
    file_token: str = ""
    sheet_id: str = ""
    link: str = ""
    error: bool = False
    error_message: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
