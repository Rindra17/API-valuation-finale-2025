from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
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