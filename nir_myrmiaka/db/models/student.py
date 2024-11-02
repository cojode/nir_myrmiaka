from nir_myrmiaka.db.base import Base
from sqlalchemy.sql.sqltypes import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

class StudentModel(Base):
    __tablename__ = "student"
    student_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    teacher_id: Mapped[int] = mapped_column(ForeignKey('teacher.teacher_id'), nullable=True)
    task_id: Mapped[int] = mapped_column(ForeignKey('task.task_id'), nullable=True)
    number_group: Mapped[str] = mapped_column(String(128), nullable=True)