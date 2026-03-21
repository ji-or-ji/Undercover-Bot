import sys
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from pathlib import Path

# 将 src 目录添加到 path
sys.path.append(str(Path(__file__).parent.parent))

from src.bot.login import NapCatLoginManager, get_webui_config, get_app_config, start_bot_with_login


class MockResponse:
    def __init__(self, payload):
        self.payload = payload
        self.status_code = 200
        self.text = str(payload)

    def json(self):
        return self.payload

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
async def test_api_post_reauth_with_webui_token():
    manager = NapCatLoginManager()
    manager.token = "plain-token"

    with patch("httpx.AsyncClient.post") as mock_post:
        mock_post.side_effect = [
            MockResponse({"code": -1, "message": "Unauthorized"}),
            MockResponse({"code": -1, "message": "Unauthorized"}),
            MockResponse({"code": 0, "data": {"Credential": "signed-credential"}, "message": "success"}),
            MockResponse({"code": 0, "data": {"qrcode": "http://qr-url"}, "message": "success"}),
        ]
        result = await manager._api_post("/QQLogin/GetQQLoginQrcode")
        assert result["data"]["qrcode"] == "http://qr-url"
        assert manager.webui_credential == "signed-credential"
        assert mock_post.call_count == 4


@pytest.mark.asyncio
async def test_handle_qr_login_retry_until_qrcode_available():
    manager = NapCatLoginManager()
    manager._api_post = AsyncMock(side_effect=[
        {"code": 0, "message": "success"},
        {"code": -1, "message": "QRCode Get Error"},
        {"code": 0, "data": {"qrcode": "http://qr-url"}, "message": "success"},
    ])
    manager.display_qr = MagicMock()
    manager.check_login_status = AsyncMock(return_value={"uin": "123456"})

    with patch("asyncio.sleep", return_value=None):
        result = await manager.handle_qr_login()
        assert result is True
        manager.display_qr.assert_called_once_with("http://qr-url")

@pytest.mark.asyncio
async def test_login_menu_retry_on_failure():
    manager = NapCatLoginManager()
    # 模拟第一次快捷登录失败，第二次成功
    manager.handle_quick_login = AsyncMock(side_effect=[False, True])
    
    with patch("builtins.input", side_effect=["1", "1"]):
        result = await manager.login_menu()
        assert result is True
        assert manager.handle_quick_login.call_count == 2


@pytest.mark.asyncio
async def test_get_quick_login_list_supports_string_items():
    manager = NapCatLoginManager()
    manager._api_post = AsyncMock(return_value={"data": ["10001", "10002"]})
    accounts = await manager.get_quick_login_list()
    assert accounts == [
        {"uin": "10001", "nickName": "未知"},
        {"uin": "10002", "nickName": "未知"},
    ]


@pytest.mark.asyncio
async def test_handle_qr_login_treats_already_logged_in_as_success():
    manager = NapCatLoginManager()

    async def fake_api(endpoint, data=None):
        if endpoint == "/QQLogin/RefreshQRcode":
            return {"code": 0, "message": "success"}
        if endpoint == "/QQLogin/GetQQLoginQrcode":
            return {"code": -1, "message": "QQ Is Logined"}
        return {"code": 0, "data": {}}

    manager._api_post = AsyncMock(side_effect=fake_api)
    manager.check_login_status = AsyncMock(return_value={"login": True})

    with patch("asyncio.sleep", return_value=None):
        result = await manager.handle_qr_login()
        assert result is True


@pytest.mark.asyncio
async def test_login_menu_returns_false_on_eof():
    manager = NapCatLoginManager()
    with patch("builtins.input", side_effect=EOFError):
        result = await manager.login_menu()
        assert result is False


@pytest.mark.asyncio
async def test_start_bot_with_login_handles_keyboard_interrupt():
    with patch("src.bot.login.NapCatLoginManager.start_service", return_value=None):
        with patch("src.bot.login.NapCatLoginManager.wait_for_ready", new=AsyncMock(return_value=True)):
            with patch("src.bot.login.NapCatLoginManager.login_menu", new=AsyncMock(side_effect=KeyboardInterrupt)):
                result = await start_bot_with_login()
                assert result is False


@pytest.mark.asyncio
async def test_start_bot_with_login_calls_open_webui():
    with patch("src.bot.login.NapCatLoginManager.start_service", return_value=None):
        with patch("src.bot.login.NapCatLoginManager.wait_for_ready", new=AsyncMock(return_value=True)):
            with patch("src.bot.login.NapCatLoginManager.login_menu", new=AsyncMock(return_value=True)):
                with patch("src.bot.login.NapCatLoginManager.open_webui_if_enabled") as mock_open:
                    result = await start_bot_with_login()
                    assert result is True
                    mock_open.assert_called_once()


def test_open_webui_if_enabled_respects_flag():
    manager = NapCatLoginManager()
    manager.port = 6099
    manager._get_webui_panel_url_from_logs = MagicMock(return_value=None)
    manager.auto_open_webui_after_login = False
    with patch("webbrowser.open") as mock_open:
        manager.open_webui_if_enabled()
        mock_open.assert_not_called()

    manager.auto_open_webui_after_login = True
    manager.token = ""
    with patch("webbrowser.open", return_value=True) as mock_open:
        manager.open_webui_if_enabled()
        mock_open.assert_called_once_with("http://127.0.0.1:6099/webui/")


def test_resolve_webui_open_url_with_token_on_unauthorized():
    manager = NapCatLoginManager()
    manager.port = 6099
    manager.token = "abc123"
    manager._get_webui_panel_url_from_logs = MagicMock(return_value=None)
    with patch("httpx.get", return_value=MagicMock(status_code=401)):
        url = manager._resolve_webui_open_url()
        assert url == "http://127.0.0.1:6099/webui/?token=abc123"


def test_resolve_webui_open_url_without_token_when_public():
    manager = NapCatLoginManager()
    manager.port = 6099
    manager.token = "abc123"
    manager._get_webui_panel_url_from_logs = MagicMock(return_value=None)
    with patch("httpx.get", return_value=MagicMock(status_code=200)):
        url = manager._resolve_webui_open_url()
        assert url == "http://127.0.0.1:6099/webui/"


def test_resolve_webui_open_url_prefers_panel_url_from_logs():
    manager = NapCatLoginManager()
    manager.token = "cfg-token"
    manager._get_webui_panel_url_from_logs = MagicMock(return_value="http://127.0.0.1:6102/webui?token=log-token")
    url = manager._resolve_webui_open_url()
    assert url == "http://127.0.0.1:6102/webui?token=log-token"


def test_resolve_webui_open_url_appends_token_when_log_url_missing_token():
    manager = NapCatLoginManager()
    manager.token = "cfg-token"
    manager._get_webui_panel_url_from_logs = MagicMock(return_value="http://127.0.0.1:6102/webui")
    url = manager._resolve_webui_open_url()
    assert url == "http://127.0.0.1:6102/webui?token=cfg-token"


def test_auto_open_webui_from_config():
    mock_cfg = {"napcat": {"webui_port": 7001, "auto_open_webui_after_login": True}}
    with patch("src.bot.login.get_app_config", return_value=mock_cfg):
        with patch("pathlib.Path.exists", return_value=False):
            manager = NapCatLoginManager()
            assert manager.auto_open_webui_after_login is True


def test_get_app_config_from_yaml():
    cfg = get_app_config("dev")
    assert isinstance(cfg, dict)
    assert cfg.get("napcat", {}).get("onebot_api")


def test_get_webui_config_prefers_app_config():
    with patch("src.bot.login.get_app_config", return_value={"napcat": {"webui_port": 7001, "webui_token": "cfg-token"}}):
        with patch("pathlib.Path.exists", return_value=False):
            cfg = get_webui_config()
            assert cfg["port"] == 7001
            assert cfg["token"] == "cfg-token"
