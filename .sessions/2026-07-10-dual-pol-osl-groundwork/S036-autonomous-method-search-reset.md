# [S036] 自主方法搜索复位：状态纠正、路线比较与 residual cascade 起步

> 2026-07-16 | 方法层重开轨 / GW Step 1 前置 | 状态：治理与候选复位完成，尚未运行实验

## 目标

在不跳 FR-22 的前提下接收用户“主控直接做、方向不行可自行换”的授权，先纠正 D040 后的事实合同与项目状态，再比较当前三条可见路线，选出**只进入 GW Step 1**的下一候选；本轮不设计、不运行 MVE。

## 记录

### 1. 事实纠正

1. D040 的合法 baseline 结果是：standard-CMA（Godard 更新含 z 因子）在注册新域 0/5 swap、fixed-label BER≈2e-4；`common/_cma.py` 的 current-CMA 缺 z 因子，5/5 swap；固定权重 ButterflyCNN ML 5/5 clean-swap、fixed≈0.5。
2. 因此旧 Problem/H1“standard-CMA 在 SOP 下发生 lock swap”已被推翻。仍成立的是：PI-BER 对 swap 失明、D022 的 ML 29/30 优势只限 PI 窄域、ML fixed-label SOP 泛化失败需要重新定位。
3. 本轮开始时 `master-state.md` 仍停在 2026-06-21/GW Step 2/Contract not started；注册表仍停在 S033 旧物理；专题有 36 个 S 文件且 inflation record 只覆盖到 27。治理修复优先于新实验。

### 2. 三路线比较

| 路线 | 当前问题合同 | A0 判断 | 本轮处理 |
|---|---|---|---|
| strict equivariance / e2cnn | 试图靠 hard equivariance 在未知 SOP 下恢复绝对 X/Y fixed label | **NO-GO（D043）**：e2cnn SO(2)/E(2) 二维空间表示与 Jones U(2)/SU(2) 双复偏振作用不匹配；即使群作用正确，等变也不提供绝对标签锚点 | 不进 MVE；仅保留为 PI/残差建模的未来材料 |
| pilot/CSI 前置 | 用已知符号估 Jones/SOP，再前馈补偿并固定标签 | 物理可行，但 D037 与 DOI `10.1109/JLT.2023.3253383` 显示强占点；FSO 迁移增量未证 | DEFER；若复活须先补新颖性与直接 FSO 证据 |
| standard-CMA 前端 + ML residual cascade | standard-CMA 保持 fixed label，ML 只学其残余误差，目标是从≈2e-4逼近 oracle≈3.5e-5，而不是让 ML 独立承担标签身份 | **仅选为下一 GW 路线，不是 Go**。优点是避开 ML 的绝对标签不可辨识性，并利用 standard-CMA 已实测的在线标签保持；风险是增益空间只有约 5.7×、残差可能无稳定可学结构，且可能与 neural-CMA/混合均衡先例撞车 | 进入候选专属 GW Step 1；先形成 M-C-A 与检索合同 |

### 3. 选择与退出纪律

- 选择 residual cascade 的含义仅是“下一条先查”，不是方法定型。
- 在 Step 1 前先把候选写成 Q# 的 M-C-A；没有具体 `M 在 C 下因 A 不足`，不得以标题联想开实验。
- 候选自己的 Step 1/2/3/必要 3.5/Step 4a 任一硬门未过，立即 stop/defer/Kill 并自主切换下一候选；D042 的自主权不改变门控。
- F1 电控偏振跟踪、G2 HARQ 重传仍明确排除。若证据迫使跨入硬件/协议层，先另做 scope change 与 D###，不能静默扩大。

### 4. 实验状态

**本轮没有运行任何新仿真、训练或 MVE，也没有产生新的 BER 数字。** 下一步仅是 residual cascade 候选 GW Step 1。

## 决策引用

- D042（新建）：软件 DSP/ML A-E+H 范围内自主排序、止损、换候选；每候选必须 Q#+GW 全链。
- D043（新建）：strict equivariance/e2cnn 作为 fixed-label 解法 A0 NO-GO。
- D040：standard-CMA 不 swap、current-CMA bug、ML fixed-weight swap 的事实纠正。

## 范围确认

- 本轮是否在 scope boundary 内：是。仅在 D030/S033 已批准的软件 DSP/ML A-E+H 内做状态修复和候选排序；F1/G2 未解禁。37-S inflation record 已写入 `topic-index.md`。

## 后续

1. 在下一步开始前重读 `stages/groundwork.md` 对应 Step 1 规范。
2. 为 residual cascade 形成候选 Q# 的 M-C-A、Step 1 检索问题与退出判据。
3. Step 1 通过后才进入获取/精读；未通过则按 D042 自主换候选并记录原因。
4. `contract.md`、`feasibility_report.md`、`literature_notes.md`、`GPT-CREATIVE-BRIEFING.md` 的 D040 后状态同步留到下一批，本轮不修改。
