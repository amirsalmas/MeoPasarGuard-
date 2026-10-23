import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Meo PasarGuard</title>
    <style>
        body { background-color: #0f0f13; color: #d4af37; font-family: Tahoma; text-align: center; padding-top: 50px; background-image: url('https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Persepolis_-_The_Gate_of_All_Nations.jpg/1200px-Persepolis_-_The_Gate_of_All_Nations.jpg'); background-size: cover; background-blend-mode: overlay; margin: 0; height: 100vh; }
        .logo { width: 120px; height: 120px; border: 2px solid #d4af37; border-radius: 50%; margin: 0 auto 20px; background-image: url('https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Faravahar_silver_coin.png/200px-Faravahar_silver_coin.png'); background-size: contain; background-repeat: no-repeat; background-position: center; background-color: #1a1a2e; box-shadow: 0 0 20px rgba(212, 175, 55, 0.5); }
        h1 { color: #d4af37; text-shadow: 0 0 15px rgba(212, 175, 55, 0.6); }
        .box { background: rgba(26, 26, 46, 0.9); border: 1px solid #d4af37; padding: 30px; border-radius: 15px; width: 80%; max-width: 500px; margin: 30px auto; }
        .btn { background-color: #d4af37; color: #1a1a2e; padding: 12px 25px; border-radius: 8px; text-decoration: none; font-weight: bold; display: inline-block; margin-top: 15px; cursor: pointer; border: none; }
        .music-player { margin-top: 20px; color: #888; font-size: 14px; }
    </style>
</head>
<body>
    <div class="logo"></div>
    <h1>پنل میو پاسارگارد</h1>
    <div class="box">
        <p>به پنل مدیریت خوش آمدید. (نسخه فوق سریع)</p>
        <button onclick="getConfig()" class="btn">دریافت کانفیگ تست</button>
        <div class="music-player">
            <span>🎵 در حال پخش موزیک...</span>
            <button onclick="toggleMusic()" style="background:none; border:none; color:#d4af37; cursor:pointer; font-size:20px;">⏸️</button>
        </div>
    </div>

    <audio id="bg-music" autoplay loop>
        <source src="/static/music-panel.mp3" type="audio/mpeg">
    </audio>

    <script>
        function getConfig() {
            alert("این یک کانفیگ تست است:\\n\\nvless://demo-user@meo.server:443?type=ws#Meo-Test");
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
