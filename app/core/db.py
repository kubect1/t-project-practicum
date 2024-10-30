from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import JSON
from typing import Any

from app.core.config import settings

class Base(DeclarativeBase):
    type_annotation_map = {
        dict[Any, Any]: JSON
    }

engine = create_async_engine(settings.database_url, echo=True)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
