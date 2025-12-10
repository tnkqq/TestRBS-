import aiohttp
from config import settings
from fastapi import HTTPException

class WheatherApi:
    
    @staticmethod
    async def get_current_weather_by_city(lat: float, lon: float) -> dict:
        async with aiohttp.ClientSession(settings.BaseUrl) as session:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': settings.WheatherToken,
                'units': 'metric',
            }
            response = await session.get( settings.WheatherPrefix, params = params )
        # print(response.url, response.status)
        try:
            resp = await response.json()
        except:
            raise HTTPException(404, detail='Wrong coords: {lat} : {lon}')
        return resp
    
    
    @staticmethod
    async def get_current_coords_by_city(city: str):
        async with aiohttp.ClientSession(settings.BaseUrl) as session:
            params = {
                'q': city,
                'appid': settings.WheatherToken,
                
            }
            response  = await session.get(settings.GeoPrefix,params=params)
        try:
            resp = await response.json()
            return resp[0]
        except:
            raise HTTPException(404, detail='Not found api city:{city}')

    