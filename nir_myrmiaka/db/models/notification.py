from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum,
    Boolean,
)
from sqlalchemy.orm import relationship, mapped_column
from datetime import datetime
from enum import Enum as PyEnum

from nir_myrmiaka.db.base import Base


class NotificationType(PyEnum):
    SUBMISSION_TOPIC_FILE_ADDED = "file_added"
    SUBMISSION_TOPIC_ACCEPTED = "submission_accepted"
    SUBMISSION_TOPIC_DECLINED = "submission_declined"
    SUBMISSION_TOPIC_COMMENT_ADDED = "comment_added"


class NotificationEntityModelType(PyEnum):
    SUBMISSION_TOPIC = "submission_topic"
    SUBMISSION = "submission"
    RESEARCH_WORK = "research_work"
    ASSIGNMENT = "assignment"
    USER_PROFILE = "user_profile"
    COMMENT = "comment"
    FILE = "file"


class Notification(Base):
    __tablename__ = "notifications"

    id = mapped_column(Integer, primary_key=True, index=True)
    user_id = mapped_column(Integer, ForeignKey("user_profile.id"))
    type = mapped_column(Enum(NotificationType))
    message = mapped_column(String)
    is_read = mapped_column(Boolean, default=False)
    created_at = mapped_column(DateTime, default=datetime.now)
    related_entity_id = mapped_column(Integer)
    related_entity_model = mapped_column(Enum(NotificationEntityModelType))

    user = relationship(
        "UserProfile", back_populates="notifications", lazy="joined"
    )
