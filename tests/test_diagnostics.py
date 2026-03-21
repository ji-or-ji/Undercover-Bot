import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from src.bot.diagnostics import NapCatDiagnostics


@pytest.mark.asyncio
async def test_diagnostics_report():
    diag = NapCatDiagnostics()

    # Mock start_service to avoid actually spawning processes
    diag.manager.start_service = MagicMock()

    # Mock wait_for_ready to True
    diag.manager.wait_for_ready = AsyncMock(return_value=True)

    # Mock webui check to predetermined values
    with patch("httpx.AsyncClient.get") as mock_get:
        # webui 200, api 401
        mock_get.side_effect = [
            MagicMock(status_code=200),
            MagicMock(status_code=401),
        ]
        web = await diag.check_webui()
        assert web["webui_html"] == 200
        assert web["api_status"] == 401

    # Mock login probing
    diag.manager.get_quick_login_list = AsyncMock(return_value=[{"uin": "123"}])
    diag.manager._api_post = AsyncMock(side_effect=[
        {"code": 0},  # RefreshQRcode
        {"data": {"qrcode": "http://qrcode-url"}},  # GetQQLoginQrcode
    ])
    login = await diag.probe_login_methods()
    assert login["quick_list_count"] == 1
    assert login["qrcode_available"] is True

    # End-to-end report
    diag.manager.wait_for_ready = AsyncMock(return_value=True)
    # 为 end-to-end 阶段再次提供 _api_post 的 side_effect
    diag.manager._api_post = AsyncMock(side_effect=[
        {"code": 0},  # RefreshQRcode
        {"data": {"qrcode": "http://qrcode-url"}},  # GetQQLoginQrcode
    ])
    with patch("httpx.AsyncClient.get") as mock_get2:
        mock_get2.side_effect = [
            MagicMock(status_code=200),
            MagicMock(status_code=401),
        ]
        report = await diag.run()
        assert report["started"] is True
        assert report["webui"]["webui_html"] == 200
        assert report["login"]["qrcode_available"] is True


@pytest.mark.asyncio
async def test_probe_login_methods_with_qrcodeurl_field():
    diag = NapCatDiagnostics()
    diag.manager.get_quick_login_list = AsyncMock(return_value=[])
    diag.manager._api_post = AsyncMock(side_effect=[
        {"code": 0},
        {"code": 0, "data": {"qrcodeurl": "http://qr-url"}},
    ])

    login = await diag.probe_login_methods()
    assert login["quick_list_count"] == 0
    assert login["qrcode_available"] is True
