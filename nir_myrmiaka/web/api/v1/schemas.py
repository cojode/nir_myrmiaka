from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class PasswordMixinSchema(BaseModel):
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Password must be at least 8 characters long.",
    )

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
    

class AssignmentCreateRequest(BaseModel):
    student_id: int = Field(None)
    teacher_id: int = Field(None)
    text: str = Field(None)