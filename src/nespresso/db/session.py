from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from nespresso.core.configs.env_reader import settings

engine = create_async_engine(
    settings.POSTGRES_DSN.get_secret_value(),
    echo=False,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
