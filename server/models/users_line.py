from pydantic import BaseModel

class UsersLine(BaseModel):
    steam_id: int