from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class PasswordMixinSchema(BaseModel):
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Password must be at least 8 characters long.",
    )

    # @field_validator('password')
    # def validate_password(cls, value):
    #     """
    #     Validate the password complexity:
    #     - At least one uppercase letter
    #     - At least one lowercase letter
    #     - At least one digit
    #     - At least one special character
    #     """
    #     if not re.search(r'[A-Z]', value):
    #         raise ValueError('Password must contain at least one uppercase letter')
    #     if not re.search(r'[a-z]', value):
    #         raise ValueError('Password must contain at least one lowercase letter')
    #     if not re.search(r'[0-9]', value):
    #         raise ValueError('Password must contain at least one digit')
    #     if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
    #         raise ValueError('Password must contain at least one special character')
    #     return value
class UsernameField(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50
    )   

class RegisterEssentials(PasswordMixinSchema, UsernameField):
    role: Optional[str] = Field(
        max_length=20
    )
    
class UserUpdateRequest(UsernameField):
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
    middle_name: Optional[str] = Field(
        None,
        max_length=30
    )
    group_id: Optional[int] = Field(
        None
    )

class UserCreateRequest(RegisterEssentials, UserUpdateRequest):
    ...