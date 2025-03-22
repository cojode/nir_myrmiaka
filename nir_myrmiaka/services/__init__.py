"""Services for nir_myrmiaka."""

from nir_myrmiaka.services.auth.auth_service import UserService
from nir_myrmiaka.services.work_managment.assignment_service import (
    AssignmentService,
)
from nir_myrmiaka.services.work_managment.researchwork_service import (
    ResearchworkService,
)

from nir_myrmiaka.services.work_managment.submission_service import (
    SubmissionService,
)

__all__ = [
    "UserService",
    "AssignmentService",
    "ResearchworkService",
    "SubmissionService",
]
