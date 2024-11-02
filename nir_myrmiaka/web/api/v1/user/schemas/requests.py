from pydantic import Field, BaseModel, EmailStr
from typing import Optional

class UserUpdateRequest(BaseModel):
    """Schema for user creation request."""
    username: str = Field(
        ...,
        min_length=3,
        max_length=30,
        pattern=r'^[a-zA-Z0-9_]+$',
        description="Username must be 3-30 characters long and can contain letters, numbers, and underscores.",
    )
    status: Optional[str] = Field(
        ...,
        max_length=50,
        pattern=r'^[a-zA-Z0-9 ]+$',
        description="Status can contain letters, numbers, and spaces, max length is 50",
    )
    first_name: Optional[str] = Field(
        ...,
        max_length=50,
        pattern=r'^[a-zA-Z0-9 ]+$',
        description="Status can contain letters, numbers, and spaces, max length is 50"
    )
    phone_number: Optional[str] = Field(
        ...,
        max_length=10,
        pattern=r'^[+][7][0-9]+$',
        description="Phone number"
    )
    
    mail: Optional[EmailStr] = None