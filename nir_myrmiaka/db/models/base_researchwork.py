from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import mapped_column, relationship

from nir_myrmiaka.db.base import Base

class BaseResearchwork(Base):
    __tablename__ = 'base_researchwork'

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100), nullable=False)
    description = mapped_column(Text, nullable=False)

    base_topic = relationship('BaseTopic', uselist=True, back_populates='research_work')
    base_submission = relationship('BaseSubmission', uselist=True, back_populates='research_work')