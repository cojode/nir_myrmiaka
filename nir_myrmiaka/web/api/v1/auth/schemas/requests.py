from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from datetime import datetime

from nir_myrmiaka.web.api.v1.schemas import PasswordMixinSchema

class UserCreateRequest(PasswordMixinSchema):
    '''Non-optional fields for values in AuthUser'''
    username: str = Field()
    first_name: str = Field(
        max_length=150
    )
    last_name: str = Field(
        max_length=150
    )
    email: EmailStr = Field(
        max_length=254
    )
    date_joined: datetime = Field()
    last_login: datetime = Field()
    
    '''Semi-optional fields for flags in AuthUser'''
    is_superuser: Optional[bool] = False
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = True
    
    '''Truly optional fields for userprofile'''
    group_id: int = Field()
    middle_name: Optional[str] = Field(
        max_length=30
    )
    role: Optional[str] = Field(
        max_length=20
    )