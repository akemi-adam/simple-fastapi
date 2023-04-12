from sqlalchemy import Column, Integer, String, DECIMAL
from database import Base

from pydantic import BaseModel

from typing import Optional


class Fish(Base):
    __tablename__ = 'fishes'

    id = Column(Integer, primary_key=True)

    specie = Column(String, nullable=False)

    size = Column(DECIMAL, nullable=True)

    def __init__(self, specie, size):
        self.specie = specie

        self.size = size


class FishCreate(BaseModel):
    specie: str

    size: float | None = None


class FishUpdate(BaseModel):
    specie: Optional[str] = None

    size: Optional[str] = None
