"""Admin panel powered by SQLAdmin with native login / password auth."""

from __future__ import annotations

from fastapi import FastAPI
from sqladmin import Admin as SQLAdmin
from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request

from nir_myrmiaka.db.models.base_assignment import BaseAssignment
from nir_myrmiaka.db.models.base_file import BaseFile
from nir_myrmiaka.db.models.base_researchwork import BaseResearchwork
from nir_myrmiaka.db.models.base_submission import BaseSubmission
from nir_myrmiaka.db.models.base_topic import BaseTopic
from nir_myrmiaka.db.models.notification import Notification, NotificationEntity
from nir_myrmiaka.db.models.submission_topic import SubmissionTopic
from nir_myrmiaka.db.models.submission_topic_comment import SubmissionTopicComment
from nir_myrmiaka.db.models.user_profile import UserProfile
from nir_myrmiaka.db.models.users_group import UserGroupTerm, UsersGroup
from nir_myrmiaka.services.auth.security import verify_password
from nir_myrmiaka.settings import settings


# ---------------------------------------------------------------------------
# Authentication backend – username + password, admin-only by ID
# ---------------------------------------------------------------------------


class AdminAuth(AuthenticationBackend):
    """Login form – username + password, only admin user by ID."""

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username", "")
        password = form.get("password", "")

        if not username or not password:
            return False

        sync_url = f"sqlite:///{settings.db_file}"
        engine = create_engine(sync_url)
        session_factory = sessionmaker(bind=engine)

        with session_factory() as session:
            user = (
                session.query(UserProfile)
                .filter(UserProfile.username == str(username))
                .first()
            )
            if user is None:
                return False
            if not verify_password(str(password), user.password):
                return False
            if user.id != settings.admin_user_id:
                return False

            request.session.update({"user_id": user.id})
            return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        user_id = request.session.get("user_id")
        if user_id is None:
            return False
        return user_id == settings.admin_user_id

# ---------------------------------------------------------------------------
# Model views – full CRUD access to every field
# ---------------------------------------------------------------------------


class UserProfileAdmin(ModelView, model=UserProfile):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = "__all__"


class UsersGroupAdmin(ModelView, model=UsersGroup):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = "__all__"


class UserGroupTermAdmin(ModelView, model=UserGroupTerm):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = "__all__"


class BaseAssignmentAdmin(ModelView, model=BaseAssignment):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = "__all__"


class BaseFileAdmin(ModelView, model=BaseFile):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = "__all__"


class BaseResearchworkAdmin(ModelView, model=BaseResearchwork):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = "__all__"


class BaseSubmissionAdmin(ModelView, model=BaseSubmission):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = "__all__"


class BaseTopicAdmin(ModelView, model=BaseTopic):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = "__all__"


class SubmissionTopicAdmin(ModelView, model=SubmissionTopic):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = "__all__"


class SubmissionTopicCommentAdmin(ModelView, model=SubmissionTopicComment):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = "__all__"


class NotificationAdmin(ModelView, model=Notification):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = "__all__"


class NotificationEntityAdmin(ModelView, model=NotificationEntity):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = "__all__"


# ---------------------------------------------------------------------------
# Registration helper
# ---------------------------------------------------------------------------


def setup_admin(app: FastAPI) -> SQLAdmin:
    """Attach SQLAdmin dashboard to *app* and return the admin instance."""

    sync_url = f"sqlite:///{settings.db_file}"
    engine = create_engine(sync_url, connect_args={"check_same_thread": False})

    auth_backend = AdminAuth(secret_key=settings.session_secret_key)

    admin = SQLAdmin(
        app=app,
        engine=engine,
        authentication_backend=auth_backend,
        base_url="/admin",
        title="NIR Myrmiaka Admin",
    )

    admin.add_view(UserProfileAdmin)
    admin.add_view(UsersGroupAdmin)
    admin.add_view(UserGroupTermAdmin)
    admin.add_view(BaseAssignmentAdmin)
    admin.add_view(BaseFileAdmin)
    admin.add_view(BaseResearchworkAdmin)
    admin.add_view(BaseSubmissionAdmin)
    admin.add_view(BaseTopicAdmin)
    admin.add_view(SubmissionTopicAdmin)
    admin.add_view(SubmissionTopicCommentAdmin)
    admin.add_view(NotificationAdmin)
    admin.add_view(NotificationEntityAdmin)

    return admin