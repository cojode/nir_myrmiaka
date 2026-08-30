from sqlalchemy import (
    ForeignKey,
    Index,
    Integer,
    String,
    DateTime,
    Text,
    Boolean,
)
from sqlalchemy.orm import mapped_column, relationship

from nir_myrmiaka.db.base import Base


class UserProfile(Base):
    __tablename__ = "user_profile"
    __table_args__ = (
        Index("merged_user_profile_group_id_d32cb94c", "group_id"),
    )

    id = mapped_column(Integer, primary_key=True)
    password = mapped_column(String(128), nullable=False)
    username = mapped_column(String(150), nullable=False, unique=True)

    email = mapped_column(String(254))
    first_name = mapped_column(String(150))
    last_name = mapped_column(String(150))
    middle_name = mapped_column(String(30))
    date_joined = mapped_column(DateTime)
    last_login = mapped_column(DateTime)
    role = mapped_column(String(20))

    is_active = mapped_column(Boolean, default=False)

    about_me = mapped_column(Text)

    group_id = mapped_column(ForeignKey("users_group.id"))

    group = relationship(
        "UsersGroup", back_populates="user_profile", lazy="selectin"
    )

    notifications = relationship(
        "Notification",
        uselist=True,
        back_populates="user",
        lazy="selectin",
    )

    assignment_subordinate = relationship(
        "BaseAssignment",
        uselist=True,
        foreign_keys="[BaseAssignment.student_id]",
        back_populates="student",
        lazy="selectin",
    )

    assignment_supervisor = relationship(
        "BaseAssignment",
        uselist=True,
        foreign_keys="[BaseAssignment.teacher_id]",
        back_populates="teacher",
        lazy="selectin",
    )

    def __str__(self) -> str:
        name = f"{self.last_name} {self.first_name}".strip()
        return f"{name} (@{self.username})" if name else self.username
