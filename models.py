from typing import Optional, List

from fastapi import File, UploadFile, Query


from pydantic import BaseModel


class RouteData(BaseModel):
    format: str = Query(..., description="Формат файла, должен быть 'csv'")
    file: UploadFile = File(..., description="CSV файл с точками маршрута")


class PointCreate(BaseModel):
    lat: float
    lng: float

    class Config:
        orm_mode = True


class RouteCreate(BaseModel):
    id: Optional[int] = None
    points: List[PointCreate]

    class Config:
        orm_mode = True
