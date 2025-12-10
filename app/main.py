from fastapi import FastAPI, HTTPException
from services.api import WheatherApi

from pydantic import BaseModel

from prometheus_client import Counter, make_asgi_app

app = FastAPI()

metrics_app = make_asgi_app()

app.mount("/metrics", metrics_app)

REQUEST_COUNTER = Counter(
    "app_request_total",
    "Total number of requests",
    ["endpoint"],
)

API = WheatherApi() 

class CityForm(BaseModel):
    lat: float
    lon: float
    country: str
    
    
class WeatherForm(BaseModel):
    name: str
    weather: list
    temp: float
    feels_like: float
    wind_speed: float
    

@app.get("/coord", response_model=CityForm, description='Get city coordinates by name.')
async def get_city_data(city: str):
    REQUEST_COUNTER.labels(endpoint="/coord").inc()
    try:
        c = await API.get_current_coords_by_city(city)
    except:
        raise HTTPException(status_code=404, detail="City not found")
    
    return { "lat" : c.get("lat"),
             "lon": c.get("lon"),
             "country":c.get("country") }
    

@app.get("/weather", response_model = WeatherForm, description='Get wheather data by coordinates.')
async def get_weather_by_coord(lat: float, lon: float):
    REQUEST_COUNTER.labels(endpoint="/weather").inc()
    
    try:
        w = await API.get_current_weather_by_city(lat, lon)
        
        return {
            "name": w.get("name"),
            "weather": w.get("weather"),
            "temp": w.get("main").get("temp"),
            "feels_like": w.get("main").get("feels_like"),
            "wind_speed": w.get("wind").get("speed"),
        }
        
    except:
        raise HTTPException(status_code=404, detail = "Data not found")
    
    
    
@app.get('/city', description='Get city weather data.')
async def get_city_weather_data(city: str):
    REQUEST_COUNTER.labels(endpoint="/city").inc()
    try:
        c = await API.get_current_coords_by_city(city)
    except:
        raise HTTPException(status_code=404, detail="City not found")
    
    try:
        lat = c.get('lat')
        lon = c.get('lon')
        w = await API.get_current_weather_by_city(lat, lon)

        return {
            "name": w.get("name"),
            "weather": w.get("weather"),
            "temp": w.get("main").get("temp"),
            "feels_like": w.get("main").get("feels_like"),
            "wind_speed": w.get("wind").get("speed"),
        }
    
    except:
        raise HTTPException(status_code=404, detail = "Data not found")
    
    
    
