from pydantic import BaseModel, constr
import re
from pydantic import BaseModel, validator


class TextInputUser(BaseModel):
  text: constr(min_length=1, strip_whitespace=True)

class User(BaseModel):
    username: str
    password: str

    @validator('username')
    def validate_username(cls, value):
        if not re.match('^([a-z]|[0-9]|@)+$', value):
            raise ValueError('formato de username errado')
        return value
