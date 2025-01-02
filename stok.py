import requests
from bs4 import BeautifulSoup
import time
import asyncio
from telegram import Bot

# Telegram bot token ve chat ID'leri
TELEGRAM_BOT_TOKEN = ""
CHAT_IDS = [""] 

# URL ve kontrol edilecek beden
PRODUCT_URL = "https://www.zara.com/tr/tr/yunlu-oversize-kaban-p03046345.html?v1=388904997&utm_campaign=productShare&utm_medium=mobile_sharing_iOS&utm_source=red_social_movil"
SIZE_TO_CHECK = "S"

# Telegram bot ile mesaj gönderme fonksiyonu
async def send_telegram_notification(message):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    for chat_id in CHAT_IDS:
        await bot.send_message(chat_id=chat_id, text=message)

# Stok kontrol fonksiyonu
def check_stock():
    try:
        
        response = requests.get(PRODUCT_URL, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        size_element = soup.find("li", class_="size-selector-sizes__size")
        if size_element:
            size_label = size_element.find("div", class_="size-selector-sizes-size__label", string=SIZE_TO_CHECK)
            if size_label and "disabled" not in size_element.get("class", []):
                return True  # Beden stokta
        return False  # Beden stokta değil

    except Exception as e:
        print(f"Hata oluştu: {e}")
        return False

async def main():
    print("Stok kontrol sistemi başlatıldı...")
    while True:
        if check_stock():
            await send_telegram_notification(f"{SIZE_TO_CHECK} bedeni stokta! Hemen al: {PRODUCT_URL}")
            break 
        else:
            await send_telegram_notification(f"{SIZE_TO_CHECK} bedeni stokta değil. Tekrar kontrol ediliyor...")
            print("Stok yok, tekrar kontrol ediliyor...")
        await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(main())
