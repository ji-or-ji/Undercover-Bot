import os
import asyncio
from fastapi import FastAPI, Request
import httpx
import uvicorn
from typing import List, Dict, Optional
try:
    from src.bot.login import start_bot_with_login, get_app_config
except ModuleNotFoundError:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from src.bot.login import start_bot_with_login, get_app_config

def load_config(env: str = "dev") -> Dict:
    return get_app_config(env)

config = load_config(os.getenv("APP_ENV", "dev"))
napcat_config = config.get("napcat") if isinstance(config.get("napcat"), dict) else {}
NAPCAT_API = (
    napcat_config.get("onebot_api") if napcat_config else None
    or config.get("napcat_api")
    or "http://127.0.0.1:3000"
)
KEYWORDS = config.get("keywords", ["炸群", "举报", "兄弟们"])

app = FastAPI()

async def send_group_msg(group_id: int, message: str):
    """向指定群发送消息"""
    url = f"{NAPCAT_API}/send_group_msg"
    data = {
        "group_id": group_id,
        "message": message
    }
    try:
        async with httpx.AsyncClient() as client:
            await client.post(url, json=data, timeout=5.0)
    except Exception as e:
        print(f"发送消息失败: {e}")

def process_message(data: Dict) -> Optional[str]:
    """处理消息并返回回复内容（如果需要回复）"""
    if data.get("post_type") == "message" and data.get("message_type") == "group":
        raw_message = data.get("raw_message", "")
        for kw in KEYWORDS:
            if kw in raw_message:
                return f"检测到关键词【{kw}】，已记录。"
    return None

@app.post("/onebot")
async def receive_message(request: Request):
    data = await request.json()
    reply = process_message(data)
    if reply:
        group_id = data.get("group_id")
        if group_id:
            await send_group_msg(group_id, reply)
    return {"status": "ok"}

async def main():
    if os.getenv("SKIP_LOGIN") == "1":
        return
    success = await start_bot_with_login()
    if not success:
        print("登录失败，程序退出。")
        return

    config_uvicorn = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config_uvicorn)
    await server.serve()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n程序已中断，正在退出。")
