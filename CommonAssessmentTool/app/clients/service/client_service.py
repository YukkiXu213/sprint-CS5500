"""
Client service module handling all database operations for clients.
Provides CRUD operations and business logic for client management.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Dict
from app.models import Client
from app.clients.schema import ClientUpdate

class ClientService:

    @staticmethod
    def get_client(db: Session, client_id: int):
        """Get a specific client by ID"""
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with id {client_id} not found"
            )
        return client

    @staticmethod
    def get_clients(db: Session, skip: int = 0, limit: int = 50) -> Dict:
        """Get clients with optional pagination."""
        if skip < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Skip value cannot be negative"
            )
        if limit < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit must be greater than 0"
            )

        clients = db.query(Client).offset(skip).limit(limit).all()
        total = db.query(Client).count()
        return {"clients": clients, "total": total}

    @staticmethod
    def update_client(db: Session, client_id: int, client_update: ClientUpdate):
        """Update a client's information"""
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with id {client_id} not found"
            )

        update_data = client_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(client, field, value)

        try:
            db.commit()
            db.refresh(client)
            return client
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update client: {str(e)}"
            )

    @staticmethod
    def delete_client(db: Session, client_id: int):
        """Delete a client and their associated records"""
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with id {client_id} not found"
            )

        try:
            db.delete(client)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete client: {str(e)}"
            )
