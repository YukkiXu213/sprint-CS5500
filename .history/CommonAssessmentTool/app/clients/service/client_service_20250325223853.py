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
                detail=f"Client with id {client_id} not found",
            )
        return client

    def get_clients(self, skip: int = 0, limit: int = 50):
        if skip < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Skip value cannot be negative",
            )
        if limit < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit must be greater than 0",
            )
<<<<<<< HEAD
        return self.repo.get_clients(skip, limit)

    def get_clients_by_criteria(self, **criteria):
=======

        clients = db.query(Client).offset(skip).limit(limit).all()
        total = db.query(Client).count()
        return {"clients": clients, "total": total}

    @staticmethod
    def get_clients_by_criteria(
        db: Session,
        employment_status: Optional[bool] = None,
        education_level: Optional[int] = None,
        age_min: Optional[int] = None,
        gender: Optional[int] = None,
        work_experience: Optional[int] = None,
        canada_workex: Optional[int] = None,
        dep_num: Optional[int] = None,
        canada_born: Optional[bool] = None,
        citizen_status: Optional[bool] = None,
        fluent_english: Optional[bool] = None,
        reading_english_scale: Optional[int] = None,
        speaking_english_scale: Optional[int] = None,
        writing_english_scale: Optional[int] = None,
        numeracy_scale: Optional[int] = None,
        computer_scale: Optional[int] = None,
        transportation_bool: Optional[bool] = None,
        caregiver_bool: Optional[bool] = None,
        housing: Optional[int] = None,
        income_source: Optional[int] = None,
        felony_bool: Optional[bool] = None,
        attending_school: Optional[bool] = None,
        substance_use: Optional[bool] = None,
        time_unemployed: Optional[int] = None,
        need_mental_health_support_bool: Optional[bool] = None,
    ):
        """Get clients filtered by any combination of criteria"""
        query = db.query(Client)

        if education_level is not None and not (1 <= education_level <= 14):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Education level must be between 1 and 14",
            )

        if age_min is not None and age_min < 18:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Minimum age must be at least 18",
            )

        if gender is not None and gender not in [1, 2]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Gender must be 1 or 2"
            )

        # Apply filters for non-None values
        if employment_status is not None:
            query = query.filter(Client.currently_employed == employment_status)
        if age_min is not None:
            query = query.filter(Client.age >= age_min)
        if gender is not None:
            query = query.filter(Client.gender == gender)
        if education_level is not None:
            query = query.filter(Client.level_of_schooling == education_level)
        if work_experience is not None:
            query = query.filter(Client.work_experience == work_experience)
        if canada_workex is not None:
            query = query.filter(Client.canada_workex == canada_workex)
        if dep_num is not None:
            query = query.filter(Client.dep_num == dep_num)
        if canada_born is not None:
            query = query.filter(Client.canada_born == canada_born)
        if citizen_status is not None:
            query = query.filter(Client.citizen_status == citizen_status)
        if fluent_english is not None:
            query = query.filter(Client.fluent_english == fluent_english)
        if reading_english_scale is not None:
            query = query.filter(Client.reading_english_scale == reading_english_scale)
        if speaking_english_scale is not None:
            query = query.filter(
                Client.speaking_english_scale == speaking_english_scale
            )
        if writing_english_scale is not None:
            query = query.filter(Client.writing_english_scale == writing_english_scale)
        if numeracy_scale is not None:
            query = query.filter(Client.numeracy_scale == numeracy_scale)
        if computer_scale is not None:
            query = query.filter(Client.computer_scale == computer_scale)
        if transportation_bool is not None:
            query = query.filter(Client.transportation_bool == transportation_bool)
        if caregiver_bool is not None:
            query = query.filter(Client.caregiver_bool == caregiver_bool)
        if housing is not None:
            query = query.filter(Client.housing == housing)
        if income_source is not None:
            query = query.filter(Client.income_source == income_source)
        if felony_bool is not None:
            query = query.filter(Client.felony_bool == felony_bool)
        if attending_school is not None:
            query = query.filter(Client.attending_school == attending_school)
        if substance_use is not None:
            query = query.filter(Client.substance_use == substance_use)
        if time_unemployed is not None:
            query = query.filter(Client.time_unemployed == time_unemployed)
        if need_mental_health_support_bool is not None:
            query = query.filter(
                Client.need_mental_health_support_bool
                == need_mental_health_support_bool
            )
>>>>>>> lulu

        try:
            return self.repo.get_clients_by_criteria(**criteria)
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
<<<<<<< HEAD
                detail=str(e)
            )

    def get_clients_by_services(self, **service_filters):
=======
                detail=f"Error retrieving clients: {str(e)}",
            )

    @staticmethod
    def get_clients_by_services(db: Session, **service_filters: Optional[bool]):
        """
        Get clients filtered by multiple service statuses.
        """
        query = db.query(Client).join(ClientCase)

        for service_name, status in service_filters.items():
            if status is not None:
                filter_criteria = getattr(ClientCase, service_name) == status
                query = query.filter(filter_criteria)

>>>>>>> lulu
        try:
            return self.repo.get_clients_by_services(**service_filters)
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
<<<<<<< HEAD
                detail=str(e)
            )

    def get_client_services(self, client_id: int):
        services = self.repo.get_client_services(client_id)
        if not services:
=======
                detail=f"Error retrieving clients: {str(e)}",
            )

    @staticmethod
    def get_client_services(db: Session, client_id: int):
        """Get all services for a specific client with case worker info"""
        client_cases = (
            db.query(ClientCase).filter(ClientCase.client_id == client_id).all()
        )
        if not client_cases:
>>>>>>> lulu
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No services found for client with id {client_id}",
            )
        return services

    def get_clients_by_success_rate(self, min_rate: int = 70):
        if not (0 <= min_rate <= 100):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Success rate must be between 0 and 100",
            )
<<<<<<< HEAD
        return self.repo.get_clients_by_success_rate(min_rate)

    def get_clients_by_case_worker(self, case_worker_id: int):
        return self.repo.get_clients_by_case_worker(case_worker_id)
=======

        return (
            db.query(Client)
            .join(ClientCase)
            .filter(ClientCase.success_rate >= min_rate)
            .all()
        )

    @staticmethod
    def get_clients_by_case_worker(db: Session, case_worker_id: int):
        """Get all clients assigned to a specific case worker"""
        case_worker = db.query(User).filter(User.id == case_worker_id).first()
        if not case_worker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Case worker with id {case_worker_id} not found",
            )

        return (
            db.query(Client)
            .join(ClientCase)
            .filter(ClientCase.user_id == case_worker_id)
            .all()
        )
>>>>>>> lulu

    def update_client(self, client_id: int, update_data: dict):

        if not self.repo.get_client(client_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with id {client_id} not found",
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
                detail=f"Failed to update client: {str(e)}",
            )
<<<<<<< HEAD
=======

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
                detail=f"No case found for client {client_id} with case worker {user_id}. "
                f"Cannot update services for a non-existent case assignment.",
            )

        update_data = service_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(client_case, field, value)
>>>>>>> lulu

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
                detail=f"Failed to update client services: {str(e)}",
            )
<<<<<<< HEAD
=======

    @staticmethod
    def create_case_assignment(db: Session, client_id: int, case_worker_id: int):
        """Create a new case assignment"""
        # Check if client exists
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with id {client_id} not found",
            )
>>>>>>> lulu

    def create_case_assignment(self, client_id: int, case_worker_id: int):

        if not self.repo.get_client(client_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
<<<<<<< HEAD
                detail=f"Client with id {client_id} not found"
            )
        if self.repo.get_client_case(client_id, case_worker_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Client {client_id} already has a case assigned to {case_worker_id}"
=======
                detail=f"Case worker with id {case_worker_id} not found",
            )

        # Check if assignment already exists
        existing_case = (
            db.query(ClientCase)
            .filter(
                ClientCase.client_id == client_id, ClientCase.user_id == case_worker_id
            )
            .first()
        )

        if existing_case:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Client {client_id} already has a case assigned to case worker {case_worker_id}",
            )

        try:
            # Create new case assignment with default service values
            new_case = ClientCase(
                client_id=client_id,
                user_id=case_worker_id,
                employment_assistance=False,
                life_stabilization=False,
                retention_services=False,
                specialized_services=False,
                employment_related_financial_supports=False,
                employer_financial_supports=False,
                enhanced_referrals=False,
                success_rate=0,
>>>>>>> lulu
            )
        try:
            return self.repo.create_case_assignment(client_id, case_worker_id)
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create case assignment: {str(e)}",
            )

<<<<<<< HEAD
    def delete_client(self, client_id: int):
        if not self.repo.get_client(client_id):
=======
    @staticmethod
    def delete_client(db: Session, client_id: int):
        """Delete a client and their associated records"""
        # First check if client exists
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
>>>>>>> lulu
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with id {client_id} not found",
            )
        try:
<<<<<<< HEAD
            self.repo.delete_client(client_id)
        except SQLAlchemyError as e:
=======
            # Delete associated client_cases
            db.query(ClientCase).filter(ClientCase.client_id == client_id).delete()

            # Delete the client
            db.delete(client)
            db.commit()

        except Exception as e:
            db.rollback()
>>>>>>> lulu
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete client: {str(e)}",
            )
