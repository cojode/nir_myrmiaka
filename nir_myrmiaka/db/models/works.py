from nir_myrmiaka.db.base import Base
from sqlalchemy.sql.sqltypes import Text, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

class WorksModel(Base):
    __tablename__ = "works"
    work_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pz_id: Mapped[int] = mapped_column(ForeignKey('pz.pz_id'))
    rspz_id: Mapped[int] = mapped_column(ForeignKey('rspz.rspz_id'))
    comm: Mapped[Text] = mapped_column()
    mark: Mapped[str] = mapped_column(String(128))