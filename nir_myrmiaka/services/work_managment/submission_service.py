from nir_myrmiaka.db.database import Database

from nir_myrmiaka.db.repositories.base_submission import (
    BaseSubmissionRepository,
)

from nir_myrmiaka.db.repositories.submission_topic import (
    SubmissionTopicRepository,
)

from nir_myrmiaka.services.work_managment.assignment_service import (
    AssignmentService,
)

from nir_myrmiaka.services.work_managment.researchwork_service import (
    ResearchworkService,
)

from datetime import datetime


class SubmissionService:
    def __init__(
        self,
        db: Database,
        assignment_service: AssignmentService,
        researchwork_service: ResearchworkService,
    ):
        self.db = db
        self.assignment_service = assignment_service
        self.researchwork_service = researchwork_service

        self.submission_topic_repo = SubmissionTopicRepository(session=db)
        self.base_submission_repo = BaseSubmissionRepository(session=db)

    async def verify_base_submission_by_id(self, base_submssion_id: int):
        base_submission = await self.base_submission_repo.find_by_id(
            base_submssion_id
        )
        if not base_submission:
            raise ValueError(
                f"Submission with provided id [{base_submssion_id}] does not exists."
            )
        return base_submission

    async def create_submission(
        self, assignment_id: int, researchwork_id: int
    ):
        await self.assignment_service.get_existing_assignment(assignment_id)

        research_work = (
            await self.researchwork_service.verify_researchwork_id_exists(
                researchwork_id
            )
        )

        base_submission = await self.base_submission_repo.create(
            **{
                "assignment_id": assignment_id,
                "semester": None,
                "created_at": datetime.today(),
                "researchwork_id": researchwork_id,
            }
        )

        for topic in research_work.get("base_topics", []):
            await self.submission_topic_repo.create(
                **{
                    "submission_id": base_submission.id,
                    "topic_id": topic.get("id", None),
                }
            )

        refreshed_base_submission = await self.verify_base_submission_by_id(
            base_submission.id
        )
        return refreshed_base_submission.to_dict()

    async def get_submissions_by_assigment_id(
        self, assignmennt_id: int
    ) -> tuple[int, dict]:
        target_submissions = await self.base_submission_repo.find_all(
            assignment_id=assignmennt_id
        )
        return len(target_submissions), [
            submission.to_dict() for submission in target_submissions
        ]
