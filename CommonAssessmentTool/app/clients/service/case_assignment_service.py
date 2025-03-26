from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import Client, ClientCase, User

class CaseAssignmentService:

    @staticmethod
    def create_case_assignment(
        db: Session, 
        client_id: int,
        case_worker_id: int
    ):
        """Create a new case assignment"""
        # Check if client exists
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with id {client_id} not found"
            )

        # Check if case worker exists
        case_worker = db.query(User).filter(User.id == case_worker_id).first()
        if not case_worker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Case worker with id {case_worker_id} not found"
            )

        # Check if assignment already exists
        existing_case = db.query(ClientCase).filter(
            ClientCase.client_id == client_id,
            ClientCase.user_id == case_worker_id
        ).first()

        if existing_case:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Client {client_id} already has a case assigned to case worker {case_worker_id}"
            )

        try:
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
                success_rate=0
            )
            db.add(new_case)
            db.commit()
            db.refresh(new_case)
            return new_case

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create case assignment: {str(e)}"
            )

    @staticmethod
    def get_clients_by_case_worker(db: Session, case_worker_id: int):
        """Get all clients assigned to a specific case worker"""
        case_worker = db.query(User).filter(User.id == case_worker_id).first()
        if not case_worker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Case worker with id {case_worker_id} not found"
            )
            
        return db.query(Client).join(ClientCase).filter(
            ClientCase.user_id == case_worker_id
        ).all()
