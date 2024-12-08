import aiohttp

from app.schemas.trip import TripBase
from app.core.config import settings
from app.models.transport_enum import TransportEnum


def get_route_info(trip: TripBase) -> tuple[int, int] | tuple[None, None]:
    """
    Return total_distance in meters and total_duration in seconds
    """
    duration = None
    distance = None
    match trip.transport_type:
        case TransportEnum.car:
            body = {
                'points': [
                    {
                        'type': "stop",
                        'lon': trip.from_place.longitude,
                        'lat': trip.from_place.latitude
                    },
                    {
                        'type': "stop",
                        'lon': trip.to_place.longitude,
                        'lat': trip.to_place.latitude
                    }
                ],
                'route_mode': 'fastest',
                'traffic_mode': 'statistics',
                'transport': 'driving',
                'output': 'summary'
            }
            url = f'http://routing.api.2gis.com/routing/7.0.0/global?key={settings.double_gis_key}'
            async with aiohttp.ClientSession() as session:
                async with session.post(url=url, body=body) as response:
                    status = response.status
                    resp = response.json()
            if status == 200:
                result = dict(resp['result'])
                duration = result['duration']
                distance = result['length']

        case TransportEnum.bus:
            body = {
                'source': {
                    'point': {
                        'lat': trip.from_place.latitude,
                        'lon': trip.from_place.longitude
                    }
                },
                'target': {
                    'point': {
                        'lat': trip.to_place.latitude,
                        'lon': trip.to_place.longitude
                    }
                },
                'transport': 'bus',
                'max_result_count': 1
            }
            url = f'https://routing.api.2gis.com/public_transport/2.0?key={settings.double_gis_key}'
            async with aiohttp.ClientSession() as session:
                async with session.post(url=url, body=body) as response:
                    status = response.status
                    resp = response.json()
            if status == 200:
                result = dict(resp[0])
                duration = result['total_duration']
                distance = result['total_distance']

        case TransportEnum.subway:
            body = {
                'source': {
                    'point': {
                        'lat': trip.from_place.latitude,
                        'lon': trip.from_place.longitude
                    }
                },
                'target': {
                    'point': {
                        'lat': trip.to_place.latitude,
                        'lon': trip.to_place.longitude
                    }
                },
                'transport': 'metro',
                'max_result_count': 1
            }
            url = f'https://routing.api.2gis.com/public_transport/2.0?key={settings.double_gis_key}'
            async with aiohttp.ClientSession() as session:
                async with session.post(url=url, body=body) as response:
                    status = response.status
                    resp = response.json()
            if status == 200:
                result = dict(resp[0])
                duration = result['total_duration']
                distance = result['total_distance']
        case TransportEnum.plane:
            pass
        case TransportEnum.train:
            pass
    return distance, duration