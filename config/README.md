# 配置目录

| 子目录 | 职责 | 入口文件 | 配置加载方式 | 依赖关系 |
| :--- | :--- | :--- | :--- | :--- |
| (root) | 存放各环境的配置文件 | dev.yaml, test.yaml, prod.yaml | 由 src/ 源码加载 | N/A |

## 运行相关环境变量

- NAPCAT_WEBUI_TOKEN：优先于 NapCat.Shell/config/webui.json 中的 token，用于调用 WebUI `/api` 接口时的 Authorization 认证。
- SKIP_LOGIN：当值为 `1` 时，跳过 NapCat 登录流程，直接启动 FastAPI（用于 CI/集成测试）。

## 启动顺序（强制）

1. 启动 NapCat：由 `src/bot/login.py` 自动拉起 `NapCat.Shell/launcher-user.bat`。
2. 等待 WebUI 就绪：探测 `http://127.0.0.1:{port}/webui/` 返回 200。
3. 验证 API 可用：请求 `http://127.0.0.1:{port}/api/base/GetSysStatus`，200 表示 token 有效；401/403 表示服务就绪但未授权。
4. 获取登录方式：优先尝试快捷登录列表，其次密码登录，最后二维码登录。

可使用诊断脚本验证：

```bash
python -m src.bot.diagnostics
```
