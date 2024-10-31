from sqlalchemy.orm import Mapped, mapped_column, relationship
from nir_myrmiaka.db.base import Base

class UsersModel(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)