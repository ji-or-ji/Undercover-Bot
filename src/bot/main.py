import os
import asyncio
import logging
import time
from fastapi import FastAPI, Request
import httpx
import uvicorn
from typing import List, Dict, Optional
try:
    from src.bot.login import start_bot_with_login, get_app_config
    from src.bot.repeater import get_repeater, create_repeater_config
except ModuleNotFoundError:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from src.bot.login import start_bot_with_login, get_app_config
    from src.bot.repeater import get_repeater, create_repeater_config
# 导入模块

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NapCatLoginManager")

# 加载配置
def load_config(env: str = "dev") -> Dict:
    return get_app_config(env)

# 加载配置
config = load_config(os.getenv("APP_ENV", "dev"))
napcat_config = config.get("napcat") if isinstance(config.get("napcat"), dict) else {}
NAPCAT_API = (
    napcat_config.get("onebot_api") if napcat_config else None
    or config.get("napcat_api")
    or "http://127.0.0.1:3000"
)

BOT_QQ: int = napcat_config.get("bot_qq", 0) if isinstance(napcat_config, dict) else config.get("bot_qq", 0)    # 机器人QQ
AT_REPLY_TEXT = "awa"    # @ 回复文本
MAX_RETRIES = 3    # 最大重试次数
RETRY_DELAY = 1.0    # 重试延迟时间

# 初始化 FastAPI 应用
app = FastAPI()

# 发送群消息
async def send_group_msg(group_id: int, message: str):
    url = f"{NAPCAT_API}/send_group_msg"    # 发送群消息 API 地址
    data = {
        "group_id": group_id,
        "message": message
    }
    last_exception = None        # 最后一次异常信息
    for attempt in range(MAX_RETRIES):     # 最大重试次数
        try:
            async with httpx.AsyncClient() as client:     # 异步 HTTP 客户端
                resp = await client.post(url, json=data, timeout=5.0)    # 发送 POST 请求发送群消息
                if resp.status_code == 200:    # 状态码为 200 时
                    return True
                if resp.status_code != 200:    # 状态码不是 200 时
                    logging.getLogger("NapCatLoginManager").warning(f"HTTP {resp.status_code}: {resp.text}")    # 记录警告日志
                    last_exception = Exception(f"HTTP {resp.status_code}: {resp.text}")    # 记录异常信息
                    continue
        except httpx.TimeoutException as e:    # 超时异常
            logging.getLogger("NapCatLoginManager").warning(f"发送消息超时 (尝试 {attempt + 1}/{MAX_RETRIES})")    # 记录警告日志
            last_exception = e    # 记录异常信息
        except Exception as e:    # 其他异常
            logging.getLogger("NapCatLoginManager").error(f"发送消息异常 (尝试 {attempt + 1}/{MAX_RETRIES}): {e}")    # 记录错误日志
            last_exception = e    # 记录异常信息
        if attempt < MAX_RETRIES - 1:    # 重试次数小于最大重试次数减一
            await asyncio.sleep(RETRY_DELAY)    # 等待重试延迟时间
    logging.getLogger("NapCatLoginManager").error(f"发送消息最终失败: {last_exception}")    # 记录错误日志
    return False

# 检查是否 @ 机器人
def is_at_bot(data: Dict) -> bool:
    message = data.get("message", [])    # 获取消息段落
    if isinstance(message, list):    # 检查消息段落是否为列表
        for segment in message:    # 遍历消息段落
            if isinstance(segment, dict) and segment.get("type") == "at":    # 检查消息段落是否为 @ 事件
                target = segment.get("data", {}).get("qq")    # 获取 @ 事件的目标QQ
                if target is not None and str(target) == str(BOT_QQ):    # 检查目标QQ是否为机器人QQ
                    return True
    return False

# 处理消息
def process_message(data: Dict) -> Optional[str]:
    if data.get("post_type") == "message" and data.get("message_type") == "group":
        if is_at_bot(data):
            logging.getLogger("NapCatLoginManager").info(f"收到 @ 事件: group_id={data.get('group_id')}, user_id={data.get('user_id')}")    # 记录信息日志
            return AT_REPLY_TEXT
    return None

@app.on_event("startup")
async def init_repeater():
    repeater_config = create_repeater_config(config)
    repeater = get_repeater(config=repeater_config, send_func=send_group_msg)
    logging.getLogger("NapCatLoginManager").info("复读机模块初始化完成")

@app.post("/onebot")
async def receive_message(request: Request) -> Dict[str, str]:
    data = await request.json()
    reply = process_message(data)
    if is_at_bot(data) and reply:
        group_id = data.get("group_id")
        if group_id:
            # 记录发送回复的开始时间
            start_time = time.time()
            success = await send_group_msg(group_id, reply)
            elapsed = (time.time() - start_time) * 1000
            if success:
                logging.getLogger("NapCatLoginManager").info(f"发送回复成功: group_id={group_id}, reply={reply}, elapsed={elapsed:.2f}ms")    # 记录信息日志
            else:
                logging.getLogger("NapCatLoginManager").error(f"发送回复失败: group_id={group_id}, reply={reply}")    # 记录错误日志
    # 获取复读机实例
    repeater = get_repeater()
    if repeater:
        try:
            await repeater.handle_message(data)    # 处理消息
        except Exception as e:
            logging.getLogger("NapCatLoginManager").error(f"复读机处理消息异常: {e}")    # 记录错误日志
    return {"status": "ok"}

async def main():    # 主函数
    if os.getenv("SKIP_LOGIN") == "1":
        return
    success = await start_bot_with_login()
    if not success:
        logging.getLogger("NapCatLoginManager").error("登录失败，程序退出。")    # 记录错误日志
        return

    config_uvicorn = uvicorn.Config(app, host="0.0.0.0", port=8000)    # 配置 uvicorn 服务器
    server = uvicorn.Server(config_uvicorn)    # 创建 uvicorn 服务器
    logging.getLogger("NapCatLoginManager").info(f"服务器已启动，监听地址: http://0.0.0.0:8000")    # 记录信息日志
    await server.serve()

if __name__ == "__main__":     # 主函数
    try:
        asyncio.run(main())    # 运行主函数
    except KeyboardInterrupt:
        logging.getLogger("NapCatLoginManager").info("\n程序已中断，正在退出。")
