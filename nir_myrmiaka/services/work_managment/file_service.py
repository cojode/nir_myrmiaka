from nir_myrmiaka.services.common.crud_service import BaseCRUDService

from nir_myrmiaka.db.database import Database

from nir_myrmiaka.db.repositories.base_file import (
    BaseFile,
    BaseFileRepository,
)

from nir_myrmiaka.services.cdn.minio_async import AsyncMinIOClient

import datetime
import uuid
import aiofiles
import os


class BaseFileService(BaseCRUDService[BaseFile]):
    def __init__(self, db: Database, minio_client: AsyncMinIOClient):
        self.minio_client = minio_client
        super().__init__(db, BaseFileRepository)

    async def upload_and_create_file(
        self, submission_topic_id: int, file
    ) -> BaseFile:
        """Handles complete file upload workflow"""
        file_id = str(uuid.uuid4())
        temp_path = f"/tmp/{file_id}"

        try:
            async with aiofiles.open(temp_path, "wb") as buffer:
                while chunk := await file.read(1024 * 1024):
                    await buffer.write(chunk)

            object_name = f"files/{file_id}/{file.filename}"

            # await self.minio_client.upload_file(temp_path, object_name)

            return await self._create_model(
                original_filename=file.filename,
                submission_topic_id=submission_topic_id,
                storage_path=object_name,
                upload_date=datetime.datetime.now(datetime.timezone.utc),
                content_type=file.content_type,
                size=os.path.getsize(temp_path),
                is_reviewed=False,
            )
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    async def delete_file(self, file_id: int) -> bool:
        """Deletes file from storage and database"""
        file = await self._get_model_by_id(file_id)
        object_name = file.get("storage_path", None)

        if object_name:
            await self.minio_client.delete_file(object_name)

        await self._delete_model(file_id)
        return True

    async def get_file_by_id(self, file_id: int):
        """Retrieves file metadata with temporary download URL"""
        file = await self._get_model_by_id(file_id)

        url = await self.minio_client.generate_presigned_url(
            file.get("storage_path", None)
        )
        return {**file, "download_url": url}
