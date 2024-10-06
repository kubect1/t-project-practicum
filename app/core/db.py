from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings


Base = declarative_base()

engine = create_async_engine(settings.database_url, echo=True)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
