from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import requests
from typing import Optional

app = FastAPI()


db = []

# creating the model schema for our db
class City(BaseModel):
    name: str
    timezone: str


@app.get('/')
def index():
    return{'key': 'value'}

# get cities
@app.get('/cities', tags=['City']) # tags=['City'] tags are used to organise and group our request in Swagger
async def get_cities():
    results = []
    for city in db:
        req = requests.get(f'http://worldtimeapi.org/api/timezone/{city["timezone"]}')
        current_time = req.json()['datetime']
        timezone_abbreviation = req.json()['abbreviation']
        results.append({**city,  'current_time': current_time, 'timezone_abbreviation':timezone_abbreviation})
    return results

# get city
@app.get("/cities/{city_id}", tags=['City'])
async def get_city(city_id:int): 
    for city in db:
        if city_id ==  int(db.index(city)):
            # city=db[city_id-1]
            req = requests.get(f'http://worldtimeapi.org/api/timezone/{city["timezone"]}')
            current_time = req.json()['datetime']
            timezone_abbreviation = req.json()['abbreviation']
            return {**city, "current_time": current_time,  'timezone_abbreviation':timezone_abbreviation}
    return{'message': f"City with this id number{city_id} was not found in db!"}



# post request: create a city
@app.post('/cities', tags=['City'])
# city is the args, and City is the model the city should be in.
async def create_city(city:City):
    db.append(city.dict()) 
    return {'message': 'New city added successfully!'}


# delete request: delete a city
@app.delete('/cities/{city_id}', tags=['City'])
async def delete_city(city_id: int):
    for city in db:
        if city_id ==  int(db.index(city)):
            db.remove(city)
            return{'message': f'City with the following id number {city_id} was deleted successfully!'}
    return {"message": f"City with the following id number {city_id} was not found!"}









