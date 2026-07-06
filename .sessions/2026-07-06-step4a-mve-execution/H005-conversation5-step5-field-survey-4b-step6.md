# Handoff: 对话 5 — Step 5 田野调查补完 + 4b（C/E）+ Step 6（仿真器设计）

> 来源: S004（SC-NDA-ML MVE PASS + feasibility_report + Step 5 baseline 选定轻量版）| 交接目标: 新对话补完 Step 5 田野调查 + 做 4b + 进 Step 6
> 文件名: H005-conversation5-step5-field-survey-4b-step6.md
> 日期: 2026-07-06

## 到哪了（状态）

专题 `.sessions/2026-07-06-step4a-mve-execution/` 续接 S004。**SC-NDA-ML MVE PASS Go 判定（D005）+ feasibility_report.md 写完 + Step 5 Baseline 选定轻量版完成（D-S5-01）**：

**Step 4a 完整出参**（`projects/simulation/feasibility_report.md`）：A0/A'/A/B/D 全维度汇总 + Go 决策。公平对照 fair gain @ HD-FEC AWGN +0.704 / weak +1.199 / moderate +1.922 dB 全 ≥0.5dB，strong 物理不可达但工作区(≥15dB)全赢 DA。TL-20 预期 5 项全 PASS 0 DEVIATION。NDA-vs-oracle gap 全 <3dB。

**Step 5 轻量版**（`projects/simulation/decision_log.md` D-S5-01）：基于 literature_notes ~22 篇精读统计 + 候选评估表（7 候选），**选定 DA ML（pilot sp=4）= FR-15 目标 baseline**。理由：①领域共识（B11 自选 NDA-ML 天然对照）②FR-14 最强简单先验（pilot sp=4 近最优）③FR-15 贡献目标（MVE D005 已验证赢之）④代码良好（common/_recovery.py:da_ml_recovery）⑤算法描述详细（B11 行 181/191）。

**未完成**（H005 待办）：①Step 5 田野调查（gw-validate Step 2，≥10 篇额外论文 abstract 扫描）②Step 4b（C/E 维度，依赖 baseline 参数）③Step 6（仿真器设计）。

## 下一步干什么（对话 5，守 3 步上限）

### 步骤 1：报到 + 框架重读

报到（session-governance Trigger 1）+ 读：
- `.sessions/2026-07-06-step4a-mve-execution/topic-index.md`（13 不变量 + D001-D005 + D-S5-01）
- `projects/simulation/feasibility_report.md`（Step 4a 出参，本轮 4b 补完的对象）
- `projects/simulation/decision_log.md`（D-S5-01 baseline 选定，本轮田野调查补完的对象）
- `stages/gw-validate.md`（Step 5 完整工作流，重点 Step 2 田野调查）
- `stages/gw-feasibility.md` §4b（C/E 维度，本轮补完）
- `stages/groundwork.md`（Step 6 = 仿真器设计的入口）
- `thesis-lessons.md` TL-21（文档数字审计确定性 grep）/ TL-23（验证完再写文档）

### 步骤 2：派子 agent 补 Step 5 田野调查（gw-validate Step 2）

**子 agent 任务**：检索"星地 FSO / 单载波 M-APSK 载波同步 experiment comparison baseline"≥10 篇，扫 abstract 实验设置，与精读统计（D-S5-01 评估表）交叉验证。

**关键纪律**：
- 守 AGENTS.md「主对话严禁 WebSearch / webReader」→ 必须在子 agent 中执行，返回 ≤500 词摘要
- 守 tools-guide.md → 用 `tools/search --source ieee` 或 `tools/search --source semantic_scholar`（脚本，结果结构化可控）
- 扫 abstract 看"实验设置里用了什么 baseline"，不读全文
- 与 D-S5-01 评估表交叉：田野中出现但精读未覆盖的方法 → 标"候选补充"；精读高频但田野罕见 → 标"可能非领域共识"

**预期结果**：DA ML / pilot-aided 大类大概率在田野中也是高频 baseline（载波同步主流范式），确认 D-S5-01 选定。若发现新高频 baseline，补进评估表。

**更新 decision_log.md D-S5-01**：田野调查结果填进"待办"段，置信度从"中高"升到"高"（或标注发现的新候选）。

### 步骤 3：做 Step 4b（C/E 维度）补完 feasibility_report.md

**维度 C（仿真条件可行性）**（gw-feasibility §4b）：
1. 仿真环境能否创造条件让核心方法（NDA-ML 升 M₀ 次幂）优势体现？→ MVE 已验证能（common/ 信道 + 估计器跑通）
2. 目标方法关键特征在仿真中是否有足够大差异信号？→ MVE fair gain 0.7-1.9dB 有差异信号
3. 仿真是否包含 NDA-ML 擅长的信号特征？→ GG 块衰落 + Wiener PN + deep fade 全包含
4. 领域专属检查（domain-comms.md "过于平滑"预警）→ 无（MVE BER 曲线陡峭，非平滑假象）

**维度 E（资源/风险比例）**：
1. Baseline 代码状态：DA ML 已实现（common/），NDA-ML 已实现（MVE 跑通），代码状态良好
2. 时间投入估计 vs 贡献：MVE 已 PASS，Step 6-7 工程量中等（正式仿真器 + 训练/评估流水线）
3. 失败兜底：形态 A（AWGN 频谱效率）已 MVE PASS 可独立成立；形态 C 即使 Step 6 退化也有 weak/moderate 数据支撑

**4b 决策**：大概率 Go（MVE 已 PASS，仿真条件已验证，资源风险可控）。填进 feasibility_report.md C/E 段 + Go 决策用户确认。

## 纪律（和下一步直接相关的约束）

1. **D005 MVE Go 判定 + D-S5-01 baseline 选定**：本轮在此基础上补完 Step 5 + 4b，不重跑 MVE
2. **田野调查必须子 agent**（守 AGENTS.md 主对话严禁 WebSearch）+ 用 tools/search 脚本（结构化结果）
3. **FR-22 GW 流程强制门控**：Step 5 + 4b 是合法阶段推进（4a Go 后），Step 6（仿真器设计）前必须 4b 通过
4. **FR-12 MVE→Formal 架构差异门控**（Step 6 触发）：simulator-design.md 必须含 MVE vs Formal 架构差异对照表（动作空间/决策粒度/对比范式/奖励语义/先验强度）。MVE 架构摘要见 `_mve_results.json` fr11_architecture_summary
5. **不变量 6 profile 第 8 次防线**：4b Go 不等于可以直接写论文。Step 6（仿真器设计）+ Step 7（实现）还在前面
6. **TL-23 验证完再写文档**：4b 是分析性维度（仿真条件 + 资源风险评估），不需额外验证，分析完直接写 feasibility_report.md
7. **TL-21 文档数字审计**：feasibility_report.md C/E 段若引用 MVE 数字，用 Python json.load 从 `_mve_results.json` 提取
8. **D006 红线**：NDA-ML 是前馈层（升 M₀ 次幂 + 单正弦 ML 闭式，无环路 TF），不撞 D006

## 接口变更（如有代码改动）

```yaml
# 本轮已改（S004 产出，下轮继承）：
- projects/simulation/feasibility_report.md（Step 4a 出参，C/E ⬜ 待 4b 补完）
- projects/simulation/decision_log.md（D-S5-01 baseline 选定 + D-4a-01/02 引用，田野调查待办）
- explore/single-carrier-nda-ml/sc_nda_ml_mve.py + _mve_results.json + _mve_ber_curves.png（MVE 产出）

# 下轮产出（Step 5 田野调查 + 4b + Step 6 入口）：
- projects/simulation/decision_log.md（D-S5-01 田野调查结果更新 + D-4b-01 4b 决策）
- projects/simulation/feasibility_report.md（C/E 段补完）
- 若进 Step 6：projects/simulation/SPEC.md 补 NDA-ML 正式仿真器段 + simulator-design.md（守 FR-12）
# common/ 不动（D003 修复后稳定），explore/ 探针转 experiments/ 待 Step 6 后
```

## 失败数据附录（如涉及路线失败）

无（本轮 MVE PASS + baseline 选定，未 Kill 任何方向）。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| Step 5 田野调查 ≥10 篇未做 | gw-validate Step 2 严格性 | D-S5-01 轻量版基于 ~22 篇精读，置信度中高 | H005 步骤 2 子 agent 补做 |
| 单载波 DA ML 近最优（pilot sp=4）vs B11 论文 DA ML（decision-feedback）不对等 | FR-14 baseline 公平对照 | D004 公平对照框架部分缓解 | Step 6 视情况补 decision-feedback DA ML 对照 |
| 子 agent MVE 脚本是 `_time_domain_crlb.py` 薄包装 | MVE 独立性 | 主线 grep 核查底层代码合格→结论有效 | Step 6 正式仿真器需独立实现（不复用 explore 探针）|
| strong 湍流 HD-FEC 不可达（物理上限）| FR-21 工作点 | oracle 也不可达 = 物理上限非方法缺陷 | 若需 strong 工作点，换 AIR 指标（SPEC §7）或更低 FEC 阈值 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| SC-NDA-ML AWGN gain @ HD-FEC | ≥ 0.5 dB（公平对照）| D005 + SPEC §5 | **+0.704 dB（MVE PASS）** |
| SC-NDA-ML weak/moderate gain @ HD-FEC | ≥ 0.5 dB | D005 + SPEC §5 | **+1.199/+1.922 dB（MVE PASS）** |
| SC-NDA-ML strong NDA 工作区赢 DA | NDA BER < DA BER（≥15dB）| D005 形态 C | **全 5/5 赢（per-point +1.19~+2.62dB）** |
| NDA-ML vs oracle gap | < 3 dB（排除升幂 bug）| TL-22 | **0.38/1.49/1.97/2.58 dB（全 <3dB）** |
| DA ML 是领域共识 baseline | 田野调查 ≥10 篇确认 | gw-validate Step 2 | ⬜ 待 H005（精读统计已确认，置信度中高）|

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（13 条）+ D001-D005 + D-S5-01 决策
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] feasibility_report.md Go 决策（核查 `projects/simulation/feasibility_report.md` Go/No-Go 段）
  - [ ] DA ML 选定 FR-15 目标 baseline（核查 `projects/simulation/decision_log.md` D-S5-01）
  - [ ] MVE fair gain 数字（核查 `_mve_results.json` gain_analysis.awgn/weak/moderate.gain_nda_vs_da_fair_db）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on（problem-driven-redirection + cut-pattern + deep-read 3 个依赖均稳定）
- [ ] 已确认当前范围未违反"明确不含"（不回头救 6 次 Kill / 不改框架 / 不跳 Contract-Execute / 不污染 common）

## 下一轮

**对话 5**（本 H005 目标）：Step 5 田野调查补完 + 4b（C/E）+ 视情况 Step 6 入口
- 步骤 1：报到 + 框架重读（gw-validate Step 2 + gw-feasibility §4b + groundwork Step 6）
- 步骤 2：派子 agent 补 Step 5 田野调查（≥10 篇，守主对话严禁 WebSearch）
- 步骤 3：做 4b（C/E 维度）补完 feasibility_report.md + 4b Go 决策

**对话 6**（视对话 5 结果）：
- 若 4b Go → Step 6（仿真器设计，守 FR-12 MVE→Formal 架构差异门控）→ Step 7（实现）
- 若 4b 有致命信号 → Pivot（回 Step 5 重选 baseline 或调整仿真条件）

**对话 7**（最后）：B3 架构决策（多孔径阵列 vs 单链路）+ 视情况开 B7 Gardner TED FOE MVE
