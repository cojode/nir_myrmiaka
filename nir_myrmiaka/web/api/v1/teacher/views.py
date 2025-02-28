from fastapi import APIRouter, HTTPException, Depends, status

from punq import Container
from nir_myrmiaka.container.container import init_container

from nir_myrmiaka.services.work_managment.work_management_service import (
    WorkManagementService,
)

router = APIRouter()


@router.get("/browse-assignments", status_code=status.HTTP_201_CREATED)
async def browse_assignments(
    teacher_id: int, container: Container = Depends(init_container)
):
    work_management_service: WorkManagementService = container.resolve(
        WorkManagementService
    )

    try:
        return await work_management_service.browse_assignments(teacher_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/accept_assignment", status_code=status.HTTP_201_CREATED)
async def accept_assignment(
    teacher_id: int,
    semestr: int,
    assignment_id: int,
    container: Container = Depends(init_container),
):
    work_management_service: WorkManagementService = container.resolve(
        WorkManagementService
    )

    try:
        return await work_management_service.accept_assignment(
            teacher_id, semestr, assignment_id
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/decline_assignment", status_code=status.HTTP_201_CREATED)
async def accept_assignment(
    teacher_id: int, assignment_id: int, container: Container = Depends(init_container)
):
    work_management_service: WorkManagementService = container.resolve(
        WorkManagementService
    )

    try:
        return await work_management_service.decline_assignment(
            teacher_id, assignment_id
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
