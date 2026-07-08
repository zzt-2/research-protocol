# Handoff: 闭环版 sandbox 救援路线 FAIL——三 Go 全不够格 + Go1 物理根因证伪，交主控定夺 Kill

> 来源: S005（工作对话闭环版 sandbox 执行）| 交接目标: 主控对话核查闭环版 sandbox 结果 + 定夺 Kill
> 文件名: H005-closed-loop-sandbox-fail-to-master.md
> 日期: 2026-07-08

## 到哪了（状态）

**工作对话 S005 完成阶段 1.5 重设计 + 闭环版 sandbox 全量 21 点**。救援路线（D003：闭环 hold + power-boosted pilot）**未能翻盘**。用户追问"能大大方方讲吗"+"确实有提升就行"后，再查发现 **Go3 增益是 h 均衡口径 bug 导致的假阳性——B2-Q2 没有真实提升**。

**再查后修正的最终结论（推翻本 session 前半段 Go3 数据）**：

| Go 判据 | 前面报的 | 再查后（最终）| 物理 |
|---|---|---|---|
| Go1 动态恢复 C<A | FAIL（hold 够好，0.05rad）| ❌ **FAIL**（论据修正：非 fade 期 blind 一块锁定无惯性，不是"hold 够好"——hold 误差实际 0.32rad 是 CFO 斜率，但恢复仍无差异）| 非 fade 期块内闭式估计无收敛惯性 |
| Go2 范围扩展 | FAIL | ❌ **FAIL**（A/C 全 21 点 BER >> HD-FEC）| 无可达空间 |
| Go3 稳态 BER fair gain | PARTIAL（+0.42dB）| ❌ **FAIL（假阳性）**：h 均衡口径 bug | 公平对照下 pilot≈blind，无真实增益 |

**🔴 决定性发现（Go3 假阳性证伪）**：

用户追问后做决定性分解实验（weak 24dB，400 块，逐块分类，**同一 h 均衡同一信道实现**）：

| 处理 | fade 块 BER | 非 fade 块 BER |
|---|---|---|
| blind（nda_ml M₀=8）| **0.00322** | **0.00122** |
| pilot（da_ml）| 0.00330 | 0.00123 |
| hold（常数补偿）| 0.00466 | — |

fade 块 **pilot 对 blind 没有优势**（0.00330 vs 0.00322，pilot 微输）。前面 Go3 "+0.4dB" 来自 `_sandbox_closed_loop_three_way.py` 的 h 均衡口径不一致：`c2_ber_fade_da_ml` 用 **pilot h 均衡**，`c2_ber_fade_closed_hold` 用 **blind h 均衡**——pilot h 本身比 blind h 准，不是 pilot 估计器的功劳。同一 h 均衡下增益消失。

**根因**：fade 块 BER 高的主因是 SNR 低（信号弱），pilot 和 blind 都受同样的 SNR 限制——pilot 已知符号去调制，但噪声仍在，低 SNR 下估计精度都差。B2-Q2 核心命题"fade 期 pilot-aided fallback 比 blind freeze 更优"在当前信道 + SNR 区间**不成立**。

## 下一步干什么（主控定夺 Kill）

**主线建议：Kill B2-Q2**。理由（再查后修正）：
1. **Go3 假阳性**（h 均衡口径 bug，公平对照下 pilot≈blind）——**B2-Q2 没有真实提升，不是量级问题**
2. Go1 动态恢复不成立（非 fade 期 blind 一块锁定无惯性）
3. Go2 无 HD-FEC 可达空间
4. B2-Q2 核心命题（pilot fallback 优于 blind freeze）在当前信道实证不成立

**但 Kill 是用户的**（profile"Go/Kill 是用户的"）。主控对话需：
1. 核查 Go3 假阳性（重跑决定性分解实验，确认 pilot≈blind）
2. 向用户报告"B2-Q2 无真实提升（假阳性）"+ 定夺 Kill

**挣扎口子极窄**：h 均衡口径 bug 是公平对照问题，修了就没了。pilot 在低 SNR fade 块对 blind 无优势是物理特性（SNR 限制）。除非换信道模型（加 pilot 能解但 blind 不能的损伤，如快速 SOP 旋转——但这偏离当前信道假设）。

## 纪律（和下一步直接相关的约束）

1. **Go3 假阳性是硬结论**：决定性分解实验（同 h 均衡）显示 pilot≈blind，公平对照下无增益。这不是"增益小"，是"提升不存在"
2. **诚实交代**：本 session 前半段 + S004 V5 核查都没抓到 h 均衡口径 bug（V5 只核查 n_recover + fair gain 算式，没核查 c2 子集 BER 的 h 均衡一致性）——V5 盲区记教训
3. **守 profile"Go/Kill 是用户的"**：主线建议 Kill，但用户拍板
4. **B2-Q2 Kill 不影响 NDA-ML/B7**：B2-Q2 是独立候选，Kill 后 NDA-ML（step4a dormant）/ B7（active）继续
5. **复用基建投入不浪费**：即使 B2-Q2 Kill，闭环 freeze 实现 + power-boost 框架 + n_recover v2 度量 + h 均衡公平对照方法可复用于其他候选

## 失败数据附录（闭环版 sandbox，V5 主线独立核查）

### 三 Go 全不够格（闭环版，21 点全量）

| Go 判据 | 结果 | 关键数据 |
|---|---|---|
| Go1 动态恢复 | ❌ FAIL | nR_A==nR_C 全 21 点（0/21 有差异），均值 2.85-3.49 块 |
| Go2 范围扩展 | ❌ FAIL | A/C 全 21 点 BER 0.08-0.30 >> HD-FEC 3.8e-3 |
| Go3 稳态 BER fair gain | ❌ **FAIL（假阳性）** | 前面报 +0.42dB 是 h 均衡口径 bug；公平对照（同 h 均衡）pilot≈blind |

### 🔴 Go3 假阳性决定性证据（再查后，推翻前面 Go3 数据）

决定性分解实验（weak 24dB，400 块，逐块分类，**同一 h 均衡同一信道实现**）：

| 处理 | fade 块 BER | 非 fade 块 BER |
|---|---|---|
| blind（nda_ml M₀=8）| **0.00322** | **0.00122** |
| pilot（da_ml）| 0.00330 | 0.00123 |
| hold（常数补偿）| 0.00466 | — |

fade 块 pilot≈blind（0.00330 vs 0.00322，pilot 微输）。前面 Go3 "+0.4dB" 来自 h 均衡口径不一致（`c2_ber_fade_da_ml` 用 pilot h，`c2_ber_fade_closed_hold` 用 blind h）。

blind 在非 fade 块完全正常（0.00122 随 SNR 正常下降），无 bug。fade 块 BER 高的主因是 SNR 低，pilot 和 blind 都受同样 SNR 限制。

### Go1 论据修正（前面 0.05rad 错，实际 0.32rad，但结论不变）

前面报"hold 误差 0.05 rad"用块平均相位测，把残余 CFO（F_RESIDUAL=1MHz）块内 0.64 rad 斜率平均掉了。按符号级重测 hold 误差均值 0.32 rad（来源 CFO 斜率）。但 Go1 仍不成立——真实原因是非 fade 期 blind 块内闭式估计每块独立重新锁定，fade 结束后一块即锁定，无收敛惯性可缩短。

## 接收方验证（主控对话续接时必须完成）

- [ ] 已读取 topic-index 不变量段落（15 不变量）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] **Go3 假阳性**（重跑决定性分解实验：weak 24dB 同 h 均衡下 pilot vs blind fade 块 BER，确认 pilot≈blind）—— **这是 Kill 的核心依据，必须独立复现**
  - [ ] h 均衡口径 bug（核查 `_sandbox_closed_loop_three_way.py` 的 c2 子集：fade 块 da_ml 用 rx_pilot，fade 块 hold 用 rx_blind，h 均衡不一致）
  - [ ] Go1 nR_A==nR_C（grep `_sandbox_closed_loop_results.json` 21 点全相等）
- [ ] 已确认再查后的结论（非只信工作对话前半段 Go3 +0.4dB）
- [ ] 已向用户报告"B2-Q2 无真实提升（假阳性）"+ 定夺 Kill

## 下一轮

**主控对话定夺 Kill**：
1. **核查 Go3 假阳性**（重跑决定性分解实验，确认公平对照下 pilot≈blind）——这是核心，必须独立复现
2. 向用户报告"B2-Q2 无真实提升"+ Kill 决策（若 Kill，记 D004 Kill B2-Q2 + 更新 topic-index status closed）

**若 Kill**：B2-Q2 专题转 closed，NDA-ML/B7 继续。复用资产保留（闭环 freeze + power-boost 框架 + n_recover v2 + **h 均衡公平对照方法**）。

**挣扎口子极窄**：h 均衡口径 bug 修了就没增益。pilot 在低 SNR fade 块对 blind 无优势是物理特性（SNR 限制）。除非换信道（加 pilot 能解但 blind 不能的损伤，如快速 SOP 旋转——但偏离当前信道假设）。
