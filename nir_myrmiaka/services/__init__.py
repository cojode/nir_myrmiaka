"""Services for nir_myrmiaka."""

from nir_myrmiaka.services.auth.auth_service import UserService
from nir_myrmiaka.services.work_managment.assignment_service import (
    AssignmentService,
)
from nir_myrmiaka.services.work_managment.researchwork_service import (
    ResearchworkService,
)

from nir_myrmiaka.services.work_managment.submission_service import (
    SubmissionService,
)

from nir_myrmiaka.services.work_managment.submission_topic_service import (
    SubmissionTopicService,
)

from nir_myrmiaka.services.work_managment.comment_service import (
    SubmissionTopicCommentService,
)

from nir_myrmiaka.services.work_managment.file_service import BaseFileService

from nir_myrmiaka.services.cdn.minio_async import AsyncMinIOClient

from nir_myrmiaka.services.notify.notify_service import (
    NotificationService,
    NotificationEntityService,
)

__all__ = [
    "UserService",
    "AssignmentService",
    "ResearchworkService",
    "SubmissionService",
    "SubmissionTopicService",
    "SubmissionTopicCommentService",
    "AsyncMinIOClient",
    "BaseFileService",
    "NotificationService",
    "NotificationEntityService",
]
