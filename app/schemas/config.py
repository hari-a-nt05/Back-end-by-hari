from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ConfigBase(BaseModel):
    path: str
    value: str


class ConfigCreate(ConfigBase):
    pass


class ConfigUpdate(BaseModel):
    value: str


class ConfigOut(ConfigBase):
    config_id: int
    updated_at: datetime
