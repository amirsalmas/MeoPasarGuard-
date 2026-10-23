import os
import requests
import json
from datetime import datetime, timedelta

LUCXUI_URL = os.getenv("LUCXUI_URL", "")
LUCXUI_USER = os.getenv("LUCXUI_USER", "admin")
LUCXUI_PASS = os.getenv("LUCXUI_PASS", "admin")
LUCXUI_INBOUND_ID = int(os.getenv("LUCXUI_INBOUND_ID", "1"))

def create_lucxui_user(username: str, data_gb: int, days: int):
    if not LUCXUI_URL:
        # اگر پنل ست نشده باشد، یک کانفیگ دمو برمی‌گرداند تا ربات خطا ندهد
        return f"vless://demo-{username}@demo.server:443?type=ws#Demo-{username}"
        
    try:
        # 1. Login
        login_res = requests.post(f"{LUCXUI_URL}/login", json={"username": LUCXUI_USER, "password": LUCXUI_PASS}, timeout=10)
        token = login_res.json().get("obj")
        if not token: return None

        # 2. Create Client
        expire_time = int((datetime.now() + timedelta(days=days)).timestamp() * 1000) if days > 0 else 0
        total_bytes = data_gb * 1024 * 1024 * 1024 if data_gb > 0 else 0
        
        payload = {
            "id": LUCXUI_INBOUND_ID,
            "settings": json.dumps({"clients": [{"email": username, "totalGB": total_bytes, "expiryTime": expire_time, "enable": True, "subId": username}]})
        }
        headers = {"Authorization": f"Bearer {token}"}
        add_res = requests.post(f"{LUCXUI_URL}/panel/api/inbounds/addClient", json=payload, headers=headers, timeout=10)
        
        if add_res.json().get("success"):
            return f"{LUCXUI_URL}/sub/{username}"
        return None
    except Exception as e:
        print(f"LucX-UI Error: {e}")
        return None
