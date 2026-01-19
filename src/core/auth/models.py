from pydantic import BaseModel
from pydantic import BaseModel, constr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None



class PasswordChangeRequest(BaseModel):
    current_password: constr(min_length=6)
    new_password: constr(min_length=6)
