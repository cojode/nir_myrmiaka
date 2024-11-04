from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sa_update, delete as sa_delete
from typing import Type, TypeVar, Generic, Dict, Any, Optional, List
from sqlalchemy.orm import declarative_base

ModelType = TypeVar("ModelType", bound=declarative_base())

class BaseCRUD(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(self, db: AsyncSession, create_with: Dict[str, Any]) -> ModelType:
        """Create a new instance in the database."""
        obj = self.model(**create_with)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def read(self, db: AsyncSession, search_for: Dict[str, Any]) -> Optional[ModelType]:
        """Read an instance from the database."""
        query = select(self.model).filter_by(**search_for)
        result = await db.execute(query)
        return result.scalars().first()

    async def read_all(self, db: AsyncSession, search_for: Optional[Dict[str, Any]] = None) -> List[ModelType]:
        """Read multiple instances from the database based on search criteria."""
        query = select(self.model)
        if search_for:
            query = query.filter_by(**search_for)
        result = await db.execute(query)
        return result.scalars().all()

    async def update(self, db: AsyncSession, obj_id: Any, replace_with: Dict[str, Any]) -> Optional[ModelType]:
        """Update an instance in the database."""
        query = sa_update(self.model).where(self.model.id == obj_id).values(**replace_with).execution_options(synchronize_session="fetch")
        await db.execute(query)
        await db.commit()
        return await self.read(db, {"id": obj_id})

    async def delete(self, db: AsyncSession, obj_id: Any) -> bool:
        """Delete an instance from the database."""
        query = sa_delete(self.model).where(self.model.id == obj_id).execution_options(synchronize_session="fetch")
        await db.execute(query)
        await db.commit()
        return True