from sqlalchemy import ForeignKey, Integer, Boolean
from sqlalchemy.orm import mapped_column, relationship

from nir_myrmiaka.db.base import Base


class SubmissionTopic(Base):
    __tablename__ = "submission_topic"

    id = mapped_column(Integer, primary_key=True)
    is_accepted = mapped_column(Boolean)
    is_reviewed = mapped_column(Boolean)

    submission_id = mapped_column(
        ForeignKey("base_submission.id"), nullable=False
    )

    student_id = mapped_column(ForeignKey("user_profile.id"), nullable=False)
    teacher_id = mapped_column(ForeignKey("user_profile.id"), nullable=False)

    topic_id = mapped_column(ForeignKey("base_topic.id"))
    comment_id = mapped_column(ForeignKey("submission_topic_comment.id"))

    comments = relationship(
        "SubmissionTopicComment",
        back_populates="submission_topic",
        foreign_keys="[SubmissionTopicComment.submission_topic_id]",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    submission = relationship(
        "BaseSubmission", back_populates="submission_topics", lazy="selectin"
    )
    topic = relationship(
        "BaseTopic", back_populates="submission_topics", lazy="selectin"
    )

    files = relationship(
        "BaseFile",
        uselist=True,
        back_populates="submission_topic",
        lazy="selectin",
    )

    def __str__(self) -> str:
        return f"SubmissionTopic #{self.id}"
