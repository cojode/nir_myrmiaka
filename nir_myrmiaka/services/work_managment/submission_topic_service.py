from nir_myrmiaka.db.database import Database
from nir_myrmiaka.db.repositories.submission_topic import (
    SubmissionTopicRepository,
    SubmissionTopic,
)

from nir_myrmiaka.services.common.crud_service import BaseCRUDService


class SubmissionTopicService(BaseCRUDService[SubmissionTopic]):
    def __init__(self, db: Database):
        super().__init__(db, SubmissionTopicRepository)

    async def create_submission_topic(
        self, submission_id: int, topic_id: int
    ) -> dict:
        return await self._create_model(
            submission_id=submission_id, topic_id=topic_id
        )

    async def get_submission_topics_by_submission_id(
        self, submission_id: int
    ) -> tuple[int, dict]:
        topics = await self.repo.find_all(submission_id=submission_id)
        return len(topics), [topic.to_dict() for topic in topics]
