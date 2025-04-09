from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.clients.schema import ServiceUpdate
from app.models import Client, ClientCase, User


class ClientCaseService:
    @staticmethod
    def get_client_services(db: Session, client_id: int):
        """Get all services for a specific client with case worker info"""
        client_cases = (
            db.query(ClientCase).filter(ClientCase.client_id == client_id).all()
        )
        if not client_cases:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No services found for client with id {client_id}",
            )
        return client_cases

    @staticmethod
    def update_client_services(
        db: Session, client_id: int, user_id: int, service_update: ServiceUpdate
    ):
        """Update a client's services and outcomes for a specific case worker"""
        client_case = (
            db.query(ClientCase)
            .filter(ClientCase.client_id == client_id, ClientCase.user_id == user_id)
            .first()
        )

        if not client_case:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No case found for client {client_id} with case worker {user_id}.",
            )

        update_data = service_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(client_case, field, value)

        try:
            db.commit()
            db.refresh(client_case)
            return client_case
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update client services: {str(e)}",
            )

    @staticmethod
    def get_clients_by_services(db: Session, **service_filters: Optional[bool]):
        """Get clients filtered by multiple service statuses."""
        query = db.query(Client).join(ClientCase)
        for service_name, status in service_filters.items():
            if status is not None:
                filter_criteria = getattr(ClientCase, service_name) == status
                query = query.filter(filter_criteria)
        try:
            return query.all()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving clients: {str(e)}",
            )

    @staticmethod
    def get_clients_by_success_rate(db: Session, min_rate: int = 70):
        """Get clients with success rate at or above the specified percentage"""
        if not (0 <= min_rate <= 100):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Success rate must be between 0 and 100",
            )
        return (
            db.query(Client)
            .join(ClientCase)
            .filter(ClientCase.success_rate >= min_rate)
            .all()
        )
