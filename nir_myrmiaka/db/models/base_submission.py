from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import mapped_column, relationship

from nir_myrmiaka.db.base import Base


class BaseSubmission(Base):
    __tablename__ = 'base_submission'
    __table_args__ = (
        Index('base_submission_assignment_id_907d9d53', 'assignment_id'),
        Index('base_submission_research_work_id_6a4c7968', 'research_work_id')
    )

    id = mapped_column(Integer, primary_key=True)
    assignment_id = mapped_column(ForeignKey('base_assignment.id'), nullable=False)
    semester = mapped_column(String(100))
    created_at = mapped_column(DateTime)
    research_work_id = mapped_column(ForeignKey('base_researchwork.id'))

    assignment = relationship('BaseAssignment', back_populates='base_submission')
    research_work = relationship('BaseResearchwork', back_populates='base_submission')
    base_file = relationship('BaseFile', uselist=True, back_populates='submission')