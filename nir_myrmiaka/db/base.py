from sqlalchemy import inspect
from typing import Any, Dict
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.hybrid import hybrid_property

from nir_myrmiaka.log import logger

from nir_myrmiaka.db.meta import meta


class Base(DeclarativeBase):
    metadata = meta

    def to_dict(self, include_hybrid: bool = True) -> Dict[str, Any]:
        """Full serialization including relationships"""
        insp = inspect(self)
        data = self._get_scalar_fields(insp, include_hybrid)

        # Handle relationships
        for attr in insp.mapper.relationships:
            if insp.attrs[attr.key].loaded_value is not None:
                data[attr.key] = self._process_relationship(
                    getattr(self, attr.key), attr.uselist
                )

        logger.info(f"Converted model {self} to dict")
        return data

    def to_plain_dict(self) -> Dict[str, Any]:
        """Strictly scalar fields and hybrid properties only"""
        return self._get_scalar_fields(inspect(self), include_hybrid=True)

    def _get_scalar_fields(self, insp, include_hybrid: bool) -> Dict[str, Any]:
        """Core scalar field extraction logic"""
        data = {}

        # 1. Regular columns
        for attr in insp.mapper.column_attrs:
            data[attr.key] = self._format_value(getattr(self, attr.key))

        # 2. Hybrid properties
        if include_hybrid:
            for name, obj in insp.class_.__dict__.items():
                if isinstance(obj, hybrid_property):
                    try:
                        if inspect(self).persistent:
                            data[name] = self._format_value(
                                getattr(self, name)
                            )
                        else:
                            logger.warning(
                                f"Skipping hybrid property {name} - instance is detached"
                            )
                            data[name] = None
                    except Exception as e:
                        logger.warning(
                            f"Could not access hybrid property {name}: {str(e)}"
                        )
                        continue

        return data

    def _format_value(self, value: Any) -> Any:
        """Type conversion helper"""
        if value is None:
            return None
        if hasattr(value, "isoformat"):
            return value.isoformat()
        return value

    def _process_relationship(self, value, is_collection: bool) -> Any:
        """Relationship serialization (not used in plain_dict)"""
        if is_collection:
            return [
                (
                    item.to_plain_dict()
                    if hasattr(item, "to_plain_dict")
                    else None
                )
                for item in value
            ]
        return (
            value.to_plain_dict() if hasattr(value, "to_plain_dict") else None
        )
