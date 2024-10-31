from nir_myrmiaka.db.base import Base
from sqlalchemy.sql.sqltypes import String, Date, func
from sqlalchemy.orm import Mapped, mapped_column

class GlobalMarkModel(Base):
    __tablename__ = "global_mark"
    global_mark_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    mark: Mapped[str] = mapped_column(String(128))
    dates: Mapped[Date] = mapped_column(default=func.now())