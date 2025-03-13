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
        print(user)
        if user == None:
            raise ValueError(
                f"User with provided id {user_id} does not exists"
            )
        if user.role != role:
            raise ValueError(
                f"User with provided id {user_id} does not have specified role ({role})"
            )

    async def create_assignment(self, payload):
        new_assignment_data = {
            "student_id": payload.student.user_id,
            "teacher_id": payload.teacher.user_id,
            "is_accepted": False,
            "created_at": datetime.now(),
            "is_reviewed": False,
            "text": payload.text,
        }
        await self.verify_exists_and_role_specified(
            new_assignment_data["student_id"], "Student"
        )
        await self.verify_exists_and_role_specified(
            new_assignment_data["teacher_id"], "Teacher"
        )

        return await self.base_assignment_repo.create(**new_assignment_data)

    async def browse_assignments(self, teacher_id: int):
        self.verify_exists_and_role_specified(teacher_id, "Teacher")
        return await self.base_assignment_repo.find_and_count(teacher_id=teacher_id)

    async def browse_accepted_students(self, teacher_id: int):
        self.verify_exists_and_role_specified(teacher_id, "Teacher")
        return await self.base_assignment_repo.find_and_count(
            teacher_id=teacher_id, is_accepted=True
        )

    async def accept_assignment(self, teacher_id, semester, assignment_id):
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
            assignment_id=assignment_id,
            semester=semester,
            created_at=datetime.now(),
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

        return await self.base_assignment_repo.save(target_base_assignment)
