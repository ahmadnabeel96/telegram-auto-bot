import time
import random
import asyncio
from datetime import datetime
from telegram import Bot
from openai import OpenAI
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

def get_prompt():
    hour = datetime.now().hour

    if 5 <= hour < 17:
        prompts = [
            "اكتب ذكر صباحي جميل من سطرين مع ايموجي",
            "اكتب دعاء صباحي قصير ومريح",
            "اكتب عبارة اسلامية صباحية هادئة"
        ]
    else:
        prompts = [
            "اكتب دعاء مسائي مؤثر من سطرين",
            "اكتب ذكر مسائي جميل",
            "اكتب عبارة اسلامية مريحة للمساء"
        ]

    return random.choice(prompts)

def generate_text():
    prompt = get_prompt()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

async def post():
    text = generate_text()
    await bot.send_message(chat_id=CHANNEL_ID, text=text)
    print("✅ Posted:", text)

async def main_loop():
    while True:
        await post()
        await asyncio.sleep(7200)  # كل 2 ساعات

asyncio.run(main_loop())
