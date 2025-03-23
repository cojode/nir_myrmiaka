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

    # async def _affect_assignment(
    #     self,
    #     teacher_id: int,
    #     assignment_id: int,
    #     is_reviewed: bool | None = None,
    #     is_accepted: bool | None = None,
    # ) -> dict:
    #     await self.verify_teacher(teacher_id)
    #     assignment = await self.get_assignment_by_id(assignment_id)
    #     if assignment["teacher_id"] != teacher_id:
    #         raise ValueError("Teacher is not related to this assignment")

    #     update_data = {}
    #     if is_reviewed is not None:
    #         update_data["is_reviewed"] = is_reviewed
    #     if is_accepted is not None:
    #         update_data["is_accepted"] = is_accepted

    #     return await self.update_assignment(assignment_id, **update_data)

    # async def accept_assignment(
    #     self, teacher_id: int, assignment_id: int
    # ) -> dict:
    #     return await self._affect_assignment(
    #         teacher_id=teacher_id,
    #         assignment_id=assignment_id,
    #         is_reviewed=True,
    #         is_accepted=True,
    #     )

    # async def decline_assignment(
    #     self, teacher_id: int, assignment_id: int
    # ) -> dict:
    #     return await self._affect_assignment(
    #         teacher_id=teacher_id,
    #         assignment_id=assignment_id,
    #         is_reviewed=True,
    #         is_accepted=False,
    #     )

    # async def review_assignment(
    #     self, teacher_id: int, assignment_id: int
    # ) -> dict:
    #     return await self._affect_assignment(
    #         teacher_id=teacher_id,
    #         assignment_id=assignment_id,
    #         is_reviewed=True,
    #     )
