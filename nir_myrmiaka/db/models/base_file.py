from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import mapped_column, relationship

from nir_myrmiaka.db.base import Base


class BaseFile(Base):
    __tablename__ = "base_file"
    __table_args__ = (
        Index("base_file_submission_id_a4445a9e", "submission_id"),
        Index("base_file_topic_id_0936a51b", "topic_id"),
    )

    id = mapped_column(Integer, primary_key=True)
    is_accepted = mapped_column(Boolean, nullable=False)
    upload_date = mapped_column(DateTime, nullable=False)
    is_reviewed = mapped_column(Boolean, nullable=False)
    filename = mapped_column(String(100))
    topic_id = mapped_column(ForeignKey("base_topic.id"))
    submission_id = mapped_column(ForeignKey("base_submission.id"))
    comment = mapped_column(Text)

    submission = relationship("BaseSubmission", back_populates="base_file")
    topic = relationship("BaseTopic", back_populates="base_file")
