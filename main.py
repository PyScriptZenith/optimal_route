
from fastapi import FastAPI, File, UploadFile, status, HTTPException
from fastapi.responses import JSONResponse
from database import POSTGRES_CONNECTION_PATH

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from db_models import Route, Point
from models import PointCreate, RouteCreate
from utils import get_optimal_route
import csv
from io import StringIO



app = FastAPI()



engine = create_engine(POSTGRES_CONNECTION_PATH,
                       echo=True)

Session = sessionmaker(bind=engine)


session = Session()


@app.post("/api/routes/")
async def upload_file_and_create_route(file: UploadFile = File(...)):
    """
    Создает оптимальный маршрут по координатам точек
    Args:
        file: csv файл с координатами точек

    Returns: оптимальный маршрут

    """

    # Валидация на формат файла

    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Файл должен быть в формате CSV.")
    contents = await file.read()

    # Преобразуем байтовые данные в строку

    csv_data = contents.decode('utf-8')

    # Преобразуем строку CSV в объект StringIO для чтения с помощью модуля csv

    csv_file = StringIO(csv_data)


    points = []

    points_for_API_request = []

    # Чтение CSV файла и сохранение его содержимого в список точек

    reader = csv.reader(csv_file)

    for i, row in enumerate(reader):
        if i == 0:  # Пропускаем первую строку с заголовками
            continue
        lat = float(row[1])
        lng = float(row[2])

        coordinate = [lng, lat]

        points_for_API_request.append(coordinate)


    # Валидация на ограничение API - не более 50 точек

    if len(points_for_API_request) > 50:
        return JSONResponse(status_code=400, content={"message": "Максимальное количество точек для маршрута - 50."})

    try:

        # Отправляем запрос к стороннему API на получение оптимального маршрута

        optimal_route = get_optimal_route(points_for_API_request)
        for route in optimal_route:

            lng = route[0]
            lat = route[1]


            points.append(PointCreate(lat=lat, lng=lng))

        # Создаем оптимальный маршрут

        return await create_route(RouteCreate(points=points))

    except:

        # Если не удалось построить маршрут

        return JSONResponse(status_code=500, content={"message": "Невозможно построить маршрут."})


async def create_route(route_data: RouteCreate):

    """
    Записывает построенный оптимальный маршрут в БД
    Args:
        route_data: координаты

    Returns: маршрут

    """

    # Создаем пустой маршрут

    new_route = Route()
    session = Session()

    try:
        # Записываем его в БД

        session.add(new_route)
        session.commit()

        # Создаем точки, привязываем их к маршруту и сохраняем в БД

        for point in route_data.points:
            new_point = Point(lat=point.lat, lng=point.lng, route=new_route)
            session.add(new_point)
        session.commit()

        created_route = {"id": new_route.id, "points": route_data.points}
        return created_route

    finally:
        session.close()


@app.get("/api/routes/{route_id}", response_model=RouteCreate, status_code=status.HTTP_200_OK)
def get_route(route_id: int):
    route = session.query(Route).filter(Route.id == route_id).first()

    return route





