# 源代码目录

| 子目录 | 职责 | 入口文件 | 配置加载方式 | 依赖关系 |
| :--- | :--- | :--- | :--- | :--- |
| bot | 核心机器人逻辑，处理消息上报与回复 | main.py | config/ 目录下的 yaml 文件 | NapCat.Shell (OneBot 协议) |
| tests | 单元测试与集成测试 | N/A | config/test.yaml | pytest |
