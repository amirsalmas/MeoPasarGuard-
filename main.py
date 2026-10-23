import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>MEOV2RAY | میو وی تو ری</title>
    <style>
        body { background-image: url('/static/bg.jpg'); background-color: #0f0f13; color: #d4af37; font-family: Tahoma, sans-serif; text-align: center; padding-top: 40px; background-size: cover; background-blend-mode: overlay; margin: 0; min-height: 100vh; padding-bottom: 50px; }
        .logo { width: 120px; height: 120px; border: 2px solid #d4af37; border-radius: 50%; margin: 0 auto 20px; background-image: url('/static/logo.png'); background-size: contain; background-repeat: no-repeat; background-position: center; background-color: #1a1a2e; box-shadow: 0 0 20px rgba(212, 175, 55, 0.5); }
        h1 { color: #d4af37; text-shadow: 0 0 15px rgba(212, 175, 55, 0.6); margin-bottom: 5px; }
        .subtitle { color: #aaa; font-size: 14px; margin-bottom: 30px; }
        
        .box { background: rgba(26, 26, 46, 0.9); border: 1px solid #d4af37; padding: 20px; border-radius: 15px; width: 90%; max-width: 600px; margin: 20px auto; box-shadow: 0 0 20px rgba(0,0,0,0.8); }
        
        .grid { display: grid; grid-template-columns: 1fr; gap: 15px; margin-top: 20px; }
        .card { background: #151525; border: 1px solid #333; border-radius: 10px; padding: 15px; text-align: right; transition: 0.3s; }
        .card:hover { border-color: #d4af37; transform: scale(1.02); }
        .card a { color: #d4af37; text-decoration: none; font-weight: bold; font-size: 16px; display: block; margin-bottom: 5px; }
        .card p { color: #ccc; font-size: 13px; margin: 0; }
        
        .btn { background-color: #d4af37; color: #1a1a2e; padding: 12px 25px; border-radius: 8px; text-decoration: none; font-weight: bold; display: inline-block; margin-top: 15px; cursor: pointer; border: none; font-size: 16px; }
        .btn:hover { background-color: #b8962e; }
        
        .music-player { margin-top: 20px; color: #888; font-size: 14px; }
        .footer { margin-top: 40px; color: #555; font-size: 12px; }
    </style>
</head>
<body>
    <div class="logo"></div>
    <h1>𝐌𝐄𝐎𝐕𝟐𝐑𝐀𝐘 | میو وی تو ری</h1>
    <div class="subtitle">⚜️ یک نام، چندین ابزار، یک دنیای متفاوت ⚜️</div>

    <div class="box" style="text-align: center;">
        <h3 style="color: #d4af37; margin-top:0;">🌐 با کانفیگ‌های ما، به‌راحتی وصل شو! 🚀</h3>
        <p style="color: #ccc; font-size: 14px;">به دنیای میو وی تو ری خوش اومدی؛ جایی برای دسترسی به کانفیگ‌ها، ابزارهای کاربردی و سرویس‌های تلگرامی! 🖤</p>
        <button onclick="getConfig()" class="btn">دریافت کانفیگ تست</button>
    </div>

    <div class="box">
        <h3 style="color: #d4af37; text-align: center; margin-top: 0;">♛ خدمات و ربات‌های ما ♛</h3>
        <div class="grid">
            <div class="card">
                <a href="https://t.me/meov2ray" target="_blank">🌐 ۱ | کانال کانفیگ‌های ما</a>
                <p>⚡ برای اتصال، کانفیگ‌های رایگان و پرمیوم ما رو بررسی کن.</p>
            </div>
            <div class="card">
                <a href="https://t.me/meodeploybot" target="_blank">🤖 ۲ | ربات دیپلوی پنل</a>
                <p>⚙️ ابزار حرفه‌ای دیپلوی و راه‌اندازی انواع پنل‌ها.</p>
            </div>
            <div class="card">
                <a href="https://t.me/Fdstucshbot" target="_blank">🎭 ۳ | ربات دهات مافیا</a>
                <p>🃏 وارد بازی شو و قدرت استراتژی خودت رو نشون بده!</p>
            </div>
            <div class="card">
                <a href="https://t.me/soefsiuseubot" target="_blank">📩 ۴ | ربات ایمیل موقت</a>
                <p>✉️ ابزاری برای ساخت ایمیل موقت و دریافت پیام‌ها.</p>
            </div>
            <div class="card" style="border-color: #d4af37;">
                <a href="#" style="cursor: not-allowed; color: #888;">🛒 ۵ | ربات خرید و فروش کانفیگ</a>
                <p style="color: #888;">⏳ به‌زودی... سرویس جدید در راهه! 🔥</p>
            </div>
        </div>
    </div>

    <div class="box" style="text-align: center; border-radius: 50px;">
        <h4 style="color: #d4af37; margin-top: 0;">👑 چرا MEOV2RAY؟</h4>
        <p style="color: #ccc; font-size: 13px;">⚡ دسترسی آسان | 🛠️ ابزارهای متنوع | 📱 سرویس‌های کاربردی تلگرامی</p>
        <p style="color: #aaa; font-size: 12px; margin-top: 10px;">🖤 ما تازه شروع کردیم؛ منتظر قابلیت‌های جدید باش!</p>
    </div>

    <div class="music-player">
        <span>🎵 در حال پخش موزیک...</span>
        <button onclick="toggleMusic()" style="background:none; border:none; color:#d4af37; cursor:pointer; font-size:20px;">⏸️</button>
    </div>

    <audio id="bg-music" autoplay loop>
        <source src="/static/music-panel.mp3" type="audio/mpeg">
    </audio>

    <div class="footer">Designed with 🦁 for MeoPasarGuard</div>

    <script>
        function getConfig() {
            alert("به زودی...\\n\\nبرای دریافت کانفیگ به کانال ما مراجعه کنید!");
        }
        const player = document.getElementById('bg-music');
        function toggleMusic() { if (player.paused) { player.play(); } else { player.pause(); } }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_CONTENT

@app.get("/api/status")
async def status():
    return {"status": "online", "panel": "Meo PasarGuard"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
