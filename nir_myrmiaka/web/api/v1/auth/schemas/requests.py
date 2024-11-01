from pydantic import Field

from nir_myrmiaka.web.api.v1.schemas import PasswordMixinSchema


class UserCreateRequest(PasswordMixinSchema):
    """Schema for user creation request."""
    login: str = Field(
        ...,
        min_length=3,
        max_length=30,
        pattern=r'^[a-zA-Z0-9_]+$',
        description="Username must be 3-30 characters long and can contain letters, numbers, and underscores.",
    )
    status: str = Field(
        ...,
        max_length=50,
        pattern=r'^[a-zA-Z0-9 ]+$',
        description="Status can contain letters, numbers, and spaces, max length is 50",
    )
