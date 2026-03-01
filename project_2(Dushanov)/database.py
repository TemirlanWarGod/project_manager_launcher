import json
import os
from datetime import datetime

USERS_FILE = "database/users.json"
NUMBERS_FILE = "database/numbers.json"

def ensure_files():
    """Создание файлов БД при отсутствии"""
    os.makedirs("database", exist_ok=True)
    
    for file in [USERS_FILE, NUMBERS_FILE]:
        if not os.path.exists(file):
            with open(file, 'w', encoding='utf-8') as f:
                json.dump([] if file == NUMBERS_FILE else {}, f)

def load_users():
    """Загрузка пользователей"""
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    """Сохранение пользователей"""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

def load_numbers():
    """Загрузка номеров"""
    try:
        with open(NUMBERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_numbers(numbers):
    """Сохранение номеров"""
    with open(NUMBERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(numbers, f, indent=4, ensure_ascii=False)

def add_user(user_id, username):
    """Добавление нового пользователя"""
    users = load_users()
    if str(user_id) not in users:
        users[str(user_id)] = {
            "username": username,
            "registered_at": datetime.now().isoformat()
        }
        save_users(users)
        return True
    return False

def add_number(user_id, username, phone_number):
    """Добавление нового номера"""
    numbers = load_numbers()
    numbers.append({
        "user_id": user_id,
        "username": username,
        "phone": phone_number,
        "added_at": datetime.now().isoformat()
    })
    save_numbers(numbers)

def get_user_numbers(user_id):
    """Получение номеров пользователя"""
    numbers = load_numbers()
    return [n for n in numbers if n["user_id"] == user_id]