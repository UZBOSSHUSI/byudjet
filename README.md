# Telegram Ovoz Berish Boti

Ushbu Telegram bot foydalanuvchidan ism so'rab, "🗳 Ovoz berish" tugmasini ko'rsatadi, telefon raqami va kelgan tasdiqlash kodini qabul qilib, *"✅ Ovoz o'tdi!"* javobini beradi.

## 🚀 Botni Ishga Tushirish Yo'riqnomasi

### 1. Kerakli kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 2. `.env` Faylini Tekshirish
`.env` faylida sizning Telegram Bot tokeningiz joylashgan:
```env
BOT_TOKEN=your_bot_token_here
```

### 3. Oddiy Ishga Tushirish
Terminal yoki konsolda quyidagi buyruqni bosing:
```bash
python bot.py
```

---

## 🌐 Noutbuk O'chiq / Yopiq Bo'lsa Ham Bot 100% Ishlashi Uchun (Bepul Serverga Joylash)

Agarda siz noutbukingizni o'chirib qo'ysangiz ham Telegram'da `/start` yozganda bot 100% javob berishi kerak bo'lsa, botni **Bepul Server (Cloud Hosting)** ga joylash kerak:

### 1-usul: Render.com (Tavsiya etiladi - Tekin 24/7 Server)
1. Kodni GitHub akkauntingizga yuklang (push qiling).
2. [Render.com](https://render.com) saytiga kiring va akkaunt oching.
3. **"New +"** -> **"Background Worker"** tugmasini bosing.
4. GitHub dagi bot reposini ulang.
5. **Environment Variables** bo'limiga:
   - Key: `BOT_TOKEN`
   - Value: `sizning_bot_tokeningiz`
6. **"Create Background Worker"** tugmasini bosing. Render botni 24/7 bepul yurgizib beradi!

---

## 💻 Kompyuteringizda (Noutbuk Ochiq Bo'lganda) 24/7 Yurgizish

Bot kodi ichida uzluksiz avto-qayta ulanish (auto-reconnect) mavjud.

- **`run.bat` orqali:** Fayl ustiga 2 marta bosing. Bot to'xtab qolsa ham avtomatik qayta ishga tushadi.
- **`autostart.py` orqali:**
  ```bash
  python autostart.py
  ```

---

## 📱 Bot Boshqaruv ketma-ketligi

1. Foydalanuvchi Telegram'da `/start` tugmasini bosadi.
2. Bot: `"Assalomu alaykum! Ismingizni kiriting:"` deydi.
3. Foydalanuvchi ismini kiritadi (Masalan: *Ali*).
4. Bot: `"Rahmat, Ali! Endi pastdagi '🗳 Ovoz berish' tugmasini bosing:"` deydi.
5. Foydalanuvchi **'🗳 Ovoz berish'** tugmasini bosadi.
6. Bot telefon raqam so'raydi. Foydalanuvchi **'📱 Telefon raqamni yuborish'** tugmasi yoki matn orqali telefon raqam yuboradi.
7. Bot kelgan tasdiqlash kodini so'raydi.
8. Kod kiritilganda bot **"✅ Ovoz o'tdi!"** deb javob beradi va ma'lumotlarni SQLite bazasiga saqlaydi.
