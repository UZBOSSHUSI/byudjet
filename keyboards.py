from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_vote_keyboard() -> ReplyKeyboardMarkup:
    """Ovoz berish tugmasi"""
    kb = [
        [KeyboardButton(text="🗳 Ovoz berish")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)

def get_phone_keyboard() -> ReplyKeyboardMarkup:
    """Telefon raqam yuborish tugmasi"""
    kb = [
        [KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)

def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Ovoz berib bo'lingandan keyingi asosiy menyu"""
    kb = [
        [KeyboardButton(text="📊 Ovozlar statistikasi")],
        [KeyboardButton(text="🔄 Qayta ovoz berish")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
