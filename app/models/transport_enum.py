from enum import Enum


class TransportEnum(str, Enum):
    subway: str = '1'
    bus: str = '2'
    car: str = '3'
    train: str = '4'
    plane: str = '5'