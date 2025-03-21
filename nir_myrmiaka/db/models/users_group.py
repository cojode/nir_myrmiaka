from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import mapped_column, relationship

from nir_myrmiaka.db.base import Base


class UsersGroup(Base):
    __tablename__ = "users_group"

    id = mapped_column(Integer, primary_key=True)
    group_name = mapped_column(String(20), nullable=False)

    user_profile = relationship(
        "UserProfile", uselist=True, back_populates="group"
    )
