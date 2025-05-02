from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum,
    Boolean,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum

from nir_myrmiaka.db.base import Base


class NotificationType(PyEnum):
    SUBMISSION_TOPIC_FILE_ADDED = "file_added"
    SUBMISSION_TOPIC_ACCEPTED = "submission_accepted"
    SUBMISSION_TOPIC_DECLINED = "submission_declined"
    SUBMISSION_TOPIC_COMMENT_ADDED = "comment_added"


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profile.id"))
    type = Column(Enum(NotificationType))
    message = Column(String)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    related_entity_id = Column(Integer)

    user = relationship(
        "UserProfile", back_populates="notifications", lazy="joined"
    )
