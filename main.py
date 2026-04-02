import asyncio
import random
import os
from telegram import Bot
from openai import OpenAI

# ====== الإعدادات ======
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

used_posts = set()

# ====== توليد منشور ======
def generate_post():
    prompt = """
اكتب عبارة قصيرة جداً (سطر واحد فقط) بأسلوب ديني محفز للنشر على تيليجرام.
الشروط:
- قصيرة (أقل من 15 كلمة)
- مؤثرة وقابلة للانتشار
- بدون إيموجي
- بدون شرح
- عربية فصحى بسيطة
أمثلة:
"لا تيأس، فالله يفتح أبواباً لم تتخيلها."
"كل تأخير فيه حكمة… ثق بالله."
"""

    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt,
        max_output_tokens=60,
    )

    text = response.output[0].content[0].text.strip()
    return text

# ====== إرسال منشور ======
async def send_post():
    for _ in range(5):  # محاولة منع التكرار
        post = generate_post()
        if post not in used_posts:
            used_posts.add(post)
            await bot.send_message(chat_id=CHANNEL_ID, text=post)
            print("Posted:", post)
            return

# ====== النظام الأساسي ======
async def main():
    while True:
        print("🚀 نشر 3 منشورات...")

        for i in range(3):
            await send_post()
            await asyncio.sleep(10)  # 10 ثواني بين كل منشور

        print("⏳ انتظار 3 ساعات...")
        await asyncio.sleep(3 * 60 * 60)

# ====== تشغيل ======
if __name__ == "__main__":
    asyncio.run(main())
