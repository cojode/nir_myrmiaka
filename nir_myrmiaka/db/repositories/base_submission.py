from nir_myrmiaka.db.models.base_submission import BaseSubmission
from nir_myrmiaka.db.repositories.crud import ExtendedCRUDRepository


class BaseSubmissionRepository(ExtendedCRUDRepository[BaseSubmission]):
    def __init__(self, session):
        super().__init__(session, BaseSubmission)
