import aiohttp

from app.core.config import settings
from app.models.transport_enum import TransportEnum
from app.schemas.route import Route
from app.schemas.coordinates import Coordinates


async def get_route_info(source: Coordinates, target: Coordinates, transport: TransportEnum) -> tuple[Route, bool]:
    count_try = 2
    bad_request_status = False
    match transport:
        case TransportEnum.car:
            body = {
                'points': [
                    {
                        'type': "stop",
                        'lon': float(source.longitude),
                        'lat': float(source.latitude)
                    },
                    {
                        'type': "stop",
                        'lon': float(target.longitude),
                        'lat': float(target.latitude)
                    }
                ],
                'route_mode': 'fastest',
                'traffic_mode': 'statistics',
                'transport': 'driving',
                'output': 'summary'
            }
            url = f'http://routing.api.2gis.com/routing/7.0.0/global?key={settings.double_gis_key}'
            async with aiohttp.ClientSession() as session:
                for i in range(count_try):
                    async with session.post(url=url, json=body) as response:
                        status = response.status
                        resp = await response.json()
                    if status == 200:
                        result = resp['result'][0]
                        duration = result['duration']
                        distance = result['length']
                        return Route(distance=distance, duration=duration), bad_request_status
                bad_request_status = True
                return Route(distance=0, duration=0), bad_request_status

            
        case TransportEnum.bus:
            body = {
                'source': {
                    'point': {
                        'lat': float(source.latitude),
                        'lon': float(source.longitude)
                    }
                },
                'target': {
                    'point': {
                        'lat': float(target.latitude),
                        'lon': float(target.longitude)
                    }
                },
                'transport': ['bus'],
                'max_result_count': 1
            }
            url = f'https://routing.api.2gis.com/public_transport/2.0?key={settings.double_gis_key}'
            async with aiohttp.ClientSession() as session:
                for i in range(count_try):
                    async with session.post(url=url, json=body) as response:
                        status = response.status
                        resp = await response.json()
                    if status == 200:
                        result = dict(resp[0])
                        duration = result['total_duration']
                        distance = result['total_distance']
                        return Route(distance=distance, duration=duration), bad_request_status
                bad_request_status = True
                return Route(distance=0, duration=0), bad_request_status

        case TransportEnum.subway:
            body = {
                'source': {
                    'point': {
                        'lat': float(source.latitude),
                        'lon': float(source.longitude)
                    }
                },
                'target': {
                    'point': {
                        'lat': float(target.latitude),
                        'lon': float(target.longitude)
                    }
                },
                'transport': ['metro'],
                'max_result_count': 1
            }
            url = f'https://routing.api.2gis.com/public_transport/2.0?key={settings.double_gis_key}'
            async with aiohttp.ClientSession() as session:
                for i in range(count_try):
                    async with session.post(url=url, json=body) as response:
                        status = response.status
                        resp = await response.json()
                    if status == 200:
                        result = dict(resp[0])
                        duration = result['total_duration']
                        distance = result['total_distance']
                        return Route(distance=distance, duration=duration), bad_request_status
                bad_request_status = True
                return Route(distance=0, duration=0), bad_request_status

        case TransportEnum.plane:
            return Route(distance=0, duration=0), bad_request_status
        case TransportEnum.train:
            return Route(distance=0, duration=0), bad_request_status
