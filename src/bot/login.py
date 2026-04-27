# from fastapi import logger
import os
import json
import subprocess
import time
import httpx
import qrcode
import asyncio
import hashlib
import yaml
import webbrowser
import re
from urllib.parse import quote
from pathlib import Path
from typing import List, Dict, Optional, Any
import logging
# 导入logging模块，用于记录日志
import logging

# 获取项目根目录
ROOT_DIR = Path(__file__).parent.parent.parent    # 项目根目录
NAPCAT_DIR = ROOT_DIR / "NapCat.Shell"   
WEBUI_CONFIG_PATH = NAPCAT_DIR / "config" / "webui.json"

# 获取应用配置
def get_app_config(env: Optional[str] = None) -> Dict[str, Any]:
    target_env = env or os.getenv("APP_ENV", "dev")
    config_path = ROOT_DIR / "config" / f"{target_env}.yaml"
    if not config_path.exists():
        return {}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}

def get_webui_config():
    config: Dict[str, Any] = {"port": 6099, "token": ""}
    app_config = get_app_config()
    napcat_block = app_config.get("napcat") if isinstance(app_config, dict) else {}
    if isinstance(napcat_block, dict):
        if napcat_block.get("webui_port") is not None:
            config["port"] = napcat_block.get("webui_port")
        if napcat_block.get("webui_token"):
            config["token"] = napcat_block.get("webui_token")
    if app_config.get("napcat_webui_port") is not None:
        config["port"] = app_config.get("napcat_webui_port")
    if app_config.get("napcat_webui_token"):
        config["token"] = app_config.get("napcat_webui_token")
    if not WEBUI_CONFIG_PATH.exists():
        return config
    try:
        with open(WEBUI_CONFIG_PATH, "r", encoding="utf-8") as f:
            webui_config = json.load(f)
            if webui_config.get("port") is not None and app_config.get("napcat_webui_port") is None and not (isinstance(napcat_block, dict) and napcat_block.get("webui_port") is not None):
                config["port"] = webui_config.get("port")
            if webui_config.get("token") and not app_config.get("napcat_webui_token") and not (isinstance(napcat_block, dict) and napcat_block.get("webui_token")):
                config["token"] = webui_config.get("token")
            return config
    except Exception:
        return config

class NapCatLoginManager:
    @staticmethod
    def _to_bool(value: Any, default: bool = False) -> bool:
        if value is None:
            return default
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return value.strip().lower() in ("1", "true", "yes", "on", "y")
        return default

    def __init__(self):
        config = get_webui_config()
        app_config = get_app_config()
        napcat_block = app_config.get("napcat") if isinstance(app_config, dict) else {}
        self.port = config.get("port", 6099)
        self.token = config.get("token", "")
        self.auto_open_webui_after_login = False
        if isinstance(napcat_block, dict):
            self.auto_open_webui_after_login = self._to_bool(napcat_block.get("auto_open_webui_after_login"), False)
        if isinstance(app_config, dict) and app_config.get("napcat_auto_open_webui_after_login") is not None:
            self.auto_open_webui_after_login = self._to_bool(app_config.get("napcat_auto_open_webui_after_login"), False)
        env_token = os.getenv("NAPCAT_WEBUI_TOKEN")
        if env_token:
            self.token = env_token
        env_auto_open = os.getenv("NAPCAT_AUTO_OPEN_WEBUI_AFTER_LOGIN")
        if env_auto_open is not None:
            self.auto_open_webui_after_login = self._to_bool(env_auto_open, self.auto_open_webui_after_login)
        # NapCat API 前缀为 /api
        self.base_url = f"http://127.0.0.1:{self.port}/api"
        self.webui_credential: Optional[str] = None
        self.process = None

    @staticmethod
    def _is_unauthorized_response(payload: Any) -> bool:
        return isinstance(payload, dict) and payload.get("code") == -1 and str(payload.get("message", "")).lower() == "unauthorized"

    @staticmethod
    def _extract_qr_text(payload: Dict[str, Any]) -> Optional[str]:
        data = payload.get("data")
        if isinstance(data, dict):
            for key in ("qrcode", "qrcodeUrl", "qrcodeurl"):
                value = data.get(key)
                if isinstance(value, str) and value.strip():
                    return value.strip()
        if isinstance(data, str) and data.strip():
            return data.strip()
        for key in ("qrcode", "qrcodeUrl", "qrcodeurl"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        txt_obj = payload.get("text")
        if isinstance(txt_obj, str) and "http" in txt_obj:
            start = txt_obj.find("http")
            end = txt_obj.find("\n", start)
            return (txt_obj[start:end] if end != -1 else txt_obj[start:]).strip()
        return None

    @staticmethod
    def _normalize_account_entry(account: Any) -> Dict[str, str]:
        if isinstance(account, dict):
            uin = account.get("uin") or account.get("account") or account.get("user_id") or ""
            nick = account.get("nickName") or account.get("nickname") or "未知"
            return {"uin": str(uin) if uin is not None else "", "nickName": str(nick)}
        if isinstance(account, (str, int)):
            return {"uin": str(account), "nickName": "未知"}
        return {"uin": "", "nickName": "未知"}

    @staticmethod
    def _is_already_logged_in_message(message: Optional[str]) -> bool:
        if not isinstance(message, str):
            return False
        msg = message.lower()
        return "logined" in msg or "logged in" in msg or "already login" in msg

    @staticmethod
    def _format_login_identity(status: Dict[str, Any]) -> str:
        for key in ("uin", "account", "user_id", "uid", "nick", "nickname"):
            value = status.get(key)
            if value is not None and str(value).strip():
                return str(value).strip()
        return "已登录账号"

    async def _authenticate_webui(self) -> bool:
        if not self.token:
            return False
        token_hash = hashlib.sha256(f"{self.token}.napcat".encode("utf-8")).hexdigest()
        login_url = f"{self.base_url}/auth/login"
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(login_url, json={"hash": token_hash}, timeout=10.0)
                body = resp.json()
                credential = body.get("data", {}).get("Credential") if isinstance(body.get("data"), dict) else None
                if isinstance(credential, str) and credential:
                    self.webui_credential = credential
                    return True
        except Exception as e:
                    logging.getLogger("NapCatLoginManager").error(f"WebUI 鉴权失败: {e}")
        return False

    async def _post_with_token(self, url: str, payload: Dict[str, Any], auth_token: Optional[str]):
        headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, headers=headers, timeout=10.0)
            try:
                return resp.json()
            except Exception:
                return {
                    "code": resp.status_code,
                    "message": "non-json-response",
                    "text": resp.text,
                    "url": url
                }

    async def _api_post(self, endpoint: str, data: Optional[Dict] = None):
        url = f"{self.base_url}{endpoint if endpoint.startswith('/') else '/'+endpoint}"
        payload = data or {}
        auth_candidates = [self.webui_credential, self.token]
        tried: List[Optional[str]] = []
        try:
            for candidate in auth_candidates:
                if candidate in tried:
                    continue
                tried.append(candidate)
                result = await self._post_with_token(url, payload, candidate)
                if not self._is_unauthorized_response(result):
                    return result
            if await self._authenticate_webui():
                result = await self._post_with_token(url, payload, self.webui_credential)
                if not self._is_unauthorized_response(result):
                    return result
            return {"code": -1, "message": "Unauthorized", "data": None, "url": url}
        except Exception as e:
            logging.getLogger("NapCatLoginManager").error(f"API 请求失败 [{endpoint}]: {e}")
            return {"code": -1, "message": str(e), "data": None}

    async def wait_for_ready(self, timeout=30):
        """等待 WebUI 就绪"""
        logging.getLogger("NapCatLoginManager").info(f"正在检测 NapCat WebUI 是否就绪 (http://127.0.0.1:{self.port})...")
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                async with httpx.AsyncClient() as client:
                    # 先探测静态页面
                    resp = await client.get(f"http://127.0.0.1:{self.port}/webui/", timeout=1.0)
                    if resp.status_code == 200:
                        # 再探测 API 可用性（校验 token）
                        ping = await client.get(
                            f"http://127.0.0.1:{self.port}/api/base/GetSysStatus",
                            headers={"Authorization": f"Bearer {self.token}"} if self.token else {},
                            timeout=2.0
                        )
                        if ping.status_code in (200, 401, 403):
                            return True
            except Exception:
                pass
            await asyncio.sleep(1)
        return False

    def start_service(self):
        """自动启动 NapCat 服务"""
        bat_path = NAPCAT_DIR / "launcher-user.bat"
        if not bat_path.exists():
            raise FileNotFoundError(f"找不到启动脚本: {bat_path}")
        
        logging.getLogger("NapCatLoginManager").info(f"正在启动 NapCat 服务: {bat_path}")
        # 在 Windows 上使用 subprocess.Popen 启动服务
        # 使用 shell=True 并在新的终端窗口启动，以便用户观察日志（可选）
        # 这里我们直接启动，不阻塞
        self.process = subprocess.Popen(
            [str(bat_path)], 
            cwd=str(NAPCAT_DIR), 
            shell=True,
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0
        )
        return self.process

    async def get_quick_login_list(self):
        """获取历史账号列表"""
        res = await self._api_post("/QQLogin/GetQuickLoginList")
        # 如果新版 API 不同，可能需要调整。根据 JS 逻辑，存在 GetQuickLoginList 和 GetQuickLoginListNew
        if not res.get("data"):
            res = await self._api_post("/QQLogin/GetQuickLoginListNew")
        data = res.get("data")
        if isinstance(data, list):
            normalized: List[Dict[str, str]] = []
            for item in data:
                entry = self._normalize_account_entry(item)
                if entry.get("uin"):
                    normalized.append(entry)
            return normalized
        return []

    async def check_login_status(self):
        """检查登录状态"""
        res = await self._api_post("/QQLogin/CheckLoginStatus")
        data = res.get("data")
        if isinstance(data, dict):
            if data.get("login") or data.get("isLogin") or data.get("uin") or data.get("account") or data.get("user_id"):
                return data
        if isinstance(data, bool) and data:
            return {"login": True}
        if self._is_already_logged_in_message(res.get("message")):
            return {"login": True}
        return None

    def display_qr(self, qr_text: str):
        """在终端显示二维码"""
        qr = qrcode.QRCode()
        qr.add_data(qr_text)
        qr.make(fit=True)
        # 使用 ascii 字符在终端打印
        qr.print_ascii(invert=True)
        logging.getLogger("NapCatLoginManager").info(f"\n请使用手机 QQ 扫描上方二维码登录")
        logging.getLogger("NapCatLoginManager").info(f"原始链接: {qr_text}")

    def open_webui_if_enabled(self):
        if not self.auto_open_webui_after_login:
            return
        webui_url = self._resolve_webui_open_url()
        try:
            webbrowser.open(webui_url)
            logging.getLogger("NapCatLoginManager").info(f"已自动打开 NapCat WebUI: {webui_url}")
        except Exception as e:
            logging.getLogger("NapCatLoginManager").error(f"自动打开 NapCat WebUI 失败: {e}")

    def _resolve_webui_open_url(self) -> str:
        log_panel_url = self._get_webui_panel_url_from_logs()
        if log_panel_url:
            token = str(self.token).strip() if self.token else ""
            if "token=" in log_panel_url or not token:
                return log_panel_url
            sep = "&" if "?" in log_panel_url else "?"
            return f"{log_panel_url}{sep}token={quote(token, safe='')}"
        base_webui_url = f"http://127.0.0.1:{self.port}/webui/"
        token = str(self.token).strip() if self.token else ""
        if not token:
            return base_webui_url
        api_status_url = f"http://127.0.0.1:{self.port}/api/base/GetSysStatus"
        status_code: Optional[int] = None
        try:
            resp = httpx.get(api_status_url, timeout=2.0)
            status_code = resp.status_code
        except Exception:
            status_code = None
        if status_code == 200:
            return base_webui_url
        return f"{base_webui_url}?token={quote(token, safe='')}"

    def _get_webui_panel_url_from_logs(self) -> Optional[str]:
        logs_dir = NAPCAT_DIR / "logs"
        if not logs_dir.exists():
            return None
        try:
            log_files = sorted([p for p in logs_dir.glob("*.log") if p.is_file()], key=lambda p: p.stat().st_mtime, reverse=True)
        except Exception:
            return None
        pattern = re.compile(r"WebUi User Panel Url:\s*(https?://\S+)")
        for log_file in log_files[:5]:
            try:
                with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
            except Exception:
                continue
            for line in reversed(lines):
                match = pattern.search(line)
                if match:
                    url = match.group(1).strip()
                    if "127.0.0.1" in url:
                        return url
            for line in reversed(lines):
                match = pattern.search(line)
                if match:
                    url = match.group(1).strip()
                    if "localhost" in url:
                        return url
            for line in reversed(lines):
                match = pattern.search(line)
                if match:
                    return match.group(1).strip()
        return None

    async def login_menu(self):
        """交互式登录菜单"""
        while True:
            print("\n" + "="*30)
            print("      NapCat 登录选择")
            print("="*30)
            print("1. 快捷登录 (使用本地缓存)")
            print("2. 账号选择登录 (输入密码)")
            print("3. 扫码登录")
            print("0. 退出")
            print("="*30)
            try:
                choice = input("请选择登录方式 [0-3]: ").strip()
            except EOFError:
                print("\n未检测到可用输入流，退出登录流程。")
                return False
            except KeyboardInterrupt:
                print("\n已取消登录流程。")
                return False
            
            try:
                if choice == "1":
                    if await self.handle_quick_login():
                        return True
                elif choice == "2":
                    if await self.handle_password_login():
                        return True
                elif choice == "3":
                    if await self.handle_qr_login():
                        return True
                elif choice == "0":
                    return False
                else:
                    print("无效选择，请重新输入。")
            except KeyboardInterrupt:
                print("\n已取消登录流程。")
                return False
            except Exception as e:
                print(f"\n登录过程中发生错误: {e}")
                print("将返回主菜单...")
                await asyncio.sleep(2)

    async def handle_quick_login(self):
        accounts = await self.get_quick_login_list()
        if not accounts:
            print("未找到本地缓存账号。")
            return False
        
        print("\n可用的缓存账号:")
        for i, acc in enumerate(accounts):
            uin = acc.get("uin")
            nick = acc.get("nickName") or "未知"
            print(f"{i+1}. {uin} ({nick})")
        
        idx_str = input("请选择账号序号 (回车返回): ").strip()
        if not idx_str: return False
        
        try:
            idx = int(idx_str) - 1
            if 0 <= idx < len(accounts):
                target_uin = accounts[idx].get("uin")
                print(f"正在尝试快捷登录账号: {target_uin}...")
                await self._api_post("/QQLogin/SetQuickLogin", {"uin": str(target_uin)})
                
                # 等待并检查状态
                for _ in range(10):
                    status = await self.check_login_status()
                    if status:
                        print(f"登录成功! 欢迎: {self._format_login_identity(status)}")
                        return True
                    await asyncio.sleep(2)
                print("快捷登录超时，请重试或尝试其他方式。")
            else:
                print("无效的序号。")
        except ValueError:
            print("请输入有效的数字。")
        return False

    async def handle_password_login(self):
        accounts = await self.get_quick_login_list()
        print("\n历史账号 (或手动输入):")
        for i, acc in enumerate(accounts):
            uin = acc.get("uin")
            print(f"{i+1}. {uin}")
        
        uin_input = input("请输入 QQ 账号 (或选择序号, 回车返回): ").strip()
        if not uin_input: return False
        
        target_uin = uin_input
        try:
            idx = int(uin_input) - 1
            if 0 <= idx < len(accounts):
                target_uin = accounts[idx].get("uin")
        except ValueError:
            pass # 直接使用输入作为 UIN
            
        password = input(f"请输入账号 {target_uin} 的密码: ").strip()
        if not password: return False
        
        md5_pass = hashlib.md5(password.encode()).hexdigest()
        print(f"正在尝试密码登录 {target_uin}...")
        res = await self._api_post("/QQLogin/PasswordLogin", {"uin": str(target_uin), "passwordMd5": md5_pass})
        
        if res.get("code") == 0:
            print("登录指令已发送，正在检查状态...")
            for _ in range(15):
                status = await self.check_login_status()
                if status:
                    print(f"登录成功! 欢迎: {self._format_login_identity(status)}")
                    return True
                await asyncio.sleep(2)
        else:
            print(f"登录请求失败: {res.get('message')}")
        return False

    async def handle_qr_login(self):
        print("\n正在获取登录二维码...")
        refresh_res = await self._api_post("/QQLogin/RefreshQRcode")
        qr_text: Optional[str] = None
        last_message = refresh_res.get("message")
        for _ in range(8):
            res = await self._api_post("/QQLogin/GetQQLoginQrcode")
            qr_text = self._extract_qr_text(res)
            last_message = res.get("message") or last_message
            if qr_text:
                break
            await asyncio.sleep(0.8)
        if not qr_text:
            if self._is_already_logged_in_message(last_message):
                status = await self.check_login_status()
                if status:
                    print(f"检测到账号已登录，欢迎: {self._format_login_identity(status)}")
                    return True
            print(f"获取二维码失败。{last_message or ''}".strip())
            return False
        
        self.display_qr(qr_text)
        
        print("等待扫码... (超时时间 120s)")
        start_time = time.time()
        while time.time() - start_time < 120:
            status = await self.check_login_status()
            if status:
                print(f"\n扫码成功! 欢迎: {self._format_login_identity(status)}")
                return True
            await asyncio.sleep(3)
        
        print("\n扫码超时，请重试。")
        return False

async def start_bot_with_login():
    manager = NapCatLoginManager()
    try:
        # 1. 启动服务
        manager.start_service()
        
        # 2. 等待就绪
        if not await manager.wait_for_ready():
            print("错误: NapCat 服务启动超时或 WebUI 无法访问。")
            return False
        
        # 3. 进入登录流程
        if await manager.login_menu():
            manager.open_webui_if_enabled()
            print("所有登录流程已完成，进入主程序...")
            return True
        return False
    except (KeyboardInterrupt, asyncio.CancelledError):
        print("登录流程已中断。")
        return False
    except Exception as e:
        print(f"启动失败: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(start_bot_with_login())
