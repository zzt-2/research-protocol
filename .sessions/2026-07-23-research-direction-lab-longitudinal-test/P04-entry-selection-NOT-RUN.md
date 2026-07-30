# P04 入口选择（NOT RUN — 本轮只选不跑，按绑定裁决）

> 来源: D041 / CP032；绑定裁决"同一对话选择 P04 的不同机制族入口，但不运行"
> 日期: 2026-07-30
> STATUS: **REJECTED** — 本文件提出的入口（16APSK 环比失配 + 湍流标签失配）经绑定裁决
> 失效，已撤回。新 P04 = C_CONTINUOUS_GG_OOD_SELECTOR_ROBUSTNESS，同对话端到端执行（见
> P04-continuous-gg-ood-entry.md + worker-log step-031）。本文件正文保留作 rejected brief 供审计。

## 当前族覆盖（D039 §4）

| 族 | D039 内容 | 状态 |
|---|---|---|
| A | CPR 选择器鲁棒性（SNR 失配、cand_rank 工作区） | **关闭**（P01+P02 连续=2 达上限） |
| B-content | 同步/估计器交互（FOE 残差→CPR、定时偏移→selector） | **关闭**（T030 FOE-residual 撤回；`FOE_RESIDUAL_CPR_CASCADE_FAMILY` forbidden） |
| 定点族 | 固定点/资源-性能协同设计（绑定裁决标签 `B_FIXED_POINT_...`，D039 内容=族 E "量化位宽"） | **开**（P03 连续=1，未达上限） |
| C | 湍流场景边界（饱和/闪烁、上下行、多普勒谱形变） | 未开 |
| D | 调制/编码层（HD/SD-FEC、APSK 环比失配、16APSK 旋转模糊） | 未开 |
| E-其他 | 窗口长度 vs 估计方差、低复杂度降级 | 未开 |

## P04 入口候选评估（problem-bearing 四门 + file:line，不运行）

为满足"至少 5 机制族"，P04 **优先开新族**（C 或 D），而非定点族第 2 包。原因：定点族 P03 已 RESOLVED，
开第 2 包只会在 sub-MDE 的 two_exp 弱提示上打转（profile 反对早收敛但也反对在同轴打转，D039 §4 同族≤2）。
开新族更快达到 5 族覆盖（当前 A 关闭 + 定点族 1 = 2 族实际贡献；C/D 各开 1 包 → 4 族；P05 校准时评估）。

**推荐入口：D 调制/编码层族 — 16APSK 环比失配对 DA/NDA 选择器的影响**

四门预评估（下一对话执行前需 freeze file:line）：
1. **物理 DOF 存在**：DA/NDA 选择器的 `per_block`（`_a4_switch_common768_30seed.py:110-139`）对 16APSK
   demod (`m16apsk_demod`)，其决策路径 `decide` 用功率统计 CV + 盲 h 不直接依赖星座几何，但**分支输出**
   `ne_nda/ne_da` 由 demod 决定——若接收端持有的星座环比（ring ratio）与发送端失配，demod 判决点偏移 →
   分支输出错误计数变化 → selector 选错分支的 regret 变化。这是对已完成方法的新失效条件（FR-23）。
2. **baseline 失效对齐 lever**：原 selector 假设标准 16APSK；环比失配是新失效条件（类比 P01 的 SNR 失配）。
3. **命名传统 comparator**：接收端可见的环比估计器（从 demod 软符号统计估环比）+ 原 decide 规则；
   δ(环比)-invariant，true 环比不进 decide。
4. **file:line 证据**：`m16apsk_demod`、`resolve_m16apsk_blockwise`（common）、`per_block:128-139` 需执行前 freeze。

**备选入口（若 D 门不全过）：C 湍流场景边界 — 饱和/闪烁强度失配**。门1：原 selector 的 CV 统计
依赖湍流强度（weak/moderate/strong 的 CV 分布不同）；若接收端持有的湍流等级标称值失配，stage-1 CV
边界 `cv_awgn_theory(γ)` 与实际 CV 分布错配 → 选错分支。comparator = 接收端可见湍流等级估计器（从 CV
统计反估）。需验证 `generate_shared_realization_apsk` 的湍流参数可独立注入（不破坏 shared channel TL-13）。

## 不运行

本轮只记录入口选择。下一对话由用户中转 P04 执行指令；执行前需 freeze 四门 file:line + 判据 + MDE + seed 隔离。
P04-entry-selection-NOT-RUN.md 不计有效包数（entry selection only，per D039 count_excludes: entry_preflight_only）。

---

## REJECTED（2026-07-30 绑定裁决撤回）

本文件上述两个入口（16APSK 环比失配 / 湍流标签失配）经绑定裁决独立审计 **全部 FAIL**，已撤回。
保留 rejected brief 供审计（不计有效 P04）。

### 失效依据（file:line 证据）

1. **γ（环比）是调制格式配置，不是当前信道随机量**：16APSK 环比是发射端星座几何参数
   （`system_model.tex:5` "(8,8)-16APSK ... per Du et al."），随调制格式确定，不随逐 window 信道
   随机变化。不是 receiver-visible random channel quantity。

2. **selector 不读取环比**：冻结选择器 `decide(rx_seg, gamma_db, gamma_lin)`
   （`_a4_switch_common768_30seed.py:97-107`）信息边界经审计干净——只消费 raw-power CV
   （`:102-103`）、nominal γ（`:104,106-107`）、blind power proxy（`:106`）。环比只进入 `per_block`
   内的 `m16apsk_demod`（`:124-139`），即**分支输出 ne_da/ne_nda 的产生**，而 selector 只读分支输出
   错误计数（`main:335-342`）。selector 决策路径上环比是**不可见的**，故"环比失配改变 selector 的
   branch regret"无机制可作用——它改变的是 demod 判决点，这是 matched/configured demod 的显然常规解。

3. **matched/configured demod 是显然常规解**：若接收端环比失配，常规做法 = 用配置/估计的环比 demod
   （标准接收机假设），无需新方法。这违反 problem-bearing 门控（基线已是常规解 = 无问题可作用）。

4. **备选"湍流标签失配"同样不成立**：selector `decide` 不读取 turbulence label（weak/moderate/strong
   是 `main:312` 的循环变量，从不传入 `decide`；论文 `method.tex:75` 明确"turbulence label ...
   are not control inputs"；`abstract.tex:2` "same received-power-driven rule ... without
   turbulence-specific retuning"）。selector 对湍流标签本就无依赖，故"标签失配造成 selector regret"
   无作用面。

5. **合法问题改写**（绑定裁决）：新 P04 = **C_CONTINUOUS_GG_OOD_SELECTOR_ROBUSTNESS**——
   "固定/AWGN 拟合的 CV decision boundary（`cv_awgn_theory(γ)=0.74+0.12exp(-γ/5)` × margin 1.10，
   在 AWGN 下离线拟合）在文献参数范围内、训练未见过的连续 GG 分布（介于 weak/moderate/strong 三锚点
   之间的连续 σ_R²→(α,β)，由 Al-Habash plane-wave mapping `system_model.tex:16-21` 生成）上，
   是否产生 selector-specific regret？" 这是真正可作用的新失效条件（fixed boundary 在训练分布外
   的 GG 形状上评估），不是换名重开 A 族（A 族子轴 SNR-mismatch/cand_rank/region-retune 全关闭，
   但连续 GG 形状失配是独立 mechanism family）。

