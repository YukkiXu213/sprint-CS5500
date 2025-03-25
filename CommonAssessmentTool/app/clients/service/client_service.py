# app/clients/service/client_service.py

from fastapi import HTTPException, status
from typing import Optional, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from .client_repository import IClientRepository
from ...models import Client, ClientCase, User

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

    def get_clients(self, skip: int = 0, limit: int = 50):
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
        return self.repo.get_clients(skip, limit)

    def get_clients_by_criteria(self, **criteria):

        try:
            return self.repo.get_clients_by_criteria(**criteria)
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    def get_clients_by_services(self, **service_filters):
        try:
            return self.repo.get_clients_by_services(**service_filters)
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    def get_client_services(self, client_id: int):
        services = self.repo.get_client_services(client_id)
        if not services:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No services found for client with id {client_id}"
            )
        return services

    def get_clients_by_success_rate(self, min_rate: int = 70):
        if not (0 <= min_rate <= 100):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Success rate must be between 0 and 100"
            )
        return self.repo.get_clients_by_success_rate(min_rate)

    def get_clients_by_case_worker(self, case_worker_id: int):
        return self.repo.get_clients_by_case_worker(case_worker_id)

    def update_client(self, client_id: int, update_data: dict):

        if not self.repo.get_client(client_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with id {client_id} not found"
            )
        try:
            updated_client = self.repo.update_client(client_id, update_data)
            if not updated_client:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Client with id {client_id} not found"
                )
            return updated_client
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update client: {str(e)}"
            )

    def update_client_services(self, client_id: int, user_id: int, service_update: dict):
        try:
            updated_case = self.repo.update_client_services(client_id, user_id, service_update)
            if not updated_case:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No case found for client {client_id} with case worker {user_id}."
                )
            return updated_case
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update client services: {str(e)}"
            )

    def create_case_assignment(self, client_id: int, case_worker_id: int):

        if not self.repo.get_client(client_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with id {client_id} not found"
            )
        if self.repo.get_client_case(client_id, case_worker_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Client {client_id} already has a case assigned to {case_worker_id}"
            )
        try:
            return self.repo.create_case_assignment(client_id, case_worker_id)
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create case assignment: {str(e)}"
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
