# minio_async.py
from aiobotocore.session import get_session
from aiobotocore.config import AioConfig
import aiofiles
from typing import Optional

from nir_myrmiaka.settings import settings
from nir_myrmiaka.log import logger

class AsyncMinIOClient:
    def __init__(self):
        self.endpoint = settings.minio_endpoint
        self.access_key = settings.minio_access_key
        self.secret_key = settings.minio_secret_key
        self.bucket_name = settings.minio_bucket_name
        self.session = get_session()

        self.config = AioConfig(
            connect_timeout=2.0,
            read_timeout=3.0,
            retries={"max_attempts": 0},
        )

    async def ensure_bucket(self):
        async with self.session.create_client(
            "s3",
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            config=self.config,
        ) as client:
            try:
                await client.create_bucket(Bucket=self.bucket_name)
            except client.exceptions.BucketAlreadyOwnedByYou:
                pass

    async def upload_file(self, file_path: str, object_name: str) -> bool:
        async with self.session.create_client(
            "s3",
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            config=self.config,
        ) as client:
            await self.ensure_bucket()
            async with aiofiles.open(file_path, mode="rb") as file:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=await file.read(),
                )

    async def delete_file(self, object_name: str) -> bool:
        async with self.session.create_client(
            "s3",
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            config=self.config,
        ) as client:
            await client.delete_object(
                Bucket=self.bucket_name, Key=object_name
            )
            return True

    async def download_file(self, object_name: str, file_path: str) -> bool:
        async with self.session.create_client(
            "s3",
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            config=self.config,
        ) as client:
            response = await client.get_object(
                Bucket=self.bucket_name, Key=object_name
            )
            async with response["Body"] as stream:
                async with aiofiles.open(file_path, "wb") as file:
                    while chunk := await stream.read(
                        1024 * 1024
                    ):  # 1MB chunks
                        await file.write(chunk)

    async def generate_presigned_url(
        self, object_name: str, expires: int = 3600
    ) -> Optional[str]:
        async with self.session.create_client(
            "s3",
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            config=self.config,
        ) as client:
            return await client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": object_name},
                ExpiresIn=expires,
            )

    async def check_connection(self, check_bucket: bool = False) -> bool:
        try:
            async with self.session.create_client(
                "s3",
                endpoint_url=self.endpoint,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                config=self.config,
            ) as client:
                await client.list_buckets()

                if check_bucket:
                    try:
                        await client.head_bucket(Bucket=self.bucket_name)
                    except client.exceptions.NoSuchBucket:
                        return False
                return True
        except Exception as e:
            logger.error(f"MinIO connection error: {e}")
            return False
