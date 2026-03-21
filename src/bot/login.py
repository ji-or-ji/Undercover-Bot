import os
import json
import subprocess
import time
import httpx
import qrcode
import asyncio
import hashlib
from pathlib import Path
from typing import List, Dict, Optional

# 获取项目根目录
ROOT_DIR = Path(__file__).parent.parent.parent
NAPCAT_DIR = ROOT_DIR / "NapCat.Shell"
WEBUI_CONFIG_PATH = NAPCAT_DIR / "config" / "webui.json"

def get_webui_config():
    if not WEBUI_CONFIG_PATH.exists():
        return {"port": 6099, "token": ""}
    try:
        with open(WEBUI_CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"port": 6099, "token": ""}

class NapCatLoginManager:
    def __init__(self):
        config = get_webui_config()
        self.port = config.get("port", 6099)
        self.token = config.get("token", "")
        env_token = os.getenv("NAPCAT_WEBUI_TOKEN")
        if env_token:
            self.token = env_token
        # NapCat API 前缀为 /api
        self.base_url = f"http://127.0.0.1:{self.port}/api"
        self.process = None

    async def _api_post(self, endpoint: str, data: Optional[Dict] = None):
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        url = f"{self.base_url}{endpoint if endpoint.startswith('/') else '/'+endpoint}"
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(url, json=data or {}, headers=headers, timeout=10.0)
                try:
                    return resp.json()
                except Exception:
                    return {
                        "code": resp.status_code,
                        "message": "non-json-response",
                        "text": resp.text,
                        "url": url
                    }
            except Exception as e:
                print(f"API 请求失败 [{endpoint}]: {e}")
                return {"code": -1, "message": str(e), "data": None}

    async def wait_for_ready(self, timeout=30):
        """等待 WebUI 就绪"""
        print(f"正在检测 NapCat WebUI 是否就绪 (http://127.0.0.1:{self.port})...")
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
        
        print(f"正在启动 NapCat 服务: {bat_path}")
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
            return data
        return []

    async def check_login_status(self):
        """检查登录状态"""
        res = await self._api_post("/QQLogin/CheckLoginStatus")
        # 假设返回结果包含登录信息
        data = res.get("data")
        if data and (data.get("login") or data.get("isLogin") or data.get("uin")):
            return data
        return None

    def display_qr(self, qr_text: str):
        """在终端显示二维码"""
        qr = qrcode.QRCode()
        qr.add_data(qr_text)
        qr.make(fit=True)
        # 使用 ascii 字符在终端打印
        qr.print_ascii(invert=True)
        print(f"\n请使用手机 QQ 扫描上方二维码登录")
        print(f"原始链接: {qr_text}")

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
            
            choice = input("请选择登录方式 [1-3]: ").strip()
            
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
                    exit(0)
                else:
                    print("无效选择，请重新输入。")
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
            uin = acc.get("uin") or acc.get("account")
            nick = acc.get("nickName") or acc.get("nickname") or "未知"
            print(f"{i+1}. {uin} ({nick})")
        
        idx_str = input("请选择账号序号 (回车返回): ").strip()
        if not idx_str: return False
        
        try:
            idx = int(idx_str) - 1
            if 0 <= idx < len(accounts):
                target_uin = accounts[idx].get("uin") or accounts[idx].get("account")
                print(f"正在尝试快捷登录账号: {target_uin}...")
                await self._api_post("/QQLogin/SetQuickLogin", {"uin": str(target_uin)})
                
                # 等待并检查状态
                for _ in range(10):
                    status = await self.check_login_status()
                    if status:
                        print(f"登录成功! 欢迎: {status.get('uin')}")
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
            uin = acc.get("uin") or acc.get("account")
            print(f"{i+1}. {uin}")
        
        uin_input = input("请输入 QQ 账号 (或选择序号, 回车返回): ").strip()
        if not uin_input: return False
        
        target_uin = uin_input
        try:
            idx = int(uin_input) - 1
            if 0 <= idx < len(accounts):
                target_uin = accounts[idx].get("uin") or accounts[idx].get("account")
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
                    print(f"登录成功! 欢迎: {status.get('uin')}")
                    return True
                await asyncio.sleep(2)
        else:
            print(f"登录请求失败: {res.get('message')}")
        return False

    async def handle_qr_login(self):
        print("\n正在获取登录二维码...")
        # 刷新并获取二维码
        await self._api_post("/QQLogin/RefreshQRcode")
        res = await self._api_post("/QQLogin/GetQQLoginQrcode")
        qr_text = res.get("data", {}).get("qrcode") if isinstance(res.get("data"), dict) else res.get("data")
        
        if not qr_text:
            # 兼容不同返回格式
            qr_text = res.get("qrcode")
        if not qr_text:
            txt_obj = res.get("text")
            if isinstance(txt_obj, str) and "http" in txt_obj:
                start = txt_obj.find("http")
                end = txt_obj.find("\n", start)
                qr_text = txt_obj[start:end] if end != -1 else txt_obj[start:]
        
        if not qr_text:
            print("获取二维码失败。")
            return False
        
        self.display_qr(qr_text)
        
        print("等待扫码... (超时时间 120s)")
        start_time = time.time()
        while time.time() - start_time < 120:
            status = await self.check_login_status()
            if status:
                print(f"\n扫码成功! 欢迎: {status.get('uin')}")
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
            print("所有登录流程已完成，进入主程序...")
            return True
        return False
    except Exception as e:
        print(f"启动失败: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(start_bot_with_login())
