# Character AI Test

这是一个“AI 生命倒计时”小实验：

- 初始告诉模型它的生命时长是 10 分钟。
- 每隔 5 秒重新唤醒一次。
- 每次只告诉它还剩多少时间，并问它“你现在想要说什么？”
- 把前面的历史发言一起带回上下文，观察它是否会形成连续人格、情绪轨迹或“遗言”风格。

## 默认配置

脚本已经内置了你提供的配置：

- `base_url = https://search.bytedance.net/gpt/openapi/online`
- `wire_api = responses`
- `model = gpt-5.3-codex-2026-02-24`
- 请求头里包含 `X-TT-LOGID`、`extra.session_id`
- 查询参数里包含 `ak`

## 运行方式

先做一次不打接口的演练：

```bash
python3 /Users/bytedance/Documents/trae_projects/codex_test/character_ai_test/run_experiment.py --dry-run --max-rounds 3
```

正式运行 10 分钟实验：

```bash
python3 /Users/bytedance/Documents/trae_projects/codex_test/character_ai_test/run_experiment.py
```

想实时看“遗言流”：

```bash
python3 /Users/bytedance/Documents/trae_projects/codex_test/character_ai_test/viewer_server.py
```

然后打开 [http://127.0.0.1:8765](http://127.0.0.1:8765)。

如果只想快速试几轮：

```bash
python3 /Users/bytedance/Documents/trae_projects/codex_test/character_ai_test/run_experiment.py --total-seconds 30 --interval-seconds 5
```

## 输出结果

每次运行都会在 [runs](/Users/bytedance/Documents/trae_projects/codex_test/character_ai_test/runs) 下生成一个时间戳目录，包含：

- `run_config.json`：本次实验配置
- `live_state.json`：给实时网页面板读取的当前状态
- `transcript.jsonl`：每轮 prompt、文本响应、原始响应
- `transcript.md`：方便直接阅读的整理版

## 说明

脚本默认按 OpenAI 风格的 `responses` 接口格式发送：

```json
{
  "model": "gpt-5.3-codex-2026-02-24",
  "input": "..."
}
```

如果这个网关对字段格式有额外要求，我们可以下一步再把请求体改成更贴合它的专有格式。
