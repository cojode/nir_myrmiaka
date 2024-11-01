from nir_myrmiaka.db.base import Base
from sqlalchemy.sql.sqltypes import Text
from sqlalchemy.orm import Mapped, mapped_column

class PZModel(Base):
    __tablename__ = "pz"
    pz_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    state: Mapped[str] = mapped_column(Text)