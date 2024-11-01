from nir_myrmiaka.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

class AdminModel(Base):
    __tablename__ = "admin"
    admin_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))