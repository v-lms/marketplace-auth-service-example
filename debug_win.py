import asyncio
import asyncpg
import sys

async def run_test():
    print(f"1. Попытка подключения к 127.0.0.1:5433...")
    try:
        # Добавляем жесткий таймаут 5 секунд
        conn = await asyncio.wait_for(
            asyncpg.connect(
                host="127.0.0.1",
                port=5444,
                user="postgres",
                password="postgres",
                database="auth_db",
                ssl=False
            ),
            timeout=5.0
        )
        print("2. ✅ СОЕДИНЕНИЕ УСТАНОВЛЕНО!")

        version = await conn.fetchval("SELECT version();")
        print(f"3. Версия базы: {version}")

        await conn.close()
        print("4. Соединение закрыто.")

    except asyncio.TimeoutError:
        print("❌ ОШИБКА: Таймаут! База не ответила за 5 секунд. Проверьте порты в Docker.")
    except Exception as e:
        print(f"❌ ОШИБКА: {type(e).__name__}: {e}")

if __name__ == "__main__":
    print(f"--- Запуск диагностики (Python {sys.version}) ---")

    # ПРИНУДИТЕЛЬНЫЙ ФИКС ДЛЯ WINDOWS
    if sys.platform == 'win32':
        print("--- Применяю WindowsSelectorEventLoopPolicy ---")
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(run_test())
    except KeyboardInterrupt:
        print("\nТест прерван пользователем.")
    print("--- Диагностика завершена ---")
