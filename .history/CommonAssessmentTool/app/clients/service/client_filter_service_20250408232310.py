from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Client


class ClientFilterService:
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

        # Apply dynamic filters
        filters = {
            Client.currently_employed: employment_status,
            Client.age: (age_min, lambda col, value: col >= value),
            Client.gender: gender,
            Client.level_of_schooling: education_level,
            Client.work_experience: work_experience,
            Client.canada_workex: canada_workex,
            Client.dep_num: dep_num,
            Client.canada_born: canada_born,
            Client.citizen_status: citizen_status,
            Client.fluent_english: fluent_english,
            Client.reading_english_scale: reading_english_scale,
            Client.speaking_english_scale: speaking_english_scale,
            Client.writing_english_scale: writing_english_scale,
            Client.numeracy_scale: numeracy_scale,
            Client.computer_scale: computer_scale,
            Client.transportation_bool: transportation_bool,
            Client.caregiver_bool: caregiver_bool,
            Client.housing: housing,
            Client.income_source: income_source,
            Client.felony_bool: felony_bool,
            Client.attending_school: attending_school,
            Client.substance_use: substance_use,
            Client.time_unemployed: time_unemployed,
            Client.need_mental_health_support_bool: need_mental_health_support_bool,
        }

        for column, value in filters.items():
            if isinstance(value, tuple):
                actual_value, comparator = value
                if actual_value is not None:
                    query = query.filter(comparator(column, actual_value))
            elif value is not None:
                query = query.filter(column == value)

        try:
            return query.all()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving clients: {str(e)}",
            )
