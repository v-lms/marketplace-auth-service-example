import asyncio
import sys
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from src.infrastructure.persistence.models import Base
from src.settings import Settings

# 1. КРИТИЧЕСКИЙ ФИКС ДЛЯ WINDOWS + PYTHON 3.13
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

settings = Settings()
target_metadata = Base.metadata

def do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    # 2. ПРИНУДИТЕЛЬНО ПРАВИМ URL (игнорируем localhost и включаем ssl=disable)
    url = settings.database_url.replace("localhost", "127.0.0.1")
    if "ssl=" not in url:
        url += "?ssl=disable" if "?" not in url else "&ssl=disable"

    print(f"\n[ALEMBIC] Connecting to: {url}\n")

    connectable = create_async_engine(
        url,
        poolclass=pool.NullPool,
    )

    try:
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)
    except Exception as e:
        print(f"\n[FATAL ERROR]: {e}")
        raise
    finally:
        await connectable.dispose()

if context.is_offline_mode():
    # Для оффлайн режима тоже используем 127.0.0.1
    url = settings.database_url.replace("localhost", "127.0.0.1")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()
else:
    asyncio.run(run_migrations_online())