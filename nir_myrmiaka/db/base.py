from sqlalchemy import inspect
from typing import Any, Dict
from sqlalchemy.orm import DeclarativeBase

from nir_myrmiaka.log import logger

from nir_myrmiaka.db.meta import meta


class Base(DeclarativeBase):

    metadata = meta

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the model instance into a dictionary, including relationships if loaded.
        """

        insp = inspect(self)
        data = {}

        for attr in insp.mapper.column_attrs:
            value = getattr(self, attr.key)
            if value is not None and hasattr(value, "isoformat"):
                value = value.isoformat()
            data[attr.key] = value

        for attr in insp.mapper.relationships:
            if insp.attrs[attr.key].loaded_value is not None:
                if attr.uselist:
                    data[attr.key] = [
                        (
                            item.to_plain_dict()
                            if hasattr(item, "to_plain_dict")
                            else None
                        )
                        for item in getattr(self, attr.key)
                    ]
                else:
                    data[attr.key] = (
                        getattr(self, attr.key).to_plain_dict()
                        if hasattr(getattr(self, attr.key), "to_plain_dict")
                        else None
                    )
            else:
                data[attr.key] = None
        logger.info(f"Converted model {self} to {data}")
        return data

    def to_plain_dict(self) -> Dict[str, Any]:
        """
        Converts the model instance into a dictionary with only scalar fields.
        Avoids relationships to prevent circular dependencies and lazy loading.
        """
        insp = inspect(self)
        data = {}

        for attr in insp.mapper.column_attrs:
            value = getattr(self, attr.key)
            if value is not None and hasattr(value, "isoformat"):
                value = value.isoformat()
            data[attr.key] = value

        return data
