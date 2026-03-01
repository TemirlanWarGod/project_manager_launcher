from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from datetime import datetime
import keyboards as kb
import database as db

router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    username = message.from_user.username or "no_username"
    
    # Регистрация пользователя
    is_new = db.add_user(user_id, username)
    
    welcome_text = "Добро пожаловать!" if is_new else "С возвращением!"
    
    await message.answer(
        f"{welcome_text}\n\nВыберите действие:",
        reply_markup=kb.main_keyboard()
    )

@router.message(F.text == "📱 Добавить номер")
async def add_number(message: Message):
    """Добавление номера"""
    await message.answer(
        "Введите номер телефона в формате +7XXXXXXXXXX:",
        reply_markup=kb.close_keyboard()
    )

@router.message(F.text.regexp(r'^\+7\d{10}$'))
async def process_number(message: Message):
    """Обработка введенного номера"""
    phone = message.text.strip()
    user_id = message.from_user.id
    username = message.from_user.username or "no_username"
    
    # Сохраняем номер
    db.add_number(user_id, username, phone)
    
    await message.answer(
        f"✅ Номер {phone} успешно добавлен!",
        reply_markup=kb.main_keyboard()
    )

@router.message(F.text == "📋 Мои номера")
async def show_numbers(message: Message):
    """Показать номера пользователя"""
    user_id = message.from_user.id
    numbers = db.get_user_numbers(user_id)
    
    if not numbers:
        await message.answer("У вас пока нет добавленных номеров.")
        return
    
    text = "📋 Ваши номера:\n\n"
    for i, num in enumerate(numbers, 1):
        date = datetime.fromisoformat(num['added_at']).strftime("%d.%m.%Y %H:%M")
        text += f"{i}. {num['phone']}\n   Добавлен: {date}\n"
    
    await message.answer(text)

@router.message(F.text == "👤 Профиль")
async def show_profile(message: Message):
    """Показать профиль пользователя"""
    user_id = str(message.from_user.id)
    users = db.load_users()
    
    if user_id in users:
        user_data = users[user_id]
        reg_date = datetime.fromisoformat(user_data['registered_at']).strftime("%d.%m.%Y")
        
        numbers = db.get_user_numbers(int(user_id))
        
        text = f"""
👤 Ваш профиль:
        
🆔 ID: {user_id}
📱 Username: @{user_data['username']}
📅 Зарегистрирован: {reg_date}
🔢 Всего номеров: {len(numbers)}
        """
        await message.answer(text)
    else:
        await message.answer("Профиль не найден. Нажмите /start")

@router.callback_query(F.data == "close")
async def close_callback(callback: CallbackQuery):
    """Закрытие сообщения"""
    await callback.message.delete()
    await callback.answer()