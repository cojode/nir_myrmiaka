from sqlalchemy import ForeignKey, Integer, Text, Boolean, DateTime
from sqlalchemy.orm import mapped_column, relationship

from nir_myrmiaka.db.base import Base


class SubmissionTopicComment(Base):
    __tablename__ = "submission_topic_comment"

    id = mapped_column(Integer, primary_key=True)
    comment = mapped_column(Text)
    is_reviewed = mapped_column(Boolean, default=False)

    created_at = mapped_column(DateTime)

    submission_topic_id = mapped_column(
        ForeignKey("submission_topic.id"), nullable=False
    )

    user_id = mapped_column(
        ForeignKey("user_profile.id"), nullable=False
    )

    submission_topic = relationship(
        "SubmissionTopic",
        back_populates="comments",
        lazy="selectin",
        foreign_keys=[submission_topic_id],
    )

    user = relationship(
        "UserProfile",
        lazy="selectin",
        foreign_keys=[user_id],
    )

    def __str__(self) -> str:
        snippet = (self.comment or "")[:50]
        return f"Comment #{self.id}: {snippet}"
