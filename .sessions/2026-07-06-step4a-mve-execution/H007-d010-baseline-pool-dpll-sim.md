# Handoff: D-010 baseline 标准确立 + baseline 池建设 + DPLL 仿真待跑

> 来源: S010 | 交接目标: 跑 DPLL BER 仿真，立住异族 baseline，再决定写简报跟老师沟通路线
> 文件名: H007-d010-baseline-pool-dpll-sim.md

## 已完成边界

### 1. blit IEEE venue 解析缺陷已修
`tools/blit.py:ieee_search`（原 217-243 行）venue 原硬编码空串，已加多策略解析（description/publisher 元素 + fallback 正则）。**实测验证成功**：3 组 blit IEEE 查询共 22 条结果，venue 全部非空、提取准确（实测拿到 `Journal of Lightwave Technology` / `IEEE Transactions on Communications` / `IEEE Photonics Journal` 等）。

### 2. 老师电话标准固化（D-010 + voice.md）
导师 2026-07-08 电话确立 baseline 选取 5 条标准（D-010 active）：
1. 同场景（星地湍流信道）
2. 同类型层级（载波同步/定时/均衡层，不深入子层）
3. 不找接近方法当 baseline（VV 同族禁主比）
4. 近年+权威（2022+ IEEE Trans）
5. 找方向/复现只看够好的（避 letter/仿真不全）

voice.md 末尾已记 4 条原话。D-010 已写进 decisions.md。

### 3. baseline 池检索 + 精读完成
- **10 组查询**（7 API tools/search + 3 blit IEEE），合计召回 ~220 篇
- **4 篇第一梯队精读**（C1/C3/C4/C6），结论：**没有一篇是干净 baseline**，都缺要素
- 详见下方"失败数据附录"

### 4. 关键认知修正：通信领域 baseline 是自实现的
通信论文 baseline 一般是**自实现**（在自己参数下跑经典方法），不要求别人论文用一样参数。引用文献只证明"方法在该层合法、有人用过"。所以：
- baseline 结构 = 自实现（DA-ML 主 + DPLL 异族 + VV/BPS fellow）
- 文献引用支撑合法性（C1 证 DPLL 在星地FSO载波同步有人用 / C6 证星地 Gamma-Gamma + 相位估计有人做）
- C4/C6 不是 baseline，是 related work 场景引用

## 不要做什么

- **不要找"完全相同场景+方法"的别人论文照搬参数当 baseline**——通信领域不这么做，自实现是常态
- **不要用 VV/BPS 当主 baseline**——老师明说"不找接近方法"，D-009 已证 VV 跟 NDA-ML 同族持平
- **不要信子 agent 检索报告的标题/DOI 配对**——本轮发现 C2 子 agent 报的标题跟 DOI 对不上（10.1109/JLT.2023.3270673 实际是 B9 DRE 自相干，不是 Multi-Aperture MIMO Equalizer）。Crossref 核验 DOI 是必须的
- **不要用 dpll_track（4次方鉴相器）跑 16APSK**——16APSK 的 M₀=8 非 4 次方对称，要用 dpll_track_dd（decision-directed）改 m16apsk 判决

## 必读

1. `.sessions/2026-07-06-step4a-mve-execution/topic-index.md` — 不变量 + 当前位置（S010）
2. `.sessions/2026-07-06-step4a-mve-execution/decisions.md` D-010 — 老师 5 条标准 + 工具链核查
3. `.sessions/2026-07-06-step4a-mve-execution/voice.md` 末尾 — 老师电话原话
4. `projects/simulation/common/_recovery.py` L8-75 — dpll_track / dpll_track_dd 实现
5. `projects/simulation/common/_kf.py` — KF 4 变体实现
6. `stages/gw-feasibility.md` §D — MVE 维度 D 规范（如果要跑正式 MVE）

## 接口变更（如有代码改动）

- `tools/blit.py:ieee_search` — venue 解析已改（加 description/publisher 元素解析 + fallback 正则），无接口变更

## 失败数据附录（4 篇精读结论）

| # | 论文 | venue/年 | 缺口 | 结论 |
|---|---|---|---|---|
| C1 | Paillier DPLL | JLT 2020 | BPSK(非16APSK) + 相位屏(非GG) + 2020(略早) + 无多seed | ⚠️有条件：DPLL 族星地FSO代表作，需重实现到16APSK+GG |
| C3 | Zhang AKF+盲均衡 | Photonics J 2023 | lognormal(非GG) + 4孔径SIMO + π/4-QPSK + venue非顶级Trans | ⚠️谨慎：架构差异大，仅方法学参考 |
| C4 | Wang 帧同步+载波恢复 | OE 2024 | **非CPR层**(帧同步+FOE) + 相位屏(非GG) + QPSK/16QAM | ❌不可当baseline |
| C6 | Zhou 元学习 | IoT-J 2024 | **MIMO信道估计**(非逐符号CPR) + 4QAM + PLL/Tikhonov单偏移(非Wiener) | ⚠️有条件：场景对口但指标不对齐，作定性参照 |

**结构性发现**：4 篇都没有"星地+Gamma-Gamma+单载波逐符号CPR+16APSK+近年Trans"全满足。这印证 D006 open gap：星地FSO湍流下的单载波CPR本身就是领域空白——不是检索不到位，是这个交叉点确实没人做。

**C2 勘误**：子 agent 检索报告 C2（DOI 10.1109/JLT.2023.3270673）标题为"Multi-Aperture MIMO Adaptive Equalizer"，Crossref 核验实际是"Simplified Self-Coherent FSO + DRE"（= B9，已精读过，自相干绕开载波同步路线，非均衡层 baseline）。子 agent 标题-DOI 配对有误，已剔除。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| DPLL 不支持 m16apsk | baseline 要在我们的调制下跑 | dpll_track_dd 判决写死 qam16 | 本轮改 hard_decision(mod='m16apsk') |
| blit venue 修复未在 tools-guide 记录 | FR-06 工具引入检查 | 代码已改文档未更新 | 专题稳定后批量更新 tools-guide |
| 框架/skill 候选更新点未落实 | D-010 标注了3个候选点 | groundwork S4-7 / code-quality / tools-guide | 专题稳定后批量改 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| DPLL BER 仿真 | 在 16APSK+GG 下 BER 曲线合理（高SNR趋近oracle，低SNR不崩） | TL-20 理论预期 | 未跑 |
| DPLL vs NDA-ML | DPLL 不应远超 NDA-ML（否则 NDA-ML 无价值）；也不应全输（否则 DPLL 太弱不像合法baseline） | D-009 NDA-ML vs VV 持平逻辑 | 未跑 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称（列出验证了哪些）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反"明确不含"

## 下一轮

### 任务：跑 DPLL BER 仿真，立住异族 baseline

**目标**：在 NDA-ML 主实验的相同参数下（16APSK + Gamma-Gamma + 2.5GBaud + 10kHz + 5 湍流场景），跑 DPLL 的 BER 曲线，确认 DPLL 作为非近亲异族 baseline 立得住。

**执行步骤**：

1. **适配 dpll_track_dd 支持 m16apsk**
   - `common/_recovery.py:8` 的 `dpll_track_dd`，判决分支（:21-27）写死了 qpsk/qam16
   - 改法：加 `elif mod == 'm16apsk': dec = hard_decision(rotated, mod='m16apsk')`
   - `hard_decision`（_modulation.py:84）已支持 m16apsk，直接调
   - **不要用 dpll_track（:59）**——它用 4 次方鉴相器，对 16APSK 不对（M₀=8）

2. **跑 DPLL BER 仿真**
   - 复用主实验脚本框架（`simulator/` 下的 sc_nda_ml 主实验）
   - 参数全对齐主实验：16APSK / 2.5GBaud / 10kHz / 5 湍流场景（weak/moderate/strong/uplink_moderate/uplink_strong）/ SNR 扫描
   - DPLL 参数：omega_n / zeta 需调（dpll_track_dd 默认 omega_n=8e6, zeta=√2/2，可能要适配 16APSK + GG）
   - 5 seed
   - 输出：DPLL BER 曲线 + vs NDA-ML/DA-ML/VV/BPS 对照

3. **TL-20 先建理论预期**
   - DPLL 是闭环跟踪，对 Wiener PN 应能跟踪（跟 VV 滑窗类似性能量级）
   - 预期：DPLL BER 在 VV 和 BPS 之间（闭环反馈 vs 前馈滑窗），跟 NDA-ML 持平或略差（DPLL 有锁定范围限制）
   - **不应远超 NDA-ML**（否则 NDA-ML 无价值）；**也不应全输**（否则 DPLL 太弱不像合法 baseline）

4. **判断 baseline 池是否立住**
   - DPLL BER 合理 → baseline 池立住（DA-ML 主 + DPLL 异族 + VV/BPS fellow）
   - 数据出来后决定写不写简报跟老师沟通路线 A/B

**工具调用**：
- python 路径：win32 用 `python`（系统 python 3.11，有 playwright + numpy），不是 `~/.venvs/torch/bin/python`
- bash 路径：`cd D:/code/study/research-protocol && ...`
- 主实验脚本在 `projects/simulation/simulator/`
- 信道在 `projects/simulation/common/_channel.py`

### 文件指针

- 主实验结果：`results/sc_nda_ml_main/_main_experiment_5seed.json`（已有 NDA/DA/VV/BPS/oracle 5 seed BER）
- 主实验脚本：`projects/simulation/simulator/` 下（grep 找 run_main 或 sc_nda_ml_main）
- fair_gain 框架：`projects/simulation/simulator/fair_comparison.py`（DPLL 不含 pilot overhead，跟 NDA 一样 γ_tot=γ_d）
- DPLL 实现：`projects/simulation/common/_recovery.py:8`（dpll_track_dd）/ `:59`（dpll_track，**不要用**）
- KF 实现：`projects/simulation/common/_kf.py`（4 变体，可选补跑）
