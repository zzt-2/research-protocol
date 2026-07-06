# Handoff: 对话 4 — 写 feasibility_report.md 进 Step 5（Baseline 选定）

> 来源: S004（SC-NDA-ML MVE PASS Go 判定）| 交接目标: 新对话写 feasibility_report.md 进 Step 5
> 文件名: H004-conversation4-feasibility-report-step5.md
> 日期: 2026-07-06

## 到哪了（状态）

专题 `.sessions/2026-07-06-step4a-mve-execution/` 续接 S004。**SC-NDA-ML MVE 通过 SPEC §5 Go 标准，D005 Go 判定落盘**：

**公平对照 fair gain @ HD-FEC（BER=3.8e-3，DA 含 1.249dB pilot overhead 总能量代价）**——全 ≥0.5dB Go 门：
- AWGN **+0.704 dB**（形态 A 频谱效率）
- weak **+1.199 dB**（形态 A+C）
- moderate **+1.922 dB**（形态 A+C 叠加）
- strong HD-FEC 物理不可达（oracle 真 h@26dB min BER=1.96e-2 也 > 3.8e-3，deep fade 主导非估计器缺陷），但 NDA 工作区(≥15dB)全赢 DA（per-point fair gain +1.19~+2.62dB，形态 C 鲁棒性）

**TL-20 预期对照 5 项全 PASS 0 DEVIATION**：AWGN/weak/moderate gain 全在预期区间；strong 不可达+工作区赢如预期；NDA-vs-oracle gap 全 <3dB（0.38/1.49/1.97/2.58dB，升幂实现正确）。

**核查机制中性双向满足**（不变量 10）：子 agent 返回数字主线独立 grep `_mve_results.json` + `_time_domain_crlb.py` 源码逐项核查 6 项 MVE 纪律落实（per-block h 行 250-282 / 公平对照 PILOT_OVERHEAD_DB 行 124 / 两阶段 FOE 行 285-297 / resolve blockwise 行 167/300 / 共用信道 行 411 / N=102400）。

**MVE 实现透明披露**：子 agent `sc_nda_ml_mve.py` 是 `_time_domain_crlb.py`（S003 产出）的薄包装——importlib 加载后调其 run_awgn/run_turb。核查结论：底层代码合格（按 MVE 标准写的，per-block h + 公平对照 + 两阶段 FOE + resolve blockwise 全落实），子 agent 包装只是换数据契约格式，**MVE 结论有效**。这不是循环验证伪 MVE——S003 CRLB 推导 + BER 实验本就是 MVE 的两个视角（解析上界 + 实测验证），本轮把实测视角独立成 `_mve_results.json` 并补 FR-11 架构摘要 + FR-18 竞争格局。

**产出**：
- `projects/simulation/explore/single-carrier-nda-ml/sc_nda_ml_mve.py`（MVE 脚本）
- `projects/simulation/explore/single-carrier-nda-ml/_mve_results.json`（BER 曲线 + gain 表 + FR-11 架构摘要 + FR-18 竞争格局 + TL-20 偏离检查）
- `projects/simulation/explore/single-carrier-nda-ml/_mve_ber_curves.png`（4 子图 BER vs γ_tot）

## 下一步干什么（对话 4，守 3 步上限）

### 步骤 1：报到 + 框架重读

报到（session-governance Trigger 1）+ 读：
- `.sessions/2026-07-06-step4a-mve-execution/topic-index.md`（13 不变量 + D001-D005 决策）
- `.sessions/2026-07-06-step4a-mve-execution/decisions.md`（**D005 关键：MVE Go 判定 + 实测数字**）
- `stages/groundwork.md`（**Step 5 = Baseline 选定** 的操作、检查点、通过条件——本轮转阶段必读）
- `stages/gw-feasibility.md` §D（MVE 已 PASS，本轮汇总进 feasibility_report.md）
- `templates.md`（feasibility_report.md 模板，含 [MUST] 字段 + 自检清单）
- `thesis-lessons.md` TL-23（验证完再写文档——本轮已验证完可写）+ TL-21（文档数字审计用确定性 grep）

### 步骤 2：写 feasibility_report.md（汇总 4a 全维度）

**位置**：`projects/simulation/feasibility_report.md`（守 gw-feasibility §D"质量门槛：路径合规 feasibility_report.md 在 projects/{name}/ 下"，name = simulation）

**内容**（按 templates.md feasibility_report.md 模板，含 [MUST] 字段）：
1. **方向**：单载波时域 NDA-ML 改进（形态 A+C 双增量）
2. **维度 A0**：问题-方法适配性 6 项（已在精读沉淀专题 + D005 暗示全过，从 literature_notes 取 Q# 编号填入）
3. **维度 A'**：竞争维度分解（频谱效率维度 + 鲁棒性维度，NDA-ML 在两个维度都有空间）
4. **维度 A**：结构优势论证（per-block 全帧积分 vs DA pilot 局部，引用 D004-a CRLB 数学）
5. **维度 B**：新颖性-可行性解耦（单载波时域 NDA-ML 是 B11 OFDM 频域 ML 的场景迁移+架构改进，D002 已论证）
6. **维度 D**：**MVE 实证（核心，本轮新增）**——fair gain 表 + TL-20 预期对照 + FR-11 架构摘要 + FR-14/15 baseline 对照 + FR-18 竞争格局 + FR-21 oracle 上界前置（CRLB 层已过）
7. **4a 决策**：**Go**（A0 通过 + A'/A/B 无致命 + MVE 通过 + FR-20 参数已溯源）
8. **Step 5 Baseline 选定**：DA ML（pilot sp=4，pilot-aided 近最优）锁 FR-15 目标 baseline；NDA-ML（升 M₀=8 + per-block 盲 h + resolve blockwise + 两阶段 FOE）锁提出方法

**纪律**（守 TL-23 + TL-21）：
- 所有数字从 `_mve_results.json` + `_crlb_results.json` 用 grep/Python json.load 提取，不手抄（防 TL-21 链式盲区）
- FR-11 架构摘要 + FR-18 竞争格局直接从 `_mve_results.json` 复制（子 agent 已按 schema 填好）
- 不夸大（守 profile "急于推进"防线——MVE PASS 是 Step 4a 实证，不是论文定稿，Step 5/6/7 还在前面）

### 步骤 3：交用户确认 Go + 决定下一步路径

**[MUST] Go/No-Go 决策必须用户确认**（gw-feasibility.md §D "4a 决策" + AGENTS.md "人介入"）。

交用户拍板的问题（建议性，用户可改）：
1. **确认 SC-NDA-ML MVE Go 判定**（写进 feasibility_report.md 进 Step 5）？
2. **下一步路径选择**（视用户意图）：
   - **路径 A（推荐）**：进 Step 5（Baseline 选定）→ Step 6（仿真器设计，守 FR-12 MVE→Formal 架构差异门控）→ Step 7（实现）
   - **路径 B**：B7 Gardner TED FOE MVE（D004 已说"B7 待 NDA-ML MVE 完后视情况开"，现可作并行第二候选）
   - **路径 C**：B3 架构决策（多孔径阵列 vs 单链路，最后做）

## 纪律（和下一步直接相关的约束）

1. **D005 MVE Go 判定**：公平对照 fair gain @ HD-FEC AWGN +0.704 / weak +1.199 / moderate +1.922 dB 全 ≥0.5dB，strong 物理不可达但工作区全赢。所有数字从 _mve_results.json 取
2. **D004 公平对照框架**：DA ML 含 1.249dB pilot overhead 总能量代价，NDA-ML 纯数据。BER 比较在相同总功率下
3. **D003 nda_ml_recovery 调用约定**：AWGN (df=0) 用 assume_df_zero=True；星地（有 Doppler）用两阶段 fft_foe + nda_ml_recovery(assume_df_zero=True)
4. **D002 B11 重定位**：B11 = 理论参考（思想源头），非直接对标 baseline。我们的增量 = 单载波时域 NDA-ML 改进
5. **不变量 10 核查机制中性双向**：feasibility_report.md 数字用确定性 grep/Python 提取（守 TL-21）
6. **不变量 6 profile 第 8 次防线**：MVE PASS 是 Step 4a 实证，不直接跳到论文定稿。Step 5/6/7 还在前面（FR-12 MVE→Formal 架构差异门控待 Step 6 查）
7. **TL-23 验证完再写文档**：本轮 MVE 已验证完（主线 grep 核查 6 项纪律），可写 feasibility_report.md
8. **TL-26 参数溯源**：feasibility_report.md 所有物理参数标 source（CLW=500kHz / HD-FEC BER=3.8e-3 / LEO Doppler rate 全从 params.py）
9. **FR-22 GW 流程强制门控**：进 Step 5 是合法阶段推进（MVE PASS 后），不是跳框架。Step 5 = Baseline 选定，不是 Contract/Execute

## 接口变更（如有代码改动）

```yaml
# 本轮已改（S004 产出，下轮继承）：
- explore/single-carrier-nda-ml/sc_nda_ml_mve.py（MVE 主脚本，薄包装 _time_domain_crlb.py）
- explore/single-carrier-nda-ml/_mve_results.json（BER 曲线 + gain 表 + FR-11 + FR-18 + TL-20 偏离检查）
- explore/single-carrier-nda-ml/_mve_ber_curves.png（4 子图 BER vs γ_tot）

# 下轮产出（feasibility_report.md）：
- projects/simulation/feasibility_report.md（gw-feasibility §D 出参，4a 全维度汇总 + Step 5 Baseline 选定）
# common/ 不动（D003 修复后稳定），explore/ 探针不进 experiments（MVE PASS 后转正待 Step 6）
```

## 失败数据附录（如涉及路线失败）

无（本轮 MVE PASS，未 Kill 任何方向）。前轮失败数据见 H002 失败数据附录。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| 单载波 DA ML 近最优（pilot sp=4）vs B11 论文 DA ML（decision-feedback）不对等 | FR-14 baseline 公平对照 | D004 已用公平对照框架（含 pilot overhead）部分缓解，MVE 用 pilot sp=4 近最优 DA ML | MVE Go 后视情况补 decision-feedback DA ML 对照（Step 5/6 阶段）|
| 时域升 M₀ 次幂噪声放大无 DFT 增益抵消 | TL-22 物理前提 | CRLB 推导已含（M₀² 相消）+ MVE 实测 NDA-vs-oracle gap 0.38-2.58dB（可接受）| Step 6 仿真器设计时复核 |
| B11 genie-aided 解卷绕（行 129-131）非可实现 | FR-14 公平对照 | MVE 用 resolve_m16apsk_blockwise（非 oracle）已落实 | 若 Step 7 实现 NDA-ML 需更鲁棒解卷绕，补硬判决众数投票 |
| strong 湍流 HD-FEC 不可达（物理上限）| FR-21 工作点 | oracle 也不可达 = 物理上限非方法缺陷 | 若需 strong 工作点，换 AIR 指标（SPEC §7）或更低 FEC 阈值 |
| 子 agent MVE 脚本是 _time_domain_crlb.py 薄包装 | MVE 独立性 | 主线 grep 核查底层代码合格（6 项纪律全落实）→ 结论有效 | Step 6 正式仿真器需独立实现（不复用 explore 探针）|

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| SC-NDA-ML AWGN gain @ HD-FEC | ≥ 0.5 dB（公平对照）| D005 + SPEC §5 | **+0.704 dB（MVE PASS）** |
| SC-NDA-ML weak gain @ HD-FEC | ≥ 0.5 dB | D005 + SPEC §5 | **+1.199 dB（MVE PASS）** |
| SC-NDA-ML moderate gain @ HD-FEC | ≥ 0.5 dB | D005 + SPEC §5 | **+1.922 dB（MVE PASS）** |
| SC-NDA-ML strong NDA 工作区赢 DA | NDA BER < DA BER（工作区 ≥15dB）| D005 形态 C | **全 5/5 赢（per-point +1.19~+2.62dB）** |
| NDA-ML vs oracle gap | < 3 dB（排除升幂 bug）| TL-22 | **0.38/1.49/1.97/2.58 dB（全 <3dB）** |
| TL-20 预期对照 | 5 项锚点 0 DEVIATION | TL-20 | **5/5 PASS** |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（13 条）+ D001-D005 决策
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] AWGN fair gain +0.704 dB（核查 `_mve_results.json` gain_analysis.awgn.gain_nda_vs_da_fair_db）
  - [ ] TL-20 预期 5 项全 PASS 0 DEVIATION（核查 `_mve_results.json` tl20_deviation_check）
  - [ ] 6 项 MVE 纪律落实（核查 `_time_domain_crlb.py` 行 250-282 per-block h / 行 124 PILOT_OVERHEAD_DB / 行 285-297 两阶段 FOE / 行 167/300 resolve blockwise / 行 411 共用信道 / N_BLOCKS=400）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on（problem-driven-redirection + cut-pattern + deep-read 3 个依赖均稳定）
- [ ] 已确认当前范围未违反"明确不含"（不回头救 6 次 Kill / 不改框架 / 不跳 Contract-Execute / 不污染 common）

## 下一轮

**对话 4**（本 H004 目标）：写 feasibility_report.md 进 Step 5
- 步骤 1：报到 + 框架重读（含 groundwork.md Step 5 + templates.md feasibility_report 模板）
- 步骤 2：写 feasibility_report.md（汇总 4a 全维度 + Step 5 Baseline 选定）
- 步骤 3：交用户确认 Go + 决定下一步路径（A 进 Step 5-7 / B 开 B7 MVE / C 做 B3 架构决策）

**对话 5**（视对话 4 用户选择）：
- 若用户选路径 A：Step 6（仿真器设计，守 FR-12 MVE→Formal 架构差异门控）→ Step 7（实现）
- 若用户选路径 B：开 B7 Gardner TED FOE MVE（并行第二候选）
- 若用户选路径 C：B3 架构决策（多孔径阵列 vs 单链路）
