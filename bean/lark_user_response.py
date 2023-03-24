from dataclasses import dataclass

@dataclass
class UserResponseData:
    access_token: str
    token_type: str
    expires_in: int
    name: str
    en_name: str
    avatar_url: str
    avatar_thumb: str
    avatar_middle: str
    avatar_big: str
    open_id: str
    union_id: str
    email: str
    enterprise_email: str
    user_id: str
    mobile: str
    tenant_key: str
    refresh_expires_in: int
    refresh_token: str
    sid: str

@dataclass
class UserResponse:
    code: int
    msg: str
    data: UserResponseData
