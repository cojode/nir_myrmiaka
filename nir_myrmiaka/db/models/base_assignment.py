from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, Text
from sqlalchemy.orm import mapped_column, relationship

from nir_myrmiaka.db.base import Base

class BaseAssignment(Base):
    __tablename__ = "base_assignment"
    __table_args__ = (
        Index("base_assignment_student_id_28cc3722", "student_id"),
        Index("base_assignment_teacher_id_829fa074", "teacher_id"),
    )

    id = mapped_column(Integer, primary_key=True)
    is_accepted = mapped_column(Boolean, default=None)
    is_reviewed = mapped_column(Boolean, nullable=False)
    created_at = mapped_column(DateTime, nullable=False)
    student_id = mapped_column(ForeignKey("user_profile.id"), nullable=False)
    teacher_id = mapped_column(ForeignKey("user_profile.id"), nullable=False)
    text = mapped_column(Text, nullable=False)

    student = relationship(
        "UserProfile",
        foreign_keys=[student_id],
        back_populates="assignment_subordinate",
        lazy="selectin",
    )
    teacher = relationship(
        "UserProfile",
        foreign_keys=[teacher_id],
        back_populates="assignment_supervisor",
        lazy="selectin",
    )
    submissions = relationship(
        "BaseSubmission",
        uselist=True,
        back_populates="assignment",
        lazy="selectin",
    )
