from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from nir_myrmiaka.db.base import Base

class BaseFile(Base):
    __tablename__ = "base_file"

    id = mapped_column(Integer, primary_key=True)
    original_filename = mapped_column(String)
    upload_date = mapped_column(DateTime, nullable=False)
    content_type = mapped_column(String)
    size = mapped_column(Integer)
    is_reviewed = mapped_column(Boolean, default=False)
    storage_path = mapped_column(String, nullable=False)

    submission_topic_id = mapped_column(
        ForeignKey("submission_topic.id"), nullable=False
    )

    submission_topic = relationship(
        "SubmissionTopic", back_populates="files", lazy="joined"
    )
