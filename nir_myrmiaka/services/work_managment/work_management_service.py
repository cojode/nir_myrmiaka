from nir_myrmiaka.db.models.base_assignment import BaseAssignment
from nir_myrmiaka.services.auth.auth_service import UserService

from nir_myrmiaka.db.repositories.base_assignment import BaseAssignmentRepository
from nir_myrmiaka.db.repositories.base_submission import (
    BaseSubmissionRepository,
)

from nir_myrmiaka.db.database import Database

from datetime import datetime


class WorkManagementService:

    _student_role_symbolic = "Student"
    _teacher_role_symbolic = "Teacher"

    def __init__(self, db: Database, user_service: UserService):
        self.db = db
        self.user_service: UserService = user_service
        self.base_assignment_repo = BaseAssignmentRepository(session=db)
        self.base_submission_repo = BaseSubmissionRepository(session=db)

    async def verify_student(self, user_id):
        await self.user_service.verify_exists_and_role_specified(
            user_id=user_id, role=self._student_role_symbolic
        )

    async def verify_teacher(self, user_id):
        await self.user_service.verify_exists_and_role_specified(
            user_id=user_id, role=self._teacher_role_symbolic
        )

    async def create_assignment(
        self, student_user_id: int, teacher_user_id: int, text: str
    ) -> dict:
        new_assignment_data = {
            "student_id": student_user_id,
            "teacher_id": teacher_user_id,
            "created_at": datetime.now(),
            "is_reviewed": False,
            "text": text,
        }
        await self.verify_student(new_assignment_data["student_id"])
        await self.verify_teacher(new_assignment_data["teacher_id"])
        created_assignment = await self.base_assignment_repo.create(
            **new_assignment_data
        )
        return created_assignment.to_dict()

    async def browse_teacher_assignments(
        self, teacher_id: int
    ) -> tuple[int, list[dict]]:
        await self.verify_teacher(teacher_id)
        count, found_assignments = (
            await self.base_assignment_repo.find_and_count(
                teacher_id=teacher_id
            )
        )
        return count, [item.to_dict() for item in found_assignments]

    async def browse_student_assignments(
        self, student_id: int
    ) -> tuple[int, list[dict]]:
        await self.verify_student(student_id)
        count, found_assignments = (
            await self.base_assignment_repo.find_and_count(
                student_id=student_id
            )
        )

        return count, [item.to_dict() for item in found_assignments]

    async def browse_accepted_students(
        self, teacher_id: int
    ) -> tuple[int, list[dict]]:
        await self.verify_teacher(teacher_id)
        count, accepted_assignments = (
            await self.base_assignment_repo.find_and_count(
                teacher_id=teacher_id, is_accepted=True
            )
        )

        return count, [item.to_dict() for item in accepted_assignments]

    async def _affect_assignment(
        self,
        teacher_id: int,
        assignment_id: int,
        is_reviewed: bool | None = None,
        is_accepted: bool | None = None,
    ) -> BaseAssignment:
        await self.verify_teacher(teacher_id)
        target_base_assignment: BaseAssignment = (
            await self.base_assignment_repo.find_by_id(assignment_id)
        )

        if target_base_assignment is None:
            raise ValueError("Assignment not found")

        if target_base_assignment.teacher_id != teacher_id:
            raise ValueError("Teacher is not related to this assignment")

        if is_reviewed is not None:
            target_base_assignment.is_reviewed = is_reviewed
        if is_accepted is not None:
            target_base_assignment.is_accepted = is_accepted

        return await self.base_assignment_repo.save(target_base_assignment)

    async def accept_assignment(self, teacher_id, assignment_id):
        await self._affect_assignment(
            teacher_id=teacher_id,
            assignment_id=assignment_id,
            is_reviewed=True,
            is_accepted=True,
        )

        return await self.base_submission_repo.create(
            assignment_id=assignment_id,
            created_at=datetime.now(),
        )

    async def decline_assignment(
        self, teacher_id: int, assignment_id: int
    ) -> dict:
        declined_assignment = await self._affect_assignment(
            teacher_id=teacher_id,
            assignment_id=assignment_id,
            is_reviewed=True,
            is_accepted=False,
        )
        return declined_assignment.to_dict()

    async def review_assignment(
        self, teacher_id: int, assignment_id: int
    ) -> dict:
        reviewed_assignment = await self._affect_assignment(
            teacher_id=teacher_id,
            assignment_id=assignment_id,
            is_reviewed=True,
        )

        return reviewed_assignment.to_dict()
