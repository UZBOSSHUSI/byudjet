import subprocess
import time
import sys

def run_bot_forever():
    print("===================================================")
    print("🤖 TELEGRAM BOT 24/7 AVTO-TIKLANISH REJIMIDA")
    print("===================================================")
    
    while True:
        try:
            print("🚀 Bot ishga tushirilmoqda...")
            process = subprocess.run([sys.executable, "bot.py"])
            print(f"\n⚠️ Bot jarayoni yakunlandi (kod: {process.returncode}). 3 soniyadan so'ng qayta yuritiladi...")
        except KeyboardInterrupt:
            print("\n🛑 Bot foydalanuvchi tomonidan to'xtatildi.")
            break
        except Exception as e:
            print(f"\n❌ Xatolik yuz berdi: {e}. 5 soniyadan so'ng qayta yuritiladi...")
            time.sleep(5)
            continue
        
        time.sleep(3)

if __name__ == "__main__":
    run_bot_forever()
