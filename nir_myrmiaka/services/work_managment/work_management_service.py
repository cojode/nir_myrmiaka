from nir_myrmiaka.db.models.base_assignment import BaseAssignment
from nir_myrmiaka.db.models.users_userprofile import UsersUserprofile

from nir_myrmiaka.db.repositories.base_assignment import BaseAssignmentRepository
from nir_myrmiaka.db.repositories.base_submission import BaseSubmissionRepository
from nir_myrmiaka.db.repositories.users_userprofile import UsersUserprofileRepository

from nir_myrmiaka.db.database import Database

from datetime import datetime


class WorkManagementService:
    def __init__(self, db: Database):
        self.db = db
        self.users_userprofile_repo = UsersUserprofileRepository(session=db)
        self.base_assignment_repo = BaseAssignmentRepository(session=db)
        self.base_submission_repo = BaseSubmissionRepository(session=db)

    async def verify_exists_and_role_specified(self, user_id, role: str):
        user: UsersUserprofile = await self.users_userprofile_repo.find_one(
            user_id=user_id
        )
        if user == None:
            raise ValueError("User with provided id does not exists")
        if user.role != role:
            raise ValueError("User does not have specified role")

    @staticmethod
    def _extract_from_payload(payload, *args):
        return {key: payload.__getattribute__(key) for key in args}

    async def create_assignment(self, payload):
        new_assignment_data = self._extract_from_payload(
            payload, "student_id", "teacher_id", "text"
        )
        self.verify_exists_and_role_specified(
            new_assignment_data["student_id"], "Student"
        )
        self.verify_exists_and_role_specified(
            new_assignment_data["teacher_id"], "Teacher"
        )

        new_assignment_data["is_accepted"] = False
        new_assignment_data["created_at"] = datetime.now()
        new_assignment_data["is_reviewed"] = False
        return await self.base_assignment_repo.create(**new_assignment_data)

    async def browse_assignments(self, teacher_id):
        self.verify_exists_and_role_specified(teacher_id, "Teacher")
        return await self.base_assignment_repo.find_and_count(teacher_id=teacher_id)

    async def accept_assignment(self, teacher_id, semestr, assignment_id):
        self.verify_exists_and_role_specified(teacher_id, "Teacher")
        target_base_assignment: BaseAssignment = (
            await self.base_assignment_repo.find_by_id(assignment_id)
        )

        if target_base_assignment is None:
            raise ValueError("Assignment not found")

        target_base_assignment.is_reviewed = True
        target_base_assignment.is_accepted = True

        await self.base_assignment_repo.save(target_base_assignment)

        return await self.base_submission_repo.create(
            {
                "assignment_id": target_base_assignment["id"],
                "semestr": semestr,
                "created_at": datetime.now(),
            }
        )

    async def decline_assignment(self, teacher_id, assignment_id):
        self.verify_exists_and_role_specified(teacher_id, "Teacher")
        target_base_assignment: BaseAssignment = (
            await self.base_assignment_repo.find_by_id(assignment_id)
        )

        if target_base_assignment is None:
            raise ValueError("Assignment not found")

        target_base_assignment.is_reviewed = True
        target_base_assignment.is_accepted = False

        await self.base_assignment_repo.save(target_base_assignment)
