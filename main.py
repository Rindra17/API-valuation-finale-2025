from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

app = FastAPI()

@app.get("/ping")
def ping():
    return Response( content="pong", status_code=200, media_type="text/plain" )

class CarCharacteristics(BaseModel):
    max_speed: int
    max_fuel_capacity: int

class Car(BaseModel):
    identifier: str
    brand: str
    model: str
    characteristics: CarCharacteristics

cars_list: List[Car] = []

def serialize_cars():
    car_serialized = []
    for car in cars_list:
        car_serialized.append(car.model_dump())
    return car_serialized
@app.post("/cars")
def create_cars(cars: Car):
    cars_list.append(cars)
    serialized_car = serialize_cars()
    return JSONResponse(content=serialized_car, status_code=201, media_type="application/json")

@app.get("/cars")
def get_cars():
    return JSONResponse(content=serialize_cars(), status_code=200, media_type="application/json")

@app.get("/cars/{id}")
def get_car(id: str):
    for car in cars_list:
        if car.identifier == id:
            return JSONResponse(content=car.model_dump(), status_code=200, media_type="application/json")
    return JSONResponse(content="Car not found", status_code=404, media_type="application/json")
