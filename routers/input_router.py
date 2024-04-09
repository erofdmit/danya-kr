import asyncio

from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db_ops.connector import get_db_session
from db_ops.db_create import DetectionDataModel
from routers.models import DetectionDataPydantic, DetectorDataPydantic



input_router = APIRouter(tags=['input'], prefix='/input')
loop = asyncio.get_event_loop()


@input_router.post('/put_detector_data')
async def put_detector_data(detector_data: DetectionDataPydantic, session: AsyncSession = Depends(get_db_session)):
    new_detector_data = DetectionDataModel(
        detector_id=detector_data.detector_id,
        detection_value=detector_data.value
    )

    async with session.begin():
        session.add(new_detector_data)
        await session.commit()  
    await session.refresh(new_detector_data) 
    return new_detector_data
