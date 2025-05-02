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

    async def _create_submssion_topics_by_researchwork_pattern(
        self,
        research_work: dict,
        submission_id: int,
        student_id: int,
        teacher_id: int,
    ):
        for topic in research_work.get("base_topics", []):
            await self.submission_topic_service.create_submission_topic(
                submission_id,
                topic.get("id"),
                student_id,
                teacher_id,
            )

    async def _discard_submission_topics_related(self, submission_id: int):
        await self.submission_topic_service.delete_submission_topics_by_submission_id(
            submission_id=submission_id
        )

    async def create_submission(
        self, assignment_id: int, researchwork_id: int, submission_title: str
    ) -> dict:
        assignment = await self.assignment_service.get_assignment_by_id(
            assignment_id=assignment_id
        )
        research_work = await self.researchwork_service.get_researchwork_by_id(
            researchwork_id
        )

        submission = await self._create_model(
            assignment_id=assignment_id,
            student_id=assignment.get("student_id"),
            teacher_id=assignment.get("teacher_id"),
            semester=None,
            submission_title=submission_title,
            created_at=datetime.today(),
            researchwork_id=researchwork_id,
        )

        await self._create_submssion_topics_by_researchwork_pattern(
            research_work,
            submission["id"],
            assignment.get("student_id"),
            assignment.get("teacher_id"),
        )

        return await self.get_submission_by_id(submission["id"])

    async def edit_submission_by_id(
        self,
        submission_id: int,
        submission_title: str | None,
        researchwork_id: int | None,
    ) -> dict:
        submission = await self.get_submission_by_id(submission_id)
        await self.researchwork_service.get_researchwork_by_id(researchwork_id)
        if (
            researchwork_id
            and submission.get("researchwork_id") != researchwork_id
        ):
            await self._discard_submission_topics_related(submission_id)
            research_work = (
                await self.researchwork_service.get_researchwork_by_id(
                    researchwork_id
                )
            )
            await self._create_submssion_topics_by_researchwork_pattern(
                research_work,
                submission_id,
                submission["student_id"],
                submission["teacher_id"],
            )

        return await self._update_model(
            submission_id,
            submission_title=submission_title,
            researchwork_id=researchwork_id,
        )

    async def get_submissions_by_assignment_id(
        self, assignmnet_id: int
    ) -> tuple[int, dict[str, any]]:
        count, submissions = await self.repo.find_and_count(
            assignment_id=assignmnet_id
        )
        return count, [submission.to_dict() for submission in submissions]
