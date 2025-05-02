"""
Container initialization module.

This module contains functions to initialize container for application.

Initialization of container consists of registration of all application services
and repositories. All registrations are done in singleton scope.

"""

from functools import lru_cache

from punq import Container, Scope

from nir_myrmiaka.services import (
    UserService,
    AssignmentService,
    ResearchworkService,
    SubmissionService,
    SubmissionTopicService,
    SubmissionTopicCommentService,
    BaseFileService,
    AsyncMinIOClient,
    NotificationService,
)
from nir_myrmiaka.settings import settings
from nir_myrmiaka.db.database import Database


@lru_cache(1)
def init_container() -> Container:
    """
    Initialize container for application.

    This function uses lru_cache decorator to cache result of container
    initialization. This means that first call to this function will initialize
    container and subsequent calls will return cached result.

    :return: Initialized container.
    :rtype: Container
    """
    return _init_container()


def _init_container() -> Container:
    """
    Initialize container for application.

    This function registers all services and repositories in container.

    :return: Initialized container.
    :rtype: Container
    """
    container = Container()
    container.register(
        Database,
        scope=Scope.singleton,
        factory=lambda: Database(
            url=str(settings.db_url),
            ro_url=str(settings.db_url),
        ),
    )

    container.register(UserService, scope=Scope.singleton)
    container.register(AssignmentService, scope=Scope.singleton)
    container.register(ResearchworkService, scope=Scope.singleton)
    container.register(SubmissionTopicService, scope=Scope.singleton)
    container.register(SubmissionTopicCommentService, scope=Scope.singleton)
    container.register(SubmissionService, scope=Scope.singleton)
    container.register(AsyncMinIOClient, scope=Scope.singleton)
    container.register(BaseFileService, scope=Scope.singleton)
    container.register(NotificationService, scope=Scope.singleton)

    return container
