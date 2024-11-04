from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import mapped_column, relationship

from nir_myrmiaka.db.base import Base

class AuthUser(Base):
    __tablename__ = 'auth_user'

    id = mapped_column(Integer, primary_key=True)
    password = mapped_column(String(128), nullable=False)
    is_superuser = mapped_column(Boolean, nullable=False)
    username = mapped_column(String(150), nullable=False, unique=True)
    last_name = mapped_column(String(150), nullable=False)
    email = mapped_column(String(254), nullable=False)
    is_staff = mapped_column(Boolean, nullable=False)
    is_active = mapped_column(Boolean, nullable=False)
    date_joined = mapped_column(DateTime, nullable=False)
    first_name = mapped_column(String(150), nullable=False)
    last_login = mapped_column(DateTime)

    users_userprofile = relationship('UsersUserprofile', uselist=True, back_populates='user')