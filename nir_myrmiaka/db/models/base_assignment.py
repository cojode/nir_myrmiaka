from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import mapped_column, relationship

from nir_myrmiaka.db.base import Base


class BaseAssignment(Base):
    __tablename__ = "base_assignment"
    __table_args__ = (
        Index("base_assignment_student_id_28cc3722", "student_id"),
        Index("base_assignment_teacher_id_829fa074", "teacher_id"),
    )

    id = mapped_column(Integer, primary_key=True)
    is_accepted = mapped_column(Boolean, nullable=False)
    created_at = mapped_column(DateTime, nullable=False)
    student_id = mapped_column(ForeignKey("users_userprofile.id"), nullable=False)
    teacher_id = mapped_column(ForeignKey("users_userprofile.id"), nullable=False)
    text = mapped_column(Text, nullable=False)
    is_reviewed = mapped_column(Boolean, nullable=False)

    student = relationship(
        "UsersUserprofile", foreign_keys=[student_id], back_populates="base_assignment"
    )
    teacher = relationship(
        "UsersUserprofile", foreign_keys=[teacher_id], back_populates="base_assignment_"
    )
    base_submission = relationship(
        "BaseSubmission", uselist=True, back_populates="assignment"
    )
