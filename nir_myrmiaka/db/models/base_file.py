from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import mapped_column, relationship

from nir_myrmiaka.db.base import Base

class BaseFile(Base):
    __tablename__ = "base_file"

    id = mapped_column(Integer, primary_key=True)
    upload_date = mapped_column(DateTime, nullable=False)
    filename = mapped_column(String, nullable=False)

    topic_submission_id = mapped_column(ForeignKey("submission_topic.id"))

    submission_topic = relationship("SubmissionTopic", back_populates="files")
