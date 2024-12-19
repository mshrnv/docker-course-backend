from pydantic import BaseModel, Field, ConfigDict


class UserCreateUpdateSchema(BaseModel):
    username: str
    password: str
    is_admin: bool = False


class UserSchema(UserCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int