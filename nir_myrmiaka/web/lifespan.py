from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import select, delete, text

from nir_myrmiaka.db.meta import meta
from nir_myrmiaka.db.models import load_all_models

from nir_myrmiaka.scripts.group_parser import GroupParser
from nir_myrmiaka.scripts.researchowork_parser import ResearchworkParser

from nir_myrmiaka.db.models.users_group import UserGroupTerm, UsersGroup

from nir_myrmiaka.db.models.base_researchwork import BaseResearchwork
from nir_myrmiaka.db.models.base_topic import BaseTopic

from nir_myrmiaka.db.database import Database
from nir_myrmiaka.services.cdn.minio_async import AsyncMinIOClient
from nir_myrmiaka.container.container import init_container

from nir_myrmiaka.settings import settings

from nir_myrmiaka.log import logger


async def _check_minio_connectivity() -> None:
    logger.info("Checking CDN availabilty...")
    client = AsyncMinIOClient()
    if not await client.check_connection():
        raise RuntimeError("CDN is not accessible")
    logger.info("CDN is available")


async def create_tables(db: Database) -> None:  # pragma: no cover
    """Populates tables in the database."""
    async with db._async_engine.begin() as connection:
        await connection.run_sync(meta.create_all)
        await fill_tables(db)


async def fill_tables(db: Database):
    """Fills tables with static data"""

    async with db.get_session() as session:
        # * Groups
        saved_term = await session.execute(select(UserGroupTerm).limit(1))
        saved_term = saved_term.scalar()
        actual_term, groups_to_add = await GroupParser(
            None if not saved_term else saved_term.term
        ).get_groups()

        if groups_to_add:
            print("Adding groups...")
            await session.execute(delete(UsersGroup))
            await session.execute(delete(UserGroupTerm))
            session.add_all(
                [UsersGroup(group_name=name) for name in groups_to_add]
            )
            session.add(UserGroupTerm(term=actual_term))
            await session.commit()
        else:
            print("Groups are up to date")

        # * Researchworks & Topics
        saved_rw = await session.execute(
            text("SELECT COUNT(*) FROM base_researchwork")
        )
        if saved_rw.scalar() == 0:
            print("Adding researchworks...")
            session.add_all(
                [
                    BaseResearchwork(
                        id=item[0], name=item[1], description=item[2]
                    )
                    for item in ResearchworkParser.get_researchworks()
                ]
            )
        else:
            print("Researchworks are up to date")

        saved_topics = await session.execute(
            text("SELECT COUNT(*) FROM base_topic")
        )
        if saved_topics.scalar() == 0:
            print("Adding topics...")
            session.add_all(
                [
                    BaseTopic(
                        id=item[0], name=item[1], research_work_id=item[2]
                    )
                    for item in ResearchworkParser.get_topics()
                ]
            )
        else:
            print("Topics are up to date")


@asynccontextmanager
async def lifespan_setup(
    app: FastAPI,
) -> AsyncGenerator[None, None]:  # pragma: no cover
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data
    in the state, such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    app.middleware_stack = None
    await _check_minio_connectivity()

    container = init_container()
    db: Database = container.resolve(Database)
    app.state.db = db

    load_all_models()
    await create_tables(db)

    app.middleware_stack = app.build_middleware_stack()

    yield
    await db._async_engine.dispose()
    await db._read_only_async_engine.dispose()
