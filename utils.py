from typing import List
import os
import requests
import polyline

from dotenv import load_dotenv

load_dotenv(".env")


def get_optimal_route(coordinates: List[List[float]]) -> List[List[float]]:
    """
    Строит оптимальный маршрут по координатам точек
    """
    API_KEY = os.getenv("OPENROUTESERVICE_API_KEY")

    body = {
        "coordinates": coordinates,
        "radiuses": [
            500,
        ],
    }
    headers = {
        "Accept": "application/json, application/geo+json, "
                  "application/gpx+xml, img/png; charset=utf-8",
        "Authorization": API_KEY,
        "Content-Type": "application/json; charset=utf-8",
    }
    call = requests.post(
        "https://api.openrouteservice.org/v2/directions/driving-car",
        json=body,
        headers=headers,
    )

    response = call.json()

    # Получаем закодированный оптимальный маршрут

    route_geometry_str = response["routes"][0]["geometry"]

    # Декодируем маршрут в координаты точек

    decoded_geometry = polyline.decode(route_geometry_str)

    start_point = coordinates[0]
    end_point = coordinates[-1]

    decoded_geometry_fixed = [[lat, lon] for lon, lat in decoded_geometry]

    # Добавляем в маршрут начальную и конечную точку

    decoded_geometry_fixed.insert(0, start_point)
    decoded_geometry_fixed.append(end_point)

    return decoded_geometry_fixed
