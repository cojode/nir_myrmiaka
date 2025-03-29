from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, relationship

from nir_myrmiaka.db.base import Base


class UsersGroup(Base):
    __tablename__ = "users_group"

    id = mapped_column(Integer, primary_key=True)
    group_name = mapped_column(String(20), nullable=False)

    user_profile = relationship(
        "UserProfile", uselist=True, back_populates="group"
    )


class UserGroupTerm(Base):
    __tablename__ = "users_group_term"
    id = mapped_column(Integer, primary_key=True)
    term = mapped_column(String, unique=True)
