from fastapi import FastAPI, Request
import httpx
import uvicorn

app = FastAPI()

# Napcat 的 API 地址（默认是 5700 端口，如果没改过就是这里）
NAPCAT_API = "http://127.0.0.1:5700"

# 要监控的关键词列表
KEYWORDS = ["炸群", "举报", "兄弟们"]

async def send_group_msg(group_id: int, message: str):
    """向指定群发送消息"""
    url = f"{NAPCAT_API}/send_group_msg"
    data = {
        "group_id": group_id,
        "message": message
    }
    async with httpx.AsyncClient() as client:
        await client.post(url, json=data)

@app.post("/onebot")
async def receive_message(request: Request):
    data = await request.json()
    
    # 只处理群消息
    if data.get("post_type") == "message" and data.get("message_type") == "group":
        group_id = data["group_id"]
        user_id = data["user_id"]
        raw_message = data["raw_message"]
        
        print(f"群 {group_id} 中的 {user_id} 说：{raw_message}")
        
        # 检查是否包含关键词
        for kw in KEYWORDS:
            if kw in raw_message:
                reply = f"检测到关键词【{kw}】，已记录。"
                await send_group_msg(group_id, reply)
                print(f"已回复：{reply}")
                break  # 只回复一次

    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)