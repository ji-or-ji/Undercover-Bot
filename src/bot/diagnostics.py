import asyncio
from typing import Dict, Any

import httpx

from .login import NapCatLoginManager


class NapCatDiagnostics:
    def __init__(self):
        self.manager = NapCatLoginManager()

    async def check_webui(self) -> Dict[str, Any]:
        port = self.manager.port
        base_web = f"http://127.0.0.1:{port}"
        result: Dict[str, Any] = {"webui_html": None, "api_status": None}
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(f"{base_web}/webui/", timeout=3.0)
                result["webui_html"] = resp.status_code
            except Exception as e:
                result["webui_html"] = f"error:{e}"

            try:
                headers = {"Authorization": f"Bearer {self.manager.token}"} if self.manager.token else {}
                ping = await client.get(f"{base_web}/api/base/GetSysStatus", headers=headers, timeout=3.0)
                result["api_status"] = ping.status_code
            except Exception as e:
                result["api_status"] = f"error:{e}"
        return result

    async def probe_login_methods(self) -> Dict[str, Any]:
        summary: Dict[str, Any] = {}
        quick_list = await self.manager.get_quick_login_list()
        summary["quick_list_count"] = len(quick_list) if isinstance(quick_list, list) else 0

        await self.manager._api_post("/QQLogin/RefreshQRcode")
        qr_res = await self.manager._api_post("/QQLogin/GetQQLoginQrcode")
        qrcode_text = self.manager._extract_qr_text(qr_res)
        summary["qrcode_available"] = True if qrcode_text else False
        return summary

    async def run(self) -> Dict[str, Any]:
        report: Dict[str, Any] = {"started": False, "webui": {}, "login": {}}

        # Ensure start order: start NapCat -> wait ready -> detect methods
        self.manager.start_service()

        ready = await self.manager.wait_for_ready(timeout=30)
        report["started"] = ready
        report["webui"] = await self.check_webui()
        if not ready:
            return report

        report["login"] = await self.probe_login_methods()
        return report


async def main():
    diag = NapCatDiagnostics()
    report = await diag.run()

    print("\n=== NapCat 启动与登录方式诊断 ===")
    print(f"- 服务启动就绪: {report.get('started')}")
    web = report.get("webui", {})
    print(f"- WebUI 页面状态: {web.get('webui_html')} (期望 200)")
    print(f"- API 探测状态: {web.get('api_status')} (200=Token有效；401/403=就绪但未授权)")

    if report.get("started"):
        login = report.get("login", {})
        print(f"- 快捷登录账号个数: {login.get('quick_list_count')}")
        print(f"- 二维码可获取: {login.get('qrcode_available')}")
        if web.get("api_status") in (401, 403):
            print("- 提示: API 返回未授权，请设置 NAPCAT_WEBUI_TOKEN 或使用浏览器访问 /webui?token=... 完成认证")


if __name__ == "__main__":
    asyncio.run(main())
