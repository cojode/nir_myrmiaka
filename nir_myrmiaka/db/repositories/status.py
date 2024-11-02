from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from nir_myrmiaka.db.models.status import StatusModel as Status
from nir_myrmiaka.db.models.users import UsersModel as User

async def get_status_id(db: AsyncSession, status_value: str) -> int | None:
    stmt = select(Status).where(Status.value == status_value)
    result = await db.execute(stmt)
    return result.scalars().first().status_id