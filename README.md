# 卧底机器人 (UndercoverBot)

> 一个用于潜伏在QQ群中监控关键词、自动预警、收集证据的机器人框架。\
> 初衷是帮助大家快速建立防线，应对网络不良信息。\
> **目前处于初期想法阶段，欢迎感兴趣的朋友一起讨论和开发！**

***

## 项目愿景

做一个**简单、易部署、可扩展**的QQ机器人，能够：

- 用多个小号潜入不同群聊，实时监控消息
- 通过关键词匹配、AI分析识别风险内容
- 自动预警（通过另一个号发送通报，多号合作）
- 收集证据（消息记录、二维码、分享链接）
- 提供Web界面管理配置和查看日志

目标是让即使不会编程的人，也能 **“点一下按钮、扫几下码登入”** 就快速搭建自己的“卧底网络”。

***

## 技术思路

我(们)会尝试基于以下成熟组件构建：

- **[Napcat](https://github.com/NapNeko/NapCatQQ)**：基于OneBot协议的QQ机器人框架，负责登录小号、收发消息。
- **Python后端**：接收Napcat上报的消息，进行逻辑处理（关键词匹配、限流、存储、调用AI等）。
- **数据库**：SQLite（轻量）/MySQL，存储消息记录、配置、证据。
- **Redis**：用于限流计数、任务队列。
- **Web管理界面**：Flask/FastAPI + 简单HTML，方便查看和管理。

**[架构简图](docs/开发指南/架构设计/整体架构.drawio)** （正在更新中...）

**!\[架构图]\(docs/开发指南/架构设计/整体架构.drawio.png 系统整体架构)**

***

## 当前进展

- [x] 确认技术可行性（Napcat + Python 可实时接收/发送消息）
- [ ] 完成单账号关键词匹配原型
- [ ] 设计多账号协同方案
- [ ] 开发多账号支持、数据库存储、限流模块
- [ ] preview: 二维码识别、Web管理界面

更多细节可查看 [项目看板](https://gitee.com/ji-or-ji/Undercover-Bot/board)，当然，你也可以化身为赛博监工（[监工报表在这儿](docs/赛博监工/TODU.md)）。

***

## 如何参与

我(们)非常欢迎各种形式的贡献：

- **提出想法**：在 Issues 里告诉我(们)你想要的功能
- **代码贡献**：Fork 项目，提交 Pull Request
- **文档完善**：帮助我(们)写更易懂的文档
  ~~-~~ **~~测试反馈~~**~~：部署试用，反馈 bug 或优化建议~~ **（目前未实现）**

***

## 快速部署指南（请注意，当前未完成核心功能，本部署教程暂时无效）

### 方式一：通过 Git 克隆（推荐开发者）

#### 1. 获取项目代码

```bash
# 克隆项目到本地
git clone https://gitee.com/ji-or-ji/Undercover-Bot.git
cd Undercover-Bot
```

#### 2. 安装 Python 依赖

```bash
# 确保已安装 Python 3.9+
python --version

# 安装项目依赖
pip install -r requirements.txt
```

#### 3. 下载 NapCat 框架

NapCat 是项目的核心组件，需要单独下载：

1. 访问 [NapCat GitHub 仓库](https://github.com/NapNeko/NapCatQQ)
2. 下载最新版本的 `NapCat.Shell` 压缩包
3. 解压到项目根目录，确保目录结构如下：

   ```txt
   Undercover-Bot/
   ├── NapCat.Shell/     # NapCat 框架目录
   ├── src/             # 项目源代码
   ├── config/          # 配置文件
   └── ...
   ```

#### 4. 配置环境

```bash
# 复制配置文件（根据需求选择环境）
cp config/dev.yaml config/local.yaml

# 编辑配置文件，设置你的关键词和 NapCat API 地址
# 使用文本编辑器打开 config/local.yaml 进行修改
```

#### 5. 运行项目

```bash
# 设置环境变量（可选，默认为 dev 环境）
set APP_ENV=local  # Windows
# 或 export APP_ENV=local  # Linux/Mac

# 启动机器人
python -m src.bot.main
```

### 方式二：通过 ZIP 包下载（推荐普通用户）

#### 1. 下载项目

1. 访问项目 Gitee 页面
2. 点击右上角的 "克隆/下载" 按钮
3. 选择 "下载 ZIP"
4. 解压到本地目录

#### 2. 安装 Python 环境

1. 下载并安装 [Python 3.9+](https://www.python.org/downloads/)
2. 安装时务必勾选 "Add Python to PATH"

#### 3. 安装依赖包

打开命令提示符或终端，进入项目目录：

```bash
cd 你的解压目录/Undercover-Bot
pip install -r requirements.txt
```

#### 4. 下载并配置 NapCat

1. 从 [NapCat 发布页面](https://github.com/NapNeko/NapCatQQ/releases) 下载最新版
2. 解压得到 `NapCat.Shell` 文件夹
3. 将整个文件夹移动到项目根目录下

#### 5. 首次运行配置

```bash
# 首次运行会引导登录
python -m src.bot.main
```

按照屏幕提示选择登录方式：

- **快捷登录**：使用本地缓存的 QQ 账号
- **账号密码登录**：输入 QQ 号和密码
- **扫码登录**：使用手机 QQ 扫描二维码

### 配置文件说明

项目提供三种预设配置：

- `config/dev.yaml` - 开发环境配置
- `config/test.yaml` - 测试环境配置  
- `config/prod.yaml` - 生产环境配置

你可以通过设置 `APP_ENV` 环境变量来切换配置，或创建自己的配置文件：

```yaml
# config/local.yaml 示例
napcat_api: "http://127.0.0.1:3000"  # NapCat WebUI 地址
keywords:
  - "炸群"
  - "举报"
  - "兄弟们"
  # 添加你的自定义关键词
```

### 常见问题

#### Q1: NapCat 启动失败怎么办？

- 确保已下载正确的 NapCat 版本
- 检查 `NapCat.Shell` 目录是否在项目根目录
- 尝试手动运行 `NapCat.Shell/launcher-user.bat`

#### Q2: 依赖安装失败？

- 确保 Python 版本为 3.9+
- 尝试使用国内镜像源：`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`

#### Q3: 登录时遇到问题？

- 确保 NapCat WebUI 已正常启动（默认地址：<http://127.0.0.1:6099）>
- 检查网络连接
- 尝试不同的登录方式

### 下一步

成功部署后，你可以：

1. 修改 `config/` 下的配置文件，添加监控关键词
2. 查看 `src/bot/main.py` 了解消息处理逻辑
3. 参与项目开发，提交 Issue 或 Pull Request

***

## 交流方式

- Gitee Issues：直接在此仓库提问
- QQ扯皮群；1083803674

***

## 开源协议

本项目采用 **GNU General Public License v3.0**，这意味着；

- 你可以自由使用、修改、分发本代码
- 但任何分发（包括修改后的版本）都必须同样采用 GPL-3.0 协议开源
- 如果你将本项目用于网络服务，建议查阅 GPL-3.0 关于聚合体的条款

**我(们)的愿景**希望这个项目能被用于保护网络环境、维护社区清朗， **而不是用于恶意攻击、侵犯隐私或任何违法违规行为**。技术本身是中立的，但使用者应有底线。愿每一位开发者都心怀善意。

***

## 特别声明

- 本项目由一名高一学生在课余时间独立开发，技术水平有限，代码并不优雅，  **架构也可能随时调整** 。
- 开发过程中会 **大量使用 AI 辅助编程** ，甚至某些模块 **可能由AI代劳** ，代码风格可能会比较“AI味”，介意的朋友请轻拍。
- 由于学业压力，项目**可能随时暂停更新或直接崩解**，我会尽力维护。
- **请勿将本项目用于任何攻击性、违法违规或侵犯他人权益的行为**。再次强调， **技术无罪，但使用者应有底线。**
- 本项目使用了 Napcat 等第三方开源库，感谢这些项目的作者。但**本项目与这些第三方库的作者无关，任何因本项目引发的问题请勿牵连他们**，如有问题请优先在本仓库及扯皮群反馈。
- 使用本项目前， **请务必阅读并同意[用户协议](TERMS.md)** ，该协议详细说明了 **免责条款**和 **合法使用承诺**。
- 如果你能接受以上“佛系”状态，欢迎一起玩耍、贡献代码或提出建议！

**让我们一起，让网络环境更清朗！**
