# [S006] GW Step 4a — Q-A 预测驱动自适应编码风险失配（MVE 证据驱动 KILL）

> 2026-08-03 | 阶段: GW Step 4a 可行性预判（A0/A′/A/B/D） | 状态: 完成 — Q-A 当前实例化 **KILL（recommendation，待用户确认）**，family 不 Kill；Q-B A0§0 判据3 致命暂存

## 目标

一个对话内完成（用户执行提示词 2026-08-03-1249）：
1. 对 Q-A/Q-B 完成 A0§0 与 A0 初筛，只选一个最强 survivor（Q-A 优先）；
2. 对 Q-A 完成 A′、A、B；
3. 全部前置门无致命时运行 bounded MVE；
4. 输出 Step 4a recommendation（executor 不自行 Go/No-Go）；
5. 不进入 Step 4b/5/Contract/Execute。

## 记录

### Phase A — A0§0 + A0 §1-6

- **A0§0**: Q-A 四判据全过（literature_notes §6 Q-A）→ 进 §1-6。**Q-B 判据3 致命**（R003 闭包：无合法 coherent 星地 AMC baseline，L023/L124/TCOMM2026/LCOMM2026 全 terrestrial，L165 sat 但 AO）→ A0§0 致命暂存，不进 §1-6。**survivor = Q-A**。
- **Galijasevic 身份债解除**: 直接读 content.md（title/authors/DOI 10.1109/OJCOMS.2024.011100 与 metadata.json 一致；"DOI 解析异常"= Crossref 未索引该 DOI，NSF PAR 是 authoritative OA，metadata.json note 已解释，非身份伪造）。公式/码率集/反馈模型从原 PDF 核对：选码=预测增益单值查表(content.md:116)；feedback=error-free+delay(content.md:116)；FER=Polyanskiy NA(content.md:257,261，**但 PDF→md 把 eq(23) 转丢**→ V1 禁重建，改用 Table-1 阈值绕过)；码率=16 离散 8/9…8/77(content.md:128)；信道=lognormal PSI=10(content.md:263)。
- **A0 §1-6**（Q-A）: §1 PASS（gap 存在[EMPIRICAL content.md:360/116 + Nguyen content.md:81脚注2]，量级待 C）；§2 PASS（时变+延迟+带噪=环境动态复杂）；§3 PASS（≥2 跨域 STRONG 先例：SALAD arXiv2510.05784 / Forbes2026 LEO NTN / Gao WCNC2024 / Chen&Han2023，子 agent ≤500词摘要）；§4 PASS（连续状态≫1000，贪心=Galijasevic=已知违约，非平凡）；§5 PASS（无 fatal 负面证据；Chen&Han2023 反向支持 A）；**§6 ⚠ 待 Phase C 量化**（全局 margin 覆盖度未知）。A0 通过（条件性）。

### Phase B — A′/A/B（Q-A）

- **A′**: 创新落点=(a)FER违约率维度（条件 margin 解 heteroscedastic 耦合）。条件性通过。
- **A**: baseline ladder B0(固定最低)/B1(Galijasevic点预测=M本体,Go对手)/B2(dev全局margin)/B3(dev分位数)/B4(条件分箱)/C1(条件分位数risk-aware)/O1(true-state oracle,Kill工具)。FR-03 增强基线强制；Go 判据=C1>最强增强 baseline ≥5% goodput 且 FER 违约不增；oracle 禁 Go。结构优势声称=条件化解耦合。条件性通过。
- **B**: 空白零假设 5 原因，2 个条件性致命点（全局margin已够 / τ_c物理性）待 Phase C。条件性通过。

### Phase C — headroom probe + testbed 语义 + V5 独立重算

- **C0 testbed 语义**: `_gg_time.py` 输出辐照度 h(E[h]=1,AR(1)块间)，与 Galijasevic gain 同构，调用链一致可复用；FER/选码层需新建（用 Table-1 阈值绕过 V1）。不 BLOCKED。
- **C1 τ_c 物理性**: td/tau_c 是谱非二元，td>tau_c 不致命（Nguyen2024 在此区用 ESN 工作=预测动机非终点）。dead-end#2 不成立。
- **C2 headroom probe**: 子 agent 跑脚本（dev seeds 0-49/test 50-99，27 cells × 7 methods，metamorphic gate (a) PASS）。raw: `projects/simulation/results/amc_q_a_risk_aware_rate/probe_headroom_raw.json`。
- **C3 V5 主线独立重算**:
  - **outage floor**（scipy N=2e6）: GG(5,2)=5.74% / (2.5,1.2)=11.85% / (4,0.5)=19.79%；**Galijasevic lognormal PSI=10 也有 15.60%**。即使 oracle O1 无法满足 FER 1e-6（floor 2-3 量级高于 1e-4 目标）。
  - **Pareto 支配**（27 cells 独立重算）: **C1 在 0/27 cells Pareto-dominate B1（M 本体）**；每 cell 是 TRADE（C1 更低违约但更低 goodput）= 保守重缩放，非前沿外推。
- **C4 预注册 Kill 裁决**: 命中 2 条（简单裕量覆盖≥95%主指标 / 退化为静态 margin calibration）+ 1 更深层诊断（主要失效=不可恢复 outage 非 prediction-uncertainty rate over-selection）。**Q-A 的 A 不是主要失效模式**。

### Phase D — 跳过

Phase C headroom probe（含 paired/seed隔离/冻结metric/metamorphic gate/V5）即 §D MVE-等价且 **FAILED**。按 §A0 致命立即停止 + §D "MVE 显示核心方法无结构性优势"→ Phase C 闭合 KILL，无需 held-out MVE。

### Step 4a recommendation = KILL（Q-A 当前实例化），family 不 Kill

依据（MVE 证据驱动，非 oracle-Kill，TL-32/FR-25 + profile 务实可毕业）: (1) C1 0/27 Pareto-dominate B1；(2) outage floor 使 1e-4 目标结构不可达；(3) 命中预注册 Kill 条件。不 Kill family: 2 reframe 路径（(a)加 outage action 改 M=新 Q-A'；(b)提高 operating point 需 14.8-65.8dB 不可行）均需新 GW 周期。可回收产出: probe 脚本 + outage-floor 诊断 + Pareto 评估方法。

## 决策引用

- D001-D005（历史，有效）。
- **D006（新建）**：Step 4a Q-A 实例化 KILL（MVE 证据驱动），family 不 Kill，2 reframe 路径记录，Q-B 判据3 致命暂存。
- **V007（新建）**：D006 + Step 4a 独立终审验证（14 项 checklist）。
- **R001-landscape / R001-receipt / R002 / R003**（历史，有效）。
- feasibility_report.md（新建）: `projects/thesis-fso/amc-groundwork/feasibility_report.md`。

## 范围确认

- 本轮是否在 scope boundary 内: **是**（Step 4a A0→A′→A/B→D，不动 Skill/p05 log/dormant receiver/common/params.py/正式论文结论；不进 4b/5/Contract/Execute；不覆盖旧 receiver feasibility_report）。
- executor 不自行最终 Go/No-Go，提交 recommendation 待用户确认（已遵守）。

## 后续

- **本轮 Step 4a 终态 = Q-A 实例化 KILL（recommendation），待用户确认**。
- **未宣称 Groundwork 闭合**: 当前 5 CORE < ≥8 整体完成门；缺 3 篇须进 Step 5 前补齐或用户处理。
- **下一合法动作（待用户确认）**: (i) 接受 KILL → 评估 Q-B 自建 baseline 工程量（用户决策）/ 调整 C / 换 AMC 子族 / 停止；(ii) reframe → 新 GW 周期（新 Q-A'）；(iii) 补齐 3 篇 CORE。
- **禁 agent 自行放宽 C**（跨阶段决策）。
