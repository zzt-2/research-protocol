# [S006] 对话 6 — 三方对照主脚本 + MVE-SPEC + smoke test（正式 MVE 留对话 7）

> 2026-07-08 | sandbox 后半（步骤 5+6a）| 状态：脚本+SPEC 落地，smoke test PASS，正式 MVE 跑数留对话 7
> 续接：H005（sandbox 前 4 步完成，剩步骤 5+6）

## 目标

本轮范围（用户确认）：步骤 5（三方对照主脚本 `b7_gardner_ted_mve.py`）+ 步骤 6a（`B7-MVE-SPEC.md` 契约）+ smoke test 验证管道。**正式 MVE 跑数 + Go/Kill 判断留对话 7**（profile 风险控制：不宜长上下文塞完 MVE 结果）。

## 记录

### 1. Handoff 验证（Trigger 5）

H005 四条关键事实声称全 PASS（独立核查原始 JSON + 代码）：
- B7Params 15 字段 0 DEAD/CRITICAL：`params.py` L606-780+ 核查 ✓
- PSA FOE = 谱不对称法：`_psa_foe_asymmetry.py` docstring 含 Δf̂=α·ln(P+/P−)/2 ✓
- G(f_D)=K_max·|cos(πf_D/B)|，K_max=0.13214186 vs 0.2a 锚点 0.132142（误差 0.0001%）✓
- CRB std=59.42kHz << 扫频间隔 1GHz（小 16830 倍）✓

### 2. 步骤 6a：B7-MVE-SPEC.md 落地

仿 SC-NDA-ML-MVE-SPEC.md 结构（更近的模板），10 节：核心假设 / TL-20 预期（引用 `_fair_comparison_framework.md §5` 不重复）/ FR-04 最小实例 / 三方对照架构（C7+V2）/ pass-fail 标准（D005 务实 + FR-25 Go/Kill 分离）/ 扫描设计（含 smoke test 配置）/ BER 评估简化 / 执行约束 / 子 agent 返回格式 / 与 NDA-ML 边界。

**pass-fail 标准三维**：BER 2e-2 锚校验 + HD-FEC 主判据 + 范围比 1.9×。Go = 三维全成立；Conditional Go = BER 2e-2 成立但 HD-FEC 偏弱（叙事转范围+鲁棒性）；Kill = V3 红线警报或三维全崩。

### 3. 步骤 5：三方对照主脚本 b7_gardner_ted_mve.py 落地

三方实现：
- **B7 proposed FOE**：前馈扫频 0-23GHz step 1GHz（poster `content.md:49` 单边），CV multiplier 1 扫频找 G(f_D)=max_τ|S-curve| 峰，单峰清晰直接 argmax，双峰可比时 TED2 std 消歧（`content.md:37`）。LPF2 噪声抑制（`content.md:65` 0.6dB 来源）。
- **Gardner 1986 TR**：Python 重写用户 `Tx2Rx.m L176-214` 反馈定时环（NCO + PI 环路滤波器 C1=1/2^5, C2=C1²/2 + Cubic 内插），`PSKTimingErrDetector.m L11-12` 零直流变种 Gardner TED。任务是 STR 非 FOE，作 V3 祖师爷警报对照。
- **PSA FOE**：import 同目录 `_psa_foe_asymmetry.py`（S005 谱不对称法重写，C6 audit）。

三方共用信号（TL-13）：固定 seed 20260707 的 QPSK 25GBaud + 相同确定性 f_D 注入。

### 4. Smoke test + 系统调试（修 3 个 bug）

**systematic-debugging Phase 1-4**：smoke test 跑通后发现 BER 异常，按 TL-20「偏离即查」诊断，修 3 个 bug：

| Bug | 根因 | 修复 |
|-----|------|------|
| BER 全爆（f_D=0 也爆）| `_tx_qpsk_symbols` 用 MF 下采样重建参考符号，采样偏移错（offset=1 而非 0）| 改 `make_tx` 直接返回原始 QPSK 符号作 BER 参考，不从 rx 重建 |
| B7 FOE est 全错（5GHz→-20GHz）| 双边扫频 -24~+24 跨 2 个 baud 周期，G(f_D)=K_max·\|cos(πf_D/B)\| 周期模糊 | 改单边 0-23GHz（poster `content.md:49` 一致）|
| B7 TED2 std 消歧系统选错候选 | 单峰清晰时硬凑第二候选，TED2 std 选了 residual≈B 的伪峰（TR 收敛但 BER 爆）| 单峰（第二峰 <70% 主峰）直接 argmax，不触发消歧 |
| PSA BER 全爆（est 准也爆）| PSA 谱不对称法对 f_D=0 有非零估计偏置（log-asymmetry 噪声底），补偿后残余 ~0.3GHz 频偏让 TR loop 失效 | 三方补偿后都加 `residual_foe_mth_power`（M=4，对齐 poster `content.md:47` MP FOC）做残余清理，公平对照 |

**Smoke test 最终结果**（n_sym=4096, 1 seed, 5 f_D 点, OSNR 17dB）：

| f_D (GHz) | B7 BER | 1986 BER | PSA BER | B7 est err | PSA est err |
|---|---|---|---|---|---|
| 0 | 9.2e-3 | 2.4e-2 | 2.5e-2 | 0 | 0.44 |
| 5 | 1.4e-2 | 0.47 | 3.3e-2 | 0 | 0.14 |
| 12 | 7.5e-3 | 0.49 | 6.9e-2 | 0 | 5.27 |
| 15 | 1.6e-2 | 0.48 | 2.9e-2 | 0 | 2.56 |
| 23 | 1.0e-2 | 0.49 | 0.17 | 0 | 21.47 |

**符合 TL-20 预期的关键观察**：
- **B7 vs Gardner 1986**：1986 全爆（0.47-0.49，没 FOE），B7 低 1-2 数量级 → **V3 祖师爷警报不触发**（任务正交验证成立）✓
- **B7 vs PSA 范围优势**：B7 全 f_D BER ~1e-2 稳定；PSA 在 12GHz（半 baud 边界）BER 升到 6.9e-2，23GHz BER 0.17（D006 coarse-only 弱限制体现）✓
- **PSA est 误差**：12/15/23GHz 全偏（D006 coarse-only 弱），但加 MP FOC 残余清理后 BER 仍可解调（说明 PSA 在边界退化但非完全失效）

**smoke test 结论**：管道跑通，三方归因可信，脚本着正式 MVE 跑数。14.4s/5 点（正式 MVE 24 点 × 3 OSNR × 3 seed 预估 ~600s，在 900s 子 agent 上限内）。

### 5. 本轮重要发现（带进对话 7）

**发现 A：B7 候选消歧的边界条件**（`content.md:37` "TED2 std 判决"内在限制）
- TED2 std 小 ≠ BER 低。当 residual f_D ≈ 整数倍 baud rate，G(f_D) 峰化让 TR loop 收敛（te_std 小），但 BER 爆（谱周期折叠）。
- 实现：单峰清晰（第二峰 <70% 主峰）直接 argmax，不触发 TED2 std 消歧。poster 的"两个候选"只在 cos 双峰可比时出现。
- **对话 7 警惕**：若正式 MVE 出现 B7 est 系统性偏到 baud rate 整数倍外，查这个消歧逻辑。

**发现 B：PSA 需要 MP FOC 残余清理**（poster DSP 链 `content.md:47` FOE→TR→MIMO EQ→MP FOC→CPR）
- MVE 简化省略 MP FOC 对 PSA 不公平（PSA 谱不对称法对 f_D=0 有偏置，补偿后残余频偏让 TR 失效）。
- 修复：三方补偿后都加 M=4 次方残余 FOE 清理（公平对照，对齐 poster MP FOC）。
- **D006 PSA coarse-only 弱限制扩展**：不仅线性区窄（~1GHz），估准后还有残余偏置需 MP FOC 清理。fair gain BER gain 标为上界。

**发现 C：BER 评估的符号对齐**（TR loop 输出 vs 参考符号的索引关系）
- TR loop 用 mk 计数器，输出符号起始点和参考符号差整数偏移（依赖 loop 初始化）。
- `qpsk_hard_decision_ber` 自动扫 lag -4..+4 找最佳对齐（不硬编码）。
- **对话 7 警惕**：若 BER 出现系统性 0.25（QPSK 随机 +1/4 偏移），查 lag 对齐。

## 决策引用

- 无新建 D###。本轮是执行（脚本+SPEC+smoke test），无架构决策变更。sandbox 发现（A/B/C）登记为已知限制带进对话 7，若正式 MVE 触发再升 D007。

## 范围确认

- 本轮是否在 scope boundary 内：**是**。步骤 5+6a + smoke test，不跑正式 MVE（用户确认范围）。
- 未触发 Trigger 3（扩大范围）。

## 后续

**对话 7（正式 MVE 跑数 + Go/Kill 判断）**：
1. 跑 `python explore/b7-gardner-ted-foe/b7_gardner_ted_mve.py`（正式配置：4096 sym × 3 seed × 24 f_D 点 × 3 OSNR 条件，预估 ~600s）
2. 守 V2+V3（祖师爷警报）+ TL-20 偏离即查（重点查发现 A/B/C 三处）
3. **MVE 结果交用户做 Go/Conditional Go/Kill 判断**（profile：不宜长上下文塞完）
4. consistency 检查（MVE vs Formal bit-exact，但 Formal 还没建，对话 7 可能只做 V1-V6 算法正确性验证）

**待观察**：
- 正式 MVE 下 B7 BER gain @ BER 2e-2 是否 ≈0.6dB（poster 锚校验）
- 正式 MVE 下 HD-FEC 3.8e-3 是否可达（25GBaud QPSK OSNR 17/10dB 的工作点）
- PSA 在 12-23GHz 的 BER 退化曲线是否符合 D006 coarse-only 弱预期
