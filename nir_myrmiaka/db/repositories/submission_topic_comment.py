from nir_myrmiaka.db.models.submission_topic_comment import (
    SubmissionTopicComment,
)
from nir_myrmiaka.db.repositories.crud import ExtendedCRUDRepository

from sqlalchemy import update, select


class SubmissionTopicCommentRepository(
    ExtendedCRUDRepository[SubmissionTopicComment]
):
    def __init__(self, session):
        super().__init__(session, SubmissionTopicComment)

    async def review_comments_by_submission_topic_id(
        self,
        submission_topic_id: int,
    ):
        async with self.database.get_session() as session:
            stmt = (
                update(SubmissionTopicComment)
                .where(
                    SubmissionTopicComment.submission_topic_id
                    == submission_topic_id
                )
                .values(is_reviewed=True)
            )

            await session.execute(stmt)

            await session.commit()

            result = await session.execute(
                select(SubmissionTopicComment).where(
                    SubmissionTopicComment.submission_topic_id
                    == submission_topic_id
                )
            )
            updated_comments = result.scalars().all()

            return updated_comments
