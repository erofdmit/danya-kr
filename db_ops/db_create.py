from sqlalchemy import ForeignKey, create_engine, Column, Integer, Float, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()

class DetectionDataModel(Base):
    __tablename__ = "detections_data"
    detection_id = Column(Integer, primary_key=True)
    detector_id = Column(Integer, ForeignKey('detectors_data.detector_id'))
    detection_value = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class MachineModel(Base):
    __tablename__ = "machines_data"

    machine_id = Column(Integer, primary_key=True)
    machine_name = Column(String)
    expluatation_start = Column(DateTime(timezone=True))


class DetectorModel(Base):
    __tablename__ = "detectors_data"

    detector_id = Column(Integer, primary_key=True)
    machine_id = Column(Integer, ForeignKey('machines_data.machine_id'))
    type_name = Column(String)
    
    
async def create_detector_data_table_async(database_url):
    engine = create_async_engine(database_url, echo=True)
    
    # AsyncSession configuration
    async with engine.begin() as conn:
        # await the creation of all tables
        await conn.run_sync(Base.metadata.create_all)
    
    print("Table created successfully (async).")
    
    
import asyncio

# Assuming create_detector_data_table_async is defined as shown before

async def main():
    database_url = "postgresql+asyncpg://postgres:postgres@localhost:7890/smirnov_db"
    await create_detector_data_table_async(database_url)

# This is the standard way to run the main coroutine with asyncio
if __name__ == "__main__":
    asyncio.run(main())