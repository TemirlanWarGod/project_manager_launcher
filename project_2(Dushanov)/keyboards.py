from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_keyboard():
    """Основная клавиатура"""
    button1 = KeyboardButton(text="📱 Добавить номер")
    button2 = KeyboardButton(text="📋 Мои номера")
    button3 = KeyboardButton(text="👤 Профиль")
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [button1],
            [button2, button3]
        ],
        resize_keyboard=True
    )
    return keyboard

def close_keyboard():
    """Кнопка закрытия"""
    button = InlineKeyboardButton(text="❌ Закрыть", callback_data="close")
    return InlineKeyboardMarkup(inline_keyboard=[[button]])