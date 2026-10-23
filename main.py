import os
import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import delete
from database import engine, Base, AsyncSessionLocal
from models import User
from bot import setup_bot

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. ساخت دیتابیس
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # 2. روشن کردن ربات تلگرام
    bot_app = setup_bot()
    bot_task = asyncio.create_task(bot_app.run_polling())
    
    # 3. تسک پس‌زمینه برای حذف منقضی‌ها
    async def cleanup_task():
        while True:
            await asyncio.sleep(60) # هر 1 دقیقه
            async with AsyncSessionLocal() as session:
                now = datetime.now(timezone.utc)
                result = await session.execute(select(User).where(User.expire_at < now))
                expired_users = result.scalars().all()
                for u in expired_users:
                    await session.delete(u)
                    try:
                        await bot_app.bot.send_message(chat_id=u.telegram_id, text="⚠️ حجم یا زمان کانفیگ شما به پایان رسید و از سیستم حذف شد.")
                    except: pass
                await session.commit()
                
    asyncio.create_task(cleanup_task())
    yield
    bot_task.cancel()

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/status")
async def status():
    return {"status": "online", "panel": "Meo PasarGuard"}
