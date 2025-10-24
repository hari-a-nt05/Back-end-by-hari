from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint

from app.core.database import Base
from app.utils.helper import get_current_time


class Config(Base):
    __tablename__ = "config"
    config_id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String, nullable=False, unique=True)
    value = Column(String, nullable=False)
    updated_at = Column(DateTime, default=get_current_time, onupdate=get_current_time)
    __table_args__ = (UniqueConstraint("path", name="uq_config_path"),)
