# Handoff: 对话 3 — 跑 SC-NDA-ML MVE（形态 A+C 双增量验证）

> 来源: S003（时域 CRLB GO_MVE + 信道校准修复 + MVE-SPEC 写完）| 交接目标: 新对话跑 SC-NDA-ML MVE
> 文件名: H003-conversation3-run-sc-nda-ml-mve.md
> 日期: 2026-07-06

## 到哪了（状态）

专题 `.sessions/2026-07-06-step4a-mve-execution/` 续接 S003。**单载波时域 NDA-ML 改进通过 FR-21 oracle 上界前置门控，GO_MVE**（D004）：

**CRLB 层理论支撑**（D004-a）：
- CRB_NDA(φ) = σ²/Σ_n |s(n)|²h(n)（全 N 符号）
- CRB_DA(φ) = σ²/Σ_{n∈P} |s_p|²h(n)（仅 N_p=N/4 pilot）
- M₀² 严格相消 → 比值 N_p/N = 1/4 → **CRLB 层 NDA-ML 优于 DA ML**

**公平对照 gain @ HD-FEC**（D004-b，信道校准修复后）：
- AWGN **+0.70 dB**（形态 A 频谱效率）
- weak **+1.20 dB**（形态 A+C）
- moderate **+1.92 dB**（形态 A+C 叠加）
- strong 物理不可达 HD-FEC（oracle 也不可达），但 NDA 全工作区赢 DA（形态 C 鲁棒性）

**信道校准修复**（关键，避免 BER floor 假象）：
- per-block h 均衡（NDA 盲 ĥ=mean(|rx|²)−1/(2γ)，DA pilot ĥ=mean(|r(p)/s(p)|²)，oracle 真 h）
- 两阶段相位（fft_foe(M0=8) 粗估 CFO + nda_ml_recovery(assume_df_zero=True) 估残余 CPE）
- SNR 扫扩至 26dB（TL-22 物理可达性）

**MVE-SPEC 已写完**：`projects/simulation/explore/single-carrier-nda-ml/SC-NDA-ML-MVE-SPEC.md`（9 节契约）。

## 下一步干什么（对话 3 三步，守 3 步上限）

### 步骤 1：报到 + 框架重读

报到（session-governance Trigger 1）+ 读：
- `.sessions/2026-07-06-step4a-mve-execution/topic-index.md`（不变量 13 条 + D001-D004 决策）
- `.sessions/2026-07-06-step4a-mve-execution/decisions.md`（D004 关键：公平对照框架 + CRLB 结论）
- `stages/gw-feasibility.md` §D 维度 D（MVE 11 步，重点 FR-11 架构摘要 + FR-14/15 baseline 对照 + FR-18 竞争格局）
- `thesis-lessons.md` TL-20（先建理论预期）/ TL-22（震撼结果查物理前提）/ TL-23（验证完再写文档）
- **本轮契约**：`projects/simulation/explore/single-carrier-nda-ml/SC-NDA-ML-MVE-SPEC.md`（9 节执行契约）
- **本轮关键产出**（执行依据）：
  - `_time_domain_crlb.py` + `_crlb_results.json`（CRLB + 修复后公平对照数据，gain 预期表来源）
  - `_ber_floor_diagnostic.py` + `_ber_floor_diagnostic.json`（信道校准修复方案）

### 步骤 2：派子 agent 跑 SC-NDA-ML MVE（守 FR-11/14/15/18）

**子 agent 任务**：按 SC-NDA-ML-MVE-SPEC.md §6 扫描设计 + §8 执行约束跑 MVE。

**关键纪律**：
- 守 D003：NDA-ML 调用——AWGN (df=0) 用 `nda_ml_recovery(assume_df_zero=True)`；星地（有 Doppler）用两阶段 `fft_foe(M0=8)` 粗估 CFO + `nda_ml_recovery(assume_df_zero=True)` 估残余 CPE
- 守公平对照：DA ML 总能量 = 信息符号 SNR + 1.25dB pilot overhead；NDA-ML 总能量 = 信息符号 SNR（纯数据）
- per-block h 均衡：NDA 盲 ĥ=mean(|rx|²)−1/(2γ)，DA pilot ĥ=mean(|r(p)/s(p)|²)，oracle 真 h
- N≥100000 符号/点（守 FR-21）
- block_size=256 + resolve_m16apsk_blockwise 解 M₀-fold 模糊

**扫描设计**（SPEC §6）：
- 调制：(8,8)-16APSK
- 信道：AWGN [5,8,10,12,14,16,18,20] + 湍流 weak/moderate/strong [5,10,15,20,22,24,26]
- 方案：DA ML（pilot sp=4）/ NDA-ML（升 M₀=8 + 盲 h + resolve blockwise）/ oracle（真相位 + 真 h）
- 输出：BER vs γ_tot 曲线 + 公平 gain 表 @ HD-FEC

**FR-11 架构摘要**（MVE 结果必含）：
- 动作空间：NDA-ML 升 M₀ 次幂盲去调制（连续相位估计）
- 决策粒度：per-block（256 符号）CPE 估计
- 对比范式：NDA-ML（无 pilot）vs DA ML（pilot sp=4，25% overhead），公平对照含 pilot 能量代价
- 奖励语义：BER @ HD-FEC threshold（信息符号有效 SNR）
- 先验对照：DA ML（最强简单先验，pilot-aided 近最优）

**FR-18 竞争格局分析**（MVE 结果必含）：
- 简化环境偏差：单载波时域（无 OFDM DFT 处理增益）+ GG 块衰落（无时变 h）+ per-block 独立 CPE（无跨块跟踪）
- 对主方法（NDA-ML）影响：升幂噪声放大无 DFT 增益抵消，deep fade 处不利
- 对 baseline（DA ML）影响：pilot sp=4 在 deep fade 处崩溃
- 预判真实化后：加跨块 KF/CPE 跟踪 → DA ML 高 SNR 反超可能强化（cross-over 位置移动）；加 OFDM 频域 ML → 完全不同架构（B11 路径，已 D002 排除）

### 步骤 3：主线整合 MVE 结果 → Go/Conditional/Kill 判定

**主线核查**（守不变量 10）：
- 子 agent 返回数字主线独立 grep 核查 JSON（不信任报告）
- 对照 SC-NDA-ML-MVE-SPEC.md §2 TL-20 预期表，标注每场景 PASS/DEVIATION
- 验证 NDA-ML vs oracle gap < 3dB（排除升幂实现错误）

**判定**（守 SPEC §5 + D004）：
- **Go (§D PASS)**：AWGN gain ≥ 0.5dB AND weak/moderate gain ≥ 0.5dB → 进 Step 5（Baseline 选定），写 feasibility_report.md
- **Conditional Go**：0.3 ≤ AWGN gain < 0.5dB，weak/moderate 仍 ≥ 0.5dB → 记录风险进 Step 5
- **Kill/Fail**：AWGN gain < 0.3dB OR weak/moderate gain < 0 → 转 B7

**MVE 结果产出**：
- `explore/single-carrier-nda-ml/sc_nda_ml_mve.py`（MVE 脚本）
- `explore/single-carrier-nda-ml/_mve_results.json`（BER 曲线 + gain 表 + 架构摘要 FR-11 + 竞争格局 FR-18）
- 可选：BER vs γ_tot 曲线 PNG

## 纪律（和下一步直接相关的约束）

1. **D004 公平对照框架**：DA ML 含 1.25dB pilot overhead 总能量代价，NDA-ML 纯数据。所有 BER 比较在相同总功率下
2. **D004-a CRLB 数学**：M₀² 严格相消，CRB_NDA/CRB_DA = N_p/N = 1/4。后续升幂 ML 分析用正确公式（不是上一轮误推的 64×）
3. **D003 nda_ml_recovery 调用**：AWGN (df=0) 用 `assume_df_zero=True`；星地（有 Doppler）用两阶段 fft_foe + nda_ml_recovery
4. **信道校准**：必须用 per-block h 均衡 + 两阶段 FOE+CPE（avoid BER floor 假象，根因见 _ber_floor_diagnostic.json）
5. **不变量 6 profile 第 8 次防线**：MVE 结果若强于预期（如 strong +4dB），先 TL-22 查物理前提（NDA-vs-oracle gap）再判 Go
6. **不变量 10 核查机制中性双向**：子 agent 返回数字主线独立 grep 核查 JSON
7. **TL-20 先建理论预期**：对照 SPEC §2 预期表，偏离即查
8. **TL-23 验证完再写文档**：MVE 出结果先核查再写进 feasibility_report.md
9. **TL-26 参数溯源**：所有参数从 params.py 取
10. **TL-13 共用同一信道**：用 generate_shared_realization_apsk

## 接口变更（如有代码改动）

```yaml
# 本轮已改（S003 产出，下轮继承）：
# common/ 已稳定（D003 修复后），本轮不动 common
# explore/single-carrier-nda-ml/ 已有：
- _time_domain_crlb.py（CRLB 推导 + 公平对照）
- _crlb_results.json（CRLB + 修复后公平对照数据）
- _ber_floor_diagnostic.py + .json（信道校准修复方案）
- SC-NDA-ML-MVE-SPEC.md（MVE 执行契约）

# 下轮产出（MVE 执行）：
- sc_nda_ml_mve.py（MVE 主脚本）
- _mve_results.json（BER 曲线 + gain 表 + FR-11 架构摘要 + FR-18 竞争格局）
```

## 失败数据附录（如涉及路线失败）

无（本轮 CRLB GO_MVE，未跑 MVE）。前轮失败数据见 H002 失败数据附录。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| 单载波 DA ML 近最优（pilot sp=4）vs B11 论文 DA ML（decision-feedback）不对等 | FR-14 baseline 公平对照 | D004 已用公平对照框架（含 pilot overhead）部分缓解 | MVE 验证后视情况补 decision-feedback DA ML 对照 |
| 时域升 M₀ 次幂噪声放大无 DFT 增益抵消 | TL-22 物理前提 | CRLB 推导已含（M₀² 相消） | MVE 验证 NDA-vs-oracle gap |
| B11 genie-aided 解卷绕（行 129-131）非可实现 | FR-14 公平对照 | MVE 用 resolve_m16apsk_blockwise（非 oracle） | 若 MVE NDA-ML 需更鲁棒解卷绕，补硬判决众数投票 |
| strong 湍流 HD-FEC 不可达（物理上限） | FR-21 工作点 | oracle 也不可达 = 物理上限非方法缺陷 | 若需 strong 工作点，换 AIR 指标或更低 FEC 阈值 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| SC-NDA-ML AWGN gain @ HD-FEC | ≥ 0.5 dB（公平对照）| D004 + SPEC §5 | CRLB 预测 +0.70dB（待 MVE 验证）|
| SC-NDA-ML weak/moderate gain @ HD-FEC | ≥ 0.5 dB | D004 + SPEC §5 | CRLB 预测 +1.2/+1.9dB（待 MVE 验证）|
| SC-NDA-ML strong NDA 全工作区赢 DA | NDA BER < DA BER（全 SNR）| D004 形态 C | CRLB 预测 是（待 MVE 验证）|
| NDA-ML vs oracle gap | < 3 dB（排除升幂 bug）| TL-22 | CRLB 0.38-2.58dB（待 MVE 验证）|

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（13 条）+ D001-D004 决策
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] CRB_NDA/CRB_DA = N_p/N = 1/4（核查 `_crlb_results.json` meta.analytic_crlb_conclusion.ratio）
  - [ ] 修复后 weak HD-FEC 可达（核查 `_crlb_results.json` gain_analysis.weak.hdfec_reachable=true min_ber=5.37e-4）
  - [ ] SC-NDA-ML-MVE-SPEC.md 9 节结构（核查 §1-9 全在）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on（problem-driven-redirection + cut-pattern + deep-read 3 个依赖均稳定）
- [ ] 已确认当前范围未违反"明确不含"（不回头救 6 次 Kill / 不改框架 / 不跳框架 / 不污染 common）

## 下一轮

**对话 3**（本 H003 目标）：跑 SC-NDA-ML MVE
- 步骤 1：报到 + 框架重读（含 SC-NDA-ML-MVE-SPEC.md 契约）
- 步骤 2：派子 agent 跑 MVE（守 FR-11/14/15/18）
- 步骤 3：主线核查 + Go/Conditional/Kill 判定

**对话 4**（视对话 3 结果）：
- 若 Go → 写 feasibility_report.md 进 Step 5（Baseline 选定）+ 视情况开 B7
- 若 Conditional/Kill → 转 B7 Gardner TED FOE 全流程

**对话 5**（最后）：B3 架构决策（多孔径阵列 vs 单链路）+ 视情况跑 B3 MVE
