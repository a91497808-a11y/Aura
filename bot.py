
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from google import genai
from google.genai import types as genai_types

# 1. BotFather'dan olgan tokeningizni yozing:
TELEGRAM_BOT_TOKEN = "8862107968:AAEqE9-yld4AayfzAkUF8e90YTHAaM6i7a4"

# 2. Google AI Studio'dan olgan API kalitingizni yozing:
GEMINI_API_KEY = "AQ.Ab8RN6I6MBXckib8-XW1QMh1Sq-LxABqmA8oJQHwYufVcZpLgQ"

client = genai.Client(api_key=GEMINI_API_KEY)
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

SYSTEM_INSTRUCTION = (
    "Sen aqlli, tezkor va matematika hamda boshqa fanlardan misollarni "
    "juda yaxshi yechadigan yordamchisan. Har qanday matematik yoki mantiqiy "
    "savolga javob berganda, avval qadam-baqadam (formulalar va izohlar bilan) "
    "tushuntirib, oxirida aniq javobni yoz."
)

@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.answer(
        "Assalomu alaykum! Men sun'iy intellekt botiman.\n"
        "Menga istalgan savolingizni yuborishingiz yoki matematika misollarini tashlashingiz mumkin!"
    )

@dp.message(F.text)
async def handle_message(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=message.text,
            config=genai_types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.3,
            ),
        )
        await message.answer(response.text)
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {e}")

async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
