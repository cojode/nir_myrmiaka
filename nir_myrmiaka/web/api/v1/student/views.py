from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from punq import Container
from nir_myrmiaka.container.container import init_container
from nir_myrmiaka.services.work_managment.work_management_service import WorkManagementService
from nir_myrmiaka.web.api.v1.schemas import AssignmentCreateRequest

router = APIRouter()

@router.post("/create-assignment", status_code=status.HTTP_201_CREATED)
async def create_assignment(
    payload: AssignmentCreateRequest,
    container: Container = Depends(init_container)
):
    work_management_service = container.resolve(WorkManagementService)
    
    try:
        info = await work_management_service.create_assignment(payload)
        return info
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
