from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)

from app.database import Base


class SyncJob(Base):

    __tablename__ = "sync_jobs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    status = Column(String)
    created_at = Column(DateTime)