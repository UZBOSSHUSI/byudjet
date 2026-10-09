import asyncio
import logging
import re
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from config import BOT_TOKEN
from database import init_db, save_vote, has_user_voted, get_votes_count, get_all_votes
from keyboards import get_vote_keyboard, get_phone_keyboard, get_main_menu_keyboard

# Logging sozlamasi
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FSM (Finite State Machine) Holatlari
class VotingState(StatesGroup):
    waiting_for_name = State()
    waiting_for_vote_click = State()
    waiting_for_phone = State()
    waiting_for_code = State()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    """Jarayonni bekor qilish"""
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
        await message.answer("❌ Jarayon bekor qilindi.", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Hozirda hech qanday faol jarayon yo'q.")

@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """/start buyrug'ini qayta ishlash"""
    await state.clear()
    user_voted = await has_user_voted(message.from_user.id)
    
    if user_voted:
        await message.answer(
            f"Assalomu alaykum, {message.from_user.first_name}!\n\n"
            "Siz allaqachon ovoz berdingiz. E'tiboringiz uchun rahmat!",
            reply_markup=get_main_menu_keyboard()
        )
        return

    await state.set_state(VotingState.waiting_for_name)
    await message.answer(
        "Assalomu alaykum! Xush kelibsiz.\n\n"
        "Ovoz berish jarayonini boshlash uchun iltimos **Ismingizni kiriting:**",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )

@dp.message(VotingState.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    """Foydalanuvchi ismini qabul qilish va Ovoz berish tugmasini ko'rsatish"""
    if not message.text:
        await message.answer("Iltimos, ismingizni matn ko'rinishida kiriting:")
        return

    name = message.text.strip()
    if len(name) < 2:
        await message.answer("Iltimos, haqiqiy ismingizni kiriting (kamida 2 ta harf):")
        return

    await state.update_data(full_name=name)
    await state.set_state(VotingState.waiting_for_vote_click)
    
    await message.answer(
        f"Rahmat, **{name}**!\n\n"
        "Endi ovoz berish uchun pastdagi **'🗳 Ovoz berish'** tugmasini bosing:",
        parse_mode="Markdown",
        reply_markup=get_vote_keyboard()
    )

@dp.message(VotingState.waiting_for_vote_click)
async def process_vote_click(message: Message, state: FSMContext):
    """'Ovoz berish' tugmasi bosilganda telefon raqam so'rash"""
    if message.text != "🗳 Ovoz berish":
        await message.answer(
            "Iltimos, ovoz berish uchun pastdagi **'🗳 Ovoz berish'** tugmasini bosing:",
            parse_mode="Markdown",
            reply_markup=get_vote_keyboard()
        )
        return

    await state.set_state(VotingState.waiting_for_phone)
    
    await message.answer(
        "Ovoz berish uchun telefon raqamingizni kiriting (masalan, +998901234567) "
        "yoki pastdagi **'📱 Telefon raqamni yuborish'** tugmasini bosing:",
        parse_mode="Markdown",
        reply_markup=get_phone_keyboard()
    )

@dp.message(VotingState.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    """Telefon raqamni qabul qilish (kontakt yoki matn sifatida)"""
    phone = None
    if message.contact:
        phone = message.contact.phone_number
        if not phone.startswith("+"):
            phone = "+" + phone
    elif message.text:
        phone = message.text.strip()
        clean_phone = re.sub(r'[^\d+]', '', phone)
        if len(clean_phone) < 7:
            await message.answer("Iltimos, to'g'ri telefon raqam kiriting (masalan, +998901234567) yoki tugmani bosing:")
            return
        phone = clean_phone
    else:
        await message.answer("Iltimos, telefon raqamingizni kiriting yoki tugma orqali yuboring:")
        return

    await state.update_data(phone_number=phone)
    await state.set_state(VotingState.waiting_for_code)

    await message.answer(
        f"Sizning telefon raqamingiz: **{phone}**\n\n"
        "Telefoningizga kelgan **tasdiqlash kodini kiriting:**",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )

@dp.message(VotingState.waiting_for_code)
async def process_code(message: Message, state: FSMContext):
    """Tasdiqlash kodini qabul qilish va ovozni saqlash"""
    if not message.text:
        await message.answer("Iltimos, kelgan tasdiqlash kodini matn shaklida kiriting:")
        return

    code = message.text.strip()
    if not code:
        await message.answer("Iltimos, kelgan tasdiqlash kodini kiriting:")
        return

    data = await state.get_data()
    full_name = data.get("full_name", message.from_user.full_name)
    phone_number = data.get("phone_number", "Noma'lum")
    username = message.from_user.username or ""

    # Bazaga saqlash
    await save_vote(
        user_id=message.from_user.id,
        username=username,
        full_name=full_name,
        phone_number=phone_number,
        verification_code=code
    )

    await state.clear()

    await message.answer(
        "✅ **Ovoz o'tdi!**\n\n"
        "Ovozingiz muvaffaqiyatli qabul qilindi. E'tiboringiz uchun rahmat!",
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard()
    )

@dp.message(F.text == "🔄 Qayta ovoz berish")
async def process_re_vote(message: Message, state: FSMContext):
    """Qayta ovoz berish buyrug'i"""
    await state.set_state(VotingState.waiting_for_name)
    await message.answer(
        "Ismingizni qaytadan kiriting:",
        reply_markup=ReplyKeyboardRemove()
    )

@dp.message(F.text == "📊 Ovozlar statistikasi")
@dp.message(Command("stats"))
async def process_stats(message: Message):
    """Ovozlar statistikasini ko'rsatish"""
    count = await get_votes_count()
    await message.answer(
        f"📊 **Baza statistikasi:**\n\n"
        f"Jami qabul qilingan ovozlar: **{count} ta**",
        parse_mode="Markdown"
    )

@dp.message(Command("admin"))
async def process_admin(message: Message):
    """Admin uchun barcha ovozlar ro'yxatini chiqarish"""
    votes = await get_all_votes()
    if not votes:
        await message.answer("Hozircha hech qanday ovoz yo'q.")
        return
    
    res = f"📋 **Barcha ovozlar ro'yxati ({len(votes)} ta):**\n\n"
    for v in votes[:20]:
        user_id, name, phone, code, voted_at = v
        res += f"👤 {name} | 📱 {phone} | 🔑 Kod: `{code}` | 🕒 {voted_at}\n"
    
    if len(votes) > 20:
        res += f"\n... va yana {len(votes) - 20} ta ovoz bor."
    
    await message.answer(res, parse_mode="Markdown")

async def main():
    logger.info("Ma'lumotlar bazasi retsializatsiya qilinmoqda...")
    await init_db()
    
    logger.info("Bot ishga tushirilmoqda (24/7 rejim)...")
    try:
        while True:
            try:
                await dp.start_polling(bot, handle_signals=False)
                break
            except (KeyboardInterrupt, SystemExit):
                logger.info("Bot foydalanuvchi tomonidan to'xtatildi.")
                break
            except Exception as e:
                logger.error(f"⚠️ Ulanishda xatolik yuz berdi: {e}. 5 soniyadan so'ng qayta ulanadi...")
                await asyncio.sleep(5)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot to'xtatildi.")

