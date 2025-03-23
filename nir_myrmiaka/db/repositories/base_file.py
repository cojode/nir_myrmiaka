from nir_myrmiaka.db.models.base_file import BaseFile
from nir_myrmiaka.db.repositories.crud import ExtendedCRUDRepository


class BaseFileRepository(ExtendedCRUDRepository[BaseFile]):
    def __init__(self, session):
        super().__init__(session, BaseFile)
