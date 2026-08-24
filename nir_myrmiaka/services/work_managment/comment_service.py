from nir_myrmiaka.services.common.crud_service import BaseCRUDService

from nir_myrmiaka.db.database import Database

from nir_myrmiaka.db.repositories.submission_topic_comment import (
    SubmissionTopicComment,
    SubmissionTopicCommentRepository,
)

from nir_myrmiaka.db.repositories.submission_topic import (
    SubmissionTopicRepository,
)

import datetime


class SubmissionTopicCommentService(BaseCRUDService[SubmissionTopicComment]):
    def __init__(self, db: Database):
        super().__init__(db, SubmissionTopicCommentRepository)
        self.submission_topic_repo = SubmissionTopicRepository(session=db)

    async def _get_submission_topic(self, submission_topic_id: int):
        """Get submission topic and verify it exists."""
        topic = await self.submission_topic_repo.find_by_id(submission_topic_id)
        if not topic:
            raise ValueError(
                f"Submission topic with id {submission_topic_id} not found"
            )
        return topic

    async def _check_user_is_participant(
        self, submission_topic_id: int, user_id: int
    ):
        """Verify that user is either student or teacher of the submission topic."""
        topic = await self._get_submission_topic(submission_topic_id)
        if user_id not in (topic.student_id, topic.teacher_id):
            raise PermissionError(
                "User is not a participant of this submission topic"
            )
        return topic

    async def create_comment(
        self, comment: str, submission_topic_id: int, user_id: int
    ):
        await self._check_user_is_participant(submission_topic_id, user_id)
        comment = await self._create_model(
            submission_topic_id=submission_topic_id,
            user_id=user_id,
            created_at=datetime.datetime.today(),
            comment=comment,
            is_reviewed=False,
        )
        return comment

    async def get_comments_by_submission_topic_id(
        self, submission_topic_id: int
    ):
        comments = (
            await self.repo.get_comments_by_submission_topic_id(
                submission_topic_id=submission_topic_id
            )
        )
        return len(comments), [c.to_dict() for c in comments]

    async def get_comment_by_id(self, comment_id: int):
        return await self._get_model_by_id(comment_id)

    async def update_comment(
        self, comment_id: int, user_id: int, new_text: str
    ):
        comment = await self.repo.find_by_id(comment_id)
        if not comment:
            raise ValueError(f"Comment with id {comment_id} not found")
        if comment.user_id != user_id:
            raise PermissionError(
                "Only the author can edit this comment"
            )
        return await self._update_model(comment_id, comment=new_text)

    async def delete_comment(self, comment_id: int, user_id: int):
        comment = await self.repo.find_by_id(comment_id)
        if not comment:
            raise ValueError(f"Comment with id {comment_id} not found")
        if comment.user_id != user_id:
            raise PermissionError(
                "Only the author can delete this comment"
            )
        await self._delete_model(comment_id)

    async def review_comments_by_submission_topic_id(
        self, submission_topic_id: int
    ):
        comments = (
            await self.repo.review_comments_by_submission_topic_id(
                submission_topic_id
            )
        )
        return len(comments), [comment.to_dict() for comment in comments]