from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime
)

from sqlalchemy.sql import func

from app.database import Base


class AgentMetric(Base):

    __tablename__ = (
        "agent_metrics"
    )

    id = Column(
        Integer,
        primary_key=True
    )

    agent_name = Column(
        String
    )

    execution_time = Column(
        Float
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )