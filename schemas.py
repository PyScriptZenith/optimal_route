from sqlalchemy.orm import relationship, declarative_base

from sqlalchemy import Integer, Column, Float, ForeignKey

Base = declarative_base()


class Point(Base):

    __tablename__ = "points"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    route_id = Column(
        Integer, ForeignKey("routes.id")
    )  # Ссылка на маршрут, к которому относится точка
    route = relationship("Route", back_populates="points")


class Route(Base):

    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    points = relationship("Point", back_populates="route")
