from typing import Optional
from app.models.candidate import Candidate
from fastapi_filter.contrib.sqlalchemy import Filter


class CandidateFilter(Filter):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

    class Constants(Filter.Constants):
        model = Candidate
