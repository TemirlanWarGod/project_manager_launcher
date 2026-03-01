import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import router
import database as db

async def main():
    """Основная функция"""
    # Инициализация БД
    db.ensure_files()
    
    # Создание бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Подключение роутеров
    dp.include_router(router)
    
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())