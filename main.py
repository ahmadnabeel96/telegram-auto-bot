import time
import random
from datetime import datetime
from telegram import Bot
from openai import OpenAI

# 🔑 حط معلوماتك هون
TELEGRAM_TOKEN = "8331609314:AAH9DF0y6lUUJTfxf8zmjT-gV34wmEP1Aw0"
CHANNEL_ID = "@anwar_aldhikr"
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# إعداد البوت
bot = Bot(token=TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

# 🧠 تحديد المحتوى حسب الوقت
def get_prompt():
    hour = datetime.now().hour

    # صباح
    if 5 <= hour < 17:
        prompts = [
            "اكتب ذكر صباحي جميل من سطرين مع ايموجي",
            "اكتب دعاء صباحي قصير ومريح مع ايموجي",
            "اكتب عبارة صباحية اسلامية هادئة من سطرين"
        ]
    # مساء
    else:
        prompts = [
            "اكتب دعاء مسائي مؤثر من سطرين مع ايموجي",
            "اكتب ذكر مسائي جميل وقصير مع ايموجي",
            "اكتب عبارة اسلامية مريحة للمساء من سطرين"
        ]

    return random.choice(prompts)

# ✨ توليد النص
def generate_text():
    prompt = get_prompt()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

# 📤 النشر
def post():
    try:
        text = generate_text()
        bot.send_message(chat_id=CHANNEL_ID, text=text)
        print("✅ تم النشر:", text)
    except Exception as e:
        print("❌ خطأ:", e)

# 🔁 تشغيل كل 3 ساعات
while True:
    post()
    time.sleep(10800)  # 3 ساعات
