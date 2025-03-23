from sqlalchemy import ForeignKey, Integer, Text, Boolean
from sqlalchemy.orm import mapped_column, relationship

from nir_myrmiaka.db.base import Base


class SubmissionTopicComment(Base):
    __tablename__ = "submission_topic_comment"

    id = mapped_column(Integer, primary_key=True)
    comment = mapped_column(Text)
    is_reviewed = mapped_column(Boolean, default=False)

    submission_topic_id = ForeignKey("submission_topic.id")

    submission_topic = relationship(
        "SubmissionTopic", back_populates="comments", lazy="joined"
    )
