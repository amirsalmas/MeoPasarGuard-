import os
import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import delete, select  # <--- select اینجا اضافه شد
from database import engine, Base, AsyncSessionLocal
from models import User
from bot import setup_bot

# تسک پس‌زمینه برای حذف منقضی‌ها
async def cleanup_task(bot_app):
    while True:
        await asyncio.sleep(60) # هر 1 دقیقه
        try:
            async with AsyncSessionLocal() as session:
                now = datetime.now(timezone.utc)
                # پیدا کردن کاربرانی که تاریخ انقضاشون گذشته
                result = await session.execute(select(User).where(User.expire_at < now))
                expired_users = result.scalars().all()
                for u in expired_users:
                    await session.delete(u)
                    try:
                        await bot_app.bot.send_message(
                            chat_id=u.telegram_id, 
                            text="⚠️ حجم یا زمان کانفیگ شما به پایان رسید و از سیستم حذف شد."
                        )
                    except Exception:
                        pass
                await session.commit()
        except Exception as e:
            print(f"Cleanup Error: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. ساخت دیتابیس
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # 2. روشن کردن ربات تلگرام به روش استاندارد Async
    bot_app = setup_bot()
    await bot_app.initialize()
    await bot_app.start()
    await bot_app.updater.start_polling()
    
    # 3. اجرای تسک حذف خودکار
    asyncio.create_task(cleanup_task(bot_app))
    
    yield
    
    # خاموش کردن ربات موقع ری‌استارت
    await bot_app.updater.stop()
    await bot_app.stop()
    await bot_app.shutdown()

app = FastAPI(lifespan=lifespan)

# سرو کردن فایل‌های استاتیک
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index():
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>فایل index.html پیدا نشد!</h1>"

@app.get("/api/status")
async def status():
    return {"status": "online", "panel": "Meo PasarGuard"}
