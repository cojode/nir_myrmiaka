from nir_myrmiaka.db.models.submission_topic import SubmissionTopic
from nir_myrmiaka.db.repositories.crud import ExtendedCRUDRepository


class SubmissionTopicRepository(ExtendedCRUDRepository[SubmissionTopic]):
    def __init__(self, session):
        super().__init__(session, SubmissionTopic)
