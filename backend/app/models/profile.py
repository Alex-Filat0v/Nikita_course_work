from pydantic import BaseModel

class UserProfile(BaseModel):
    username: str
    fullname: str
    birthdate: str
    phone: str
    bio: str = ""