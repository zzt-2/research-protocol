# [S007] 对话 7 — V5 独立核查未记录 MVE 数据 + LPF2 不公平 bug + 范围优势公平性审计

> 2026-07-09 | sandbox 后半收尾（V5 核查）| 状态：D008 Kill B7-Q1（范围优势解决不存在的问题），专题 closed
> 续接：H006（对话 6 脚本+SPEC+smoke test 完成，剩正式 MVE）

## 目标

本轮目标：执行 H006 交代的"对话 7 正式 MVE 跑数 + Go/Kill 判断"。实际发现 H005 已过时（H006 才是最新），且正式 MVE 已在某未记录对话跑完（数据在 `_mve_results.json` + `_mve_osnr_sweep_results.json`，未提交无 S### 记录）。本轮做 V5 主线独立核查 + TL-20 偏离诊断 + 范围优势公平性审计（类比 B5 D003 先例）。

## 记录

### 1. 状态发现（H005 过时 + 未记录 MVE）

**H005 已被 H006 取代**：H005（对话 5 写）说"剩步骤 5/6"，但 H006（对话 6 写，Jul 8 00:20）显示步骤 5（三方对照脚本）+ 步骤 6a（SPEC）+ smoke test 已在 S006 完成并提交（commit `e9d0e48`）。

**未记录对话跑了正式 MVE**：文件系统证据——
- `_mve_results.json`（Jul 8 09:45，593.4s，n_sym=4096×3seed×24f_D×3OSNR）= 正式 MVE 非烟雾测试
- `_mve_osnr_sweep_results.json`（Jul 8 11:40，180.7s，11 OSNR×3f_D）
- `b7_gardner_ted_mve.py` 被改 +377 行（加 PSA two-stage + 4thpow + Kay + 强 alpha 校准）
- git status: M/_mve_results.json + ??/_mve_osnr_sweep_results.json，**未提交无 S### 记录**

主线未盲目重跑（浪费 ~10min 无新信息），直接对已有数据做 V5 核查。

### 2. V5 主线独立核查（从原始 JSON 重算）

| 指标 | 结果 | SPEC 预期 | 判定 |
|---|---|---|---|
| B7 est 精度 | 全准 err=0（3 OSNR 条件×24 点）| 全准 | ✓ |
| V3 祖师爷红线 | 1986 全爆 ~0.49，B7 低 1-2 数量级 | gap>0.1dB | ✓ 不触发 |
| 范围比（BER<0.05）| B7 21/24 vs PSA 10/24 = 2.10× | ≈1.9×±20% | ✓ |
| BER gain @ BER 2e-2 vs PSA | **+4.08 dB**（f_D=5GHz）| ≈0.6±0.2 | **❌ TL-20 偏离 +3.5dB** |

BER gain +4.08dB vs poster 0.6dB，偏离远超 ±0.2dB 容差 → 触发红线警报第 2+4 条（TL-20 偏离即查 + PSA 弱虚高排查）。

### 3. TL-20 偏离根因诊断（systematic-debugging Phase 1-3）

**Phase 1 物理一致性核查**：高 OSNR(35dB)极限下 B7 BER floor=0.003 vs 4thpow=0.005 vs Kay=0.006。若都估准 f_D（FOE 残留≈0），BER 应趋同（只剩 TR+判决）。B7 floor 低 1.5-2× → **下游链不同**。

**Phase 2 根因定位**：脚本 L848-854（B7）vs L860-879（4thpow/Kay/PSA）对照——
- B7 下游链：FOE 补偿 → **`_lpf2` 低通（L851）** → residual_mth_power → TR → BER
- 其他 baseline：FOE 补偿 → ~~无 LPF2~~ → residual_mth_power → TR → BER

**LPF2（13.75GHz butter 低通）只给 B7 加了，其他 baseline 全没有**。这是 apples-to-oranges 不公平对照。

**Phase 3 最小化验证**（`_lpf2_fairness_check.py`，f_D=5GHz 线性区内全加 LPF2，48.5s）：

| 对照 | 原 MVE（B7 独享 LPF2）| 公平配置（全加 LPF2）| Δgain |
|---|---|---|---|
| B7 vs 4thpow @17dB | +0.65 dB | **+0.03 dB** | -0.62 dB |
| B7 vs Kay @17dB | +1.98 dB | +1.49 dB | -0.49 dB |
| B7 vs PSA @17dB | +4.75 dB | +2.49 dB | -2.27 dB |

**结论**：B7 FOE 方法本身在"都能估准"的线性区内 vs 4thpow **gain≈0（+0.03dB）**。+4.08dB 是三重虚高：①LPF2 不公平独享 ~0.6-0.8dB ②PSA baseline 偏弱 ~2dB ③Kay est_err=1.01GHz 适配问题。

### 4. 范围优势公平性审计（类比 B5 D003 先例，用户提示）

用户提示"范围也是有问题"+ 指引翻日志 → 找到 **B5-Q1 D003 先例**（`2026-07-08-b5-leo-doppler-spectrum-foe/decisions.md`）：
- B5 范围优势 14.4×，给 baseline 配同等条件（星历预补+2-sps）后 → **范围归零（1.00×）**，特权假象
- B5 D003 教训：范围优势可能是特权功劳，必须公平对照实测

**B7 公平范围对照**（`_scope_fairness_check.py`，5 f_D 点×OSNR17dB±LPF2，199.3s）+ **数学本质分析**：

| 维度 | B5（特权假象）| B7（机制本质）|
|---|---|---|
| 范围优势来源 | 星历预补+采样率特权 | Gardner TED 周期相关（周期=baud）|
| baseline 限制 | 人为没给星历/采样率 | 4thpow **4 次方数学混叠** ±fs/2M=±6.25GHz |
| 公平对照后 | 配星历→范围归零 | **配任何条件都无法突破 ±6.25GHz** |

**数学证明**：4thpow r[k]^4 把频偏×4，FFT 可观测 ±fs_rx/2=±25GHz，除以 4 得等效范围 ±6.25GHz。f_D>6.25GHz 时 4f_D 超奈奎斯特→混叠→必估错。实测印证：f_D=5GHz（范围内）4thpow err=0；f_D=12/15/23GHz 全混叠估错（err=12.5/12.5/25）。

**B7 G(f_D)=K_max·|cos(πf_D/B)| 周期=2B=50GHz，单边扫频 0-25GHz 一个周期内无模糊**（D006 解析式闭合）。

**结论**：B7 范围优势 vs 4thpow 是机制本质差异（TED 周期相关 vs 4 次方混叠），**非特权假象，与 B5 根本不同**。不能用 B5 D003 逻辑 Kill。

### 5. 最终定性（V5 全核查 + B5 先例排除后）

| 维度 | 结论 | 证据 |
|---|---|---|
| BER gain | **≈0 vs 公平 baseline**（+0.03dB vs 4thpow 全加LPF2）| Phase3 实测 |
| 范围优势 | **真实，机制本质**（vs 4thpow ±6.25GHz 数学限制）| 数学证明+实测 |
| V3 祖师爷 | 不触发 | 实测 |
| LPF2 不公平 | 确认 bug（+4dB 三重虚高主因之一）| Phase3 实测 |

**与 B5/NDA-ML 的区别**：B5 范围优势是特权假象（给条件归零）→ Kill 路径 1；NDA-ML vs VV 持平是数学同族；**B7 范围优势是机制本质 + BER gain 公平条件下≈0**，是独立判断情况。

### 6. 产出文件

- `_lpf2_fairness_check.py` + `_lpf2_fairness_results.json`（LPF2 公平性验证）
- `_scope_fairness_check.py` + `_scope_fairness_results.json`（范围优势公平对照）

## 决策引用

- D007（新建）：LPF2 不公平 bug 登记 + BER gain 虚高结论 + 范围优势机制本质确认（非 B5 特权假象）
- D008（新建，续）：**Kill B7-Q1**——范围优势解决的是不存在的问题（LEO Doppler ±4.8GHz 被 4thpow ±6.25GHz 恰好覆盖），与 B5 D003 殊途同归
- D006（引用）：PSA coarse-only 弱限制（本轮扩展确认 PSA 即使加 LPF2 仍弱 ~2.5dB，是 baseline 本身弱）
- B5 D003（跨专题引用）：范围优势特权假象先例，B7 经公平对照排除"特权假象"但终因"需求不存在"殊途同归 Kill

## 范围确认

- 本轮是否在 scope boundary 内：**是**。V5 核查 + 偏离诊断 + 公平性审计是 H006 交代的"对话 7 正式 MVE 跑数 + Go/Kill 判断"的实质执行（数据已存在，核查替代重跑）。
- 未触发 Trigger 3（扩大范围）。LPF2 bug 修复 + 重跑留用户决策后。

## 后续

**🔴 续：用户追问"能大多少"触发真实需求核查 → D008 Kill B7-Q1**

S007 正文写完后，用户追问"能大多少"——主线核查真实 LEO 光学 Doppler 量级：
- LEO Doppler 最大 ±4.8GHz（1550nm v=7.5km/s），sat.1553 极端值 10GHz
- **4thpow ±6.25GHz 恰好覆盖 ±4.8GHz 真实 Doppler**
- B7 范围优势只在 6.25-25GHz 区间成立，但真实 LEO Doppler 够不着
- poster 真实动态测试仅 ±100MHz（45GHz 调谐是实验室设定）

**结论**：B7 范围优势解决的是不存在的问题，与 B5 D003 殊途同归。D008 Kill B7-Q1，专题 closed。复用资产保留（Gardner TR Python + PSA 谱不对称法 + 4thpow/Kay + G(f_D) 解析式）作 baseline 库扩展 + 教训素材。

**候选池现状**：NDA-ML dormant（卡 D-008/009）/ B3 active（阶段 0 +2~3dB 最高）/ B2·B5·B7 closed（Killed）。下一候选决策交用户（新对话）。
