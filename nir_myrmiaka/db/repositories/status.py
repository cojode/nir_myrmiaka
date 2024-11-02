from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from nir_myrmiaka.db.models.status import StatusModel as Status
from nir_myrmiaka.db.models.users import UsersModel as User

async def default_status_fill_routine(db: AsyncSession):
    """
        Fill on table creation predefined status list
    """
