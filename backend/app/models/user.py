from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    username: str

class UserInDB(UserOut):
    hashed_password: str