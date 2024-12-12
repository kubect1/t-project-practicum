import aiohttp

from app.core.config import settings
from app.models.transport_enum import TransportEnum
from app.schemas.route import Route
from app.schemas.coordinates import Coordinates


async def get_route_info(source: Coordinates, target: Coordinates, transport: TransportEnum) -> Route:
    duration = 0
    distance = 0
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
                async with session.post(url=url, json=body) as response:
                    status = response.status
                    resp = await response.json()
            if status == 200:
                result = resp['result'][0]
                duration = result['duration']
                distance = result['length']
            else:
                return None
            
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
                async with session.post(url=url, json=body) as response:
                    status = response.status
                    resp = await response.json()
            if status == 200:
                result = dict(resp[0])
                duration = result['total_duration']
                distance = result['total_distance']
            else:
                return None

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
                async with session.post(url=url, json=body) as response:
                    status = response.status
                    resp = await response.json()
            if status == 200:
                result = dict(resp[0])
                duration = result['total_duration']
                distance = result['total_distance']
            else:
                return None

        case TransportEnum.plane:
            pass
        case TransportEnum.train:
            pass
    return Route(distance=distance, duration=duration)