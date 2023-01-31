from sqlalchemy import Column, Integer, String, TEXT, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()  # создает енджин вместе с модельнками


class RezkaSeriesModel(Base):
    __tablename__ = "rezka_series"

    id = Column(Integer, primary_key=True)

    current_url = Column(String(100), nullable=True)
    title = Column(String(255), nullable=True)
    release_year = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    genre = Column(String(250), nullable=True)
    age_group = Column(String(100), nullable=True)
    duration = Column(String(100), nullable=True)
    image = Column(TEXT, nullable=True)

    created_at = Column(DateTime, default=func.now())
