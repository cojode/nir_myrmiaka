import enum
from pathlib import Path
from tempfile import gettempdir

from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = "127.0.0.1"
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = True

    minio_host: str = "localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket_name: str = "my-bucket"

    # Current environment
    environment: str = "dev"
    version: str = "v1"

    log_level: LogLevel = LogLevel.INFO
    # Variables for the database
    db_file: Path = TEMP_DIR / "db.sqlite3"
    db_echo: bool = True

    @property
    def minio_endpoint(self) -> str:
        return f"http://{self.minio_host}"

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(scheme="sqlite+aiosqlite", path=f"///{self.db_file}")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="NIR_MYRMIAKA_",
        env_file_encoding="utf-8",
        extra="allow",
    )

TEST_DIR = Path(__file__).parent.parent / "tests"


class TestSettings:
    DB_URL = "sqlite+aiosqlite:///:memory:"
    ECHO_SQL = False


test_settings = TestSettings()
settings = Settings()
