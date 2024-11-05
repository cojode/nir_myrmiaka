from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from nir_myrmiaka.web.api.v1.schemas import RegisterEssentials
    
class UserUpdateRequest(BaseModel):
    first_name: Optional[str] = Field(
        None,
        max_length=150
    )
    last_name: Optional[str] = Field(
        None,
        max_length=150
    )
    email: Optional[EmailStr] = Field(
        None,
        max_length=254
    )
    is_superuser: Optional[bool] = False
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = True
    
    middle_name: Optional[str] = Field(
        None,
        max_length=30
    )

class UserCreateRequest(RegisterEssentials, UserUpdateRequest):
    ...