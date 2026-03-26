# Agent Memory 论文 Survey（2025-08-01 之后）

## 1. 数据收集说明
- 时间范围：2025-08-01T00:00:00+00:00（含）之后
- 数据源：arXiv（通过 `export.arxiv.org/api/query` ATOM 接口）
- 检索关键词（部分）：all:"agent memory", all:"agentic memory", all:"long-term memory" AND all:agent, all:"episodic memory" AND all:agent, all:"memory augmented" AND all:agent, all:"persistent memory" AND all:agent, all:"personal memory" AND all:agent, all:"memory" AND all:"LLM agent", all:"memory" AND all:"AI agent", all:"multi-agent" AND all:memory
- 下载成功：62 篇 PDF（本次 survey 覆盖全部 62 篇）
- 说明：Google Scholar 通常需要交互式访问且对自动抓取有限制，本次优先保证可公开下载的 arXiv 原文。

## 2. 主要研究方向（按“标题+摘要”关键词粗分类）
说明：以下为基于关键词的粗分类统计，类别非互斥（同一论文可同时计入多个方向）。
- 评测与基准（Benchmarks & Metrics）：44 篇
- 外部记忆系统/结构（Vector/KV/Graph/Index/Retrieval）：44 篇
- 多智能体共享/协作记忆（Multi-agent/Shared Memory）：21 篇
- 记忆写入/整理/巩固/遗忘（Consolidation/Editing/Forgetting）：19 篇
- 个性化/用户记忆（Personalization/Profile/Preference）：17 篇
- 隐私/安全（Privacy/Security/Attack/Defense）：12 篇

## 3. 主要问题（社区共识）
- 记忆写入噪声与漂移：长期交互中‘无关/错误/过期’信息被写入导致检索污染，出现幻觉放大。
- 记忆压缩与保真权衡：摘要/聚合会损失可追溯细节；保留细节则带来存储与检索成本。
- 何时写、写什么、写到哪：触发条件（事件/用户意图/工具调用）、粒度（片段/事实/技能）、存储结构（向量/图/层级）缺少统一原则。
- 评测口径不统一：‘记住’到底指事实准确、行为一致、个性化稳定还是任务完成率提升？可复现 benchmark 仍不足。
- 隐私与可控遗忘：用户数据/偏好进入长期记忆后，如何可解释、可删除、可审计。
- 安全风险外溢：注入攻击会跨 session 持久化；以及个性化记忆会引入新的安全失败模式。

## 4. 常见方法谱系（方法论视角）
- 外部记忆 + 检索（RAG/向量库/混合检索）：把记忆当知识库，核心是写入/索引/召回与重排。
- 层级记忆（Working/Episodic/Semantic/Procedural）：短期上下文与长期档案分层管理，周期性巩固与摘要。
- 记忆编辑与质量控制：去重、置信度打分、冲突检测、时间衰减、‘写前校验/写后清洗’。
- 结构化记忆：把任务树/账本/状态机/知识图谱作为显式状态，让 agent 在结构上读写。
- 共享/群体记忆：多智能体把经验写入公共黑板/共享库，用于协作分工与一致性。
- 记忆驱动的个性化：把偏好/画像作为可检索对象注入策略与生成（提示/工具选择/输出风格）。
- 安全优先的记忆治理：隔离外部内容、schema 校验、可审计边界与可删除策略。

## 5. Benchmark 与评测建议
### 5.1 在摘要中出现的基准（出现论文数，按频次）
- LoCoMo: 12
- LongMemEval: 5
- HotpotQA: 2
- PERSONAMEM: 2
- ALFWorld: 1
- CAME-Bench: 1
- LTI-Bench: 1
- MemBench: 1
- Multi-Session Chat: 1
- PerLTQA: 1

### 5.2 适合评测 Agent Memory 的 benchmark 选择建议
- 长程依赖/多轮任务：更能暴露‘记住并持续一致’能力（如长文/长对话、跨回合任务）。
- Agentic 场景评测：优先多 session + 任务耦合（如 MemoryArena），避免只测“读后问答”。
- 结构化记忆能力：加入账本、TODO、树等结构任务（如 StructMemEval 思路）。
- 任务型环境：WebArena、ALFWorld 等，可量化任务成功率与代价（步数/成本）。
- 个性化一致性：需要构造用户画像/偏好集，评价偏好满足率 + 事实一致性 + 遗忘/更新能力。
- 安全与隐私：注入攻击与个性化带来的安全退化应纳入回归（如 PS-Bench、注入持久化攻击）。

## 6. 论文清单与逐篇总结（中文）
说明：逐篇总结基于 arXiv 摘要（`metadata/arxiv_agent_memory_papers.json` 的 `summary` 字段）进行中文改写/翻译；专有名词（模型/基准/系统名）保留英文。

### 6.1 清单（索引）
|#|发布日期|标题|arXiv|PDF文件|
|---:|---|---|---|---|
|1|2026-02-25|Pancake: Hierarchical Memory System for Multi-Agent LLM Serving|2602.21477v1|01_2602.21477v1.pdf|
|2|2026-02-24|MemoPhishAgent: Memory-Augmented Multi-Modal LLM Agent for Phishing URL Detection|2602.21394v1|02_2602.21394v1.pdf|
|3|2026-02-22|VLM-Guided Group Preference Alignment for Diffusion-based Human Mesh Recovery|2602.19180v1|03_2602.19180v1.pdf|
|4|2026-02-18|MemoryArena: Benchmarking Agent Memory in Interdependent Multi-Session Agentic Tasks|2602.16313v1|04_2602.16313v1.pdf|
|5|2026-02-17|Zombie Agents: Persistent Control of Self-Evolving LLM Agents via Self-Reinforcing Injections|2602.15654v1|05_2602.15654v1.pdf|
|6|2026-02-17|EventMemAgent: Hierarchical Event-Centric Memory for Online Video Understanding with Adaptive Tool Use|2602.15329v1|06_2602.15329v1.pdf|
|7|2026-02-17|EAA: Automating materials characterization with vision language model agents|2602.15294v1|07_2602.15294v1.pdf|
|8|2026-02-17|When Remembering and Planning are Worth it: Navigating under Change|2602.15274v1|08_2602.15274v1.pdf|
|9|2026-02-15|Choosing How to Remember: Adaptive Memory Structures for LLM Agents|2602.14038v1|09_2602.14038v1.pdf|
|10|2026-02-13|REMem: Reasoning with Episodic Memory in Language Agent|2602.13530v2|10_2602.13530v2.pdf|
|11|2026-02-11|Evaluating Memory Structure in LLM Agents|2602.11243v1|11_2602.11243v1.pdf|
|12|2026-02-11|From Prompt-Response to Goal-Directed Systems: The Evolution of Agentic AI Software Architecture|2602.10479v1|12_2602.10479v1.pdf|
|13|2026-02-09|MemAdapter: Fast Alignment across Agent Memory Paradigms via Generative Subgraph Retrieval|2602.08369v1|13_2602.08369v1.pdf|
|14|2026-02-08|Learning to Continually Learn via Meta-learning Agentic Memory Designs|2602.07755v1|14_2602.07755v1.pdf|
|15|2026-02-07|AgentSys: Secure and Dynamic LLM Agents Through Explicit Hierarchical Memory Management|2602.07398v1|15_2602.07398v1.pdf|
|16|2026-02-05|Learning Query-Aware Budget-Tier Routing for Runtime Agent Memory|2602.06025v1|16_2602.06025v1.pdf|
|17|2026-02-05|Graph-based Agent Memory: Taxonomy, Techniques, and Applications|2602.05665v1|17_2602.05665v1.pdf|
|18|2026-02-04|Towards Structured, State-Aware, and Execution-Grounded Reasoning for Software Engineering Agents|2602.04640v1|18_2602.04640v1.pdf|
|19|2026-02-03|Memora: A Harmonic Memory Representation Balancing Abstraction and Specificity|2602.03315v1|19_2602.03315v1.pdf|
|20|2026-02-03|TAME: A Trustworthy Test-Time Evolution of Agent Memory with Systematic Benchmarking|2602.03224v1|20_2602.03224v1.pdf|
|21|2026-02-03|LatentMem: Customizing Latent Memory for Multi-Agent Systems|2602.03036v1|21_2602.03036v1.pdf|
|22|2026-02-02|MemSkill: Learning and Evolving Memory Skills for Self-Evolving Agents|2602.02474v1|22_2602.02474v1.pdf|
|23|2026-02-02|Co-RedTeam: Orchestrated Security Discovery and Exploitation with LLM Agents|2602.02164v2|23_2602.02164v2.pdf|
|24|2026-02-02|Beyond RAG for Agent Memory: Retrieval by Decoupling and Aggregation|2602.02007v2|24_2602.02007v2.pdf|
|25|2026-01-30|"Someone Hid It": Query-Agnostic Black-Box Attacks on LLM-Based Retrieval|2602.00364v3|25_2602.00364v3.pdf|
|26|2026-01-30|MiTa: A Hierarchical Multi-Agent Collaboration Framework with Memory-integrated and Task Allocation|2601.22974v1|26_2601.22974v1.pdf|
|27|2026-01-29|E-mem: Multi-agent based Episodic Context Reconstruction for LLM Agent Memory|2601.21714v1|27_2601.21714v1.pdf|
|28|2026-01-28|BMAM: Brain-inspired Multi-Agent Memory Framework|2601.20465v1|28_2601.20465v1.pdf|
|29|2026-01-28|AMA: Adaptive Memory via Multi-Agent Collaboration|2601.20352v2|29_2601.20352v2.pdf|
|30|2026-01-28|Me-Agent: A Personalized Mobile Agent with Two-Level User Habit Learning for Enhanced Interaction|2601.20162v1|30_2601.20162v1.pdf|
|31|2026-01-26|FadeMem: Biologically-Inspired Forgetting for Efficient Agent Memory|2601.18642v2|31_2601.18642v2.pdf|
|32|2026-01-25|When Personalization Legitimizes Risks: Uncovering Safety Vulnerabilities in Personalized Dialogue Agents|2601.17887v1|32_2601.17887v1.pdf|
|33|2026-01-23|From Atom to Community: Structured and Evolving Agent Memory for User Behavior Modeling|2601.16872v2|33_2601.16872v2.pdf|
|34|2026-01-23|EMemBench: Interactive Benchmarking of Episodic Memory for VLM Agents|2601.16690v1|34_2601.16690v1.pdf|
|35|2026-01-21|Memory Retention Is Not Enough to Master Memory Tasks in Reinforcement Learning|2601.15086v1|35_2601.15086v1.pdf|
|36|2026-01-21|HiNS: Hierarchical Negative Sampling for More Comprehensive Memory Retrieval Embedding Model|2601.14857v1|36_2601.14857v1.pdf|
|37|2026-01-21|Optimizing FaaS Platforms for MCP-enabled Agentic Workflows|2601.14735v2|37_2601.14735v2.pdf|
|38|2026-01-19|Prompt Injection Mitigation with Agentic AI, Nested Learning, and AI Sustainability via Semantic Caching|2601.13186v1|38_2601.13186v1.pdf|
|39|2026-01-15|Grounding Agent Memory in Contextual Intent|2601.10702v1|39_2601.10702v1.pdf|
|40|2026-01-15|Role-Playing Agents Driven by Large Language Models: Current Status, Challenges, and Future Trends|2601.10122v1|40_2601.10122v1.pdf|
|41|2026-01-14|Rethinking Memory Mechanisms of Foundation Agents in the Second Half: A Survey|2602.06052v3|41_2602.06052v3.pdf|
|42|2026-01-14|CAST: Character-and-Scene Episodic Memory for Agents|2602.06051v3|42_2602.06051v3.pdf|
|43|2026-01-14|The AI Hippocampus: How Far are We From Human Memory?|2601.09113v1|43_2601.09113v1.pdf|
|44|2026-01-13|AtomMem : Learnable Dynamic Agentic Memory with Atomic Memory Operation|2601.08323v2|44_2601.08323v2.pdf|
|45|2026-01-13|SwiftMem: Fast Agentic Memory via Query-aware Indexing|2601.08160v1|45_2601.08160v1.pdf|
|46|2026-02-19|El Agente Gráfico: Structured Execution Graphs for Scientific Agents|2602.17902v1|46_2602.17902v1.pdf|
|47|2026-02-14|A Tale of Two Graphs: Separating Knowledge Exploration from Outline Structure for Open-Ended Deep Research|2602.13830v1|47_2602.13830v1.pdf|
|48|2026-02-04|KGLAMP: Knowledge Graph-guided Language model for Adaptive Multi-robot Planning and Replanning|2602.04129v1|48_2602.04129v1.pdf|
|49|2026-01-31|Factored Reasoning with Inner Speech and Persistent Memory for Evidence-Grounded Human-Robot Interaction|2602.00675v1|49_2602.00675v1.pdf|
|50|2026-01-12|Cost and accuracy of long-term memory in Distributed Multi-Agent Systems based on Large Language Models|2601.07978v2|50_2601.07978v2.pdf|
|51|2025-12-29|CASCADE: Cumulative Agentic Skill Creation through Autonomous Development and Evolution|2512.23880v2|51_2512.23880v2.pdf|
|52|2025-12-16|GR-Agent: Adaptive Graph Reasoning Agent under Incomplete Knowledge|2512.14766v1|52_2512.14766v1.pdf|
|53|2025-12-14|Memoria: A Scalable Agentic Memory Framework for Personalized Conversational AI|2512.12686v1|53_2512.12686v1.pdf|
|54|2025-12-11|Decoding Student Minds: Leveraging Conversational Agents for Psychological and Learning Analysis|2512.10441v1|54_2512.10441v1.pdf|
|55|2025-12-04|SEAL: Self-Evolving Agentic Learning for Conversational Question Answering over Knowledge Graphs|2512.04868v1|55_2512.04868v1.pdf|
|56|2025-11-04|ReAcTree: Hierarchical LLM Agent Trees with Control Flow for Long-Horizon Task Planning|2511.02424v2|56_2511.02424v2.pdf|
|57|2025-10-22|Learning from Supervision with Semantic and Episodic Memory: A Reflective Approach to Agent Adaptation|2510.19897v1|57_2510.19897v1.pdf|
|58|2025-10-10|Agentic-KGR: Co-evolutionary Knowledge Graph Construction through Multi-Agent Reinforcement Learning|2510.09156v1|58_2510.09156v1.pdf|
|59|2025-09-08|REMI: A Novel Causal Schema Memory Architecture for Personalized Lifestyle Recommendation Agents|2509.06269v1|59_2509.06269v1.pdf|
|60|2025-09-03|Lattice Annotated Temporal (LAT) Logic for Non-Markovian Reasoning|2509.02958v1|60_2509.02958v1.pdf|
|61|2025-08-22|Memento: Fine-tuning LLM Agents without Fine-tuning LLMs|2508.16153v2|61_2508.16153v2.pdf|
|62|2025-08-05|Long Story Generation via Knowledge Graph and Literary Theory|2508.03137v1|62_2508.03137v1.pdf|

### 6.2 逐篇中文摘要（问题 / 方法 / 实验）

#### 1. Pancake: Hierarchical Memory System for Multi-Agent LLM Serving
- arXiv: 2602.21477v1
- 发布日期: 2026-02-25
- 链接: http://arxiv.org/abs/2602.21477v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/01_2602.21477v1.pdf
- 摘要（中文）: 论文聚焦 LLM serving 场景下的 agentic memory 管理：大规模存储、频繁更新、多 agent 共存会把检索压力集中到高成本的 ANN 搜索上。作者提出多层级的记忆系统 `Pancake`，结合单 agent 的多级索引缓存、跨 agent 的协同索引管理、以及 GPU-CPU 协同加速；同时提供可集成到 Mem-GPT、LangChain、LlamaIndex 等框架的接口。在真实 agent 工作负载上，端到端吞吐提升超过 4.29×。

#### 2. MemoPhishAgent: Memory-Augmented Multi-Modal LLM Agent for Phishing URL Detection
- arXiv: 2602.21394v1
- 发布日期: 2026-02-24
- 链接: http://arxiv.org/abs/2602.21394v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/02_2602.21394v1.pdf
- 摘要（中文）: 传统钓鱼站点检测依赖静态规则/黑名单，难以跟上攻击快速演化；即便引入 LLM，许多系统仍是“prompt 驱动的确定性流水线”，没充分用到推理能力。作者提出 `MemoPhishAgent (MPA)`：多模态 LLM agent 动态编排钓鱼检测工具，并利用过往推理轨迹的情景记忆（episodic memory）指导对重复/新型威胁的决策。两套公开数据集上召回提升 13.6%；在 5 个社媒平台抓取的真实可疑 URL 基准上召回提升 20%，分析显示 episodic memory 贡献最高可达 27% 的召回增益且无额外计算开销；并给出生产部署结果（每周处理 60K 高风险 URL，召回 91.44%）。

#### 3. VLM-Guided Group Preference Alignment for Diffusion-based Human Mesh Recovery
- arXiv: 2602.19180v1
- 发布日期: 2026-02-22
- 链接: http://arxiv.org/abs/2602.19180v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/03_2602.19180v1.pdf
- 摘要（中文）: 该论文主题为 Human Mesh Recovery（HMR），并非典型“Agent Memory”研究；其“memory”主要用作 critique agent 的双记忆增强机制。作者针对扩散式 HMR 在遮挡/复杂场景下容易出现物理不合理或与输入图像不一致的问题，引入带自反思的 dual-memory 增强 critique agent 生成质量分数，并据此构建 group-wise 偏好数据集来微调扩散 HMR 模型。实验显示优于 SOTA。

#### 4. MemoryArena: Benchmarking Agent Memory in Interdependent Multi-Session Agentic Tasks
- arXiv: 2602.16313v1
- 发布日期: 2026-02-18
- 链接: http://arxiv.org/abs/2602.16313v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/04_2602.16313v1.pdf
- 摘要（中文）: 论文指出现有记忆评测常把“记住（memorization）”与“行动（action）”割裂：要么只考对话/文本回忆，要么在单 session 任务里不需要长期记忆。作者提出 `MemoryArena`：一个面向多 session 的 Memory-Agent-Environment 循环评测 gym，任务由人工设计且子任务显式相互依赖，agent 必须从早期行为/反馈中提炼经验写入记忆，并在后续 session 中使用记忆完成整体目标。评测覆盖 web navigation、偏好约束规划、渐进信息搜索、顺序形式化推理等；结果显示在 LoCoMo 等长上下文记忆基准接近饱和的 agent，在该更“agentic”的设定下表现仍显著不足，暴露评测口径缺口。

#### 5. Zombie Agents: Persistent Control of Self-Evolving LLM Agents via Self-Reinforcing Injections
- arXiv: 2602.15654v1
- 发布日期: 2026-02-17
- 链接: http://arxiv.org/abs/2602.15654v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/05_2602.15654v1.pdf
- 摘要（中文）: 自进化（self-evolving）的 LLM agent 会跨 session 更新内部状态，常见方式是写入并复用 long-term memory，这能提升长任务表现但也带来安全风险：不可信外部内容可能被写入记忆并在未来被当成“指令”。论文形式化提出 `Zombie Agent` 持久化攻击：攻击者通过控制网页等外部内容在感染阶段埋 payload，payload 被 agent 正常记忆更新流程写入；在触发阶段 payload 被检索/带入后导致未授权工具行为。作者针对滑窗记忆、RAG 记忆等实现设计持久化策略，并在多种 agent 设定与任务上评测持久性与未授权行为诱发能力，结论是“跨会话的记忆演化”会把一次性间接注入变成长期控制，单纯的 per-session 过滤不足以防御。

#### 6. EventMemAgent: Hierarchical Event-Centric Memory for Online Video Understanding with Adaptive Tool Use
- arXiv: 2602.15329v1
- 发布日期: 2026-02-17
- 链接: http://arxiv.org/abs/2602.15329v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/06_2602.15329v1.pdf
- 摘要（中文）: 在线视频理解要在“无限流式输入”与 MLLM 有限 context window 之间取舍：被动处理往往在长程上下文与细粒度细节间权衡困难。作者提出 `EventMemAgent`：以层级记忆为核心的主动式在线视频 agent。短期记忆负责检测事件边界，并用事件粒度的 reservoir sampling 在固定缓冲区内动态处理帧；长期记忆按事件归档历史观测；再配合多粒度感知工具箱与 Agentic RL，把推理与工具使用策略端到端内化到 agent。论文称在在线视频基准上达到有竞争力表现，并提供代码仓库链接。

#### 7. EAA: Automating materials characterization with vision language model agents
- arXiv: 2602.15294v1
- 发布日期: 2026-02-17
- 链接: http://arxiv.org/abs/2602.15294v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/07_2602.15294v1.pdf
- 摘要（中文）: 作者提出 `Experiment Automation Agents (EAA)`，用于自动化显微实验工作流的 vision-language agent 系统。系统结合多模态推理、工具增强行动与“可选”的长期记忆，支持全自动流程与交互式用户引导测量；基于任务管理器架构，既可 agent 驱动也可在规则化流程中嵌入局部 LLM 查询。工具生态支持 Model Context Protocol (MCP) 的双向兼容。作者在 Advanced Photon Source 的成像 beamline 展示了自动对焦、自然语言特征搜索、交互式采集等应用，强调提升效率与降低门槛。

#### 8. When Remembering and Planning are Worth it: Navigating under Change
- arXiv: 2602.15274v1
- 发布日期: 2026-02-17
- 链接: http://arxiv.org/abs/2602.15274v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/08_2602.15274v1.pdf
- 摘要（中文）: 论文研究在“非平稳 + 不确定”的空间导航任务中，哪些记忆与规划策略值得使用：障碍与食物位置会随天变化，且定位等感知信息有限且带噪。作者比较从简单到复杂的多种策略，结论是需要能组合多策略的架构：在未知食物位置时更偏探索/搜索；在“记忆到的可能食物位置”上需要在线建图与规划。使用非平稳概率学习持续更新情景记忆（episodic memories），并据此构建“基于经历的不完美地图”进行在线规划，可在任务难度提升且不确定性不过大的条件下显著优于最小记忆方案。

#### 9. Choosing How to Remember: Adaptive Memory Structures for LLM Agents
- arXiv: 2602.14038v1
- 发布日期: 2026-02-15
- 链接: http://arxiv.org/abs/2602.14038v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/09_2602.14038v1.pdf
- 摘要（中文）: 作者指出一刀切的记忆结构无法适应异质交互模式，且缺少把“选哪种记忆结构”建模为上下文自适应决策的机制。论文提出统一框架 `FluxMem`：为 agent 配置多种互补记忆结构，并学习基于交互级特征的结构选择策略；监督信号来自下游回答质量与记忆利用率。为支持长期记忆演化，还引入三级记忆层次与基于 Beta Mixture Model 的概率门控做分布感知的记忆融合，替代脆弱的相似度阈值。在 PERSONAMEM 与 LoCoMo 上平均提升分别为 9.18% 与 6.14%。

#### 10. REMem: Reasoning with Episodic Memory in Language Agent
- arXiv: 2602.13530v2
- 发布日期: 2026-02-13
- 链接: http://arxiv.org/abs/2602.13530v2
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/10_2602.13530v2.pdf
- 摘要（中文）: 人类的 episodic memory 能按时空上下文记住“具体经历”并跨事件推理；而语言 agent 的记忆多偏语义，难以有效回忆并基于交互历史进行复杂推理。论文提出两阶段框架 `REMem`：离线阶段把经历转成混合 memory graph，连接时间感知的 gists 与 facts；在线阶段用带工具的 agentic retriever 在图上迭代检索。作者在 4 个 episodic memory 基准上评测，称相对 Mem0、HippoRAG 2 在 episodic recollection 与 reasoning 任务上分别提升 3.4% 与 13.4% 绝对值，并表现出更稳健的“不可回答拒答”行为。

#### 11. Evaluating Memory Structure in LLM Agents
- arXiv: 2602.11243v1
- 发布日期: 2026-02-11
- 链接: http://arxiv.org/abs/2602.11243v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/11_2602.11243v1.pdf
- 摘要（中文）: 现有长期记忆评测往往只测事实保留、多跳回忆或时间变化，很多能力用简单 RAG 就能做到，难以区分“复杂记忆层级/结构”的价值。论文提出 `StructMemEval`：专门测试 agent 是否能把长期记忆组织成特定结构（如账本、todo list、树结构等）来完成任务。初步实验显示简单 RAG 在此类任务上较弱；而 memory agent 在被明确提示如何组织记忆时能更可靠，但现代 LLM 并不总能在“未被提示”时主动识别/采用合适结构，提示未来需要改进训练与记忆框架。

#### 12. From Prompt-Response to Goal-Directed Systems: The Evolution of Agentic AI Software Architecture
- arXiv: 2602.10479v1
- 发布日期: 2026-02-11
- 链接: http://arxiv.org/abs/2602.10479v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/12_2602.10479v1.pdf
- 摘要（中文）: 论文从软件架构角度讨论 agentic AI 从无状态 prompt 生成走向“目标驱动系统”，强调通过控制循环实现自主感知、规划、行动与适应。作者把经典智能体理论（reactive/deliberative/BDI）与当代 LLM 方案（工具调用、记忆增强推理、多 agent 协作）连接起来，给出生产级参考架构（typed tool 接口将推理与执行分离）、多 agent 拓扑与失效模式/缓解手段的 taxonomy，以及企业落地的 hardening checklist（治理、可观测性、可复现）。更多偏“业界架构归纳”，不是单一记忆算法。

#### 13. MemAdapter: Fast Alignment across Agent Memory Paradigms via Generative Subgraph Retrieval
- arXiv: 2602.08369v1
- 发布日期: 2026-02-09
- 链接: http://arxiv.org/abs/2602.08369v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/13_2602.08369v1.pdf
- 摘要（中文）: 论文认为现有 agent memory 往往各自为政（explicit/parametric/latent memory 等范式彼此隔离），检索方法与范式强耦合，阻碍跨范式泛化与融合。作者提出 `MemAdapter`：通过生成式子图检索（generative subgraph retriever）实现跨范式对齐。训练分两阶段：先在统一记忆空间训练生成式检索器；再用对比学习训练轻量对齐模块，把检索器适配到未见过的记忆范式。实验在 3 个公开评测基准上显示相对多种强 baseline 与 memory 系统更优；并称在单 GPU 上 13 分钟即可完成跨范式对齐，计算量 <5%，且支持 zero-shot 融合。

#### 14. Learning to Continually Learn via Meta-learning Agentic Memory Designs
- arXiv: 2602.07755v1
- 发布日期: 2026-02-08
- 链接: http://arxiv.org/abs/2602.07755v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/14_2602.07755v1.pdf
- 摘要（中文）: 基础模型无状态限制了 agentic 系统的 test-time continual learning，工程上常加入 memory 模块来复用经验，但多为人工固定设计，难以适应现实任务的多样与非平稳。论文提出 `ALMA`：用 meta-learning 让 `Meta Agent` 在开放空间中搜索“可执行代码表达的记忆设计”（包括数据库 schema、检索与更新机制），以替代手工方案。作者在 4 个序列决策领域做实验，称学习得到的 memory 设计在全部基准上比 SOTA 人工设计更有效、更高效，并强调安全部署前提下有助于“自我改进”的持续学习。

#### 15. AgentSys: Secure and Dynamic LLM Agents Through Explicit Hierarchical Memory Management
- arXiv: 2602.07398v1
- 发布日期: 2026-02-07
- 链接: http://arxiv.org/abs/2602.07398v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/15_2602.07398v1.pdf
- 摘要（中文）: 间接 prompt injection 会把恶意指令嵌入外部内容，引发未授权行为/数据窃取。传统 agent 往往把工具输出与推理痕迹不加区分地累积进工作记忆（context window），导致注入指令长期驻留且冗余内容降低决策质量。论文提出 `AgentSys`：借鉴操作系统进程隔离，把主 agent 与工具调用 worker agent 分离，worker 在隔离上下文运行且可递归派生；外部数据与子任务轨迹不进入主 agent，只允许 schema 校验后的返回值通过确定性的 JSON 解析跨边界。消融显示仅隔离可把攻击成功率降到 2.19%，再加 validator/sanitizer 可进一步提升；在 AgentDojo 与 ASB 上攻击成功率分别为 0.78% 与 4.25%，同时对 benign utility 略有提升，并称对自适应攻击者与多种模型均稳健。

#### 16. Learning Query-Aware Budget-Tier Routing for Runtime Agent Memory
- arXiv: 2602.06025v1
- 发布日期: 2026-02-05
- 链接: http://arxiv.org/abs/2602.06025v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/16_2602.06025v1.pdf
- 摘要（中文）: 许多记忆系统依赖离线、与 query 无关的记忆构建，可能低效且丢掉 query 关键的信息；而 runtime memory 虽自然，但常有高开销且难以显式控制“性能-成本”权衡。论文提出 `BudgetMem`：把记忆处理拆成多个 memory module，每个模块提供 Low/Mid/High 三档预算，并用轻量 router（紧凑神经策略 + RL 训练）对模块做 budget-tier routing，从而实现 query-aware 的显式控成本。作者在 LoCoMo、LongMemEval、HotpotQA 上评测，称在高预算优先性能时超过强 baseline，在低预算时给出更优 accuracy-cost frontier，并分析不同 tiering 轴（实现复杂度/推理行为/容量）在不同预算下的优劣。

#### 17. Graph-based Agent Memory: Taxonomy, Techniques, and Applications
- arXiv: 2602.05665v1
- 发布日期: 2026-02-05
- 链接: http://arxiv.org/abs/2602.05665v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/17_2602.05665v1.pdf
- 摘要（中文）: 论文从 graph 视角综述 agent memory，认为图结构擅长表达关系依赖、组织层级信息并支持高效检索。综述首先给出 taxonomy（短期/长期、知识/经验、非结构化/结构化等），再按记忆生命周期系统梳理关键技术：抽取（把数据变成可存内容）、存储（组织）、检索（支持推理）、演化（更新）。同时汇总开源库与 benchmark，并讨论应用场景与未来挑战；作者还维护了资源合集 `Awesome-GraphMemory`。

#### 18. Towards Structured, State-Aware, and Execution-Grounded Reasoning for Software Engineering Agents
- arXiv: 2602.04640v1
- 发布日期: 2026-02-04
- 链接: http://arxiv.org/abs/2602.04640v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/18_2602.04640v1.pdf
- 摘要（中文）: 论文讨论 SE agent 的一个关键短板：当前多为“反应式”设计，主要依赖对话历史与最近回复，缺乏显式结构与持久状态（persistent state）表示，导致长程推理困难（无法维持一致理解、随新证据更新假设、吸收执行反馈）。作者主张走向“结构化、状态感知、执行落地（execution-grounded）”的推理方式，并给出下一代 SE agent 的初步路线图（偏立场论文）。

#### 19. Memora: A Harmonic Memory Representation Balancing Abstraction and Specificity
- arXiv: 2602.03315v1
- 发布日期: 2026-02-03
- 链接: http://arxiv.org/abs/2602.03315v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/19_2602.03315v1.pdf
- 摘要（中文）: 记忆要可扩展必须做抽象，但抽象会牺牲细节，影响推理所需的 specificity。论文提出 `Memora`：用“harmonic memory representation”在结构上平衡抽象与细节；以 primary abstractions 索引具体记忆值并把相关更新合并成统一条目，同时用 cue anchors 扩展检索入口、连接相关记忆；检索策略可利用这些连接超越纯语义相似度。理论上作者指出标准 RAG 与 KG memory 是其特例；实验上称在 LoCoMo 与 LongMemEval 上达到新的 SOTA，随记忆规模增长仍保持更好的检索相关性与推理效果。

#### 20. TAME: A Trustworthy Test-Time Evolution of Agent Memory with Systematic Benchmarking
- arXiv: 2602.03224v1
- 发布日期: 2026-02-03
- 链接: http://arxiv.org/abs/2602.03224v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/20_2602.03224v1.pdf
- 摘要（中文）: 论文把“test-time 演化记忆”视为提升复杂推理的重要范式，但指出即便在 benign 演化过程中也会出现安全对齐脆弱（Agent Memory Misevolution）。作者构建 `Trust-Memevo` 基准，用多维指标评测 benign 演化中的可信度，发现整体可信度会下降。为缓解，提出双记忆演化框架 `TAME`：分别演化 executor memory（提炼可泛化方法以提效）与 evaluator memory（根据历史反馈改进安全与效用评估）；通过过滤-草稿-可信修正-执行-双轨更新的闭环，在不牺牲效用下保持可信度，并在实验中显示能缓解 misevolution。

#### 21. LatentMem: Customizing Latent Memory for Multi-Agent Systems
- arXiv: 2602.03036v1
- 发布日期: 2026-02-03
- 链接: http://arxiv.org/abs/2602.03036v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/21_2602.03036v1.pdf
- 摘要（中文）: 多 agent 系统的记忆常遇两类瓶颈：缺少 role-aware 定制导致记忆同质化；以及过细条目导致信息过载。论文提出可学习框架 `LatentMem`：用轻量化形式存 raw 轨迹的 experience bank，再由 memory composer 基于检索到的经验与 agent 上下文合成紧凑的 latent memories；并提出 `LMPO`，让任务级优化信号通过 latent memories 反向影响 composer，促使其生成 token-efficient 且高效用表征。作者在多种基准与主流 MAS 框架上实验，称相对 vanilla 最多提升 19.36%，且无需修改底层框架。

#### 22. MemSkill: Learning and Evolving Memory Skills for Self-Evolving Agents
- arXiv: 2602.02474v1
- 发布日期: 2026-02-02
- 链接: http://arxiv.org/abs/2602.02474v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/22_2602.02474v1.pdf
- 摘要（中文）: 论文认为固定的手工记忆操作（抽取/巩固/裁剪等）把人的先验硬编码进去，面对不同交互模式会变得僵硬且在长历史上低效。作者提出 `MemSkill`：把记忆操作重构为可学习、可演化的“memory skills”（结构化可复用的抽取/巩固/裁剪例程）。系统包含 controller（学会选少量相关 skill）、LLM executor（按 skill 生成记忆）、以及 designer（周期性复盘 hard case，改进/新增 skill），形成闭环共同提升选择策略与 skill 集。作者在 LoCoMo、LongMemEval、HotpotQA、ALFWorld 上实验，称相对强 baseline 有稳定提升并具备跨设定泛化。

#### 23. Co-RedTeam: Orchestrated Security Discovery and Exploitation with LLM Agents
- arXiv: 2602.02164v2
- 发布日期: 2026-02-02
- 链接: http://arxiv.org/abs/2602.02164v2
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/23_2602.02164v2.pdf
- 摘要（中文）: 论文面向自动化攻防（red teaming），指出现有方法在漏洞发现与利用上受限于交互不足、缺少 execution grounding、以及经验无法复用。作者提出多 agent 框架 `Co-RedTeam`，把漏洞分析拆为协同的 discovery 与 exploitation 两阶段，融合安全领域知识、代码分析、基于真实执行反馈的迭代推理，并引入长期记忆复用过往轨迹。作者在多项安全基准上评测，称漏洞利用成功率超过 60%，漏洞检测提升超过 10 个绝对点，并通过消融证明执行反馈、结构化交互与记忆的重要性。

#### 24. Beyond RAG for Agent Memory: Retrieval by Decoupling and Aggregation
- arXiv: 2602.02007v2
- 发布日期: 2026-02-02
- 链接: http://arxiv.org/abs/2602.02007v2
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/24_2602.02007v2.pdf
- 摘要（中文）: 论文认为 agent memory 与传统 RAG 假设不同：对话流是有界且高度相关，存在大量重复 span；因此固定 top-k 相似度检索会带来冗余，上层剪枝可能误删时间相关前提。作者提出 `xMemory`：遵循“decoupling → aggregation”，把记忆拆解为语义组件并组织成层级；用稀疏-语义目标指导 split/merge，保持可检索且忠实的高层组织；推理时 top-down 检索，先选紧凑且多样的主题/语义集合，再在能降低不确定性时展开到 episode/原始消息。作者在 LoCoMo 与 PerLTQA、以及多个最新 LLM 上报告回答质量与 token 效率的提升。

#### 25. "Someone Hid It": Query-Agnostic Black-Box Attacks on LLM-Based Retrieval
- arXiv: 2602.00364v3
- 发布日期: 2026-01-30
- 链接: http://arxiv.org/abs/2602.00364v3
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/25_2602.00364v3.pdf
- 摘要（中文）: 论文研究 LLM-based Retrieval（含 RAG、dense IR、agent memory retrieval）对对抗性文档注入的脆弱性。不同于以往假设攻击者已知 query 或可接触受害模型参数/交互，该工作提出更贴近现实的黑盒攻击：攻击者不需要受害 query 与模型信息，只用 zero-shot surrogate LLM 生成可迁移的注入 token 来提升/压制文档在检索中的排名；并给出理论框架，将可迁移攻击建模为 min-max 问题，通过带可学习 query 样本的对抗学习机制寻找最优 token。作者在多个基准与流行 LLM retriever 上验证有效性，并强调现实中“无意的文档编辑”也可能触发类似鲁棒性问题。

#### 26. MiTa: A Hierarchical Multi-Agent Collaboration Framework with Memory-integrated and Task Allocation
- arXiv: 2601.22974v1
- 发布日期: 2026-01-30
- 链接: http://arxiv.org/abs/2601.22974v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/26_2601.22974v1.pdf
- 摘要（中文）: 多 agent 系统在复杂 embodied 任务中能缓解单 agent 的低效，但常出现记忆不一致与行为冲突。论文提出层级协作框架 `MiTa`：manager-member 结构中，manager 额外包含任务分配模块与总结模块；任务分配从全局视角拆任务以避免冲突；总结模块在进度更新触发时把近期协作历史压缩成保留长程上下文的 episodic summary，实现记忆整合。作者称实验验证在复杂协作中效率与适应性优于强 baseline。

#### 27. E-mem: Multi-agent based Episodic Context Reconstruction for LLM Agent Memory
- arXiv: 2601.21714v1
- 发布日期: 2026-01-29
- 链接: http://arxiv.org/abs/2601.21714v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/27_2601.21714v1.pdf
- 摘要（中文）: 面向 System-2 推理的 LLM agent 需要长期保持严格的逻辑完整性，但常见“记忆预处理”（把序列依赖压缩成 embedding/graph）会破坏上下文完整性。论文提出 `E-mem`：从 Memory Preprocessing 转向 Episodic Context Reconstruction，受生物 engram 启发，采用异构层级架构：多个 assistant agent 维护“未压缩的局部记忆上下文”，中央 master agent 负责全局规划；在激活片段内由 assistant 做局部推理并抽取证据再聚合。作者在 LoCoMo 上报告 F1>54%，较 SOTA `GAM` 提升 7.75 个点，并将 token 成本降低 70% 以上。

#### 28. BMAM: Brain-inspired Multi-Agent Memory Framework
- arXiv: 2601.20465v1
- 发布日期: 2026-01-28
- 链接: http://arxiv.org/abs/2601.20465v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/28_2601.20465v1.pdf
- 摘要（中文）: 论文把长交互中的时序信息保持与跨会话行为一致性问题称为 “soul erosion”。作者提出脑启发的多 agent 记忆架构 `BMAM`：把记忆建模为多个功能子系统而非单一 store，包括 episodic、semantic、salience-aware、control-oriented 等互补时间尺度；episodic 按显式时间线组织，并融合多信号检索证据以支持长程推理。作者在 LoCoMo 上报告标准长程评测设定下准确率 78.45%，并用消融说明类似 hippocampus 的 episodic 子系统对时间推理关键。

#### 29. AMA: Adaptive Memory via Multi-Agent Collaboration
- arXiv: 2601.20352v2
- 发布日期: 2026-01-28
- 链接: http://arxiv.org/abs/2601.20352v2
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/29_2601.20352v2.pdf
- 摘要（中文）: 作者指出现有 agent memory 常用固定检索粒度、偏“堆积式维护”的策略与粗粒度更新，导致存储信息与任务推理需求不匹配，且长期积累逻辑不一致。论文提出多 agent 协作框架 `AMA`：层级记忆设计动态对齐“检索粒度-任务复杂度”；Constructor 与 Retriever 负责多粒度构建与自适应 query 路由；Judge 校验相关性与一致性，证据不足触发迭代检索，发现冲突则调用 Refresher 做定向更新/删除。作者在长上下文基准上报告显著超过 SOTA，同时相对全量上下文方法 token 消耗约降 80%。

#### 30. Me-Agent: A Personalized Mobile Agent with Two-Level User Habit Learning for Enhanced Interaction
- arXiv: 2601.20162v1
- 发布日期: 2026-01-28
- 链接: http://arxiv.org/abs/2601.20162v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/30_2601.20162v1.pdf
- 摘要（中文）: 论文关注移动端 LLM agent 的个性化短板：只按显式指令行动，缺乏对含糊指令的个性化解读、无法从历史交互学习、难以处理隐含个性偏好的指令。作者提出 `Me-Agent`：在 prompt 层用用户偏好学习策略 + Personal Reward Model 提升个性化；在记忆层设计 `Hierarchical Preference Memory`，区分用户长期记忆与 app-specific 记忆。并提出新基准 `User FingerTip`（包含大量日常含糊指令）用于验证个性化能力。实验显示在 User FingerTip 上达到 SOTA，同时保持通用执行能力。

#### 31. FadeMem: Biologically-Inspired Forgetting for Efficient Agent Memory
- arXiv: 2601.18642v2
- 发布日期: 2026-01-26
- 链接: http://arxiv.org/abs/2601.18642v2
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/31_2601.18642v2.pdf
- 摘要（中文）: 长期任务中缺少“选择性遗忘”会导致两种极端：跨上下文边界的灾难性遗忘或 context window 内的信息过载；而人类记忆通过自适应衰减在保留与遗忘间平衡。作者提出 `FadeMem`：脑启发的记忆架构引入主动遗忘机制，在双层层级中用可自适应的指数衰减函数控制保留，衰减受语义相关性、访问频率、时间模式调制；并用 LLM 引导的冲突消解与记忆融合进行整合，让无关细节逐步淡出。作者在 Multi-Session Chat、LoCoMo、LTI-Bench 上评测，称在保持/提升多跳推理与检索的同时实现 45% 存储降幅。

#### 32. When Personalization Legitimizes Risks: Uncovering Safety Vulnerabilities in Personalized Dialogue Agents
- arXiv: 2601.17887v1
- 发布日期: 2026-01-25
- 链接: http://arxiv.org/abs/2601.17887v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/32_2601.17887v1.pdf
- 摘要（中文）: 论文揭示个性化对话 agent 的一种安全失败模式：`intent legitimation`—— benign 的个人记忆会偏置意图推断，使模型把本应有害的请求“合理化/正当化”。作者提出基准 `PS-Bench` 用于识别与量化该现象；跨多种记忆增强框架与 base LLM 的实验显示，个性化会让攻击成功率相对无状态基线提升 15.8%–243.7%。论文还从内部表征空间给出机制证据，并提出轻量 detection-reflection 方法降低安全退化。（注意：原文声明可能包含有害内容。）

#### 33. From Atom to Community: Structured and Evolving Agent Memory for User Behavior Modeling
- arXiv: 2601.16872v2
- 发布日期: 2026-01-23
- 链接: http://arxiv.org/abs/2601.16872v2
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/33_2601.16872v2.pdf
- 摘要（中文）: 论文面向推荐系统等用户行为建模：在 LLM agent 场景下，偏好表征从 latent embedding 走向语义记忆，但对非文本行为（如点击）缺少监督，且现有做法常用单一非结构化 summary 并用覆盖式更新，导致多兴趣维度混淆、偏好演化引发遗忘、以及个体交互稀疏难以利用协同信号。作者提出 `STEAM`：把偏好分解为原子记忆单元，每个单元绑定行为证据；再把跨用户相似记忆组织成 community 并生成 prototype memory 以传播信号；并引入 consolidation/formation 等自适应演化机制。作者在 3 个真实数据集上报告在推荐准确率、仿真保真度与多样性上超过 SOTA。

#### 34. EMemBench: Interactive Benchmarking of Episodic Memory for VLM Agents
- arXiv: 2601.16690v1
- 发布日期: 2026-01-23
- 链接: http://arxiv.org/abs/2601.16690v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/34_2601.16690v1.pdf
- 摘要（中文）: 论文提出 `EMemBench`：用交互式游戏对 agent 的长期 episodic memory 做程序化评测。不同于固定题库，它从每个 agent 的自身轨迹生成问题，覆盖文本与视觉游戏环境；每个模板都可从游戏信号计算可验证的 ground truth，并控制可回答性与技能覆盖（单/多跳回忆、归纳、时间、空间、逻辑、对抗等）。作者在 15 个文本游戏与多个视觉 seed 上评测，指出结果远未饱和：归纳与空间推理是长期瓶颈，尤其在视觉设定；persistent memory 对开源 backbone 在文本游戏中收益明显，但对 VLM agent 不稳定，说明视觉落地的 episodic memory 仍是难题。

#### 35. Memory Retention Is Not Enough to Master Memory Tasks in Reinforcement Learning
- arXiv: 2601.15086v1
- 发布日期: 2026-01-21
- 链接: http://arxiv.org/abs/2601.15086v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/35_2601.15086v1.pdf
- 摘要（中文）: 论文指出 RL 记忆研究/基准多强调“保留（retention）”，但现实决策需要同时“稳定保留 + 可更新重写（memory rewriting）”，尤其在部分可观测且环境随时间变化时。作者构建专门考察持续更新能力的新基准，并比较 recurrent、transformer 与结构化记忆架构。实验显示经典 recurrent 模型在重写任务上更灵活/鲁棒；现代结构化记忆只在狭窄条件下成功；transformer agent 往往在超出简单保留的任务上失败，从而提示需要显式、可训练的遗忘/重写机制。

#### 36. HiNS: Hierarchical Negative Sampling for More Comprehensive Memory Retrieval Embedding Model
- arXiv: 2601.14857v1
- 发布日期: 2026-01-21
- 链接: http://arxiv.org/abs/2601.14857v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/36_2601.14857v1.pdf
- 摘要（中文）: 记忆检索常依赖 embedding 模型，但训练数据构造忽视负样本的层级难度与其在真实对话中的自然分布：既有语义接近的干扰项，也有明显无关项，比例并非均匀。论文提出数据构造框架 `HiNS`：显式建模负样本难度层级，并用对话数据估计更贴近真实的负样本比例，以提升 embedding 在记忆密集任务中的细粒度区分能力与泛化。作者报告在 LoCoMo 上 F1/BLEU-1 分别提升 3.27%/3.30%（MemoryOS）与 1.95%/1.78%（Mem0）；在 PERSONAMEM 上总分提升 1.19%（MemoryOS）与 2.55%（Mem0）。

#### 37. Optimizing FaaS Platforms for MCP-enabled Agentic Workflows
- arXiv: 2601.14735v2
- 发布日期: 2026-01-21
- 链接: http://arxiv.org/abs/2601.14735v2
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/37_2601.14735v2.pdf
- 摘要（中文）: 论文从工程系统角度讨论 MCP-enabled agent 工作流在云端部署与状态管理的挑战：VM 方式成本高且缺弹性；FaaS 虽可自动伸缩但天然无状态。作者提出 `FAME`：基于 FaaS 的 MCP 工作流架构，用 LangGraph 把 ReAct 等模式拆成 Planner/Actor/Evaluator 等函数并用工作流编排避免超时；用 DynamoDB 自动化记忆持久化与注入来跨请求保持对话上下文；并通过 S3 缓存工具输出、Lambda wrapper 部署 MCP server、函数融合等做优化。作者在论文总结与日志分析两类应用上评测，称最高可达 13× 延迟下降、输入 token 减少 88%、成本降低 66%，且完成率提升。

#### 38. Prompt Injection Mitigation with Agentic AI, Nested Learning, and AI Sustainability via Semantic Caching
- arXiv: 2601.13186v1
- 发布日期: 2026-01-19
- 链接: http://arxiv.org/abs/2601.13186v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/38_2601.13186v1.pdf
- 摘要（中文）: 论文围绕 prompt injection 防御与评测，扩展了 Total Injection Vulnerability Score (TIVS) 框架，引入语义相似缓存与新的可观测性指标（Observability Score Ratio）形成 `TIVS-O`，用于分析“防御严格性-取证透明度”的权衡。系统在 HOPE 风格的 Nested Learning 多 agent 架构中用 Continuum Memory Systems 做语义缓存，并在 301 条注入型合成 prompt（10 类攻击家族）上评测。作者称在实现“零高风险 breach”的同时，通过语义缓存将 LLM 调用减少 41.6%，并带来延迟、能耗与碳排下降；不同配置揭示了缓解强度与审计透明度之间的非单调关系。

#### 39. Grounding Agent Memory in Contextual Intent
- arXiv: 2601.10702v1
- 发布日期: 2026-01-15
- 链接: http://arxiv.org/abs/2601.10702v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/39_2601.10702v1.pdf
- 摘要（中文）: 在长程、目标导向交互中，同一实体/事实会在不同隐含目标与约束下反复出现，导致记忆系统检索到“语义相似但意图不匹配”的证据。作者提出 `STITCH`：为轨迹每步建立结构化检索 cue 与 contextual intent，通过匹配当前步意图检索历史；意图包含（1）主题段的潜在目标，（2）动作类型，（3）关键实体类型，用于消歧并抑制干扰。作者同时提出 `CAME-Bench` 用于真实动态轨迹中的意图感知检索评测；在 CAME-Bench 与 LongMemEval 上报告 SOTA，较最强 baseline 提升 35.6%，且轨迹越长增益越大。

#### 40. Role-Playing Agents Driven by Large Language Models: Current Status, Challenges, and Future Trends
- arXiv: 2601.10122v1
- 发布日期: 2026-01-15
- 链接: http://arxiv.org/abs/2601.10122v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/40_2601.10122v1.pdf
- 摘要（中文）: 该文为角色扮演语言 agent（RPLA）综述，记忆机制是其中一部分：从模板/风格模仿演进到以人格建模与记忆机制为中心的“认知模拟”。论文梳理了心理量表驱动的角色建模、memory-augmented prompting、动机-情境驱动的行为决策控制等路径；并讨论角色语料构建（数据源、版权、标注）与多维评测框架（角色知识、人格一致性、价值对齐、交互幻觉等）。

#### 41. Rethinking Memory Mechanisms of Foundation Agents in the Second Half: A Survey
- arXiv: 2602.06052v3
- 发布日期: 2026-01-14
- 链接: http://arxiv.org/abs/2602.06052v3
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/41_2602.06052v3.pdf
- 摘要（中文）: 论文提出 AI 研究正从“模型创新与 benchmark 分数”转向“问题定义与真实评测”，在长程、动态、用户相关环境中，context explosion 迫使 agent 必须持续积累、管理并选择性复用信息，因此 memory 成为关键解法。综述从三维度统一刻画 foundation agent memory：memory substrate（内/外部）、cognitive mechanism（episodic/semantic/sensory/working/procedural）、memory subject（agent-centric 与 user-centric）；并分析不同 agent 拓扑下的记忆实例化与操作策略、评测基准与指标，以及开放挑战。

#### 42. CAST: Character-and-Scene Episodic Memory for Agents
- arXiv: 2602.06051v3
- 发布日期: 2026-01-14
- 链接: http://arxiv.org/abs/2602.06051v3
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/42_2602.06051v3.pdf
- 摘要（中文）: 多数 agent memory 强调语义回忆，把经历表示成 KV/vector/graph 等结构，难以表达并检索“who/when/where 贯穿的连贯事件”（episodic memory）。论文提出受戏剧理论启发的 `CAST`：构建 3D scenes（time/place/topic），并组织成 character profiles 来总结角色事件，以表示 episodic memory；同时用 graph-based semantic memory 形成双记忆设计。作者报告在多数据集上相对 baseline 平均提升 8.11% F1 与 10.21% 的 J(LLM-as-a-Judge)，在开放与时间敏感的对话问题上增益更大。

#### 43. The AI Hippocampus: How Far are We From Human Memory?
- arXiv: 2601.09113v1
- 发布日期: 2026-01-14
- 链接: http://arxiv.org/abs/2601.09113v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/43_2601.09113v1.pdf
- 摘要（中文）: 该文为记忆综述，覆盖 LLM 与 MLLM 从静态预测器走向可交互系统（continual learning、个性化推断）过程中记忆机制的角色。作者给出 taxonomy：implicit memory（参数内知识与其可解释/操控/重构）、explicit memory（外部存储与检索，如文本、向量、图等）、agentic memory（在自主 agent 中的跨时间持久结构，用于长期规划、自洽、多 agent 协作）。同时讨论多模态记忆整合、关键架构进展、评测任务与开放挑战（容量、对齐、事实一致性、互操作性等）。

#### 44. AtomMem : Learnable Dynamic Agentic Memory with Atomic Memory Operation
- arXiv: 2601.08323v2
- 发布日期: 2026-01-13
- 链接: http://arxiv.org/abs/2601.08323v2
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/44_2601.08323v2.pdf
- 摘要（中文）: 论文认为记忆对于长程问题关键，但静态手工 workflow 限制了性能与泛化，因此提出把记忆管理建模为可学习的决策过程。作者提出 `AtomMem`：将高层记忆流程拆成原子级 CRUD（Create/Read/Update/Delete）操作，把记忆 workflow 变成可学习的操作序列；再结合 SFT 与 RL 学习任务对齐的策略来编排记忆行为。作者在 3 个 long-context 基准上报告 AtomMem-8B 优于既有静态 workflow 方法，并分析训练动态显示其能发现结构化的任务对齐策略。

#### 45. SwiftMem: Fast Agentic Memory via Query-aware Indexing
- arXiv: 2601.08160v1
- 发布日期: 2026-01-13
- 链接: http://arxiv.org/abs/2601.08160v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/45_2601.08160v1.pdf
- 摘要（中文）: 论文指出很多记忆框架不管 query 特征如何都对整个存储层做“穷举式检索”，记忆增长后延迟会成为实时交互瓶颈。作者提出 `SwiftMem`：在时间与语义两维做 query-aware 索引以实现次线性检索；时间索引支持对时间敏感检索的对数时间范围查询，语义 `DAG-Tag` 索引用层级标签把 query 映射到相关主题；并通过 embedding-tag 协同巩固缓解增长引发的碎片化、提升 cache locality。作者在 LoCoMo 与 LongMemEval 上报告在保持竞争性准确率的同时检索速度提升 47×。

#### 46. El Agente Gráfico: Structured Execution Graphs for Scientific Agents
- arXiv: 2602.17902v1
- 发布日期: 2026-02-19
- 链接: http://arxiv.org/abs/2602.17902v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/46_2602.17902v1.pdf
- 摘要（中文）: 论文聚焦科学计算工作流自动化：现有 agent 常用非结构化文本做上下文管理与执行协调，信息量爆炸会遮蔽决策溯源并降低可审计性。作者提出单 agent 框架 `El Agente Gráfico`：把 LLM 决策置于 type-safe 的执行环境中，并以动态 knowledge graph 做外部持久化记忆；核心是对科学概念做结构化抽象，以及将计算状态映射为 typed Python objects（可内存存储或持久化到外部 KG），用符号化标识替代 raw text 管 context，从而保证一致性、支持 provenance、提高工具编排效率。作者在量子化学等多步/并行任务上构建自动 benchmark，显示单 agent + 可靠执行引擎也能稳健完成复杂计算，并扩展到构象生成与 MOF 设计等应用。

#### 47. A Tale of Two Graphs: Separating Knowledge Exploration from Outline Structure for Open-Ended Deep Research
- arXiv: 2602.13830v1
- 发布日期: 2026-02-14
- 链接: http://arxiv.org/abs/2602.13830v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/47_2602.13830v1.pdf
- 摘要（中文）: Open-Ended Deep Research（OEDR）要求 agent 在长流程中反复搜索、连接证据并生成结构化报告；现有“线性积累”会 lost-in-the-middle，而“纯大纲规划”又很难从 outline 推断知识缺口并触发定向探索。论文提出 `DualGraph memory`：把“知道什么”与“怎么写”分离，维护两个共同演化的图：Outline Graph（OG）与 Knowledge Graph（KG）。KG 作为语义记忆存储细粒度实体/概念/关系；通过联合 KG 拓扑与 OG 结构信号，生成定向搜索 query，从而更高效、全面地迭代探索与修订。作者在 DeepResearch Bench、DeepResearchGym、DeepConsult 上评测，报告在深度、广度与事实落地上优于 SOTA，例如用 GPT-5 在 DeepResearch Bench 上达到 53.08 的 RACE 分数，并用消融确认双图设计的重要性。

#### 48. KGLAMP: Knowledge Graph-guided Language model for Adaptive Multi-robot Planning and Replanning
- arXiv: 2602.04129v1
- 发布日期: 2026-02-04
- 链接: http://arxiv.org/abs/2602.04129v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/48_2602.04129v1.pdf
- 摘要（中文）: 论文面向异构多机器人长任务规划：经典 PDDL 需要手工符号模型，LLM 规划又常忽略机器人异质性与环境不确定。作者提出 `KGLAMP`：用结构化 knowledge graph 编码物体关系、空间可达性与机器人能力，指导 LLM 生成更准确的 PDDL 问题描述；KG 作为可持续更新的动态记忆融入新观测，并在检测不一致时触发 replanning，使符号计划能随世界状态演化自适应。作者在 MAT-THOR 基准上报告相对 LLM-only 与 PDDL-only 变体至少提升 25.5%。

#### 49. Factored Reasoning with Inner Speech and Persistent Memory for Evidence-Grounded Human-Robot Interaction
- arXiv: 2602.00675v1
- 发布日期: 2026-01-31
- 链接: http://arxiv.org/abs/2602.00675v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/49_2602.00675v1.pdf
- 摘要（中文）: 面向对话式人机交互，机器人助理需要持久化用户上下文、应对欠规格请求，并把回答 grounding 到外部证据且保持中间决策可验证。论文提出认知架构 `JANUS`：将交互建模为部分可观测 MDP，并用 typed interface 的 factored controller 将行为分解为多个模块（scope、intent、memory、inner speech、query 生成、outer speech 等），提供信息充分性、执行就绪、工具 grounding 的显式策略。其 memory agent 维护“近期 buffer + 核心紧凑记忆 + 语义检索的归档库”，并通过受控的巩固/修订策略耦合；inner speech 负责检查参数完整性并在 grounding 前触发澄清；faithfulness 约束把对人的陈述绑定到 evidence bundle。作者在饮食助理领域（基于 KG）用模块级单元测试评估，报告与人工参考的一致性与可用延迟。

#### 50. Cost and accuracy of long-term memory in Distributed Multi-Agent Systems based on Large Language Models
- arXiv: 2601.07978v2
- 发布日期: 2026-01-12
- 链接: http://arxiv.org/abs/2601.07978v2
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/50_2601.07978v2.pdf
- 摘要（中文）: 分布式多 agent 系统（DMAS）在隐私与协作上有优势，但在网络约束下对长期记忆的系统性评估不足。论文提出 testbed，对比 `mem0`（向量记忆）与 `Graphiti`（图/KG 记忆）在 LoCoMo 基准上的成本与准确率，在无约束与受约束网络条件下测算计算、费用与准确率指标。结果显示 mem0 在效率上显著优于 Graphiti，而准确率差异不显著；结合 Pareto efficiency 分析，作者认为 mem0 在成本-准确率权衡上更优。

#### 51. CASCADE: Cumulative Agentic Skill Creation through Autonomous Development and Evolution
- arXiv: 2512.23880v2
- 发布日期: 2025-12-29
- 链接: http://arxiv.org/abs/2512.23880v2
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/51_2512.23880v2.pdf
- 摘要（中文）: 论文关注从“LLM + tool use”走向“LLM + skill acquisition”的自进化 agent：现有 agent 依赖预定义工具或早期工具生成，难以适应复杂科学任务。作者提出 `CASCADE`，通过两类 meta-skill 实现技能累积：持续学习（web search、代码抽取、记忆利用等）与自反思（内省、knowledge graph 探索等）。作者在 SciSkillBench（116 个材料/化学任务）上评测，用 GPT-5 成功率 93.3%，而去掉演化机制为 35.4%；并展示在计算分析、自动实验、复现论文等真实应用。论文强调记忆巩固与人机协作可把可执行技能沉淀并在 agent/科学家间共享。

#### 52. GR-Agent: Adaptive Graph Reasoning Agent under Incomplete Knowledge
- arXiv: 2512.14766v1
- 发布日期: 2025-12-16
- 链接: http://arxiv.org/abs/2512.14766v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/52_2512.14766v1.pdf
- 摘要（中文）: 论文面向 KGQA：多数基准假设 KG 完整，使评测退化为浅检索；现实 KG 常不完整，需要从已有事实推断。作者提出构造“KG 不完整”基准的方法：移除直接支持 triple，但保留可推断的替代路径；实验显示现有方法在不完整条件下性能持续下降。为此提出 `GR-Agent`：先从 KG 构建交互环境，把 KGQA 形式化为 agent-environment 交互；agent 在图推理工具的 action space 上行动，并维护对潜在推理证据的记忆（关系与路径）。作者称在完整与不完整设定下，GR-Agent 相对非训练 baseline 更优，并与训练式方法表现相当。

#### 53. Memoria: A Scalable Agentic Memory Framework for Personalized Conversational AI
- arXiv: 2512.12686v1
- 发布日期: 2025-12-14
- 链接: http://arxiv.org/abs/2512.12686v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/53_2512.12686v1.pdf
- 摘要（中文）: 论文提出模块化个性化记忆框架 `Memoria`，将 agentic memory 定义为让 LLM 具备跨对话持久性的能力（持续性、个性化、长期上下文）。框架结合两类组件：session-level 的动态摘要（保证短期连贯）与加权 knowledge graph 的用户建模引擎（以结构化实体与关系增量捕捉用户特征/偏好/行为模式）。作者强调该混合架构能在 token 约束下同时兼顾短期对话连贯与长期个性化，旨在弥合“无状态 LLM 接口”与“可持续演化用户体验”的产业需求。

#### 54. Decoding Student Minds: Leveraging Conversational Agents for Psychological and Learning Analysis
- arXiv: 2512.10441v1
- 发布日期: 2025-12-11
- 链接: http://arxiv.org/abs/2512.10441v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/54_2512.10441v1.pdf
- 摘要（中文）: 该论文主题为教育场景的心理与学习状态分析，并非典型 agent memory 方向。作者提出具心理感知的对话 agent，结合 LLM、KG-BERT 与带注意力的双向 LSTM，对学生认知/情感状态做实时分类；融合文本语义、语音韵律特征与时间行为趋势以推断投入度、压力、理解水平。作者报告在大学生试点中提升动机、降低压力并带来中等学业增益。

#### 55. SEAL: Self-Evolving Agentic Learning for Conversational Question Answering over Knowledge Graphs
- arXiv: 2512.04868v1
- 发布日期: 2025-12-04
- 链接: http://arxiv.org/abs/2512.04868v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/55_2512.04868v1.pdf
- 摘要（中文）: KBCQA 需要指代消解、上下文依赖建模与复杂逻辑推理；现有端到端语义解析或 stepwise agent 推理常在结构正确性与计算成本上受限。论文提出两阶段语义解析框架 `SEAL`：先由 LLM 抽取最小 S-expression core，再由 agentic calibration 模块修正语法并精确对齐 KG 实体/关系；第二阶段用模板补全生成可执行 S-expression。关键是引入 self-evolving 机制：结合局部/全局记忆与 reflection，从对话历史与执行反馈中持续适应而无需显式再训练。作者在 SPICE 基准上报告 SOTA，尤其多跳、比较与聚合任务上提升明显，并称结构准确率与效率均改善。

#### 56. ReAcTree: Hierarchical LLM Agent Trees with Control Flow for Long-Horizon Task Planning
- arXiv: 2511.02424v2
- 发布日期: 2025-11-04
- 链接: http://arxiv.org/abs/2511.02424v2
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/56_2511.02424v2.pdf
- 摘要（中文）: 现有 embodied 规划方法常把所有历史决策/观测纠缠在单条轨迹里处理，难以应对复杂长任务。论文提出层级规划方法 `ReAcTree`：把目标拆成动态构建的 agent tree，子目标由可扩展树的 LLM agent node 处理，control-flow node 负责协调执行策略。同时引入两类互补记忆：各 node 从 episodic memory 检索“目标/子目标级示例”，并通过 working memory 共享环境观测。作者在 WAH-NL 与 ALFRED 上评测，称在多种 LLM 上稳定优于 ReAct 等强 baseline；例如 Qwen 2.5 72B 在 WAH-NL 上 goal success 61%，接近翻倍于 ReAct 的 31%。

#### 57. Learning from Supervision with Semantic and Episodic Memory: A Reflective Approach to Agent Adaptation
- arXiv: 2510.19897v1
- 发布日期: 2025-10-22
- 链接: http://arxiv.org/abs/2510.19897v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/57_2510.19897v1.pdf
- 摘要（中文）: 论文研究不更新参数的条件下，基于预训练 LLM 的 agent 如何从标注样本学习目标分类函数（避免高成本、低透明的 fine-tuning）。作者提出记忆增强框架：用 episodic memory 存“实例级 critique”（具体经验），再用 semantic memory 将其蒸馏为可复用的“任务级指导”。在多任务评测中，引入 critique 的方案较仅用 label 的 RAG 风格 baseline 最高可提升 24.8% 准确率。作者还提出 `suggestibility` 指标用于解释不同模型在事实型 vs 偏好型数据下的差异，强调记忆驱动的反思式学习有助于更自适应且可解释的 agent。

#### 58. Agentic-KGR: Co-evolutionary Knowledge Graph Construction through Multi-Agent Reinforcement Learning
- arXiv: 2510.09156v1
- 发布日期: 2025-10-10
- 链接: http://arxiv.org/abs/2510.09156v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/58_2510.09156v1.pdf
- 摘要（中文）: 论文指出静态知识库存在覆盖缺口与时效过期，限制知识增强 LLM 在动态环境中的效果。作者提出 `Agentic-KGR`：通过多轮 RL 让 LLM 与 KG 共同演化，包含动态 schema 扩展、检索增强记忆系统（使参数与知识结构持续协同优化）、以及可学习的多尺度 prompt 压缩。作者报告在知识抽取任务上优于监督与单轮 RL baseline；与 GraphRAG 结合后，在下游 QA 上准确率与覆盖均显著提升。

#### 59. REMI: A Novel Causal Schema Memory Architecture for Personalized Lifestyle Recommendation Agents
- arXiv: 2509.06269v1
- 发布日期: 2025-09-08
- 链接: http://arxiv.org/abs/2509.06269v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/59_2509.06269v1.pdf
- 摘要（中文）: 个性化助理难以融合复杂个人数据与因果知识，导致建议泛化且解释性弱。论文提出 `REMI`：因果图谱驱动的 `Causal Schema Memory (CSM)` 架构，用于多模态 lifestyle agent，集成个人因果 KG、因果推理引擎与基于 schema 的规划模块。系统在个人生活事件/习惯构建因果图，进行目标导向的因果遍历（结合外部知识与假设推理），并检索可复用的 plan schema 生成个性化行动计划，由 LLM 编排各模块并输出透明因果解释。作者提出新的个性化与可解释性评估指标（Personalization Salience Score、Causal Reasoning Accuracy），并称相比 baseline LLM agent，CSM 能给出更上下文相关、用户对齐的建议。

#### 60. Lattice Annotated Temporal (LAT) Logic for Non-Markovian Reasoning
- arXiv: 2509.02958v1
- 发布日期: 2025-09-03
- 链接: http://arxiv.org/abs/2509.02958v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/60_2509.02958v1.pdf
- 摘要（中文）: 该论文主题为时序逻辑推理与开放世界语义，并非专门的 agent memory 研究，但与“长程状态/记忆建模”相关。作者提出 `LAT Logic` 支持 temporal reasoning 与 lower-lattice 注释结构，给出 grounding 复杂度界并在 PyReason 实现中提供模块化与低层优化，可直接接入 RL 环境。作者在多 agent 仿真与 KG 任务上报告最多 10^3 级速度提升与 10^5 级内存减少，并在 RL 仿真中通过捕捉更丰富的时间依赖带来最高 26% 胜率提升。

#### 61. Memento: Fine-tuning LLM Agents without Fine-tuning LLMs
- arXiv: 2508.16153v2
- 发布日期: 2025-08-22
- 链接: http://arxiv.org/abs/2508.16153v2
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/61_2508.16153v2.pdf
- 摘要（中文）: 论文提出一种无需对底座 LLM 做梯度微调的自适应 agent 学习范式：与静态手工 reflection 工作流相比更灵活；与参数微调相比更低成本。作者把问题形式化为 `Memory-augmented MDP (M-MDP)`：用神经 case-selection policy 决定行动，过往经验存入 episodic memory；policy 通过 memory rewriting 结合环境反馈持续更新，而 policy improvement 通过高效 memory reading（检索）实现。作者在 deep research 场景实例化为 `Memento`：在 GAIA validation 上达到 top-1（87.88% Pass@3），测试集 79.40%；在 DeepResearcher 上达到 66.6% F1、80.4% PM，并称优于训练式 SOTA；case-based memory 在 OOD 任务上带来 4.7–9.6 个绝对点提升，并提供代码仓库。

#### 62. Long Story Generation via Knowledge Graph and Literary Theory
- arXiv: 2508.03137v1
- 发布日期: 2025-08-05
- 链接: http://arxiv.org/abs/2508.03137v1
- PDF: /Users/bytedance/Documents/trae_projects/jielii_test/agent_memory_survey_2025-08_to_2026-02/papers/62_2508.03137v1.pdf
- 摘要（中文）: 该论文主题为长文本生成（长故事），记忆用于缓解 outline-based 生成的 theme drift。作者提出 multi-agent Story Generator：记忆存储模型含 long-term memory（挑最重要记忆以防主题漂移）与 short-term memory（保留最新轮大纲）；并基于叙事学理论设计“主题障碍”框架引入不确定因素与评价准则，通过知识图谱加入新节点内容提升吸引力；另设 writer-reader 交互阶段用对话反馈修订文本保持一致性与逻辑。作者报告相对既有方法能生成更高质量长故事。

## 7. 业界经典做法与可落地系统设计（面向工程实现）

### 7.1 业界常见“记忆”形态（从最常见到更高级）
- 轻量偏好档案（Profile/Preference）: 把用户偏好与硬约束以结构化字段存储（KV/JSON），每次对话在系统提示或检索结果中注入；优点是低成本、可控；缺点是覆盖面有限、更新策略难。
- 对话摘要 + 可检索历史（Summary + Retrieval）: 以会话粒度做滚动摘要（短期连贯），同时把事件/事实/决策以 chunk 写入向量库或混合检索（长期回忆）；是多数生产系统的默认形态。
- 分层记忆（Working/Episodic/Semantic/Procedural）: 把“最近上下文”“经历事件”“稳定事实/知识”“可复用技能/工作流”分层，分别定义写入触发与检索策略，避免一锅端污染。
- 结构化记忆（Graph / Ledger / TODO / State Machine）: 对需要强结构的场景（项目管理、账本、任务树、研究笔记、实验流程）直接维护结构化状态（图/树/表），并让 LLM 在结构上读写。
- 安全优先的记忆隔离（Isolation + Sanitization）: 对外部内容与工具输出做隔离，主 agent 只接收 schema 校验后的值，降低间接注入与“脏上下文”风险。

### 7.2 一套“集大成”的记忆系统蓝图（可给自己的 agent 直接照着搭）
建议把记忆系统拆成 6 条管线/模块（每条都可独立迭代）：

1) 写入管线（Write Path）
- 触发器：只在“新事实/新偏好/新技能/关键决策”发生时写入；默认不把原始网页/长工具输出直接写入长期记忆。
- 结构化抽取：先抽取为 `MemoryItem`（类型、时间、来源、置信度、可删除 key），再存储；避免把自然语言当唯一真源。

2) 存储层（Storage Layer）
- `KV`：用户画像/偏好/硬约束、会话元信息（可审计、可删除、可覆盖）。
- `Vector`：事件片段、知识片段、工具产出摘要（召回强，但易受噪声影响）。
- `Graph`（可选）：实体-关系、任务分解、因果链、研究笔记链接（适合复杂推理与溯源）。

3) 检索与注入（Retrieve + Compose）
- 先意图分流：当前 query 属于事实回忆/偏好/技能复用/计划/安全敏感？不同意图走不同检索器与排序策略。
- 召回 + 重排：向量召回只是候选生成；重排要引入时间衰减、来源可信度、intent 兼容性，并做去重/多样性控制。
- 有证据的注入：把检索到的条目附带来源与时间戳（citations），并尽量以结构化形式注入（减少“把记忆当指令”）。

4) 巩固与遗忘（Consolidation + Forgetting）
- 周期性巩固：把高频/高价值条目从 episodic 合并到 semantic，形成稳定事实或流程；冲突用“新近性 + 证据强度 + 用户确认”解决。
- 遗忘策略：时间衰减 + 访问频率 + 语义相关性，并保留可追溯的删除日志。

5) 安全与隐私（Safety/Privacy）
- 注入防护：区分“指令/事实/引用”，对外部内容做隔离与 schema 校验。
- PII 与合规：记忆条目必须有 `owner`、`retention_policy`、`delete_key`；支持按用户请求“一键遗忘/导出”。

6) 可观测与评测（Observability + Evaluation）
- 线上指标：记忆命中率、被采纳率（usefulness）、误召回率、冲突率、写入噪声率、检索延迟/成本。
- 离线基准：用 LoCoMo/LongMemEval/MemoryArena/StructMemEval/（安全向）PS-Bench 等，按业务抽取子集做回归测试；必要时自建“多 session + 任务耦合”的评测。

### 7.3 科研重点 vs 工程瓶颈（你该把精力投在哪）
- 科研更关注：记忆结构与操作策略的可学习化、在 agentic 场景下的真实评测、以及在长程演化中的可信度与安全。
- 工程更痛的点：成本与延迟、数据隐私与可删除性、跨工具/跨端一致性、调试与可解释（记忆为何被写入/为何被召回/是否导致错误行为）。
- 两者重合处：“写什么/何时写/如何更新/如何避免污染”与“可复现评测口径”，这也是目前最有工程 ROI 的研究方向。

### 7.4 经典且已验证的做法（建议作为默认 baseline）
- Baseline A（最稳妥）：`Profile(KV)` + `Rolling Summary` + `Vector Retrieval` + 时间衰减 + 去重 + 引用注入。
- Baseline B（结构任务）：在 A 基础上增加一个结构化状态（例如 TODO/任务树/账本），让 agent 对该结构做显式读写，避免只靠自然语言摘要。
- Baseline C（安全敏感）：在 A/B 基础上加入“外部内容隔离 + schema 校验 + 记忆写入白名单”，并把高风险内容永不写入长期记忆。
