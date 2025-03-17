from sqlalchemy import ForeignKey, Index, Integer, String, DateTime
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.inspection import inspect
from typing import Any, Dict

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

    group_id = mapped_column(ForeignKey("users_group.id"))

    group = relationship(
        "UsersGroup", back_populates="user_profile", lazy="joined"
    )

    assignment_subordinate = relationship(
        "BaseAssignment",
        uselist=True,
        foreign_keys="[BaseAssignment.student_id]",
        back_populates="student",
        lazy="joined",
    )

    assignment_supervisor = relationship(
        "BaseAssignment",
        uselist=True,
        foreign_keys="[BaseAssignment.teacher_id]",
        back_populates="teacher",
        lazy="joined",
    )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the UserProfile instance into a dictionary, including relationships if loaded.
        """
        # Get the SQLAlchemy inspector for this instance
        insp = inspect(self)

        # Extract direct attributes
        data = {
            "id": self.id,
            "password": self.password,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "middle_name": self.middle_name,
            "date_joined": (
                self.date_joined.isoformat() if self.date_joined else None
            ),
            "last_login": (
                self.last_login.isoformat() if self.last_login else None
            ),
            "role": self.role,
            "group_id": self.group_id,
        }

        data["group"] = (
            (
                self.group.to_plain_dict()
                if hasattr(self.group, "to_plain_dict")
                else None
            )
            if insp.attrs.group.loaded_value
            else None
        )

        data["assignment_subordinate"] = (
            [
                (
                    assignment.to_plain_dict()
                    if hasattr(assignment, "to_plain_dict")
                    else None
                )
                for assignment in self.assignment_subordinate
            ]
            if insp.attrs.assignment_subordinate.loaded_value
            else None
        )

        data["assignment_supervisor"] = (
            [
                (
                    assignment.to_plain_dict()
                    if hasattr(assignment, "to_plain_dict")
                    else None
                )
                for assignment in self.assignment_supervisor
            ]
            if insp.attrs.assignment_supervisor.loaded_value
            else None
        )

        return data

    def to_plain_dict(self) -> Dict[str, Any]:
        """
        Converts the UserProfile instance into a dictionary with only scalar fields.
        Avoids relationships to prevent circular dependencies and lazy loading.
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "middle_name": self.middle_name,
            "date_joined": (
                self.date_joined.isoformat() if self.date_joined else None
            ),
            "last_login": (
                self.last_login.isoformat() if self.last_login else None
            ),
            "role": self.role,
            "group_id": self.group_id,
        }
