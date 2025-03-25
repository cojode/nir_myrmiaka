from nir_myrmiaka.services.common.crud_service import BaseCRUDService

from nir_myrmiaka.db.database import Database

from nir_myrmiaka.db.repositories.submission_topic_comment import (
    SubmissionTopicComment,
    SubmissionTopicCommentRepository,
)

import datetime

class SubmissionTopicCommentService(BaseCRUDService[SubmissionTopicComment]):
    def __init__(self, db: Database):
        super().__init__(db, SubmissionTopicCommentRepository)

    async def create_comment(self, comment: str, submission_topic_id: int):
        comment = await self._create_model(
            submission_topic_id=submission_topic_id,
            created_at=datetime.datetime.today(),
            comment=comment,
            is_reviewed=False,
        )
        return comment

    async def get_comment_by_id(self, comment_id: int):
        return await self._get_model_by_id(comment_id)

    async def review_comments_by_submission_topic_id(self, submission_id: int):
        comments = await self.repo.review_comments_by_submission_id(
            submission_id
        )
        return len(comments), [comment.to_dict() for comment in comments]
