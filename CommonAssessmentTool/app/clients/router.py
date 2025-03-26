from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..auth.router import get_current_user, get_admin_user
from ..models import User
from ..database import get_db
from .service.client_service import ClientService
from .service.client_repository import SQLAlchemyClientRepository
from .schema import (
    ClientResponse,
    ClientUpdate,
    ClientListResponse,
    ServiceResponse,
    ServiceUpdate,
)

router = APIRouter(prefix="/clients", tags=["clients"])


def get_client_service(db: Session = Depends(get_db)) -> ClientService:
    repo = SQLAlchemyClientRepository(db)
    return ClientService(repo)


@router.get("/", response_model=ClientListResponse)
async def get_clients(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=150),
    current_user: User = Depends(get_admin_user),
    service: ClientService = Depends(get_client_service),
):
    return service.get_clients(skip, limit)


@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: int,
    current_user: User = Depends(get_admin_user),
    service: ClientService = Depends(get_client_service),
):
    return service.get_client(client_id)


@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: int,
    client_data: ClientUpdate,
    current_user: User = Depends(get_admin_user),
    service: ClientService = Depends(get_client_service),
):
    return service.update_client(client_id, client_data.dict(exclude_unset=True))


@router.put("/{client_id}/services/{user_id}", response_model=ServiceResponse)
async def update_client_services(
    client_id: int,
    user_id: int,
    service_update: ServiceUpdate,
    current_user: User = Depends(get_current_user),
    service: ClientService = Depends(get_client_service),
):
    return service.update_client_services(client_id, user_id, service_update.dict(exclude_unset=True))


@router.post("/{client_id}/case-assignment", response_model=ServiceResponse)
async def create_case_assignment(
    client_id: int,
    case_worker_id: int = Query(..., description="Case worker ID to assign"),
    current_user: User = Depends(get_admin_user),
    service: ClientService = Depends(get_client_service),
):
    return service.create_case_assignment(client_id, case_worker_id)


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    client_id: int,
    current_user: User = Depends(get_admin_user),
    service: ClientService = Depends(get_client_service),
):
    service.delete_client(client_id)
    return None
