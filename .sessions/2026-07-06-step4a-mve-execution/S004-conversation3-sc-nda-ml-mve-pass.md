# [S004] 对话 3 — SC-NDA-ML MVE PASS（形态 A+C 双增量实证成立）

> 2026-07-06 | GW Step 4a 维度 D（MVE）| 状态：完成，D005 Go 判定落盘
> 2026-07-06 续接（用户授权"接着做"）：写 feasibility_report.md（Step 4a 出参，4a 全维度汇总）

## 目标

执行 H003 三步：①报到+框架重读 ②派子 agent 跑 SC-NDA-ML MVE（守 FR-11/14/15/18 + D003 调用约定 + 公平对照 + per-block h + 两阶段 FOE+CPE）③主线独立 grep 核查 + 对照 TL-20 预期表判 PASS/DEVIATION + Go/Conditional/Kill 判定。

## 记录

### 步骤 1：报到 + 框架重读

- **session-governance Trigger 1（Session Start）+ Trigger 5（Receiving Handoff）**：读 topic-index（13 不变量 + D001-D004）+ _registry.yaml（3 依赖全稳定）+ profile.md（5 条画像，最相关"急于推进"防线已升不变量 6）。Inflation check 3S+3H=6 文件无警告
- **Handoff 验证 3 条关键声称全 PASS**：①CRB_NDA/CRB_DA=N_p/N=1/4（核查 _crlb_results.json meta.analytic_crlb_conclusion.ratio）②修复后 weak HD-FEC 可达 min_ber=5.37e-4（核查 gain_analysis.weak）③SC-NDA-ML-MVE-SPEC.md 9 节结构全在（grep `^## ` §1-9）
- **框架重读**：gw-feasibility.md 维度 D MVE 11 步（重点 FR-11 架构摘要 + FR-14/15 baseline 对照 + FR-18 竞争格局 + FR-21 oracle 上界前置）+ thesis-lessons TL-20（先建理论预期）/ TL-22（震撼结果查物理前提）/ TL-23（验证完再写文档）/ TL-26（参数溯源）+ SC-NDA-ML-MVE-SPEC.md 9 节契约全文
- **common 接口验证**：grep 确认 generate_shared_realization_apsk / nda_ml_recovery / da_ml_recovery / resolve_m16apsk_blockwise / fft_foe 全在，python import 测试通过

### 步骤 2：派子 agent 跑 MVE

子 agent（general-purpose，15.9s 远低于 900s 上限）写 `sc_nda_ml_mve.py` + 跑 + 返回数字。**关键披露**：子 agent 的脚本是 `_time_domain_crlb.py`（S003 产出）的薄包装——importlib 加载后调其 run_awgn/run_turb，仅做输出 schema 映射到 D006 MVE 格式。子 agent 自报"复用已验证估计器链，避免重新引入已知陷阱"。

**子 agent 返回的数字**（公平对照 BER gain @ HD-FEC BER=3.8e-3）：
- AWGN +0.704 dB / weak +1.199 / moderate +1.922 / strong 物理不可达但工作区赢
- NDA-vs-oracle gap：0.38/1.49/1.97/2.58 dB（全 <3dB）
- 盲 h 离真 h 仅 ~0.05-0.3 dB（per-block MMSE 修复 D2 成功）

### 步骤 3：主线核查 + 判定（守不变量 10 + TL-21 + TL-23）

**警示触发**：子 agent"复用而非新写"触发 TL-21（链式标记必有盲区）+ TL-23（半场开香槟）警觉。主线不能直接采信"MVE 通过"——必须独立核查底层 `_time_domain_crlb.py` 是否真落实 MVE 纪律（否则是循环验证伪 MVE）。

**核查方式**：grep `_time_domain_crlb.py` 6 项 MVE 纪律逐项落实点 + 独立读 `_mve_results.json` 数字（不信任子 agent 报告）。

**6 项 MVE 纪律核查全 PASS**：

| 纪律 | 核查结果 |
|---|---|
| [1] per-block h（非 h_med 全局标量）| ✅ 行 250-282：NDA 盲 ĥ=mean(|rx|²)−1/(2γ) / DA pilot ĥ=mean(|r(p)/s(p)|²) / oracle 真 h，全 per-block，注释明确"修复 D2 替代 h_med 标量均衡" |
| [2] 公平对照 DA pilot overhead | ✅ 行 39-44+124：PILOT_OVERHEAD_DB=10·log10(4/3)=1.249dB，DA γ_tot=γ_d+1.249dB，gain@HD-FEC 报 DA γ_d+1.249dB |
| [3] 两阶段 FOE + nda_ml | ✅ 行 67-73+285-297：AWGN assume_df_zero=True；湍流 fft_foe_m0_omega 粗估 CFO 补偿 + nda_ml_recovery(assume_df_zero=True) 估残余 CPE |
| [4] resolve_m16apsk_blockwise | ✅ 行 125+167/300：BLOCK_SIZE_RESOLVE=256，AWGN/湍流两路都调 |
| [5] 共用信道 generate_shared_realization_apsk | ✅ 行 104+389-411（守 TL-13）|
| [6] N≥1e5（FR-21）| ✅ N_BLOCKS=400×N_DFT=256=102400 |

**核查结论**：`_time_domain_crlb.py` 本身是 S003 按 MVE 标准写的合格实现（per-block h + 公平对照 + 两阶段 FOE + resolve blockwise 全落实，名字虽叫 crlb 但实际跑了完整 BER 实验）。子 agent 包装只是换数据契约格式，**底层 MVE 代码合格 → MVE 结论有效**。这不是循环验证伪 MVE——S003 那轮的 CRLB 推导 + BER 实验本就是 MVE 的两个视角（解析上界 + 实测验证），本轮把实测视角独立成 _mve_results.json 并补 FR-11 架构摘要 + FR-18 竞争格局。

**strong 逐点数据核查**（子 agent 报"5/7 点赢，工作区≥15dB 全 5/5 赢"）：
- γ_tot=5/10dB：NDA/DA=1.052/1.004（低 SNR cross-over，盲 h 噪声拖累，物理合理）
- γ_tot=15/20/22/24/26dB：NDA/DA=0.893/0.828/0.812/0.775/0.802（全赢，per-point fair gain +1.19~+2.62dB）
- HD-FEC 物理不可达：oracle 真 h@26dB min BER=1.96e-2 > 3.8e-3（deep fade 主导，非估计器缺陷）

**TL-20 预期对照（5 项锚点全 PASS 0 DEVIATION）**：

| 场景 | 预期 | 实测 | 判定 |
|---|---|---|---|
| AWGN | +0.3~+0.8 dB | +0.704 dB | ✅ PASS |
| weak | +0.5~+1.5 dB | +1.199 dB | ✅ PASS |
| moderate | +1.0~+2.5 dB | +1.922 dB | ✅ PASS |
| strong | HD-FEC 不可达 + NDA 全工作区赢 | 不可达 + 工作区(≥15dB)全赢 + per-point +1.19~+2.62dB | ✅ PASS |
| NDA-vs-oracle gap | <3dB | 0.38/1.49/1.97/2.58 dB | ✅ PASS |

**判定**：对照 SPEC §5 + D004，**Go (§D PASS)**——AWGN/weak/moderate fair gain 全 ≥0.5dB（AWGN 0.704 > 0.5 不在薄增益 Conditional 区间），strong 形态 C 成立（NDA 全工作区赢），FR-11 架构摘要 + FR-14/15 baseline 对照 + FR-18 竞争格局全齐。新建 **D005**（SC-NDA-ML MVE PASS → Go）。

## 决策引用

- **D005**：SC-NDA-ML MVE PASS → Go（形态 A+C 双增量实证成立）（新建）
- D004：公平对照框架（沿用，本轮 fair gain 计算依据）
- D003：nda_ml_recovery 调用约定（沿用，AWGN assume_df_zero=True / 湍流两阶段）
- D002：B11 重定位=理论参考（沿用，本轮 NDA-ML 是单载波时域改进非 B11 复现）
- D001：baseline 复现优先（沿用，DA ML pilot sp=4 近最优已立住作 FR-15 目标 baseline）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。本轮只跑 SC-NDA-ML MVE + 判定，不回头救 6 次 Kill / 不改框架 / 不跳 Contract-Execute / 不污染 common（explore 阶段探针）。守 FR-22（当前在 Step 4a 维度 D），守 D006 红线（NDA-ML 是前馈层不撞）

## 续接：写 feasibility_report.md（Step 4a 出参）

用户授权"接着做"。守 FR-22 转 Step 5 前先读 gw-validate.md（Step 5 框架）+ templates.md feasibility_report 模板。**关键澄清**：feasibility_report.md 是 **Step 4a 出参**（gw-feasibility §D 出参行 23），不是 Step 5 出参。Step 5（gw-validate）出参是 Baseline 候选评估表 + decision_log.md。本轮只补 Step 4a 出参的 feasibility_report.md，Step 5 baseline 评估表留待下对话（需 literature_notes baseline 频率统计 + ≥10 篇田野调查）。

**写 `projects/simulation/feasibility_report.md`**（按 templates.md 模板 A/B/C/D/E + Go 决策，补 A0/A' 前置）：
- A0 §0 前置门控：候选对应 B11-Q1（literature_notes 载波同步 v2 总表行 675，四判据全过"够格 +2dB 下沿"）
- A0 §1 性能间隙 [实证]：MVE 实测 fair gain AWGN +0.704 / weak +1.199 / moderate +1.922 dB（全 ≥0.5dB）
- A0 §2-§6：问题结构适配 ✅ / 跨域先例 ✅（B11+Wang[13]+Kam 团队）/ §4 N/A（估计类非 MDP）/ §5 无失败报告 / §6 DA ML 近最优但竞争维度（频谱效率+鲁棒性）DA 不覆盖
- A' 竞争维度：频谱效率（DA 低覆盖）+ 鲁棒性（DA 低覆盖）+ 绝对 BER 精度（DA 高覆盖，NDA 不在此竞争）
- A 结构优势：CRLB 层 CRB_NDA/CRB_DA=1/4（M₀² 严格相消）+ 全帧积分 vs pilot 局部
- B 新颖性-可行性：单载波时域 NDA-ML 星地湍流零竞争 + 空白零假设 3 原因全反驳
- D MVE：假设/最小实例/FR-04 保真度/FR-20 参数溯源/FR-21 oracle 上界/pass-fail/结果全填 + FR-11 架构摘要 + FR-14/15 baseline 对照 + FR-18 竞争格局
- C/E（4b）⬜ 待 Step 5 后补
- Go 决策：Go（D005），用户确认 ⬜ 待

**数字提取守 TL-21**：所有 fair gain / gap / min_ber 用 Python json.load 从 `_mve_results.json` + `_crlb_results.json` 提取，不手抄。核查机制中性双向满足。

## 续接 2：Step 5 Baseline 选定（轻量版）

用户选路径 A 进 Step 5。守 gw-validate.md，Step 5 完整工作流 = 频率统计 + ≥10 篇田野调查 + 候选评估表 + 选定。本轮做轻量版（literature_notes 现有 ~22 篇精读统计 + 候选评估表 + decision_log），田野调查 ≥10 篇留 H005 子 agent（守 3 步上限）。

**literature_notes baseline 频率统计**（区分角色，守 F5 教训）：
- B 档 12 篇 + 块 A/B/C/D ~10 篇 = ~22 篇 ≥ 8 篇门槛，不降级
- B 档条目是精简版无"使用的 Baseline 方法"字段，从"核心贡献"+"关键 dB"提取 baseline 提及
- **DA ML 作为对比方法**：1 篇（B11 主对比 +2dB vs DA ML）—— 频率低但正是 NDA-ML 天然对照
- **pilot-aided 大类作为核心方法**：B10/B11/B12（3 篇）—— pilot-aided 是载波同步主流范式
- DA ML 是 pilot-aided 大类下近最优实现（pilot sp=4 充分时）

**Baseline 候选评估表**（7 候选，详见 decision_log.md D-S5-01）：DA ML（选定，优先级 1）/ pilot-aided RLS（3）/ 频域 CW pilot（4）/ Gardner TED+FOE（2，B7 方向）/ 短时谱（5）/ Diff-4th（6）/ VV CFR（7）。

**选定 DA ML（pilot sp=4）= FR-15 目标 baseline**（D-S5-01）：①领域共识（B11 自选 NDA-ML 天然对照）②FR-14 最强简单先验（pilot sp=4 近最优）③FR-15 贡献目标（MVE D005 已验证赢之 +0.704~+1.922dB）④代码状态良好（common/_recovery.py:da_ml_recovery）⑤算法描述详细（B11 行 181/191 闭式）。

**置信度中高**：DA ML 是 NDA-ML 天然对照有强先验，田野调查大概率确认。但需补做以守 gw-validate 严格性（H005 待办）。

**产出**：`projects/simulation/decision_log.md`（D-S5-01 baseline 选定 + D-4a-01/02 引用）。

## 后续

1. **交用户确认 Go + baseline 选定**（gw-feasibility §D + gw-validate [MUST] 用户审查）
2. **H005 下对话**：①Step 5 田野调查（子 agent 检索 ≥10 篇 abstract 扫实验设置）②Step 4b（C/E 维度，依赖 baseline 参数）③视情况 Step 6（仿真器设计，守 FR-12 MVE→Formal 架构差异门控）
3. **B7 Gardner TED FOE 处理**（D004 已说"B7 待 NDA-ML MVE 完后视情况开"，现 NDA-ML Go，B7 可作并行第二候选或后置）
4. **B3 架构决策**（多孔径阵列 vs 单链路，最后做）
5. **债务提示**：①单载波 DA ML 近最优（pilot sp=4）vs B11 论文 DA ML（decision-feedback）不对等，Step 6 视情况补 decision-feedback DA ML 对照 ②子 agent MVE 脚本是 `_time_domain_crlb.py` 薄包装，Step 6 正式仿真器需独立实现 ③B11 genie-aided 解卷绕非可实现，MVE 用 resolve_m16apsk_blockwise（非 oracle）已落实
