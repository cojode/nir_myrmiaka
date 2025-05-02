from typing import TypeVar, Generic
from nir_myrmiaka.db.database import Database
from nir_myrmiaka.db.repositories.crud.extended import ExtendedCRUDRepository
from abc import ABC

T = TypeVar("T", bound="Base")
R = TypeVar("T", bound="ExtendedCRUDRepository")


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

    async def _search_model_by_fields(self, **kwargs) -> list[dict]:
        entities = await self.repo.find_by_fields(**kwargs)
        return [entity.to_dict() for entity in entities]

    async def _list_all_models(self) -> list[dict]:
        return await self._search_model_by_fields()

    async def _create_model(self, **kwargs) -> dict:
        entity = await self.repo.create(**kwargs)
        return entity.to_dict()

    async def _update_model(
        self, id: int, use_plain: bool = False, **kwargs
    ) -> dict:
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
