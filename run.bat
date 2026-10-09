@echo off
chcp 65001 > nul
title Telegram Bot Runner (24/7 Avto-qayta tiklanish)
echo ===================================================
echo 🤖 TELEGRAM BOT ISHGA TUSHIRILMOQDA (24/7 REJIM)
echo ===================================================

:loop
python bot.py
echo.
echo ⚠️ Bot to'xtadi yoki internet uzildi. 3 soniyadan so'ng qayta ishga tushiriladi...
timeout /t 3 > nul
goto loop
