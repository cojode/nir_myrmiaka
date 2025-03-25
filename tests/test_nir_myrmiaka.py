import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from nir_myrmiaka.db.models.user_profile import UserProfile

# Test data constants
TEST_STUDENT_USER = {
    "username": "testuser_student",
    "password": "Testpass123!",
    "role": "Student",
    "email": "test@example.com",
}

TEST_TEACHER_USER = {
    "username": "testuser_teacher",
    "password": "Testpass123!",
    "role": "Teacher",
    "email": "test@example.com",
}


@pytest.mark.anyio
async def test_health_check(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """Test health check endpoint returns 200 OK"""
    url = fastapi_app.url_path_for("health_check")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_user_registration(
    client: AsyncClient, fastapi_app: FastAPI, dbsession: AsyncSession
) -> None:
    """Test user registration creates a new user"""
    url = fastapi_app.url_path_for("register_user")
    response = await client.post(url, json=TEST_STUDENT_USER)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["data"]["username"] == TEST_STUDENT_USER["username"]

    result = await dbsession.execute(
        select(UserProfile).where(
            UserProfile.username == TEST_STUDENT_USER["username"]
        )
    )
    assert result.scalar_one_or_none() is not None


# @pytest.mark.anyio
# async def test_get_user_info(
#     client: AsyncClient, fastapi_app: FastAPI, dbsession: AsyncSession
# ) -> None:
#     """Test retrieving user info returns valid data"""
#     # Setup test data directly in database
#     from nir_myrmiaka.db.models.user_profile import UserProfile

#     await dbsession.execute(
#         insert(UserProfile).values(
#             username="existing_user",
#             role="student",
#             email="existing@example.com",
#         )
#     )
#     await dbsession.commit()

#     # Get the inserted user's ID
#     result = await dbsession.execute(
#         select(UserProfile.id).where(UserProfile.username == "existing_user")
#     )
#     user_id = result.scalar_one()

#     url = fastapi_app.url_path_for(
#         "get_info_user_api_v1_user__user_id__info_get", user_id=user_id
#     )
#     response = await client.get(url)

#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()["data"]["username"] == "existing_user"


# @pytest.mark.anyio
# async def test_create_assignment(
#     client: AsyncClient, fastapi_app: FastAPI, dbsession: AsyncSession
# ) -> None:
#     """Test assignment creation with valid data"""
#     # Setup required test data
#     from nir_myrmiaka.db.models.user_profile import UserProfile

#     await dbsession.execute(
#         insert(UserProfile).values(
#             [
#                 {"username": "student1", "role": "student"},
#                 {"username": "teacher1", "role": "teacher"},
#             ]
#         )
#     )
#     await dbsession.commit()

#     # Get the inserted IDs
#     result = await dbsession.execute(
#         select(UserProfile.id, UserProfile.username).where(
#             UserProfile.username.in_(["student1", "teacher1"])
#         )
#     )
#     users = {username: id for id, username in result}

#     url = fastapi_app.url_path_for(
#         "create_assignment_api_v1_student_create_assignment_post"
#     )
#     response = await client.post(
#         url,
#         json={
#             "student": {"user_id": users["student1"]},
#             "teacher": {"user_id": users["teacher1"]},
#             "text": "Test assignment",
#         },
#     )

#     assert response.status_code == status.HTTP_201_CREATED

#     # Verify database state
#     from nir_myrmiaka.db.models.base_assignment import BaseAssignment

#     result = await dbsession.execute(select(BaseAssignment))
#     assert result.scalar_one_or_none() is not None


# @pytest.mark.anyio
# async def test_get_all_teachers_empty(
#     client: AsyncClient, fastapi_app: FastAPI
# ) -> None:
#     """Test getting all teachers when none exist"""
#     url = fastapi_app.url_path_for(
#         "get_all_teachers_api_v1_user_all_teachers_get"
#     )
#     response = await client.get(url)

#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()["count"] == 0
#     assert response.json()["values"] == []


# @pytest.mark.anyio
# async def test_get_all_teachers_with_data(
#     client: AsyncClient, fastapi_app: FastAPI, dbsession: AsyncSession
# ) -> None:
#     """Test getting all teachers returns populated list"""
#     # Setup test data
#     from nir_myrmiaka.db.models.user_profile import UserProfile

#     await dbsession.execute(
#         insert(UserProfile).values(
#             [
#                 {"username": "teacher1", "role": "teacher"},
#                 {"username": "teacher2", "role": "teacher"},
#             ]
#         )
#     )
#     await dbsession.commit()

#     url = fastapi_app.url_path_for(
#         "get_all_teachers_api_v1_user_all_teachers_get"
#     )
#     response = await client.get(url)

#     assert response.status_code == status.HTTP_200_OK
#     data = response.json()
#     assert data["count"] == 2
#     assert any(t["username"] == "teacher1" for t in data["values"])


# @pytest.mark.anyio
# async def test_invalid_assignment_creation(
#     client: AsyncClient, fastapi_app: FastAPI
# ) -> None:
#     """Test assignment creation with invalid data"""
#     url = fastapi_app.url_path_for(
#         "create_assignment_api_v1_student_create_assignment_post"
#     )

#     # Test missing required fields
#     response = await client.post(url, json={})
#     assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

#     # Test invalid user IDs
#     response = await client.post(
#         url,
#         json={
#             "student": {"user_id": 999},
#             "teacher": {"user_id": 999},
#             "text": "Invalid assignment",
#         },
#     )
#     assert response.status_code == status.HTTP_400_BAD_REQUEST
