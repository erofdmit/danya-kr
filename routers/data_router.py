import asyncio

from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db_ops.connector import get_db_session
from db_ops.db_create import MachineModel, DetectorModel
from routers.models import DetectorDataPydantic, MachineDataPydantic


data_router = APIRouter(tags=['main'], prefix='/main')
loop = asyncio.get_event_loop()


@data_router.get('/get_machines_data')
async def get_machines_data(session: AsyncSession = Depends(get_db_session)):
    async with session.begin(): 
        q = select(MachineModel)
        result = await session.execute(q)
        data = result.scalars().all()
        return data

@data_router.get('/get_machines_data')
async def get_detectors_data(session: AsyncSession = Depends(get_db_session)):
    async with session.begin(): 
        q = select(DetectorModel)
        result = await session.execute(q)
        data = result.scalars().all()
        return data
    

@data_router.post('/put_detector')
async def put_detector_data(detector_data: DetectorDataPydantic, session: AsyncSession = Depends(get_db_session)):
    new_detector_data = DetectorModel(
        machine_id=detector_data.machine_id,
        type_name=detector_data.type_name
    )

    async with session.begin():
        session.add(new_detector_data)
        await session.commit()  
    await session.refresh(new_detector_data) 
    return new_detector_data
    
    
@data_router.post('/put_machine')
async def put_machines_data(machine_data: MachineDataPydantic, session: AsyncSession = Depends(get_db_session)):
    new_detector_data = MachineModel(
        machine_name=machine_data.name,
        expluatation_start=machine_data.start_date
    )

    async with session.begin():
        session.add(new_detector_data)
        await session.commit()  
    await session.refresh(new_detector_data) 
    return new_detector_data