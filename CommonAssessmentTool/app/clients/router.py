# app/clients/router.py

from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.auth.router import get_admin_user, get_current_user
from app.clients.schema import (
    ClientListResponse,
    ClientResponse,
    ClientUpdate,
    PredictionInput,
    ServiceResponse,
    ServiceUpdate,
)
from app.clients.service.case_assignment_service import CaseAssignmentService
from app.clients.service.client_case_service import ClientCaseService
from app.clients.service.client_service import ClientService
from app.clients.service.logic import interpret_and_calculate
from app.database import get_db
from app.models import User

router = APIRouter(prefix="/clients", tags=["clients"])

# --------- Basic CRUD ---------


@router.get("/", response_model=ClientListResponse)
async def get_clients(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=150),
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    return ClientService.get_clients(db, skip, limit)


@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    return ClientService.get_client(db, client_id)


@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: int,
    client_data: ClientUpdate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    return ClientService.update_client(db, client_id, client_data)


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    client_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    ClientService.delete_client(db, client_id)
    return None


# --------- Services ---------


@router.get("/{client_id}/services", response_model=List[ServiceResponse])
async def get_client_services(
    client_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    return ClientCaseService.get_client_services(db, client_id)


@router.put("/{client_id}/services/{user_id}", response_model=ServiceResponse)
async def update_client_services(
    client_id: int,
    user_id: int,
    service_update: ServiceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ClientCaseService.update_client_services(
        db, client_id, user_id, service_update
    )


# --------- Case Assignment ---------


@router.post("/{client_id}/case-assignment", response_model=ServiceResponse)
async def create_case_assignment(
    client_id: int,
    case_worker_id: int = Query(..., description="Case worker ID to assign"),
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    return CaseAssignmentService.create_case_assignment(db, client_id, case_worker_id)


@router.get("/case-worker/{case_worker_id}", response_model=List[ClientResponse])
async def get_clients_by_case_worker(
    case_worker_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return CaseAssignmentService.get_clients_by_case_worker(db, case_worker_id)


@router.post("/predictions")
async def predict(data: PredictionInput):
    """
    Predict client outcome score using the current ML model.
    """
    return interpret_and_calculate(data.model_dump())
