# Agentic RL 综述与方法巧思报告（截至 2026-03-03）

- 日期：2026-03-03
- 目标：聚焦 agentic RL 相关 survey，提炼“什么方法更好、哪里有巧思”
- 说明：基于近期公开综述的共同结论做综合，不局限于单篇论文口径。

## 1. 重点 survey（优先阅读）

1. The Landscape of Agentic Reinforcement Learning for LLMs: A Survey  
   - arXiv:2509.02547（v1: 2025-09-02；v4: 2026-01-24）

2. Reinforcement Learning Foundations for Deep Research Systems  
   - arXiv:2509.06733（v1: 2025-09-08；v2: 2025-11-05；TMLR 2026）

3. A Survey of Reinforcement Learning for Large Reasoning Models  
   - arXiv:2509.08827（v1: 2025-09-10；v3: 2025-10-09）

4. Reinforcement Learning Meets Large Language Models: A Survey of Advancements and Applications Across the LLM Lifecycle  
   - arXiv:2509.16679（v1: 2025-09-20）

## 2. Agentic RL 方法图谱（实用抽象）

### 2.1 核心问题建模

- 将 agent 执行过程建模为 POMDP：
  - 状态：历史对话、工具调用轨迹、外部观测
  - 动作：token 生成 + tool action（检索、代码执行、API 调用）
  - 奖励：任务完成度、轨迹质量、成本/时延/安全约束

- 与传统 RL 的关键差异：
  1. 动作空间混合（离散 token + 结构化工具参数）
  2. 奖励稀疏且延迟（长轨迹 credit assignment 难）
  3. 环境非平稳（工具、检索语料、接口随时间变化）

### 2.2 常见训练范式

1. PPO/GRPO 类在线优化：
   - 适合可在线采样、可持续收集 rollouts 的场景
   - 在长轨迹上更稳定，但成本较高

2. DPO/IPO/ORPO 类偏好优化（弱/无显式价值函数）：
   - 工程简洁，收敛快
   - 对“可验证长任务”常需额外机制补足 credit assignment

3. RLVR（可验证奖励）驱动：
   - 用可执行器/单元测试/规则检查器给确定性奖励
   - 在代码、数学、结构化任务中效果更可靠

4. 离线+在线混合（offline warm-start + online refinement）：
   - 先用高质量轨迹启动，再在线修正
   - 兼顾稳定性与样本效率，是目前较平衡路线

## 3. “比较好且有巧思”的方法模式

以下是从多篇 survey 共识中提炼的“高性价比巧思”，不是单一算法名。

1. 分层 credit assignment（最关键）
   - 做法：把长任务拆成子目标（规划-执行-验证），对子步骤给中间奖励。
   - 巧思点：降低超长轨迹方差，显著改善训练可控性。
   - 适用：deep research、多工具链任务。

2. 过程奖励模型（PRM）+ 结果奖励混合
   - 做法：同时评估“过程是否合理”和“最终答案是否正确”。
   - 巧思点：避免只优化终点导致的“投机路径”。
   - 适用：推理链、代码修复、复杂检索。

3. 可验证器优先的 reward 设计（RLVR）
   - 做法：优先把奖励落地为可执行检查（测试、编译、规则引擎）。
   - 巧思点：降低奖励模型偏差，提升泛化稳定性。
   - 适用：代码、数学、结构化输出任务。

4. 工具调用与语言动作解耦训练
   - 做法：将 tool policy 与 text policy 分开建模或分阶段训练。
   - 巧思点：减少动作空间耦合干扰，提高训练稳定性。
   - 适用：多 API、多检索器 agent。

5. 预算约束纳入目标函数（cost-aware RL）
   - 做法：将 token 成本、调用次数、时延作为约束或惩罚项。
   - 巧思点：避免“效果好但成本不可用”的伪最优策略。
   - 适用：生产部署。

6. 离线轨迹筛选 + 在线难例挖掘
   - 做法：离线阶段过滤低质量轨迹，在线阶段主动采样困难样本。
   - 巧思点：提高每次 rollout 的信息密度。
   - 适用：算力预算有限团队。

## 4. 方法选择建议（按场景）

1. 代码/数学可验证任务：
   - 首选：RLVR + 分层奖励 + offline/online 混合
   - 原因：可验证信号强，收益最稳定。

2. 开放域 research agent（检索-推理-写作）：
   - 首选：分层 credit assignment + PRM + 预算约束
   - 原因：长链路任务中中间监督是成败关键。

3. 多工具 API 复杂编排：
   - 首选：工具动作与文本动作解耦 + 约束优化（安全/成本）
   - 原因：可显著降低训练不稳定与策略崩塌。

4. 数据少、算力紧张：
   - 首选：偏好优化 warm start + 小步在线 RL
   - 原因：工程成本低，迭代快。

## 5. 我建议你优先采用的“组合配方”

- 推荐配方：
  1) SFT/偏好优化做初始化；
  2) 引入可验证奖励（能验证就不主依赖打分模型）；
  3) 分层任务拆解并给中间奖励；
  4) 加入成本/时延约束；
  5) 在线阶段只对难例做高质量 rollout。

- 这套配方的优势：
  - 在效果、稳定性、成本三者之间最平衡；
  - 对真实 agent 系统更可迁移；
  - 调参空间相对可控。

## 6. 交付文件

- Markdown：`/Users/bytedance/Documents/trae_projects/codex_test/rl_survey_test/Agentic_RL_survey_methods_report_2026-03-03.md`
- PDF：`/Users/bytedance/Documents/trae_projects/codex_test/rl_survey_test/Agentic_RL_survey_methods_report_2026-03-03.pdf`

