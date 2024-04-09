import asyncio

from fastapi import APIRouter, Body, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db_ops.connector import get_db_session
from db_ops.db_create import DetectionDataModel
from routers.methods import create_metrics
from routers.models import DetectionDataPydantic, DetectorDataPydantic, DetectorMetrics, MetricsResponseModel
import os


metrics_router = APIRouter(tags=['metrics'], prefix='/metrics')
loop = asyncio.get_event_loop()

@metrics_router.post('/metrics_from_detector', response_model=MetricsResponseModel)
async def get_metrics_from_detector(request: Request, detector_info: DetectorMetrics, session: AsyncSession = Depends(get_db_session)):
    async with session.begin(): 
        # Update the query to filter by a list of detector_ids
        query = select(DetectionDataModel).where(
            DetectionDataModel.detector_id.in_(detector_info.detector_ids)
        )
        result = await session.execute(query)
        
        detections = result.scalars().all()
        
        if not detections:
            raise HTTPException(status_code=404, detail="No detections found for the provided detector IDs.")
        
        # Prepare data for metrics creation
        detections_data = [{"timestamp": detection.timestamp, "detector_id": detection.detector_id, "value": detection.detection_value} for detection in detections]
        
        # Calculate metrics and generate plots
        stats, line_plot_filename, bar_plot_filename = create_metrics(detections_data)

        static_base_url = str(request.base_url) + "static"
        line_plot_url = f"{static_base_url}/detector_values_over_time.png"
        bar_plot_url = f"{static_base_url}/avg_value_per_detector.png"

        return {
            "stats": stats,
            "line_plot_url": line_plot_url,
            "bar_plot_url": bar_plot_url
        }


def serialize_sqlalchemy_obj(sqlalchemy_obj):
    """
    Serialize a SQLAlchemy model instance for JSON response.
    Filters out SQLAlchemy internal attributes and relationships.
    """
    return {key: value for key, value in sqlalchemy_obj.__dict__.items() if not key.startswith('_')}