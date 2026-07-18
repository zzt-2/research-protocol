# [S012] N1 §4a 维度 D MVE 判定——FAIL（MB on 16-QAM 无整形增益，ν 搜索自选均匀）

> 2026-06-17 续 7 | 阶段: N1 Groundwork §4a 维度 D（MVE）| 状态: §D MVE FAIL → N1 化身 Kill，用户选"先记录 FAIL，下轮再议替代"
> 来源: S010 §B CONDITIONAL GO 留下的待闭合项（强湍流幅度 AMBIGUOUS）| 框架: gw-feasibility.md §D
> 注: 原拟编号 S011，与对话甲 A3 MVE 前置准备的 S011 冲突，改 S012。原拟派子 agent 执行；子 agent 撞 600s 超时无产物，改主对话直接写脚本（explore/n1-pcs-gain/）

## 目标

闭合 S010 §B 判定的 AMBIGUOUS 项：用 MVE 实证验证"N1 强湍流下离线 MB 分布 ≥0.5dB gain"假设。S010 判 CONDITIONAL GO 时明确"强湍流幅度须 §D MVE 闭合"——本轮闭合，答案是否定的。

## 记录

### MVE 设计（SPEC，用户确认阈值/指标）

- **假设**：强湍流（α1.5/β0.8）下，离线单一 MB 分布 vs 均匀 16-QAM，AIR=3.0 工作点 SNR 增益 ≥0.5dB
- **阈值**（用户 AskUserQuestion 确认）：Go≥0.5 / Conditional 0.3-0.5 / Kill<0.3
- **主指标**（用户确认）：AIR（BMD rate，信息论度量，不依赖 FEC）；SER 辅助
- **保真度 FR-04**：保留 GG 块衰落 + 16-QAM + 离线单一 MB 分布（N1 核心）；省略多普勒/相位（PCS 优化幅度分布，与相位正交，S010 §B 原因2）+ 省略 FEC（用 AIR 避 LDPC 偏差）
- **baseline**：uniform（FR-14 先验+FR-15 目标）+ per-block oracle（CSI-aware 上界）
- **TL-20 预期**：MB 对 16-QAM 理论上限 ~0.5-1.0dB；weak<0.3/moderate 甜区/strong AMBIGUOUS
- SPEC + 脚本：`projects/simulation/explore/n1-pcs-gain/`（用户建议从 .sessions/ 迁出）

### 执行轨迹（调试两轮 bug，systematic-debugging）

**bug 1: SNR 惯例**。初版 `σ²=1/(2γ)` 致实际 SNR 翻倍 → AWGN uniform AIR@0dB=2.523 > Shannon 1.0（OVER-SHANNON）。根因：毕设 `_channel.py` 用 γ=Es/2N0 惯例，MVE 改自洽 σ²=1/γ（γ=Es/N0，与 Shannon 直接对应）。修复后 AWGN uniform 合理。

**bug 2: AIR 估计器**。LLR 熵法 `log2(1+exp(-|L|))` 对 uniform 系统偏高 ~1bit。三法交叉验证（`_validate_estimator.py`：LLR熵 / Y分箱 / 后验积分）：后验积分法对照 Shannon 最合理（uniform@0dB=0.899<1.0, @12dB=3.578<4.075）。改用后验积分法。

**两 bug 修复后，估计器可靠**：AWGN uniform 单调升到 4，全点 < Shannon，物理正确。

### MVE 结果（FAIL，证据充分）

全量扫描 3 湍流 × 6 γ̄ × 3 方案，229s 无降精度，结果 JSON: `explore/n1-pcs-gain/n1_pcs_gain_mve_results.json`。

| 湍流 | gain @ AIR=3.0 (dB) | offline 选的 ν | oracle vs uniform |
|------|---------------------|---------------|-------------------|
| weak | **0.0** | **0.0（=均匀）** | ≈0（无优势）|
| moderate | **-0.007** | **0.0（=均匀）** | ≈0 |
| strong | 未达 3.0（两方案 max 2.713） | **0.0（=均匀）** | ≈0 |

**决定性信号**：全部 18 个 (湍流,γ̄) 组合，离线 ν 搜索（7 候选 [0,0.05,0.1,0.2,0.4,0.8,1.5]）**最优永远是 ν=0**——MB 分布族的优化器自己认定均匀最优。连 oracle（完美 CSI）也无优势。

AWGN 控制实验（锚点2）同结论：MB 全 SNR < uniform（0dB: ν=0.2→0.510 vs uniform 0.899；10dB: ν=0.1→2.901 vs 3.161）。

### 根因（已验证为真实现象，非估计器 bug）

1. **16-QAM 阶数太低**，PS 整形空间不足（文献已知：PS gain 主要在 64/256-QAM，16-QAM 太小）
2. **MB 分布破坏 Gray 映射 bit 独立性**：概率集中内圈点（±1±1），其 Gray 标签高度相似 → bit 间相关性↑ → H(b_k)↓ → I(b_k;Y) 上限↓。抗噪增益（内圈点误码少）不足以补偿信息承载损失
3. **与 Tian 1.3dB 不矛盾**：Tian 用 **PSO 自由 2D-PMF**（非 MB 族，L509 直证）+ 报 **post-FEC BER**（非 AIR）。Tian 自己的 AIR 只报 0.3-0.4dB（R007 限制#2 早记录）。N1 锚定 MB+AIR 从结构上拿不到 Tian 的 gain

### §4a 决策表对号：Kill

- 不是 Go（MVE 未通过）
- 不是 Conditional Go（gain 不是"部分通过有改善路径"，而是结构性为零——优化器自选均匀）
- **是 Kill**（MVE 失败，核心假设"MB 有整形增益"无法修复——不是 deep fade 幅度问题，是分布族与星座根本不匹配）

**Kill 的是"N1 = 离线单一 MB 分布 on 16-QAM"这个具体化身**，不是整个 PCS 方向。Pivot 路径（Tian PSO-PMF / 64-QAM）存在但本轮不议（用户选先记录）。

### 关键诚实区分（重申 S008/S010 层层递进）

- **D005 门控解除** = "gain 数据存不存在"（R007 闭合：Tian 1.3dB 存在）
- **§4a 维度 B** = "结构有无致命原因"（S010 闭合：CONDITIONAL GO，0/5 致命）
- **§4a 维度 D MVE** = "强湍流幅度能否 ≥0.5dB"（**本轮闭合：FAIL**）
- 三者层层递进。§B 的 CONDITIONAL GO 是对的——结构上 MB 不致命（可计算），但实证上 MB 在 16-QAM 无增益。§B 看不到的"分布族与星座匹配度"问题，§D 暴露了

### 对互锁三章判定的影响

S010 判"互锁取决于 N1 §D MVE"。本轮 MVE FAIL → **互锁三章不成立（N1 腿断）**。
- A3（§B PASS，待 §D MVE）— 腿立
- 2.2（保底）— 腿立
- N1 — **腿断**（MB 化身 Kill）
- **精确表述**：互锁三章基础从"取决于 N1 §D MVE"细化为"**N1 §D MVE FAIL，互锁不成立，需另寻第三腿**"。地板（A3+2.2）仍不变。重申 S004：互锁是结果非前提——本轮 FAIL 是客观结果，不锁叙事

## 决策引用

- D005：N1 门控解除（前置已闭合，本轮在其上做 §D）
- S010：§B CONDITIONAL GO（本轮 §D 否定了其 AMBIGUOUS 项）
- gw-feasibility.md §D：MVE 流程 + §4a 决策表（Kill 定义）
- **新建 D007**：N1 §D MVE FAIL + 化身 Kill + 互锁不成立（见 decisions.md）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。§4a 维度 D 是 D001 后续阶段链 Groundwork Step 4a 的明文必做项（gw-feasibility.md §D）。属原始目标"系统性扫描找方向"的可行性预判深化。未碰 MVE/Contract/Execute 正式阶段（这是 §4a 内的 MVE，非 Contract 后的正式仿真），未改毕设仿真代码/开题报告
- 范围变更：无新增

## 后续

### N1 下一步（用户选"先记录 FAIL，下轮再议替代"）

1. **本轮不议替代方向**（已达单对话步骤上限 + 用户明确下轮再议）
2. 下轮候选（留待讨论，不预设）：
   - D004 切法⑦（不确定性来源建模）— 与 A3 接得上，针对主导损伤
   - D004 切法⑧（反向设计准则）— 纯解析，TL-05 偏好
   - N1 Pivot（Tian PSO-PMF / 64-QAM）— 天花板低（AIR 0.3-0.4dB），不推荐但可选
3. **A3 §D MVE**（对话甲 H006）可并行推进，不受 N1 FAIL 影响

### 不要做

- ❌ 把"N1 FAIL"当"PCS 方向整体不可行"（只 MB on 16-QAM 化身 Kill，PCS on 64-QAM/PSO-PMF 未测）
- ❌ 锁定"互锁三章彻底破产"（A3+2.2 仍在，第三腿待议，地板不变）
- ❌ 跳过记录直接 Pivot（用户明确先记录 FAIL，治理完整再议替代）
- ❌ 把 MVE 脚本当正式仿真产物（§4a MVE 是临时验证脚本，结果支撑 §4a 决策即可，非论文级仿真）

### 代码产物位置（用户确认的组织）

- `projects/simulation/explore/n1-pcs-gain/`：MVE 脚本 + SPEC + 验证脚本 + 结果 JSON
  - `n1_pcs_gain_mve.py`（主脚本，后验积分法 AIR）
  - `N1-MVE-SPEC.md`（执行契约）
  - `_smoke.py` / `_validate_estimator.py`（调试/验证脚本，可保留作复现证据）
  - `n1_pcs_gain_mve_results.json`（结果数据）
