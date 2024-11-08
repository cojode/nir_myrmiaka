from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Type, TypeVar, List, Optional, Any, Dict, Generic
from sqlalchemy import select as sql_select, update as sql_update, delete as sql_delete
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from nir_myrmiaka.db.repositories.crud.query_builder import QueryBuilder

from nir_myrmiaka.db.repositories.crud.exc import (
    RepositoryError,
    UniqueConstraintViolationError,
)

T = TypeVar("T")


class AbstractCRUDRepository(ABC, Generic[T]):
    @abstractmethod
    async def create(self, entity: Optional[T] = None, **kwargs: Any) -> T:
        """
        Creates an entity, either using the provided instance or from keyword arguments.

        :param entity: Optional instance of the model to create.
        :param kwargs: Additional fields to create a new instance if entity is not provided.
        :return: The created instance of the entity.
        :raises UniqueConstraintViolationError: If a unique constraint is violated.
        :raises RepositoryError: If the creation fails due to other database issues.
        """
        pass

    @abstractmethod
    async def read(
        self, builder: Optional["QueryBuilder"] = None, only_first=False
    ) -> List[T]:
        """
        Reads entities with an optional QueryBuilder for custom filtering.
        By default reads all entries, alter only_first flag to read only first entry.

        :param builder: Optional QueryBuilder instance for building complex query conditions.
        :return: List of entities matching the conditions.
        :raises RepositoryError: If the read operation fails.
        """
        pass

    @abstractmethod
    async def update(
        self, builder: Optional["QueryBuilder"] = None, **kwargs: Any
    ) -> int:
        """
        Updates entities based on conditions set in QueryBuilder and specified fields.

        :param builder: Optional QueryBuilder instance for building complex query conditions.
        :param fields: Fields to update in the matching entities.
        :return: Number of rows affected by the update.
        :raises ValueError: If no fields are provided for updating.
        :raises RepositoryError: If the update operation fails.
        """
        pass

    @abstractmethod
    async def delete(self, builder: Optional["QueryBuilder"] = None) -> int:
        """
        Deletes entities based on conditions set in QueryBuilder.

        :param builder: Optional QueryBuilder instance for building complex query conditions.
        :return: Number of rows affected by the delete operation.
        :raises RepositoryError: If the delete operation fails.
        """
        pass

    @abstractmethod
    async def save(self, entity: T) -> T:
        """
        Saves (inserts or updates) the provided entity in the database.

        :param entity: The entity instance to be saved.
        :return: The saved instance of the entity.
        :raises RepositoryError: If the save operation fails.
        """
        pass


@dataclass
class CRUDRepository(AbstractCRUDRepository[T]):
    session: AsyncSession
    model: Type[T]

    async def create(self, entity: Optional[T] = None, **kwargs: Any) -> T:
        try:
            async with self.session as session:
                instance = entity if entity else self.model(**kwargs)
                session.add(instance)
                await session.commit()
                await session.refresh(instance)
            return instance
        except IntegrityError as e:
            raise UniqueConstraintViolationError(
                f"Duplicate entry or unique constraint violated: {e}"
            ) from e
        except SQLAlchemyError as e:
            raise RepositoryError(f"Failed to create entity: \nentity={entity}, \nkwargs={kwargs} \n SQLAlchemyError: {e}") from e

    async def read(
        self, builder: Optional[QueryBuilder] = None, only_first=False
    ) -> List[T]:
        try:
            async with self.session as session:
                query = (
                    builder.apply_to(sql_select(self.model))
                    if builder
                    else sql_select(self.model)
                )
                result = await session.execute(query)
                result_scalars = result.scalars()
                return result_scalars.first() if only_first else result_scalars.all()
        except SQLAlchemyError as e:
            raise RepositoryError("Failed to read entities") from e

    async def update(
        self, builder: Optional[QueryBuilder] = None, **fields: Dict[str, Any]
    ) -> int:
        if not fields:
            raise ValueError("No fields provided to update")

        try:
            async with self.session as session:
                query = sql_update(self.model).values(**fields)
                if builder:
                    query = builder.apply_to(query)
                result = await session.execute(query)
                await session.commit()
                return result.rowcount
        except SQLAlchemyError as e:
            raise RepositoryError("Failed to update entities") from e

    async def delete(self, builder: Optional[QueryBuilder] = None) -> int:
        try:
            async with self.session as session:
                query = sql_delete(self.model)
                if builder:
                    query = builder.apply_to(query)
                result = await session.execute(query)
                await session.commit()
                return result.rowcount
        except SQLAlchemyError as e:
            raise RepositoryError("Failed to delete entities") from e

    async def save(self, entity: T) -> T:
        try:
            async with self.session.get_session() as session:
                session.add(entity)
                await session.flush()
                await session.refresh(entity)
            return entity
        except SQLAlchemyError as e:
            raise RepositoryError("Failed to save entity") from e
