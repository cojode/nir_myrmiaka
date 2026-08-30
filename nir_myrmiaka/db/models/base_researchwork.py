from sqlalchemy import (
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import mapped_column, relationship

from nir_myrmiaka.db.base import Base


class BaseResearchwork(Base):
    __tablename__ = "base_researchwork"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100), nullable=False)
    description = mapped_column(Text, nullable=False)

    base_topics = relationship(
        "BaseTopic",
        uselist=True,
        back_populates="research_work",
        lazy="selectin",
    )
    submissions = relationship(
        "BaseSubmission",
        uselist=True,
        back_populates="research_work",
        lazy="selectin",
    )

    def __str__(self) -> str:
        return self.name
