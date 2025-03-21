from nir_myrmiaka.db.database import Database

from nir_myrmiaka.db.repositories.base_submission import (
    BaseSubmission,
    BaseSubmissionRepository,
)

from nir_myrmiaka.db.repositories.submission_topic import (
    SubmissionTopicRepository,
    SubmissionTopic,
)

from nir_myrmiaka.services.work_managment.assignment_service import (
    AssignmentService,
)

from nir_myrmiaka.services.work_managment.researchwork_service import (
    ResearchworkService,
)

from datetime import datetime


class SubmissionService:

    _student_role_symbolic = "Student"
    _teacher_role_symbolic = "Teacher"

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

    async def create_submission(
        self, assignment_id: int, researchwork_id: int
    ):
        await self.assignment_service.verify_assignment_id_exists(
            assignment_id
        )

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
