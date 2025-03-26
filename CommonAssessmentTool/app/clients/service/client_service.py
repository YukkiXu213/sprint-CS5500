from fastapi import HTTPException, status
from typing import Optional, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from .client_repository import IClientRepository
from ...models import Client, ClientCase, User
from ..schema import ClientUpdate

class ClientService:
    def __init__(self, repo: IClientRepository):
        self.repo = repo

    def get_client(self, client_id: int) -> Client:
        client = self.repo.get_client(client_id)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with id {client_id} not found"
            )
        return client

    def get_clients(self, skip: int = 0, limit: int = 50) -> Dict:
        if skip < 0 or limit < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Skip must be >= 0 and limit > 0",
            )
        return self.repo.get_clients(skip, limit)

    def update_client(self, client_id: int, update_data: ClientUpdate):
        if not self.repo.get_client(client_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with id {client_id} not found"
            )
        try:
            return self.repo.update_client(client_id, update_data.dict(exclude_unset=True))
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update client: {str(e)}"
            )

    def delete_client(self, client_id: int):
        if not self.repo.get_client(client_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with id {client_id} not found"
            )
        try:
            self.repo.delete_client(client_id)
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete client: {str(e)}"
            )
