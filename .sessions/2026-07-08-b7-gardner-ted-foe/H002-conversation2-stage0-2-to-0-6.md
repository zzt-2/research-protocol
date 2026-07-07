# Handoff: 对话 2 — 阶段 0.2-0.6 前置规约续（数学同族性 + 架构 + 公平对照 + 参数 + 文件）

> 来源: S002（阶段 0.1 公式完整性核查）| 交接目标: 新对话执行阶段 0.2-0.6 五项规约
> 文件名: H002-conversation2-stage0-2-to-0-6.md
> 日期: 2026-07-08

## 到哪了（状态）

阶段 0.1 公式完整性核查**通过**（D001），不切降级。

**关键破局**（S002）：用户指出本地有 Gardner TED 的完整 Matlab 实现（`毕设/旧本科代码/PSKTimingErrDetector.m` + `Tx2Rx.m` L176-214 定时环），替代了 Gardner 1986 扫描原文（正文不可检索）。

- **Gardner TED 1986 公式**：✅ 完整可实现（本地代码作公式源）
  - `PSKTimingErrDetector.m` L11-12 = 去直流 Gardner TED：`e = (y_mid − (y_late+y_early)/2)·(y_late−y_early)`
  - `Tx2Rx.m` L176-214 = 完整定时恢复环（NCO + Farrow 立方内插 + PI 环路滤波器）
- **B7 "TED 增益↔Doppler 映射"解析式**：⚠️ 缺失（poster 0 编号公式 + Fig.1a/b 全 omitted），但**可数值重建**（用本地 TED 代码扫 Doppler 跑 S-curve）
- **0.1 报告**：`projects/simulation/explore/b7-gardner-ted-foe/_formula_completeness_check.md`

**主线踩的坑**（S002 教训，下对话避免）：
1. 没讲清阶段 0.1 在干啥就甩 4 个降级选项 → 用户"啥玩意？咱们先说说这是要干啥"（profile 第 9 次防线第 10 次验证）
2. 只查 papers/ 下原文，漏查本地代码资产（FR-26 强化：用户本地可能有论文方法的可执行实现）

## 下一步干什么（对话 2 = 阶段 0.2-0.6，不写代码）

> **守 profile 第 9 次防线 + INVARIANT 6**：阶段 0 六项规约全做完才进 sandbox。本对话做 0.2-0.6（剩 5 项），不进 sandbox。
> **守 3 步上限**：0.2 派子 agent（数学同族性 + 数值重建），0.3-0.6 主线定。若超 3 步主动建议分对话。

### 步骤 1：报到 + 重读关键文件

报到（session-governance Trigger 1）+ 读：
- 本 H002 + topic-index（13 不变量，重点 11/12/13 B7 特殊风险）
- S002 阶段 0.1 报告（`projects/simulation/explore/b7-gardner-ted-foe/_formula_completeness_check.md`）
- 本地 Gardner TED 代码（`毕设/旧本科代码/PSKTimingErrDetector.m` + `Tx2Rx.m` L176-214 + `InterpCubic.m`）—— 0.2 数值重建的核心工具
- `_B7-gardner-ted-increment.md`（B7 锚方法详情）

### 步骤 2：阶段 0.2 数学同族性检查 + B7 映射数值重建

> INVARIANT 11 前置（Gardner TED 1986 祖师爷警报）+ sim-preflight v1.3.0 V2 三方对照 + V3 祖师爷警报。

**0.2a 数值重建 B7 Fig.1a 映射图**（派子 agent，≤15 分钟）：
- 用本地 `PSKTimingErrDetector.m` 的 Gardner TED 公式
- 对每个 Doppler 频偏 f_D（0~B 扫频，B = baud rate），生成受 f_D 相位旋转的 DP-QPSK 接收信号
- 跑 TED 得 S-curve，取 max = G(f_D)
- 画 G(f_D) vs f_D 曲线，验证 poster 描述的"周期性相关"是否存在
- **判定门控**：
  - 周期相关存在 → B7 机制成立，进 0.2b
  - 周期相关不存在 → **红线警报**，B7 poster 结论不可复现，向用户报告重新评估 B7

**0.2b 数学同族性分析**（派子 agent，≤15 分钟，跟 0.2a 可合并或分开）：
- B7 锚方法（OFC 2026 Gardner TED 复用 FOE）跟 Gardner TED 1986 原版的数学关系
- B7 跟 VV / BPS 的数学关系（是否同族升幂 mean-angle 变体）
- **关键问题**：B7 的"复用 FOE"创新点是什么？跟 1986 原版的差异在哪？如果差异只是参数调度/场景迁移而非算法创新 → 数学同族 → 创新性受质疑（NDA-ML D-008 陷阱重演风险）
- 输出 `explore/b7-gardner-ted-foe/_lineage_check.md`（数学同族性结论 + 页码证据）

**判定门控**：
- 非同族 + 周期相关存在 → 进 0.3
- 数学同族 → **红线警报**，向用户报告"B7 跟 Gardner TED 1986 数学同族，创新性受质疑，建议={找拉开差距的条件/重新定位贡献/放弃 B7}"
- 周期相关不存在 → B7 机制不可复现，重新评估

### 步骤 3：阶段 0.3-0.6（主线定，不一定要子 agent）

**0.3 架构定性（前馈 vs 环路 TF）**（INVARIANT 12）：
- B7 锚方法是反馈环（Gardner TED → loop filter → NCO）。**如果我们的实现也走反馈环，环路 TF 联合建模则撞 D006**
- 注意：用户本地代码（Tx2Rx.m L176-214）也是反馈环结构
- 决策：前馈化（合法不撞 D006）还是环路（撞 D006 需单独决策）
- **建议前馈化**（避免 D006 纠缠），但需论证前馈化后 B7 的"复用 FOE"创新是否还成立
- 输出 `explore/b7-gardner-ted-foe/_architecture_decision.md`

**0.4 公平对照框架设计**：
- B7 baseline 是 PSA FOE（时域方法），跟 NDA-ML 的 DA ML（pilot overhead）不同维度
- fair gain 怎么定义？工作点选 BER 2e-2（B7 锚论文工作点）还是 HD-FEC 3.8e-3（NDA-ML 一致）？
- **建议跟 NDA-ML 对齐用 HD-FEC**（跨候选可比），但 B7 锚论文用 BER 2e-2，需论证 HD-FEC 下 B7 增量是否仍成立
- 范围维度（1.9×估计范围）怎么量化进 fair gain？
- 输出 `explore/b7-gardner-ted-foe/_fair_comparison_framework.md`

**0.5 参数真相源前置**（TL-26 + FR-26 读原文数值）：
- B7 参数一开始进 params.py 单字段（sim-preflight v1.2.0 param-source.md）：
  - Doppler range 0-23GHz（B7 OFC 2026）
  - OSNR 10dB 工作点（B7 OFC 2026）
  - LEO Doppler rate（参考 Paillier / sat.1553 / Fernandes，**读原文数值不只引位置**——D-009 教训 5）
  - 符号率 / 线宽（跟 NDA-ML 统一用 LASER_LW 单字段，但 B7 场景 25-Gbaud DP-QPSK 可能不同，需论证）
- 每个参数全标 source_type + source + audit_flag
- 输出 params.py 的 B7Params 类草稿（不直接写 params.py，先在 explore 里草拟）

**0.6 文件组织规约**：
- 定死 `explore/b7-gardner-ted-foe/` 目录结构（已在 H001 §0.6 定，本步落盘确认 + 补 _lineage_check.md / _architecture_decision.md 等）
- 命名规则：私有文件 `_` 前缀（诊断/核查），正式文件无前缀（SPEC/mve）
- 下游引用同步清单（D-007 教训 2：参数改后必须同步清理下游引用）

## 纪律（和下一步直接相关的约束）

1. **profile 第 9 次"急于推进"防线 + INVARIANT 6**：阶段 0 六项规约全做完才进 sandbox。**禁跳阶段 0 直接写代码**。S002 已验证第 10 次（主线甩降级选项被用户叫停），下对话进入新阶段前先一句话讲清"在干啥+为什么"
2. **INVARIANT 11 Gardner TED 1986 数学同族性前置**（B7 特殊）：0.2 必须做深度检查 + B7 映射数值重建。数学同族 = NDA-ML D-008 陷阱重演（vs VV 持平被当合理接受），**红线警报**
3. **INVARIANT 12 架构定性前置**（B7 特殊）：0.3 定死前馈 vs 环路。**禁边跑边定架构**（NDA-ML D-002 B11 OFDM→单载波重定位教训）。环路撞 D006 需单独决策
4. **sim-preflight v1.3.0 C6-C8 + V1-V6**：公式逐项核对（V1，0.1 已完成 1986 部分）/ 三方对照（V2+C7）/ 祖师爷警报（V3+C8，0.2 核心）/ 参数变更触发算法重审（V4）/ 子 agent 归因独立核查（V5）/ FR-26 读原文数值（V6）
5. **TL-26 参数溯源 + 读原文数值**：每个参数标文献来源 + **读原文具体数值**（D-009 教训 5）
6. **TL-13 共用同一信道**：B7 从 `common/_channel.py` 导入，禁自建
7. **本地代码使用边界**：用户 Matlab 代码（`毕设/旧本科代码/`）是 Gardner TED 1986 公式源 + 定时环参考实现，**不是 B7 proposed FOE 的实现**（B7 创新点 CV mult1/2 扫频+双候选+TED2 判决代码里没有）。0.2 数值重建只用 TED 函数部分
8. **5 个口径警示**（切法地图继承）：B7 0.6dB @ BER 2e-2 + 1.9×范围 + OSNR 10dB（不是"赢 baseline 几 dB"硬标尺，会议级别下范围+鲁棒性维度够格）

## 接口变更（如有代码改动）

无（阶段 0 不写代码，只定规约 + 数值重建探针。数值重建脚本若写，放 `explore/b7-gardner-ted-foe/_b7_map_reconstruction.py`，私有 `_` 前缀，不进 experiments/）

## 失败数据附录（如涉及路线失败）

无新增路线失败。**继承 NDA-ML 失败数据**作参照（D-008 vs VV 持平是 bug / D-009 线宽 10kHz 疑似选错 / LMMSE 复现失败公式不全）。

**S002 新增潜在失败模式**（未触发但需警惕）：B7 映射数值重建若复现不出周期相关 → B7 机制不可复现（poster 结论存疑）。0.2 步骤 2a 的判定门控会触发。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| ~~B7 OFC 2026 poster 是否落盘~~ | FR-26 证据链 | **已解决（S002）** | 已落盘 +90 行核查完 |
| B7 映射解析式缺失 | INVARIANT 13 / V1 | 0.2 数值重建验证周期相关后，若进 sandbox/MVE 补解析推导 | 0.2 / sandbox |
| B7 算法框图 Fig.1b omitted | C6 公式来源核对 | 实现时按文字描述+用户代码定时环对接 | sandbox |
| Gardner 1986 扫描原文不可检索 | FR-26 证据链 | 本地 Matlab 代码已替代；若需引 1986 具体行号需重新 OCR | 视需要 |
| NDA-ML 线宽/方向未定 | step4a-mve-execution 专题 | dormant | 不阻塞 B7，B7 参数选择可参考 NDA-ML 教训 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| ~~阶段 0.1 公式完整性~~ | ~~所有核心公式完整可实现 + 标页码~~ | ~~V1 (v1.3.0)~~ | **PASS（S002/D001）** |
| 阶段 0.2 数学同族性 + 映射数值重建 | B7 跟 Gardner TED 1986 非同族 + 周期相关可数值复现 | V3+C8 (v1.3.0) | 未跑 |
| 阶段 0.3 架构定性 | 前馈化合法不撞 D006 | INVARIANT 12 | 未跑 |
| sandbox 三方对照 | 改进版/1986 原版/PSA FOE 三方归因可信 | V2+C7 (v1.3.0) | 未跑 |
| MVE fair gain | ≥0.5dB @ HD-FEC 或 B7 锚论文 BER 2e-2 工作点 | D005 + SPEC §5 | 未跑 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（13 条，重点 11/12/13 B7 特殊风险）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] S002 D001 = Gardner TED 1986 公式源用本地 Matlab 代码（核查 `decisions.md` D001 + `毕设/旧本科代码/PSKTimingErrDetector.m`）
  - [ ] B7 poster 0 编号公式 + 4 图 omitted（核查 `papers/doi/10.1364_ofc.2026.w2a.62/content.md`）
  - [ ] S002 报告在 `explore/b7-gardner-ted-foe/_formula_completeness_check.md`（核查文件存在 + §4 判定结论）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on（4 个依赖：上游 + 切法地图 + 精读沉淀 + step4a-mve-execution）
- [ ] 已确认当前范围未违反"明确不含"（不回头救 6 次 Kill / 不判 NDA-ML 决策 / 不改框架 / 不跳框架 / 不推翻 D006 / 不污染 common）

## 下一轮

**对话 3**（阶段 0.2-0.6 完成后）：
- 阶段 1 sandbox 三方对照（Gardner TED 改进版 / 1986 原版祖师爷 / PSA FOE baseline）
- 守 sim-preflight v1.3.0 V2 三方对照 + V3 祖师爷警报
- sandbox 发现 Gardner TED 跟 1986 原版持平 → 红线警报（查数学同族性，阶段 0.2 没查清的重验）
- B7 映射数值重建脚本（`_b7_map_reconstruction.py`）若 0.2 已写，sandbox 阶段复用

**对话 4**（sandbox 通过后）：
- 阶段 2 TL-20 理论预期表 + 阶段 3 MVE + consistency
