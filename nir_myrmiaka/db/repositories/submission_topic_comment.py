from nir_myrmiaka.db.models.submission_topic_comment import (
    SubmissionTopicComment,
)
from nir_myrmiaka.db.repositories.crud import ExtendedCRUDRepository


class SubmissionTopicCommentRepository(
    ExtendedCRUDRepository[SubmissionTopicComment]
):
    def __init__(self, session):
        super().__init__(session, SubmissionTopicComment)
