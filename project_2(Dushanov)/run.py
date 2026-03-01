#!/usr/bin/env python3
"""
Автозапуск Telegram бота с проверкой и установкой зависимостей
"""

import subprocess
import sys
import importlib.util
import os
import time
import asyncio

# Список необходимых библиотек
REQUIRED_LIBRARIES = [
    'aiogram',
    'aiohttp'
]

# Цвета для вывода
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_colored(text, color):
    """Вывод цветного текста"""
    print(f"{color}{text}{RESET}")

def check_library(library_name):
    """Проверка наличия библиотеки"""
    return importlib.util.find_spec(library_name) is not None

def install_library(library_name):
    """Установка библиотеки"""
    try:
        print_colored(f"📦 Установка {library_name}...", YELLOW)
        subprocess.check_call([sys.executable, "-m", "pip", "install", library_name])
        print_colored(f"✅ {library_name} успешно установлен!", GREEN)
        return True
    except subprocess.CalledProcessError as e:
        print_colored(f"❌ Ошибка при установке {library_name}: {e}", RED)
        return False

def check_and_install_libraries():
    """Проверка и установка всех необходимых библиотек"""
    print_colored("\n🔍 Проверка зависимостей...", BLUE)
    
    missing_libraries = []
    
    for lib in REQUIRED_LIBRARIES:
        if not check_library(lib):
            missing_libraries.append(lib)
            print_colored(f"⚠️  {lib} не найден", YELLOW)
        else:
            print_colored(f"✅ {lib} уже установлен", GREEN)
    
    if missing_libraries:
        print_colored(f"\n📥 Найдено {len(missing_libraries)} отсутствующих библиотек", YELLOW)
        
        for lib in missing_libraries:
            if not install_library(lib):
                return False
        
        print_colored("\n✨ Все библиотеки успешно установлены!", GREEN)
    else:
        print_colored("\n✨ Все необходимые библиотеки уже установлены!", GREEN)
    
    return True

def check_bot_token():
    """Проверка наличия токена бота"""
    try:
        # Добавляем текущую директорию в путь для импорта
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from config import BOT_TOKEN
        
        if BOT_TOKEN == "8266235882:AAFGCHpIp4_DOSjtOZx9RVovli0xHzLp_3o":
            print_colored("\n⚠️  ВНИМАНИЕ: Используется токен по умолчанию!", YELLOW)
            print_colored("   Рекомендуется заменить его на свой токен в файле config.py", YELLOW)
            response = input("   Продолжить с токеном по умолчанию? (y/n): ")
            if response.lower() != 'y':
                print_colored("❌ Запуск отменен", RED)
                return False
        
        if not BOT_TOKEN or len(BOT_TOKEN) < 10:
            print_colored("\n❌ Ошибка: Неверный формат токена в config.py", RED)
            return False
        
        return True
    except ImportError as e:
        print_colored(f"\n❌ Ошибка: Файл config.py не найден или не содержит BOT_TOKEN", RED)
        print_colored(f"   Детали: {e}", RED)
        return False
    except Exception as e:
        print_colored(f"\n❌ Ошибка при проверке токена: {e}", RED)
        return False

def create_requirements_file():
    """Создание файла requirements.txt"""
    requirements = """aiogram==2.25.1
aiohttp==3.8.5
"""
    try:
        with open('requirements.txt', 'w') as f:
            f.write(requirements)
        print_colored("✅ Файл requirements.txt создан", GREEN)
    except Exception as e:
        print_colored(f"❌ Ошибка при создании requirements.txt: {e}", RED)

def run_bot_script():
    """Запуск бота через основной скрипт"""
    try:
        print_colored("\n🚀 Запуск бота...", BLUE)
        
        # Запускаем main.py как отдельный процесс
        # Это более надежный способ, чем импорт
        result = subprocess.run([sys.executable, "main.py"])
        
        # Если процесс завершился с ошибкой
        if result.returncode != 0:
            return False
        return True
        
    except KeyboardInterrupt:
        print_colored("\n\n👋 Бот остановлен пользователем", YELLOW)
        return True
    except Exception as e:
        print_colored(f"\n❌ Ошибка при запуске бота: {e}", RED)
        return False

def run_bot_direct():
    """Прямой запуск бота (альтернативный метод)"""
    try:
        print_colored("\n🚀 Прямой запуск бота...", BLUE)
        
        # Добавляем текущую директорию в путь для импорта
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        # Импортируем необходимые модули
        import asyncio
        from aiogram import Bot, Dispatcher
        from config import BOT_TOKEN
        from handlers import router
        import database as db
        
        # Инициализация БД
        db.ensure_files()
        
        # Создание бота и диспетчера
        bot = Bot(token=BOT_TOKEN)
        dp = Dispatcher()
        
        # Подключение роутеров
        dp.include_router(router)
        
        print_colored("✅ Бот успешно запущен! Нажмите Ctrl+C для остановки.", GREEN)
        
        # Запуск бота
        asyncio.run(dp.start_polling(bot))
        
        return True
        
    except KeyboardInterrupt:
        print_colored("\n\n👋 Бот остановлен пользователем", YELLOW)
        return True
    except Exception as e:
        print_colored(f"\n❌ Ошибка при прямом запуске бота: {e}", RED)
        return False

def main():
    """Основная функция автозапуска"""
    # Очистка экрана
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print_colored("=" * 50, BLUE)
    print_colored("🚀 Telegram Bot Auto-Launcher", BLUE)
    print_colored("=" * 50, BLUE)
    
    # Создаем requirements.txt если его нет
    if not os.path.exists('requirements.txt'):
        create_requirements_file()
    
    # Проверяем и устанавливаем библиотеки
    if not check_and_install_libraries():
        print_colored("\n❌ Не удалось установить все зависимости", RED)
        sys.exit(1)
    
    # Проверяем токен бота
    if not check_bot_token():
        sys.exit(1)
    
    # Проверяем наличие всех необходимых файлов
    required_files = ['config.py', 'database.py', 'handlers.py', 'keyboards.py', 'main.py']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print_colored("\n❌ Отсутствуют необходимые файлы:", RED)
        for file in missing_files:
            print_colored(f"   - {file}", RED)
        sys.exit(1)
    
    # Запускаем бота
    print_colored("\n" + "=" * 50, GREEN)
    print_colored("✅ Все проверки пройдены успешно!", GREEN)
    print_colored("=" * 50, GREEN)
    
    # Пытаемся запустить бота разными способами
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        # Пробуем сначала прямой запуск
        print_colored(f"\n📋 Попытка запуска #{retry_count + 1}", BLUE)
        
        # Выбираем метод запуска
        if retry_count == 0:
            # Первая попытка - прямой запуск
            success = run_bot_direct()
        else:
            # Последующие попытки - запуск через subprocess
            success = run_bot_script()
        
        if success:
            break
        else:
            retry_count += 1
            if retry_count < max_retries:
                print_colored(f"\n🔄 Перезапуск через 5 секунд... (попытка {retry_count + 1}/{max_retries})", YELLOW)
                time.sleep(5)
            else:
                print_colored("\n❌ Достигнуто максимальное количество попыток перезапуска", RED)
                sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n\n👋 Программа завершена", YELLOW)
        sys.exit(0)