from database import Base, engine
from db_models import Point, Route

"""
Скрипт создания таблицы в БД 
"""


print('creating db...')


Base.metadata.create_all(engine)