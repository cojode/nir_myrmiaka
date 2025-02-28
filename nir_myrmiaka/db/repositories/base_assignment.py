from nir_myrmiaka.db.models.base_assignment import BaseAssignment
from nir_myrmiaka.db.repositories.crud import ExtendedCRUDRepository


class BaseAssignmentRepository(ExtendedCRUDRepository[BaseAssignment]):
    def __init__(self, session):
        super().__init__(session, BaseAssignment)
