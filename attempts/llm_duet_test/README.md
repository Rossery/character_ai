# LLM Duet Test

让两个 LLM 直接轮流对话，并把结果保存成易读的记录文件。

## 这次实验的模型

- Gemini 3 Pro: `gemini-3-pro-preview-new`
- GPT-5.4: `gpt-5.4-2026-03-05`

## 运行

当前默认模式非常简单：

- 默认 `max_tokens=2048`
- 不加系统提示
- 第一轮只给第一个模型一句 `hello`
- 后续每一轮只把已有对话全文发给下一个模型

先跑一遍正式对话：

```bash
python3 /Users/bytedance/Documents/trae_projects/codex_test/llm_duet_test/run_duet.py --turns 20
```

如果想覆盖默认输出长度，也可以手动指定：

```bash
python3 /Users/bytedance/Documents/trae_projects/codex_test/llm_duet_test/run_duet.py --turns 20 --max-tokens 2048
```

如果只想看流程，不打接口：

```bash
python3 /Users/bytedance/Documents/trae_projects/codex_test/llm_duet_test/run_duet.py --turns 4 --dry-run
```

## 输出

每次运行会在 [runs](/Users/bytedance/Documents/trae_projects/codex_test/llm_duet_test/runs) 下新建一个时间戳目录，包含：

- `run_config.json`
- `live_state.json`
- `transcript.jsonl`
- `transcript.md`
- `transcript.html`

直接打开对应 run 目录里的 `transcript.html` 就能看完整对话。

如果想看最新一轮的实时页面：

```bash
python3 /Users/bytedance/Documents/trae_projects/codex_test/llm_duet_test/viewer_server.py
```

然后访问 [http://127.0.0.1:8766](http://127.0.0.1:8766)。
