from nir_myrmiaka.db.base import Base
from sqlalchemy.sql.sqltypes import String
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy import event

class StatusModel(Base):
    __tablename__ = "status"
    status_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    value: Mapped[str] = mapped_column(String(128))
    
@event.listens_for(StatusModel.__table__, "after_create")
def insert_initial_values(target, connection, **kw):
    initial_values = [{"status_id": 1, "value": "student"},
                      {"status_id": 2, "value": "teacher"},
                      {"status_id": 3, "value": "admin"}]

    connection.execute(target.insert(), initial_values)