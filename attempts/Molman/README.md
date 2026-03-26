## Molman

### 终端聊天 UI

1. 配置模型与 prompt（默认读取 `molman.yaml`）
2. 启动终端聊天

```bash
cd /Users/bytedance/Documents/trae_projects/Molman
uv sync
uv run molman-chat
```

快捷键与指令：
- `Enter` 发送消息
- `Ctrl+R` 重置会话（新的 thread_id）
- `/reset` 重置会话
- `/exit` 退出
