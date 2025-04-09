from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from sqlalchemy.orm import Session
from ...models import Client, ClientCase


class IClientRepository(ABC):

    @abstractmethod
    def get_client(self, client_id: int) -> Optional[Client]:
        pass

    @abstractmethod
    def get_clients(self, skip: int, limit: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_clients_by_criteria(self, **criteria: Any) -> List[Client]:
        pass

    @abstractmethod
    def get_clients_by_services(self, **service_filters: Any) -> List[Client]:
        pass

    @abstractmethod
    def get_client_services(self, client_id: int) -> List[ClientCase]:
        pass

    @abstractmethod
    def get_clients_by_success_rate(self, min_rate: int) -> List[Client]:
        pass

    @abstractmethod
    def get_clients_by_case_worker(self, case_worker_id: int) -> List[Client]:
        pass

    @abstractmethod
    def get_client_case(self, client_id: int, user_id: int) -> Optional[ClientCase]:
        pass

    @abstractmethod
    def update_client(self, client_id: int, update_data: Dict[str, Any]) -> Optional[Client]:
        pass

    @abstractmethod
    def update_client_services(
        self, client_id: int, user_id: int, update_data: Dict[str, Any]
    ) -> Optional[ClientCase]:
        pass

    @abstractmethod
    def create_case_assignment(self, client_id: int, case_worker_id: int) -> ClientCase:
        pass

    @abstractmethod
    def delete_client(self, client_id: int) -> None:
        pass


class SQLAlchemyClientRepository(IClientRepository):

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_client(self, client_id: int) -> Optional[Client]:
        return self.db.query(Client).filter(Client.id == client_id).first()

    def get_clients(self, skip: int, limit: int) -> Dict[str, Any]:
        clients = self.db.query(Client).offset(skip).limit(limit).all()
        total = self.db.query(Client).count()
        return {"clients": clients, "total": total}

    def get_clients_by_criteria(self, **criteria: Any) -> List[Client]:
        query = self.db.query(Client)
        for key, value in criteria.items():
            if value is not None and hasattr(Client, key):
                query = query.filter(getattr(Client, key) == value)
        return query.all()

    def get_clients_by_services(self, **service_filters: Any) -> List[Client]:
        query = self.db.query(Client).join(ClientCase)
        for service_name, status in service_filters.items():
            if status is not None:
                query = query.filter(getattr(ClientCase, service_name) == status)
        return query.all()

    def get_client_services(self, client_id: int) -> List[ClientCase]:
        return self.db.query(ClientCase).filter(ClientCase.client_id == client_id).all()

    def get_clients_by_success_rate(self, min_rate: int) -> List[Client]:
        return (
            self.db.query(Client)
            .join(ClientCase)
            .filter(ClientCase.success_rate >= min_rate)
            .all()
        )

    def get_clients_by_case_worker(self, case_worker_id: int) -> List[Client]:
        return (
            self.db.query(Client)
            .join(ClientCase)
            .filter(ClientCase.user_id == case_worker_id)
            .all()
        )

    def get_client_case(self, client_id: int, user_id: int) -> Optional[ClientCase]:
        return (
            self.db.query(ClientCase)
            .filter(ClientCase.client_id == client_id, ClientCase.user_id == user_id)
            .first()
        )

    def update_client(self, client_id: int, update_data: Dict[str, Any]) -> Optional[Client]:
        client = self.get_client(client_id)
        if not client:
            return None
        for field, value in update_data.items():
            setattr(client, field, value)
        self.db.commit()
        self.db.refresh(client)
        return client

    def update_client_services(
        self, client_id: int, user_id: int, update_data: Dict[str, Any]
    ) -> Optional[ClientCase]:
        client_case = self.get_client_case(client_id, user_id)
        if not client_case:
            return None
        for field, value in update_data.items():
            setattr(client_case, field, value)
        self.db.commit()
        self.db.refresh(client_case)
        return client_case

    def create_case_assignment(self, client_id: int, case_worker_id: int) -> ClientCase:
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
        )
        self.db.add(new_case)
        self.db.commit()
        self.db.refresh(new_case)
        return new_case

    def delete_client(self, client_id: int) -> None:
        client = self.get_client(client_id)
        if client:
            self.db.query(ClientCase).filter(ClientCase.client_id == client_id).delete()
            self.db.delete(client)
            self.db.commit()

