from typing import List, Optional
from pydantic import BaseModel, HttpUrl
import datetime

class DetectionDataPydantic(BaseModel):
    detector_id: int
    value: float
    
class MachineDataPydantic(BaseModel):
    name: str
    start_date: datetime.datetime
    
class DetectorDataPydantic(BaseModel):
    type_name: str
    machine_id: int
    

class DetectorMetrics(BaseModel):
    detector_ids: List[int]

    
class MachineMetrics(BaseModel):
    machine_id: int
    
class TypeMetrics(BaseModel):
    type_id: int

    
class MetricsResponseModel(BaseModel):
    stats: dict
    line_plot_url: HttpUrl
    bar_plot_url: HttpUrl
   
    

    