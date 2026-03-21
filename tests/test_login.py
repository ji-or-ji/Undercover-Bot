import sys
import os
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from pathlib import Path

# 将 src 目录添加到 path
sys.path.append(str(Path(__file__).parent.parent))

from src.bot.login import NapCatLoginManager

@pytest.mark.asyncio
async def test_wait_for_ready():
    manager = NapCatLoginManager()
    with patch("httpx.AsyncClient.get") as mock_get:
        # 模拟第一次失败，第二次成功
        # 第一次探测抛错；第二次 /webui/ 返回 200；随后 /api/base/GetSysStatus 返回 401 也视为就绪
        mock_get.side_effect = [
            Exception("Connection error"),
            MagicMock(status_code=200),
            MagicMock(status_code=401),
        ]
        result = await manager.wait_for_ready(timeout=5)
        assert result is True
        assert mock_get.call_count == 3

@pytest.mark.asyncio
async def test_handle_quick_login_success():
    manager = NapCatLoginManager()
    manager._api_post = AsyncMock()
    manager.check_login_status = AsyncMock()
    
    # 模拟账号列表
    manager._api_post.side_effect = [
        {"data": [{"uin": "123456", "nickName": "TestUser"}]}, # GetQuickLoginList
        {"code": 0} # SetQuickLogin
    ]
    # 模拟登录成功状态
    manager.check_login_status.return_value = {"uin": "123456"}
    
    with patch("builtins.input", side_effect=["1"]):
        result = await manager.handle_quick_login()
        assert result is True
        manager._api_post.assert_any_call("/QQLogin/SetQuickLogin", {"uin": "123456"})

@pytest.mark.asyncio
async def test_handle_password_login_success():
    manager = NapCatLoginManager()
    manager._api_post = AsyncMock()
    manager.check_login_status = AsyncMock()
    
    manager._api_post.side_effect = [
        {"data": [{"uin": "123456"}]}, # GetQuickLoginList
        {"code": 0} # PasswordLogin
    ]
    manager.check_login_status.return_value = {"uin": "123456"}
    
    with patch("builtins.input", side_effect=["1", "mypassword"]):
        result = await manager.handle_password_login()
        assert result is True

@pytest.mark.asyncio
async def test_handle_qr_login_success():
    manager = NapCatLoginManager()
    manager._api_post = AsyncMock()
    manager.check_login_status = AsyncMock()
    manager.display_qr = MagicMock()
    
    manager._api_post.side_effect = [
        {"code": 0}, # RefreshQRcode
        {"data": {"qrcode": "http://qr-url"}} # GetQQLoginQrcode
    ]
    # 模拟第三次轮询时成功
    manager.check_login_status.side_effect = [None, None, {"uin": "123456"}]
    
    with patch("asyncio.sleep", return_value=None):
        result = await manager.handle_qr_login()
        assert result is True
        assert manager.check_login_status.call_count == 3

@pytest.mark.asyncio
async def test_login_menu_retry_on_failure():
    manager = NapCatLoginManager()
    # 模拟第一次快捷登录失败，第二次成功
    manager.handle_quick_login = AsyncMock(side_effect=[False, True])
    
    with patch("builtins.input", side_effect=["1", "1"]):
        result = await manager.login_menu()
        assert result is True
        assert manager.handle_quick_login.call_count == 2
