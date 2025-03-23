from typing import Type, TypeVar, Generic, Dict, Any
from nir_myrmiaka.db.database import Database
from functools import wraps
from nir_myrmiaka.db.base import Base
from nir_myrmiaka.db.repositories.crud.extended import ExtendedCRUDRepository
from abc import ABC

T = TypeVar("T", bound="Base")


class BaseCRUDService(ABC, Generic[T]):
    def __init__(self, db: Database, repository_class):
        self.db = db
        self.repo: ExtendedCRUDRepository = repository_class(session=db)

    async def _get_model_by_id(self, id: int) -> dict:
        entity = await self.repo.find_by_id(id)
        if not entity:
            raise ValueError(f"Entity with id [{id}] not found")
        return entity.to_dict()

    async def _verify_model_exists(self, id: int) -> dict:
        return await self._get_model_by_id(id)

    async def _list_all_models(self) -> list[dict]:
        entities = await self.repo.find_all()
        return [entity.to_dict() for entity in entities]

    async def _create_model(self, **kwargs) -> dict:
        entity = await self.repo.create(**kwargs)
        return entity.to_dict()

    async def _update_model(self, id: int, **kwargs) -> dict:
        entity = await self.repo.find_by_id(id)
        if not entity:
            raise ValueError(f"Entity with id [{id}] not found")
        for key, value in kwargs.items():
            setattr(entity, key, value)
        updated_entity = await self.repo.save(entity)
        return updated_entity.to_dict()

    async def _delete_model(self, id: int) -> None:
        entity = await self.repo.find_by_id(id)
        if not entity:
            raise ValueError(f"Entity with id [{id}] not found")
        await self.repo.delete(entity)
