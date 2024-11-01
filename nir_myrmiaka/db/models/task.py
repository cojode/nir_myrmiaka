from nir_myrmiaka.db.base import Base
from sqlalchemy.sql.sqltypes import Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

class TaskModel(Base):
    __tablename__ = "task"
    task_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    global_mark_id: Mapped[int] = mapped_column(ForeignKey('global_mark.global_mark_id'))
    work_id: Mapped[int] = mapped_column(ForeignKey('works.work_id'))
    state: Mapped[str] = mapped_column(Text, nullable=False)