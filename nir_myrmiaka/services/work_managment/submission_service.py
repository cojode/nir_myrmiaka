from datetime import datetime

from nir_myrmiaka.db.database import Database

from nir_myrmiaka.services.common.crud_service import BaseCRUDService

from nir_myrmiaka.db.repositories.base_submission import (
    BaseSubmissionRepository,
    BaseSubmission,
)

from nir_myrmiaka.services.work_managment.assignment_service import (
    AssignmentService,
)
from nir_myrmiaka.services.work_managment.researchwork_service import (
    ResearchworkService,
)
from nir_myrmiaka.services.work_managment.submission_topic_service import (
    SubmissionTopicService,
)


class SubmissionService(BaseCRUDService[BaseSubmission]):
    def __init__(
        self,
        db: Database,
        assignment_service: AssignmentService,
        researchwork_service: ResearchworkService,
        submission_topic_service: SubmissionTopicService,
    ):
        super().__init__(db, BaseSubmissionRepository)
        self.assignment_service = assignment_service
        self.researchwork_service = researchwork_service
        self.submission_topic_service = submission_topic_service

    async def get_submission_by_id(self, submission_id: int):
        return await self._get_model_by_id(submission_id)

    async def create_submission(
        self, assignment_id: int, researchwork_id: int, submission_title: str
    ) -> dict:
        await self.assignment_service.get_assignment_by_id(
            assignment_id=assignment_id
        )
        research_work = await self.researchwork_service.get_researchwork_by_id(
            researchwork_id
        )

        submission = await self._create_model(
            assignment_id=assignment_id,
            semester=None,
            submission_title=submission_title,
            created_at=datetime.today(),
            researchwork_id=researchwork_id,
        )

        for topic in research_work.get("base_topics", []):
            await self.submission_topic_service.create_submission_topic(
                submission["id"], topic.get("id")
            )

        return await self.get_submission_by_id(submission["id"])

    async def get_submissions_by_assignment_id(
        self, assignmnet_id: int
    ) -> tuple[int, dict[str, any]]:
        count, submissions = await self.repo.find_and_count(
            assignment_id=assignmnet_id
        )
        return count, [submission.to_dict() for submission in submissions]
