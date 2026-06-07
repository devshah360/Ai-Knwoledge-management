from sqlalchemy import (
    Column,
    Integer,
    String,
    Float
)

from app.database import Base


class SystemMetric(Base):

    __tablename__ = "system_metrics"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    endpoint = Column(
        String
    )

    response_time = Column(
        Float
    )