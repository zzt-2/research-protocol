# Handoff: 对话 6 — 三方对照脚本+MVE-SPEC+smoke test 完成，进对话 7 正式 MVE 跑数

> 来源: S006 | 交接目标: 新对话跑正式 MVE + Go/Kill 判断
> 文件名: H006-conversation6-script-spec-smoke.md
> 日期: 2026-07-08

## 到哪了（状态）

**sandbox 后半步骤 5+6a 完成**（S006），正式 MVE 跑数留对话 7。本轮范围（用户确认）：脚本 + SPEC + smoke test，不跑正式 MVE（profile 风险控制）。

- **步骤 6a B7-MVE-SPEC.md**（主线程）：10 节契约落地，仿 SC-NDA-ML SPEC。TL-20 预期表引用 `_fair_comparison_framework.md §5` 不重复。pass-fail 三维（BER 2e-2 锚校验 + HD-FEC 主判据 + 范围比 1.9×），Go/Kill 分离（FR-25），CRB 不当 Kill 门（S005 验证）。
- **步骤 5 b7_gardner_ted_mve.py 三方对照主脚本**（主线程）：三方实现（B7 proposed FOE 前馈扫频 + Gardner 1986 TR Python 重写 + PSA FOE 谱不对称法 import）+ 共用信号（TL-13，固定 seed 20260707）。
- **smoke test**（主线程，systematic-debugging）：n_sym=4096×1seed×5f_D×OSNR17dB，14.4s。**修 3 bug**：① BER 符号对齐（make_tx 直接返回 QPSK 符号作参考）② 单边扫频 0-23GHz（poster content.md:49，避免跨 baud 周期模糊）③ PSA 残余 FOE 清理（M=4 MP FOC，对齐 content.md:47 DSP 链）。

**Smoke test 结果符合 TL-20 预期**：
- B7 est 全准（err=0），BER~1e-2 稳定 ✓
- Gardner 1986 全爆（0.47-0.49，没 FOE）→ **V3 祖师爷警报不触发** ✓
- PSA >12GHz 退化（12GHz BER 0.069，23GHz BER 0.17）→ D006 coarse-only 弱体现 ✓

**关键产出**（对话 7 会用到）：
- `explore/b7-gardner-ted-foe/b7_gardner_ted_mve.py`（三方对照主脚本，smoke test 已验证）
- `explore/b7-gardner-ted-foe/B7-MVE-SPEC.md`（MVE 契约，含正式 MVE 扫描配置）
- `explore/b7-gardner-ted-foe/_mve_results.json`（smoke test 数据，对话 7 正式跑会覆盖）
- `explore/b7-gardner-ted-foe/_fair_comparison_framework.md §5`（TL-20 预期表）

## 下一步干什么（对话 7 = 正式 MVE 跑数 + Go/Kill 判断）

> **守 sim-preflight v1.3.0**：C7 三方对照 / V2 三方归因 / V3 祖师爷红线（B7 vs Gardner 1986 gap，smoke test 已不触发）/ V5 子 agent 归因主线独立重算 / TL-20 偏离即查。

### 对话 7 任务

1. **跑正式 MVE**：`python explore/b7-gardner-ted-foe/b7_gardner_ted_mve.py`（默认配置：4096 sym × 3 seed × 24 f_D 点 0-23GHz × 3 OSNR 条件 17/10dB/无噪声，预估 ~600s，在 900s 子 agent 上限内）。**建议派子 agent 跑**（AGENTS.md 子 agent 强制委托第 4 项 MVE 执行）。
2. **主线 V5 独立重算**：子 agent 回传后，主线从 `_mve_results.json` 原始 BER 独立重算 BER gain / 范围比 / V3 gap，不信子 agent 归因。
3. **TL-20 偏离检查**：对照 `_fair_comparison_framework.md §5` 预期表，标注 DEVIATION 点并查代码（重点查 S006 发现 A/B/C 三处）。
4. **MVE 结果交用户做 Go/Conditional Go/Kill 判断**（profile：不宜长上下文塞完，单独判断节点）。

### 红线警报（正式 MVE 发现立刻停）

- **V3 祖师爷警报**（C8）：B7 vs Gardner 1986 BER gap <0.1dB（持平）。smoke test 已确认 1986 全爆 B7 低 1-2 数量级，持平可能性极低。若真持平查 B7 实现是否被错实现成反馈跟踪。
- **TL-20 偏离**：BER gain @ BER 2e-2 偏离 0.6dB >0.2dB → 查 LPF2 实现 + PSA FOE baseline。smoke test 已验证 PSA 是谱不对称法（非 pilot-aided），重点查 LPF2。
- **S006 发现 A 触发**：若 B7 est 系统性偏到 baud rate 整数倍外 → 查候选消歧逻辑（单峰 vs 双峰判断）。
- **S006 发现 B 触发**：若 PSA BER 异常高（全 f_D 都 >0.1）→ 查 residual_foe_mth_power 是否正常工作。
- **S006 发现 C 触发**：若 BER 系统性 0.25 → 查 qpsk_hard_decision_ber 的 lag 对齐扫描。

## 纪律（和下一步直接相关的约束）

1. **sim-preflight v1.3.0 C7+V2 三方对照**：B7 proposed / Gardner 1986 TR / PSA FOE 三方归因可信。守 V5 子 agent 归因主线独立重算（D-009 教训 6：只信原始数字不信归因）。
2. **V3 祖师爷红线**（C8）：B7 vs Gardner 1986 TR BER gap <0.1dB → 立即停。smoke test 已双重确认任务正交（1986 全爆 B7 低 1-2 数量级），持平可能性极低。
3. **TL-13 共用信号**：三方都用固定 seed 20260707 的 QPSK 25GBaud + 相同确定性 f_D 注入（b7_gardner_ted_mve.py 已实现）。
4. **B7Params 跟 SystemParams 物理隔离**：B7 脚本 import B7Params（25GBaud/1.8kHz），NDA-ML 脚本 import SystemParams（2.5GBaud/10kHz），不混用。
5. **D006 PSA 弱限制 + S006 发现 B 扩展**：PSA 不仅 coarse-only 线性区窄（~1GHz），估准后还有残余偏置需 MP FOC 清理。fair gain BER gain 标为上界。论文叙事分两维报告（BER gain 上界 + 范围 1.9×/OSNR 10dB 结构性优势）。
6. **环境**：本机无 `~/.venvs/torch/`，用 `python`（scoop python311，numpy 2.4.3/scipy 1.17.1/mpl 3.10.8）。
7. **Go/Kill 判断交用户**：子 agent 只给 Go/Conditional/Kill 建议，最终判断用户做（profile 画像）。

## 接口变更（如有代码改动）

本轮 sandbox 后半代码改动：
- `projects/simulation/explore/b7-gardner-ted-foe/b7_gardner_ted_mve.py`：**新建**（三方对照主脚本，~600 行）
- `projects/simulation/explore/b7-gardner-ted-foe/B7-MVE-SPEC.md`：**新建**（MVE 契约，10 节）
- `projects/simulation/explore/b7-gardner-ted-foe/_mve_results.json` + `_mve_curves.png`：**新建**（smoke test 产出，对话 7 正式跑会覆盖）

预期对话 7 代码改动：
- `_mve_results.json` + `_mve_curves.png`：正式 MVE 数据覆盖 smoke test 数据
- 可能微调 `b7_gardner_ted_mve.py`（若 TL-20 偏离触发查代码修 bug）

## 失败数据附录（如涉及路线失败）

无新增路线失败。smoke test 修 3 bug 是实现调试非路线失败。

**S006 三个实现发现**（非失败，是 sandbox 阶段对 B7 算法 + PSA baseline 的深入理解，详见 topic-index「S006 sandbox 实现发现」表）：
- A. B7 候选消歧边界（TED2 std 小 ≠ BER 低的内在限制）
- B. PSA 需 MP FOC 残余清理（D006 弱限制扩展）
- C. BER 符号对齐（TR loop lag 依赖初始化）

## 已知债务（原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| ~~B7Params 旧字段问题~~ | TL-26 + FR-26 V6 | 已解决（S005）| - |
| ~~B7 TED_gain(f_D) 解析式缺失~~ | INVARIANT 13 / V1 | 已解决（S005/D006）| - |
| ~~common psa_foe_recovery 概念错~~ | 公式忠实原文 | 已解决（S005）| - |
| ~~Leven 2007 论文落盘 + DOI~~ | FR-26 | 已解决（S005/D006）| - |
| B7 算法框图 Fig.1b omitted | C6 | 按文字描述 + 用户代码定时环对接 | 对话 7 MVE 实现（已对接）|
| **PSA FOE coarse-only 线性区 ~1GHz** | fair gain 真实性 | 已登记（D006）+ S006 扩展（需 MP FOC 清理）| 对话 7 三方对照记录 + 可选补 fine CFE stage |
| **B7 TED2 std 消歧内在限制** | content.md:37 算法忠实 | **新登记（S006 发现 A）**：residual≈baud rate 整数倍时 TED2 std 失效 | 对话 7 正式 MVE 若触发再升 D007 |
| NDA-ML 线宽/方向未定 | step4a-mve-execution | dormant | 不阻塞 B7 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| ~~sandbox 1-4（B7Params/PSA/TED_gain/CRB）~~ | ~~见 S005~~ | ~~D005+D006~~ | **PASS（S005）** |
| ~~sandbox 5 三方对照脚本 smoke test~~ | ~~三方能跑通 + 输出结构对~~ | ~~V2+C7~~ | **PASS（S006）**：14.4s 跑通，B7 est 全准，V3 不触发，PSA 退化符合 D006 |
| MVE BER gain @ BER 2e-2 | ≈0.6dB（锚论文一致性）| content.md L21/65/69 | 未跑（对话 7）|
| MVE BER gain @ HD-FEC | ≥0.3dB（跨候选主判据）| D004 + SPEC §5 | 未跑（对话 7）|
| MVE Doppler 范围比 | ≈1.9×（23/12）| content.md L21/49/69 | 未跑（对话 7）|
| MVE B7 vs Gardner 1986 gap | >0.1dB（V3 祖师爷警报）| D002 任务正交 + D006 解析闭合 | smoke test 已 PASS（gap 巨大，对话 7 正式确认）|

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（13 条，重点 11/12/13 B7 特殊风险）
- [ ] 已读取 topic-index「S006 sandbox 实现发现」表（发现 A/B/C，对话 7 正式 MVE 警示）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] S006 b7_gardner_ted_mve.py 三方能跑通（核查脚本存在 + 跑 `python explore/b7-gardner-ted-foe/b7_gardner_ted_mve.py --smoke` 复现）
  - [ ] S006 B7-MVE-SPEC.md 10 节落地（核查文件存在 + 含 TL-20 预期引用 + pass-fail 三维）
  - [ ] S006 smoke test 结果符合预期（核查 `_mve_results.json` 含 B7 BER~1e-2 / 1986 爆 / PSA >12GHz 退化）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on（4 个依赖）
- [ ] 已确认当前范围未违反"明确不含"

## 下一轮

**对话 7**（正式 MVE 跑数 + Go/Kill 判断）：
- 跑 `python explore/b7-gardner-ted-foe/b7_gardner_ted_mve.py`（正式配置，派子 agent）
- 主线 V5 独立重算 + TL-20 偏离检查（守 S006 发现 A/B/C）
- MVE 结果交用户做 Go/Conditional Go/Kill 判断
- 守 sim-preflight v1.3.0 C7+V2+V3（V3 smoke test 已不触发，正式确认）
- 注意 D006 PSA coarse-only 弱 + S006 发现 B：fair gain BER gain 标为上界
- consistency 检查（MVE vs Formal，但 Formal 还没建，可能只做 V1-V6 算法正确性验证）
