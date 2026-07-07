# Handoff: 对话 3 — 阶段 0.4-0.6 前置规约收尾（公平对照 + 参数真相源 + 文件组织）

> 来源: S003（阶段 0.2+0.3 数学同族性 + 架构定性）| 交接目标: 新对话执行阶段 0.4-0.6 收尾 + 决定是否进 sandbox
> 文件名: H003-conversation3-stage0-4-to-0-6.md
> 日期: 2026-07-08

## 到哪了（状态）

阶段 0.1-0.3 全部通过（D001/D002/D003），阶段 0 还剩 0.4-0.6 三项规约。

**阶段 0.1**（D001）：Gardner TED 1986 公式源 = 用户本地 Matlab 代码（`毕设/旧本科代码/PSKTimingErrDetector.m`），B7 映射靠数值重建，不切降级。
**阶段 0.2**（D002）：B7 数学同族性 = 弱同族 (B)，机制数值验证成立（G(f_D) 以 baud rate 25GHz 周期，铁证 G(0)=0.132142），非 NDA-ML 陷阱。
**阶段 0.3**（D003）：B7-Q1 架构 = FOE 前馈扫频 + Gardner TR 保留反馈环（跟踪 τ 不是 φ_T）+ 载波同步禁建模湍流相位。不撞 D006。

**关键产出**（下对话会用到）：
- `explore/b7-gardner-ted-foe/_b7_map_reconstruction.py` + `_b7_map_results.json`（0.2a 数值重建，sandbox 阶段复用）
- `explore/b7-gardner-ted-foe/_lineage_check.md`（0.2b 同族性分析，弱同族 (B) 证据）
- `explore/b7-gardner-ted-foe/_stage0_2_summary.md`（0.2 综合报告）
- `explore/b7-gardner-ted-foe/_architecture_decision.md`（0.3 架构定性）
- `explore/b7-gardner-ted-foe/_formula_completeness_check.md`（0.1 公式完整性）

## 下一步干什么（对话 3 = 阶段 0.4-0.6，不写代码）

> **守 profile 第 9 次防线 + INVARIANT 6**：阶段 0 六项规约全做完才进 sandbox。本对话做 0.4-0.6（剩 3 项），不进 sandbox。
> **守 3 步上限**：0.4-0.6 各算一步，正好满 3 步。

### 步骤 1：报到 + 重读关键文件

报到（session-governance Trigger 1）+ 读：
- 本 H003 + topic-index（13 不变量，重点 11/12/13 B7 特殊风险）
- S003（阶段 0.2+0.3 记录）
- 0.2/0.3 报告（`_stage0_2_summary.md` + `_architecture_decision.md`）
- B7 锚论文（`papers/doi/10.1364_ofc.2026.w2a.62/content.md`）+ 精读笔记（`papers/_read_notes/_B7-gardner-ted-increment.md`）
- N1-MVE-SPEC 模板（`projects/simulation/explore/n1-pcs-gain/N1-MVE-SPEC.md` §2 理论预期表格式）
- NDA-ML 公平对照框架（`explore/single-carrier-nda-ml/SC-NDA-ML-MVE-SPEC.md`，pilot overhead 公平对照参照）
- params.py 现有结构（`projects/simulation/params.py`）

### 步骤 2：阶段 0.4 公平对照框架设计

> INVARIANT：B7 baseline 是 PSA FOE（时域谱不对称法），跟 NDA-ML 的 DA ML（pilot overhead）不同维度。fair gain 不能照搬 NDA-ML。

**要回答的问题**：
1. **fair gain 定义**：B7 vs PSA FOE 都是前馈 FOE，无 pilot overhead 差异（不像 NDA-ML vs DA ML）。fair gain 直接用 BER gain @ 工作点？还是加 Doppler 范围维度（1.9×）？
2. **工作点选择**：
   - B7 锚论文用 BER 2e-2（receiver sensitivity 改善 0.6dB @ BER 2e-2）
   - NDA-ML 用 HD-FEC 3.8e-3（跨候选可比）
   - **建议跟 NDA-ML 对齐用 HD-FEC**，但 B7 锚论文用 BER 2e-2，需论证 HD-FEC 下 B7 增量是否仍成立（可能 B7 的 0.6dB 在 HD-FEC 处不同）
3. **范围维度量化**：B7 的 1.9× 估计范围（0-23GHz vs PSA FOE 0-12GHz）是结构性优势，怎么进 fair gain？是单独维度报告还是合成单一指标？
4. **Doppler 扫频公平性**：B7 和 PSA FOE 都在相同 Doppler 扫频 0-23GHz 测，公平。但 PSA FOE >12GHz 失败的"失败"怎么定义（BER 爆？FOE 输出漂零？）

**输出** `explore/b7-gardner-ted-foe/_fair_comparison_framework.md`

**重要债务（S003 发现）**：common 的 `psa_foe_recovery`（`_recovery.py` L435）函数名是 PSA FOE 但实现是 **pilot-aided FOE（pilot 差分相位法）**，**不是 B7 的真 baseline PSA = Power-Spectrum-Asymmetry（谱不对称法 Vieira 2023）**。sandbox 阶段做 PSA FOE baseline 需重写（用谱不对称法）。0.4 框架设计时要声明这个债务。

### 步骤 3：阶段 0.5 参数真相源前置 + 0.6 文件组织

**0.5 参数真相源**（TL-26 + FR-26 读原文数值，sim-preflight v1.2.0 param-source.md）：
B7 参数一开始进 params.py 单字段（草拟在 explore，不直接写 params.py）：
- **Doppler range 0-23GHz**（B7 OFC 2026 content.md 行 49，扫频范围）
- **OSNR 10dB 工作点**（B7 OFC 2026 content.md 行 21/69，低 SNR 极限）
- **LEO Doppler rate ±100MHz @ 1GHz/s**（B7 OFC 2026 content.md 行 47，三角波模拟参数）—— **这个 B7 自己给了原文数值**，不像 NDA-ML D-007 要查 Valjus
- **符号率 25-Gbaud**（B7 OFC 2026，DP-QPSK）—— 跟 NDA-ML 的 2.5GBaud 不同，需决策用哪个（B7 场景保 25GBaud？还是跟 NDA-ML 统一 2.5GBaud？）
- **线宽 1.8kHz**（B7 NL-FT-DFB 激光器，content.md 行 47）—— 跟 NDA-ML 的 LASER_LW=10kHz 不同，需决策
- **roll-off 0.1 / 接收 BW 36.75GHz / 2.94sps**（B7 content.md 行 47）

每个参数全标 source_type + source + audit_flag。输出 params.py 的 B7Params 类草稿（在 explore 里草拟）。

**关键决策点**（0.5）：B7 场景参数（25GBaud/1.8kHz）跟 NDA-ML 场景参数（2.5GBaud/10kHz）不同。要不要统一？统一到哪个？这影响跨候选可比性（D-007 教训：对比本就该相同）。但 B7 锚论文工作点在 25GBaud，统一到 2.5GBaud 后 0.6dB 增量是否还成立需论证。

**0.6 文件组织**：
- 确认 `explore/b7-gardner-ted-foe/` 目录结构（已有：_formula_completeness_check / _b7_map_* / _lineage_check / _stage0_2_summary / _architecture_decision）
- 补 `_fair_comparison_framework.md`（0.4 产出）+ B7Params 草稿（0.5 产出）
- 后续 sandbox/MVE 文件命名：`_crb_lower_bound.py`（FR-21 oracle，阶段 3）+ `b7_gardner_ted_mve.py`（MVE 脚本）+ `B7-MVE-SPEC.md`（契约）
- 下游引用同步清单（D-007 教训 2：参数改后必须同步清理下游引用）

## 纪律（和下一步直接相关的约束）

1. **profile 第 9 次"急于推进"防线 + INVARIANT 6**：阶段 0 六项规约全做完才进 sandbox。0.4-0.6 是收尾，做完才进 sandbox
2. **sim-preflight v1.3.0 V6 FR-26 读原文数值**：参数溯源不只引位置，要读 B7 content.md 具体数值（B7 自己给了 Doppler rate ±100MHz@1GHz/s 等，比 NDA-ML 查 Valjus 容易）
3. **TL-26 参数溯源 + D-007 教训**：符号率/线宽场景差异（B7 25GBaud/1.8kHz vs NDA-ML 2.5GBaud/10kHz）需明确决策，不模糊带过
4. **common `_recovery.py:psa_foe_recovery` 概念错**：是 pilot-aided 非谱不对称法。sandbox PSA FOE baseline 要重写，0.4 框架设计时声明债务
5. **环境**：本机无 `~/.venvs/torch/`（AGENTS.md 路径过时），用 `python`（scoop python311，numpy 2.4.3/scipy 1.17.1/mpl 3.10.8）
6. **5 个口径警示**：B7 0.6dB @ BER 2e-2 + 1.9×范围 + OSNR 10dB（会议级别，范围+鲁棒性维度够格）

## 接口变更（如有代码改动）

无（阶段 0 不写代码，只定规约 + 参数草稿。参数草稿在 explore 里，不进 params.py）

## 失败数据附录（如涉及路线失败）

无新增路线失败。0.2+0.3 全通过。

**潜在失败模式**（未触发但 0.4-0.6 要警惕）：
- 符号率/线宽场景统一决策错误（统一到 2.5GBaud 后 B7 0.6dB 增量消失，重蹈 NDA-ML D-007 覆辙）→ 0.5 必须论证统一后增量仍成立
- PSA FOE baseline 实现错（用了 pilot-aided 非谱不对称法，跟 B7 真 baseline 不是一回事）→ 0.4 声明债务，sandbox 重写

## 已知债务（原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| ~~B7 poster 落盘~~ | FR-26 | 已解决（S002）| - |
| ~~Gardner 1986 数学同族性~~ | INVARIANT 11 | 已解决（S003/D002）| - |
| ~~架构定性~~ | INVARIANT 12 | 已解决（S003/D003）| - |
| B7 TED_gain(f_D) 解析式缺失 | INVARIANT 13 / V1 | sandbox 前补解析推导 + Leven 对比 | sandbox |
| B7 算法框图 Fig.1b omitted | C6 | 按文字描述 + 用户代码定时环对接 | sandbox |
| **common `psa_foe_recovery` 概念错** | 公式忠实原文 | pilot-aided 非谱不对称法，sandbox 重写 | sandbox（0.4 声明）|
| **符号率/线宽场景差异** | TL-26 参数溯源 | B7 25GBaud/1.8kHz vs NDA-ML 2.5GBaud/10kHz，0.5 决策 | 0.5 |
| NDA-ML 线宽/方向未定 | step4a-mve-execution | dormant | 不阻塞 B7 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| ~~0.1 公式完整性~~ | ~~核心公式完整可实现~~ | ~~V1~~ | **PASS（S002/D001）** |
| ~~0.2 数学同族性 + 映射数值重建~~ | ~~非同族 + 周期相关可复现~~ | ~~V3+C8~~ | **PASS（S003/D002）** |
| ~~0.3 架构定性~~ | ~~前馈化不撞 D006~~ | ~~INVARIANT 12~~ | **PASS（S003/D003）** |
| 0.4 公平对照框架 | fair gain 定义明确 + 工作点论证 | D005 + SPEC | 未跑 |
| 0.5 参数真相源 | 每个参数标 source_type+source+audit_flag | TL-26 + V6 | 未跑 |
| sandbox 三方对照 | 改进版/1986 原版/PSA FOE 三方归因可信 | V2+C7 | 未跑 |
| MVE fair gain | ≥0.5dB @ HD-FEC 或 BER 2e-2 | D005 + SPEC §5 | 未跑 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（13 条，重点 11/12/13 B7 特殊风险）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] S003 D002 = B7 弱同族 (B)（核查 `decisions.md` D002 + `_lineage_check.md`）
  - [ ] S003 D003 = FOE 前馈化不撞 D006（核查 `decisions.md` D003 + `_architecture_decision.md`）
  - [ ] 0.2a 数值重建 G(0)=0.132142（核查 `_b7_map_results.json` 的 curves.no_noise.coarse[0].G_abs）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on（4 个依赖）
- [ ] 已确认当前范围未违反"明确不含"

## 下一轮

**对话 4**（阶段 0.4-0.6 完成后，阶段 0 全部收尾）：
- 决定是否进 sandbox（阶段 1 三方对照：B7 proposed FOE / Gardner 1986 TR / PSA FOE baseline）
- sandbox 前补 B7 TED_gain(f_D) 解析推导 + Leven M-th-power 对比（排除强同族 C 残留风险）
- PSA FOE baseline 重写（谱不对称法，非 pilot-aided）
- 守 sim-preflight v1.3.0 V2 三方对照 + V3 祖师爷警报
- sandbox 发现 B7 vs Gardner 1986 持平 → 红线警报（但 0.2 已确认任务正交，持平可能性低）

**对话 5**（sandbox 通过后）：
- 阶段 2 TL-20 理论预期表 + 阶段 3 MVE + consistency
