from nir_myrmiaka.db.database import Database
from nir_myrmiaka.db.repositories.submission_topic import (
    SubmissionTopicRepository,
    SubmissionTopic,
)

from nir_myrmiaka.services.common.crud_service import BaseCRUDService

from nir_myrmiaka.services.work_managment.comment_service import (
    SubmissionTopicCommentService,
)

from nir_myrmiaka.services.work_managment.file_service import BaseFileService
from nir_myrmiaka.services.notify.notify_service import (
    NotificationService,
    NotificationType,
)

class SubmissionTopicService(BaseCRUDService[SubmissionTopic]):

    def __init__(
        self,
        db: Database,
        submission_topic_comment_service: SubmissionTopicCommentService,
        notification_service: NotificationService,
        base_file_service: BaseFileService,
    ):
        self.comment_service = submission_topic_comment_service
        self.notification_service = notification_service
        self.base_file_service = base_file_service
        super().__init__(db, SubmissionTopicRepository)

    async def create_submission_topic(
        self,
        submission_id: int,
        topic_id: int,
        student_id: int,
        teacher_id: int,
    ) -> dict:
        return await self._create_model(
            submission_id=submission_id,
            topic_id=topic_id,
            student_id=student_id,
            teacher_id=teacher_id,
        )

    async def get_submission_topics_by_submission_id(
        self, submission_id: int
    ) -> tuple[int, dict]:
        topics = await self.repo.find_all(submission_id=submission_id)
        return len(topics), [topic.to_dict() for topic in topics]

    async def get_submission_topic_by_id(
        self, submission_topic_id: int
    ) -> dict:
        return await self._get_model_by_id(id=submission_topic_id)

    async def _affect_submission_topic(
        self,
        submission_topic_id: int,
        is_reviewed: bool | None = None,
        is_accepted: bool | None = None,
    ) -> dict:
        await self.get_submission_topic_by_id(submission_topic_id)

        update_data = {}
        if is_reviewed is not None:
            update_data["is_reviewed"] = is_reviewed
        if is_accepted is not None:
            update_data["is_accepted"] = is_accepted

        return await self._update_model(submission_topic_id, **update_data)

    async def accept_submission_topic(
        self, submission_topic_id: int, comment: str
    ) -> dict:
        await self.comment_service.create_comment(comment, submission_topic_id)
        submission = await self._affect_submission_topic(
            submission_topic_id=submission_topic_id,
            is_reviewed=True,
            is_accepted=True,
        )
        await self.notification_service.notify_user(
            submission.get("student_id"),
            NotificationType.SUBMISSION_TOPIC_ACCEPTED,
            "Your submission topic has been accepted.",
            submission_topic_id,
        )

        return submission

    async def decline_submission_topic(
        self, submission_topic_id: int, comment: str
    ) -> dict:
        await self.comment_service.create_comment(comment, submission_topic_id)
        submission = await self._affect_submission_topic(
            submission_topic_id=submission_topic_id,
            is_reviewed=True,
            is_accepted=False,
        )
        await self.notification_service.notify_user(
            submission.get("student_id"),
            NotificationType.SUBMISSION_TOPIC_DECLINED,
            "Your submission topic has been declined.",
            submission_topic_id,
        )

        return submission

    async def review_submission_topic(self, submission_topic_id: int) -> dict:
        return await self._affect_submission_topic(
            submission_topic_id=submission_topic_id,
            is_reviewed=True,
        )

    async def upload_related_file(
        self, submission_topic_id: int, file
    ) -> dict:
        base_file = await self.base_file_service.upload_and_create_file(
            submission_topic_id=submission_topic_id, file=file
        )
        submission_topic = await self.get_submission_topic_by_id(
            submission_topic_id
        )
        await self.notification_service.notify_user(
            submission_topic.get("teacher_id"),
            NotificationType.SUBMISSION_TOPIC_FILE_ADDED,
            "A new file has been uploaded to your submission topic.",
            base_file.get("id"),
        )
        return base_file
