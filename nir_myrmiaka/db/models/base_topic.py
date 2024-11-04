from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import mapped_column, relationship

from nir_myrmiaka.db.base import Base

class BaseTopic(Base):
    __tablename__ = 'base_topic'
    __table_args__ = (
        Index('base_topic_research_work_id_f512bc53', 'research_work_id'),
    )

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100), nullable=False)
    research_work_id = mapped_column(ForeignKey('base_researchwork.id'))

    research_work = relationship('BaseResearchwork', back_populates='base_topic')
    base_file = relationship('BaseFile', uselist=True, back_populates='topic')