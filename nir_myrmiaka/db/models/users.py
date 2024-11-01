from nir_myrmiaka.db.base import Base
from sqlalchemy.sql.sqltypes import String
from sqlalchemy.orm import Mapped, mapped_column

class UsersModel(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[str] = mapped_column(String(128), nullable=False)
    first_name: Mapped[str] = mapped_column(String(128))
    phone_number: Mapped[str] = mapped_column(String(128))
    mail: Mapped[str] = mapped_column(String(128))