import pydantic
from typing import Optional, Type


class CreateAd(pydantic.BaseModel):

    ad_title: str
    ad_description: str
    ad_creator: int

    @pydantic.validator("ad_title")
    def validate_title(cls, value):
        if value == '':
            raise ValueError("empty title")
        
        return value




class PathAd(pydantic.BaseModel):

    ad_title: Optional[str]
    ad_description: Optional[str]
   
    @pydantic.validator("ad_title")
    def validate_title(cls, value):
        if value == '':
            raise ValueError("empty title")
        
        return value


class CreateUser(pydantic.BaseModel):
    user_mail: str
    user_password: str



VALIDATION_CLASS = Type[CreateAd] | Type[PathAd] | Type[CreateUser]