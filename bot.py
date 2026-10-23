import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from database import AsyncSessionLocal
from models import User
from sqlalchemy import select
from services.lucxui_api import create_lucxui_user

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎁 دریافت کانفیگ تست (500MB)", callback_data="trial")],
        [InlineKeyboardButton("🛒 خرید کانفیگ", callback_data="buy")],
    ]
    await update.message.reply_text("🦁 به ربات **میو پاسارگارد** خوش آمدید!\n\nاز دکمه‌های زیر استفاده کنید:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def trial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    tg_id = query.from_user.id
    
    async with AsyncSessionLocal() as session:
        # چک کردن اینکه کاربر قبلا تست نگرفته باشه
        result = await session.execute(select(User).where(User.telegram_id == tg_id))
        if result.scalars().first():
            await query.edit_message_text("❌ شما قبلاً کانفیگ تست دریافت کرده‌اید!")
            return
            
        await query.edit_message_text("⏳ در حال ساخت کانفیگ...")
        
        # ساخت کانفیگ 500 مگابایتی 2 روزه
        sub_url = create_lucxui_user(f"trial_{tg_id}", 0.5, 2)
        
        if sub_url:
            new_user = User(telegram_id=tg_id, panel_type="lucxui", subscription_url=sub_url)
            session.add(new_user)
            await session.commit()
            await query.edit_message_text(f"✅ کانفیگ تست شما آماده شد:\n\n`{sub_url}`\n\nلینک را کپی و در اپلیکیشن خود وارد کنید.", parse_mode="Markdown")
        else:
            await query.edit_message_text("⚠️ خطا در ارتباط با سرور. لطفاً بعداً تلاش کنید.")

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🛒 برای خرید کانفیگ به ادمین پیام دهید:\n@YourAdminUsername")

def setup_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(trial, pattern="^trial$"))
    application.add_handler(CallbackQueryHandler(buy, pattern="^buy$"))
    return application
