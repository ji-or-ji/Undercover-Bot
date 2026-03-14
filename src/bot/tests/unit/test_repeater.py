import pytest
import os
import yaml
from fastapi.testclient import TestClient
from src.bot.main import app, process_message, load_config

client = TestClient(app)

def test_load_config_default():
    # 测试默认开发配置
    config = load_config("dev")
    assert isinstance(config, dict)

def test_load_config_nonexistent():
    # 测试不存在的配置
    config = load_config("nonexistent")
    assert config == {}

def test_process_message_with_keyword():
    data = {
        "post_type": "message",
        "message_type": "group",
        "group_id": 123456,
        "user_id": 7890,
        "raw_message": "大家好，兄弟们好！"
    }
    reply = process_message(data)
    assert reply == "检测到关键词【兄弟们】，已记录。"

def test_process_message_without_keyword():
    data = {
        "post_type": "message",
        "message_type": "group",
        "group_id": 123456,
        "user_id": 7890,
        "raw_message": "Hello world!"
    }
    reply = process_message(data)
    assert reply is None

def test_receive_message_endpoint_no_reply():
    response = client.post("/onebot", json={
        "post_type": "message",
        "message_type": "group",
        "raw_message": "Nothing interesting"
    })
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_receive_message_endpoint_with_reply(mocker):
    # 模拟send_group_msg以避免真实的网络调用
    mock_send = mocker.patch("src.bot.main.send_group_msg")
    
    response = client.post("/onebot", json={
        "post_type": "message",
        "message_type": "group",
        "group_id": 123456,
        "raw_message": "兄弟们出来受死"
    })
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    mock_send.assert_called_once()

def test_send_group_msg_error(mocker):
    # 测试send_group_msg中的错误处理
    import httpx
    from src.bot.main import send_group_msg
    
    # 模拟httpx.AsyncClient.post以引发异常
    mocker.patch("httpx.AsyncClient.post", side_effect=Exception("Network error"))
    
    # 由于try-except块，这不应引发异常
    import asyncio
    asyncio.run(send_group_msg(123456, "test"))
