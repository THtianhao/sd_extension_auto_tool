from dataclasses import dataclass

@dataclass
class TokenResponse:
    code: int
    msg: str
    tenant_access_token: str
    expire: int

