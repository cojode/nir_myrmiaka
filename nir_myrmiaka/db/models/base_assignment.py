from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, Text
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.inspection import inspect

from nir_myrmiaka.db.base import Base

from typing import Dict, Any

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
        lazy="joined",
    )
    teacher = relationship(
        "UserProfile",
        foreign_keys=[teacher_id],
        back_populates="assignment_supervisor",
        lazy="joined",
    )
    submissions = relationship(
        "BaseSubmission", uselist=True, back_populates="assignment"
    )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the BaseAssignment model instance into a dictionary.
        Uses inspect to ensure relationships are loaded.
        """
        # Get the SQLAlchemy inspector for this instance
        insp = inspect(self)

        # Base scalar fields
        assignment_dict = {
            "id": self.id,
            "is_accepted": self.is_accepted,
            "is_reviewed": self.is_reviewed,
            "created_at": (
                self.created_at.isoformat() if self.created_at else None
            ),
            "student_id": self.student_id,
            "teacher_id": self.teacher_id,
            "text": self.text,
        }

        # Check if the 'student' relationship is loaded
        if insp.attrs.student.loaded_value is not None:
            assignment_dict["student"] = (
                self.student.to_plain_dict()
            )  # Assuming UserProfile has a to_dict method
        else:
            assignment_dict["student"] = None  # Relationship not loaded

        # Check if the 'teacher' relationship is loaded
        if insp.attrs.teacher.loaded_value is not None:
            assignment_dict["teacher"] = (
                self.teacher.to_plain_dict()
            )  # Assuming UserProfile has a to_dict method
        else:
            assignment_dict["teacher"] = None

        # if insp.attrs.base_submission.loaded_value is not None:
        #     assignment_dict["base_submission"] = [
        #         submission.to_plain_dict()
        #         for submission in self.base_submission
        #     ]
        # else:
        #     assignment_dict["base_submission"] = []

        return assignment_dict

    def to_plain_dict(self) -> Dict[str, Any]:
        """
        Converts the BaseAssignment instance into a dictionary with only scalar fields.
        Avoids relationships to prevent circular dependencies and lazy loading.
        """
        return {
            "id": self.id,
            "is_accepted": self.is_accepted,
            "is_reviewed": self.is_reviewed,
            "created_at": (
                self.created_at.isoformat() if self.created_at else None
            ),
            "student_id": self.student_id,
            "teacher_id": self.teacher_id,
            "text": self.text,
        }
