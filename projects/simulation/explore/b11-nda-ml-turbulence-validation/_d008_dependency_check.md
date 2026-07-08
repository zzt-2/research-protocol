# 阶段 0.1 D-008 耦合依赖门控核查

> B11-Q2 专题阶段 0.1 产出物 | 日期 2026-07-08 | 来源 S002
> 核查对象：NDA-ML D-008 双 bug 修复状态 + B11-Q2 sandbox 前置条件

## 结论（先讲）

**D-008 前置条件当前状态：不满足。且更严重——D-009 sandbox 已证明该前置条件的核心前提被推翻。**

- D-008 双 bug **未修复进 common/_recovery.py**（仍等权版，status `pending_fix`）
- 但 D-009 sandbox **已跑完加权修复版的三方对照**，结论：**加权修复版 vs VV 仍全场景持平**（10kHz 实测主流线宽下 |rel|<5%，加权 vs 等权 BER 差 ≤1.7%）
- **B11-Q2 预设的"持平是 bug → 修复后应拉开"物理预期在 10kHz 线宽下不成立**——ML 加权（B11 核心）在单载波时域全线无用

**对 B11-Q2 的影响**：sandbox 前置条件不是"等 D-008 修完"，而是"等一个不会到来的'加权修复后拉开 VV'"。需重新框定 B11-Q2 的验证目标（见 §4）。

## 1. D-008 双 bug 修复状态（核查 1）

**D-008 status：`pending_fix`**（`step4a-mve-execution/decisions.md` L299）

**双 bug 定义**（D-008 L311-321）：
- Bug 1（漏 ML 加权）：`_recovery.py:232` 用 `np.angle(raised.mean())` 等权，应为 `angle(Σ|R(k)|²·ψ)/M₀` 加权（B11 Eq.16）
- Bug 2（升幂未归一化）：`_recovery.py:213` 用 `rx**M₀` 含幅度，应为 `(rx/|rx|)**M₀` 去幅度（B11 Eq.5）

**common/_recovery.py 当前实现：仍是等权版，未修复**（主线独立 grep 核查）：
- L213 `raised = rx ** M0`（未归一化升幂，Bug 2 在）
- L224 `seg_phi[k] = np.angle(raised[lo:hi].mean())`（segmented 等权，Bug 1 在）
- L232 `phi_raised = np.angle(raised.mean())`（none 等权，Bug 1 在）
- L243 `raised = rx ** M0`（FFT-df 分支未归一化）
- 全文 grep `mag = np.abs` / `yn =` / `w*yn` 零命中 → 无加权修复

**未修复原因**（H006 债务表）：H006 明示"不要改 common/_recovery.py 补加权 bug 修复"，D-008 双 bug 标为"pending 老师反馈"——因为 D-009 sandbox 已证明加权无用，修不修代码对结论无影响（加权版跑出来仍持平），所以不急着改 common。

## 2. D-009 sandbox 验证状态（核查 2）

**sandbox 已跑完**。结果文件真实存在（`explore/nda-awgn-tracking-sandbox/`）：
- `_ml_weighting_results.json`（7/7 16:46，meta 明确标"修 D-008 Bug1+Bug2"，加权公式 `yn=(rx/|rx|^M0; w=|rx|^2; phi=angle(sum(w*yn))/M0`）
- `_vv_vs_nda_checkup.json`（7/7 19:10，11 点三维扫描）
- `_uplink_vv_check.json`（7/7 21:24，层 4 决定性证据 VV Nw 调优）

**ML 加权收益定论：全线无用**（主线独立核查 JSON 原 BER + 决策 L384）：
- 11 扫描点加权 vs 等权 BER 差 **≤1.7%**（D-009 L384/401）
- JSON 实测例：AWGN 10dB weighted_none 0.0678 vs VV 0.0706（rel -4%）；16dB 0.0100 vs 0.0098（rel +2.7%）→ 全 `tie`

**NDA-ML vs VV 定论：全场景持平**（D-009 L385/449）：
- 10kHz 实测主流：加权/等权 vs VV 全程 |rel|<5%
- ≥200kHz segmented 拉开 VV -14%~-19%，但层 4 证明 VV 把 Nw 从 64 调到 16 立刻反超（500kHz 赢 68%）→ segmented 也无真增量
- 最终定论（D-009 L449）："唯一真实增量 = vs DA-ML 频谱效率"

**判定：修复版（加权版）vs VV 仍持平**。B11-Q2 预设的"sandbox 验证 NDA-ML 修复版 vs VV 不再持平"预期 **已被 D-009 sandbox 反向证伪**。

## 3. NDA-ML 方法方向 + 专题状态（核查 3）

**方法方向 X/W：pending 用户，且基本堵死**（D-009 L452/469）：
- W（segmented + 高线宽）被层 4 排除（VV Nw=16 反超）
- X（改进 VV）被打问号（VV 调参就赢 NDA，改进 VV 难超 VV 本身）
- 用户已排除 E（找老师）/ Z（转系统层），矛盾未解

**专题 status：`dormant`**（registry.yaml L386 "S008 VV/BPS ablation + D-008 双 bug + D-009 线宽选择待用户拍板...转 dormant 等 B7 出结果或 NDA-ML 线宽/方向拍板后回来"）

**判定**：B11-Q2 sandbox 用哪个版本的 NDA-ML 仍未定。但无论用哪个（等权/加权/segmented），D-009 已证明 vs VV 全持平。

## 4. vs DA-ML 主结论（核查 4）

**当前有效性：有效**。vs DA-ML 增益 **+1.35~2.5dB（下行）+2.48~3.07dB（上行）** 不依赖 ML 加权/segmented，去 pilot 是真增量（D-008 L351, D-009 L449/467）。

**这是 B11-Q2 唯一可用的真增量锚**：sandbox 以 DA-ML 为 baseline 成立。

## 5. 对 B11-Q2 sandbox 前置条件的重新框定

### 原前置条件（topic-index INVARIANT 11 / H001）

"D-008 修复前禁跑 B11-Q2 sandbox（vs VV 持平是 bug，bug 没修跑湍流验证无意义）。修完通知 B11-Q2 可进 sandbox。"

### 核查后的真实情况

原前置条件的**两个子前提都已不成立**：
1. "D-008 修复后会 vs VV 拉开" → D-009 证伪（加权修复版仍持平）
2. "等 D-008 修复" → D-009 已用 sandbox 加权版验证完，common 不修是因为修不修结论一样

### B11-Q2 的真实验证目标（需主控对话 + 用户重新确认）

B11-Q2 原命题"加湍流信道重评 NDA-ML 是否保持 +2dB"的 **+2dB 锚来自 vs DA-ML（不是 vs VV）**。vs VV 持平不影响 B11-Q2 核心命题，因为：
- B11-Q2 baseline 是 **DA-ML**（不是 VV，见 H001 阶段 0.4）
- vs DA-ML +1.35~2.5dB 是真增量（去 pilot），D-008/D-009 均确认不受双 bug 影响
- B11-Q2 的问题是"湍流下 NDA-ML vs DA-ML 是否仍 +2dB"，不是"NDA-ML vs VV 是否拉开"

**所以 B11-Q2 sandbox 前置条件应重新框定为**：
- ~~等 D-008 修复~~（D-009 已证加权无用）
- **改为**：vs DA-ML 主结论（+1.35~2.5dB）在湍流下是否成立——这正是 B11-Q2 sandbox 要验证的，不需要额外前置门控

**但**这个重新框定是**重大方向性变更**（推翻 INVARIANT 11 原设计前提），不是工作对话能拍板的。按 profile "Go/Kill 是用户的" + 不变量修改必须重新讨论，**本轮只记录发现 + 报主控对话/用户，不自作主张改 INVARIANT 11**。

## 6. 主线判定

**B11-Q2 sandbox 前置条件判定**：

| 原前置条件子项 | 状态 | 说明 |
|---|---|---|
| D-008 修复进 common | ❌ 未修复 | 但 D-009 证明修不修结论一样 |
| sandbox 验证修复版不再持平 | ❌ 已证伪 | D-009 加权版仍全场景持平 |
| 方法方向 X/W 拍板 | ❌ pending | 但不影响 vs DA-ML 结论 |
| vs DA-ML 主结论有效 | ✅ 有效 | +1.35~2.5dB 是真增量 |

**按原 INVARIANT 11 字面**：D-008 未修复 → 禁跑 sandbox（维持原判定）。

**但实质**：D-009 已证明"等 D-008 修复"是等一个不会到来的结果。B11-Q2 的真正价值锚（vs DA-ML）不受 D-008 影响。

**本轮建议（报主控对话 + 用户决策）**：
1. INVARIANT 11 原设计前提（"持平是 bug，修复后应拉开"）被 D-009 推翻，需用户拍板是否重新框定 B11-Q2 sandbox 前置条件
2. 选项 A（保守）：维持原 INVARIANT 11 字面，D-008 common 修复前不跑 sandbox（阶段 0 做完等）
3. 选项 B（重新框定）：D-008 不再是 sandbox 前置门控（因加权已证无用），B11-Q2 直接验证"湍流下 NDA-ML vs DA-ML 是否保持 +2dB"——sandbox 用现有等权版 NDA-ML 即可
4. **本轮不拍板**，记录发现交主控对话 + 用户

## 证据链

- D-008 完整条目：`step4a-mve-execution/decisions.md` L297-371
- D-009 完整条目：`step4a-mve-execution/decisions.md` L372-490
- common/_recovery.py 等权版：L213/224/232/243（主线 grep）
- sandbox 结果：`explore/nda-awgn-tracking-sandbox/_ml_weighting_results.json`（加权公式 meta + BER 数字）+ `_vv_vs_nda_checkup.json`（11 点扫描）+ `_uplink_vv_check.json`（层 4）
- H006 债务表："D-008 双 bug 未修代码 / pending 老师反馈"
- 子 agent 核查 + 主线独立 grep 交叉验证（不变量 10 中性双向）
