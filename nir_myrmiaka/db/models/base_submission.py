from sqlalchemy import DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from nir_myrmiaka.db.base import Base


class BaseSubmission(Base):
    __tablename__ = "base_submission"
    __table_args__ = (
        Index("base_submission_assignment_id_907d9d53", "assignment_id"),
        Index("base_submission_research_work_id_6a4c7968", "researchwork_id"),
    )

    id = mapped_column(Integer, primary_key=True)
    assignment_id = mapped_column(ForeignKey("base_assignment.id"), nullable=False)
    submission_title = mapped_column(String(100))
    semester = mapped_column(String(100))
    created_at = mapped_column(DateTime)
    researchwork_id = mapped_column(ForeignKey("base_researchwork.id"))

    submission_topics = relationship(
        "SubmissionTopic",
        uselist=True,
        back_populates="submission",
        lazy="joined",
    )
    assignment = relationship(
        "BaseAssignment", back_populates="submissions", lazy="joined"
    )
    research_work = relationship(
        "BaseResearchwork", back_populates="submissions", lazy="joined"
    )
