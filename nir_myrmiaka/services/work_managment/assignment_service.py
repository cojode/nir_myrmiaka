from datetime import datetime
from nir_myrmiaka.db.repositories.base_assignment import (
    BaseAssignmentRepository,
    BaseAssignment,
)
from nir_myrmiaka.db.database import Database
from nir_myrmiaka.services.auth.auth_service import UserService
from nir_myrmiaka.services.common.crud_service import BaseCRUDService

from nir_myrmiaka.exceptions.abc import DomainError


class AssignmentServiceError(DomainError):
    """Base exception class for assignment service errors."""


class AlreadyAcceptedAssignmentError(AssignmentServiceError):
    """Exception raised when a student already has an accepted assignment."""

    def __init__(self, student_id: int):
        super().__init__(
            message="Student already has an accepted assignment",
            detail={"student_id": student_id},
        )


class UnrelatedAssignmentError(AssignmentServiceError):
    """Exception raised when a teacher is not related to the assignment."""

    def __init__(self, teacher_id: int, assignment_id: int):
        super().__init__(
            message="Teacher is not related to this assignment",
            detail={"teacher_id": teacher_id, "assignment_id": assignment_id},
        )


class AssignmentService(BaseCRUDService[BaseAssignment]):
    _student_role_symbolic = "Student"
    _teacher_role_symbolic = "Teacher"

    def __init__(self, db: Database, user_service: UserService):
        super().__init__(db, BaseAssignmentRepository)
        self.user_service = user_service

    async def delete_assignment(self, assignment_id: int):
        await self._delete_model(assignment_id)

    async def verify_student(self, user_id: int):
        return await self.user_service.verify_exists_and_role_specified(
            user_id=user_id, role=self._student_role_symbolic
        )

    async def verify_student_no_active_assignment(self, user_id: int):
        user_profile = await self.verify_student(user_id)
        for assignment in user_profile.get("assignment_subordinate", []):
            if assignment.get("is_accepted", None):
                raise AlreadyAcceptedAssignmentError(student_id=user_id)

    async def verify_teacher(self, user_id: int):
        return await self.user_service.verify_exists_and_role_specified(
            user_id=user_id, role=self._teacher_role_symbolic
        )

    async def create_assignment(
        self, student_user_id: int, teacher_user_id: int, text: str
    ) -> dict:
        await self.verify_student_no_active_assignment(student_user_id)
        await self.verify_teacher(teacher_user_id)
        return await self._create_model(
            student_id=student_user_id,
            teacher_id=teacher_user_id,
            created_at=datetime.now(),
            is_reviewed=False,
            text=text,
        )

    async def get_assignment_by_id(self, assignment_id: int):
        return await self._get_model_by_id(assignment_id)

    async def update_assignment(self, assignment_id: int, **kwargs):
        return await self._update_model(assignment_id, **kwargs)

    async def get_accepted_students(self, teacher_id):
        teacher = await self.verify_teacher(teacher_id)
        result = []
        for student_id in {
            assignment.get("student_id", None)
            for assignment in teacher.get("assignment_supervisor", [])
            if assignment.get("is_accepted", False)
        }:
            result.append(await self.user_service.get_user_info(student_id))
        return len(result), result

    async def _affect_assignment(
        self,
        teacher_id: int,
        assignment_id: int,
        is_reviewed: bool | None = None,
        is_accepted: bool | None = None,
    ) -> dict:
        await self.verify_teacher(teacher_id)
        assignment = await self.get_assignment_by_id(assignment_id)
        if assignment["teacher_id"] != teacher_id:
            raise UnrelatedAssignmentError(
                teacher_id=teacher_id, assignment_id=assignment_id
            )

        update_data = {}
        if is_reviewed is not None:
            update_data["is_reviewed"] = is_reviewed
        if is_accepted is not None:
            update_data["is_accepted"] = is_accepted

        return await self.update_assignment(assignment_id, **update_data)

    async def accept_assignment(
        self, teacher_id: int, assignment_id: int
    ) -> dict:
        return await self._affect_assignment(
            teacher_id=teacher_id,
            assignment_id=assignment_id,
            is_reviewed=True,
            is_accepted=True,
        )

    async def decline_assignment(
        self, teacher_id: int, assignment_id: int
    ) -> dict:
        return await self._affect_assignment(
            teacher_id=teacher_id,
            assignment_id=assignment_id,
            is_reviewed=True,
            is_accepted=False,
        )

    async def review_assignment(
        self, teacher_id: int, assignment_id: int
    ) -> dict:
        return await self._affect_assignment(
            teacher_id=teacher_id,
            assignment_id=assignment_id,
            is_reviewed=True,
        )
