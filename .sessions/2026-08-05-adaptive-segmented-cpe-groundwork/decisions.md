# Decisions — Adaptive Intra-Window Segmented CPE Groundwork

## D001: bounded Step 1 复核，不撤销历史 adaptive-K 否决

> status: active
> date: 2026-08-06
> 取代：无
> 被取代：无
> 依据：用户原话: voice.md 2026-08-06 + system D025 + 历史 `.sessions/2026-07-06-step4a-mve-execution/decisions.md#D-011` + `internal-method-kernel-inventory.yaml#a1_adaptive_segmented_cpe`

### 决策

建立 C3 独立 Groundwork 专题，只执行最多 4 组新增 query 的 Step 1 定向复核。历史 D-011/CP004
对同动作 adaptive K 的否决继续有效；只有新检索同时支持近期合法 baseline、真实物理条件，并形成至少
一个四判据 Q#，才可进入 Step 2。Step 2 若发生，只做全文获取并停在用户覆盖面确认门。

### 理由

用户显式授权 C3 Step 1，但既有权威记录已显示相同 action signature 在主流条件下无可实现增量。
保留该反证并用 Step 1 检查是否出现足以满足 reopen condition 的新外部证据，既执行用户指定检索，
也避免换名重开已否决方向。

### 排除的替代方案

- 不预先恢复 C3 为 concept survivor；
- 不忽略 D-011、CP004 或 inventory 的失败数据；
- 不通过提高 linewidth、运行旧/新仿真或进入 Step 4a 制造正面空间；
- 不在无四判据 Q# 时下载全文进入 Step 2。

### 影响范围

仅本专题 Step 1/条件式 Step 2、RDL current control、master-state 与 registry；不改历史证据和算法代码。

### 来源

S001；用户 2026-08-06 执行指令。

## D002: C3 Step 1 物理前提不支持，停止且不进 Step 2

> status: active
> date: 2026-08-06
> 取代：无
> 被取代：无
> 依据：调研: R001 + 历史 D-011 + `internal-method-kernel-inventory.yaml#a1_adaptive_segmented_cpe`
> 触发原话: 无（技术推导）

### 决策

C3 在 Step 1 触发 `PHYSICAL_PREMISE_UNSUPPORTED`。没有四判据全 PASS 的 Q#，专题关闭，Step 2
不执行。该方向不得通过提高 linewidth、改用相同 proxy、换名或复用旧 MVE 重开。

### 核心失败机制

一般 window bias–variance tradeoff 在文献中存在，但冻结的星地 FSO 主流 10–80 kHz 条件下，C3
同动作历史实测已退化为固定 K16；receiver-visible proxy 无预测力，tuned VV 又吸收高线宽表面增益。
新增检索没有提供新信息源或把极端 linewidth 变成主流物理条件。

### 否决了什么

- 否决以 CV/SNR/linewidth proxy 选择 NDA segmentation K 作为本轮可继续的研究问题；
- 否决在当前冻结条件下进入 Step 2、Step 3、Step 4a、实现或仿真；
- 不否决一般 fixed-window CPE 文献的 baseline/防御性材料价值。

### 可复用部分

JLT 2020 fixed-window blind BPS 可作未来其他合法 CPE 问题的近期 baseline；四组 annotated search JSON
与 R001 的 direct-competitor 边界可复用。

### 具体数据

历史 adaptive-J4 gain=0.000 dB、0/8 显著胜；K16 在 35 点中 71% 持平 oracle；最强
`|rho|=0.361`；tuned VV Nw16 在 200/500 kHz 反超 14%/68%。本轮 4/4 query，raw=187，
query-dedup=179，final=151，cross-query dedup=140；无新 reopen evidence。

### 影响范围

C3 专题 closed；RDL current control 返回候选轮换。P1 closed 状态与历史 D/V/R/H 不变。

### 来源

S001 / R001。
