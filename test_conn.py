import asyncio
import asyncpg

async def test():
    try:
        # Пытаемся подключиться напрямую через asyncpg
        conn = await asyncpg.connect(
            "postgresql://postgres:postgres@127.0.0.1:5433/auth_db",
            ssl=False  # Явно выключаем SSL
        )
        print("✅ Успешное подключение напрямую через asyncpg!")
        await conn.close()
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

asyncio.run(test())