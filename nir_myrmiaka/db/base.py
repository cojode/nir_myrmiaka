from sqlalchemy.orm import DeclarativeBase

from nir_myrmiaka.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
