from sqlalchemy import ForeignKey, Integer, Text, Boolean
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

    topic_id = mapped_column(ForeignKey("base_topic.id"))
    comment_id = mapped_column(ForeignKey("submission_topic_comment.id"))

    comments = relationship(
        "SubmissionTopicComment",
        uselist=True,
        back_populates="submission_topic",
        lazy="joined",
    )

    submission = relationship(
        "BaseSubmission", back_populates="submission_topics", lazy="joined"
    )
    topic = relationship(
        "BaseTopic", back_populates="submission_topics", lazy="joined"
    )

    files = relationship(
        "BaseFile",
        uselist=True,
        back_populates="submission_topic",
        lazy="joined",
    )
