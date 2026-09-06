# Task Brief: Ch4 完整论文草稿与章级证据包更新

> **状态：PAUSED_NOT_EXECUTED（D072）**。用户明确要求先准备材料、以后自行组织正文；本任务不得执行，除非用户再次明确恢复。

> 来源: S028 / D071 / V046 / T092 | 产出: 可直接进入硕士论文的完整第四章草稿及更新后的章级证据包
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 33
  action_class: CH4_FULL_CHAPTER_DRAFTING
  mission_checkpoint: CP033
```
<!-- RDL-TASK-CONTROL:END -->

## 启动前门

即使 T092 独立图表审查 P0/P1=0，本任务也保持暂停；只有用户再次明确要求写完整正文时才可另行解冻。

## 唯一任务

以 formal 图表/表格和 immutable canonical evidence 为唯一数字源，重建旧四格 confirmation 写作包，完成一章从问题、模型、方法推导、算法、公平比较、验证设计、正式结果、机理、边界到小结均闭合的中文硕士论文第四章草稿。目标是“可以开始排入论文”，不是内部蓝图或任务报告。

## 读者、用途与章名

- 读者：导师、硕士论文盲审评阅人、答辩委员。
- 用途：正式论文第四章初稿；可直接移植到学校模板后继续润色。
- 推荐章名：**第四章 面向星地双偏振相干链路的结构约束短导频解复用方法**。
- 唯一方法身份：**结构约束方向—尺度解耦短导频偏振解复用方法族**。前向信道投影尺度是无调参主变体，导频重构尺度是同族强变体/消融；不得拆成两个创新点。

## 必须写出的故事

短导频下无约束 `2×2` 复信道 LS 估计保留目标 `H=gQ` 模型外的噪声自由度，估计误差经矩阵求逆传播到双偏振解复用；本章先从 LS 的 SVD 中提取共同酉方向，再用前向信道 Frobenius 投影或导频重构误差分别确定尺度，形成完全 receiver-visible 的输入—动作—输出链；在共同 DP-(8,8)-16APSK 星地相干平台上，相对独立开发集调参的奇异值下限基线，完整 BER–SNR 曲线和门限信噪比表明优势主要集中于极短导频区，并由 matched inverse residual、导频规律及结构失配扫描限定适用边界。

## 章节结构

完整撰写以下 4.1–4.7，正文建议 9,000–13,000 个中文字符（不含表格/公式/内部证据附录），结果节约占三分之一：

1. `4.1 引言`：星地双偏振接收需求→短导频问题→结构约束思路→本章工作与组织。
2. `4.2 系统模型与问题描述`：真实物理处理顺序、`Yp=HXp+Np`、`H=gQ`、8 实自由度 vs 5 实自由度、局部逆扰动、适用 slice。
3. `4.3 结构约束方向—尺度解耦方法`：LS/SVD共同方向、前向信道准则闭式解、导频重构准则闭式解、统一输出、`rho` 诊断、作用机理。
4. `4.4 算法流程、比较方法与复杂度`：完整伪代码、fail-closed、公平对手、独立调参、truth firewall、状态生命周期、解析复杂度。
5. `4.5 验证设置与统计方法`：平台、三档 Gamma–Gamma、SNR/Np/128 paired latents、BER、required SNR、whole-curve bootstrap、mismatch 构造。
6. `4.6 结果与讨论`：完整曲线→门限增益/导频效率→inverse residual机理→scene与mismatch边界→综合讨论。固定顺序“现象—公平比较—解释—边界”。
7. `4.7 适用范围与本章小结`：先列已验证/敏感性/未验证，再用三段总结问题、方法、证据和有限贡献。

## 核心公式

至少准确包含并解释：

```text
H_LS = Yp Xp^H (Xp Xp^H)^(-1) = U diag(s1,s2) V^H
Q_hat = U V^H
g_F = (s1+s2)/2
W_F = 2 Q_hat^H / (s1+s2)
Zp = W_tau=1 Yp
a_hat = max(0, Re<Zp,Xp> / ||Zp||_F^2)
W_P = a_hat W_tau=1
z = W y
rho = s1/s2
s_i_tilde = max(s_i, tau s1)
W_SVF = V diag(1/s_i_tilde) U^H
gain = SNR_req(baseline) - SNR_req(method)
```

结构失配只写为无量纲偏离：

```text
D_delta = diag(1+delta,1-delta) / sqrt(1+delta^2)
```

不得把 `delta` 翻译成 PDL dB。

## 必须使用的 formal 事实

- DP-(8,8)-16APSK；每偏振 4096 个载荷符号、每 method/cell/latent 32768 bits；128 paired latents。
- SNR=`5:2:41 dB`；moderate Np=`2/4/8/16`；weak/strong Np=`2`。
- 工程参考为解复用后、Ch3 CPR 前、未编码 pre-FEC BER=`3.8e-3`，不是 post-FEC 门限。
- 前向信道主变体 vs 调参强基线：Np2 required-SNR gain `0.870474 dB`，95% CI `[0.618162,1.088274] dB`；Np4 `0.120949 dB`，CI `[0.018893,0.239227] dB`。
- 导频重构变体 vs 调参强基线：Np2 `0.874731 dB`，CI `[0.628859,1.078428] dB`；Np4 `0.108033 dB`，CI `[0.025752,0.202565] dB`。
- 正文按约 `0.87 dB [0.62,1.09]`、`0.12 dB [0.02,0.24]` 等合理精度报告；精确数字保留在表。
- B2_TUNED 的 moderate/Np2 `tau=0.5`，其余 formal scene×Np 为 `tau=1.0`；来自不重叠 development set。
- 四项 crossing STABLE；5000/5000 whole-curve bootstrap valid。
- Np4 必须称统计稳定的小幅优势；C4/B3 性能接近必须正面披露。

## 跨章接口硬边界

- 物理接收顺序写成“Ch4 双偏振解复用→两路后续载波相位恢复→解调/译码”。章号表示从单支路算法到双偏振系统的研究复杂度递进，不代表 DSP runtime 顺序。
- Ch4 的 `W≈Q^H/g` 会归一化 Gamma–Gamma 公共幅度，而已录用 Ch3 selector 使用原始接收功率构造 effective-SNR gate；现有证据不支持“Ch4 与 Ch3 方法已无条件串接并联合验证”。
- 正文必须明确：两章在各自受控 slice 独立验证；Ch3 采用给定/理想解复用后的单支路模型；Ch4 只定义向后续每支路载波恢复的模块化接口。不得声称端到端联调或编码链闭合。

## 图表

- 使用 T092 已核验的四组 formal 结果图和三张表。
- 更新 `generate_method_figure.py`、`method-figure-semantic-brief.md` 与 `figures/ch4-method-flow.{svg,png}`：真实物理顺序；共同 `Q_hat` 方向支路；前向信道/导频重构两尺度准则；主方法输出；后续每支路载波恢复接口；不得暗示联合仿真。
- 全章目标五图三表：方法流程 1 图 + T092 正式结果 4 图；配置、headline、方法角色 3 表。
- 每张图 caption 必须能独立说明场景、统计口径、比较对象和边界；不出现内部代码名。

## 写作包更新

写入/更新 `projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/`：

1. 新建 `chapter-draft.md`：完整论文正文。
2. 重写 `chapter-blueprint.md`：formal 4.1–4.7 逐节蓝图与证据指针。
3. 重写 `fact-matrix.md`：以 canonical formal raw/aggregate/V046/T092 为当前事实；旧 confirmation 只列历史，不得承重。
4. 扩展 `algorithm-box.md`：共同方向、两尺度准则、B2 strong baseline、完整伪代码与复杂度。
5. 重写 `claim-and-citation-ledger.md`：formal claim、必须披露、禁止、已有本地引用指针。
6. 新建 `thesis-spine-integration-notes.md`：说明现有 `thesis-framework.md` 的 QPSK/Ch3信道估计/Ch4载波同步/Ch5 FPGA 是整体陈旧框架，列出日后统一改总纲的具体传播点；本任务不局部修改该总纲。
7. 新建 `chapter-writing-verification.md`：逐图/表/数字/公式/citation/interface/claim 的 QA 记录。
8. 更新 `README.md` 为 formal chapter draft 状态和导航。

## 引用规则

- 不检索、不下载新文献。只使用仓库现有全文、read notes、citation ledger 与 bibliography。
- 对 Roudas/Kikuchi/Schönemann/Higham 等已有本地证据，核对本地 `content.md/meta.json` 后再写精确支持范围；若 bib key 不存在，可在 `projects/thesis-fso/references.bib` 追加已由本地 authority 完整确认的条目，但不得猜页码/DOI/结论。
- 经典原子只支撑背景与数学来源；本章贡献定位为目标场景中的完整方法迁移和 receiver recipe，不声称首创原子。

## 外部语言

正文和图表不得出现 C4/B3/B2/O1 代码、D/T/CP、Grade、P0/P1、SHA、manifest、gate、arm、canonical、formal 等内部项目词。可以使用“预先冻结”“独立开发集”“配对随机实现”“独立复核”等学术表达。

## 禁止

- 不运行任何仿真、reducer、bootstrap，不改 simulation/raw/aggregate/receipt/manifest/lock。
- 不用旧 14/18 dB 四格 confirmation 作为正式结果，不保留“B2统一tau=1/全局只差scale”的陈旧表述。
- 不隐藏导频重构变体，不将其拆成第二贡献；不声称主变体胜过该变体。
- 不声称 first/SOTA/新SVD/新Procrustes/任意偏振信道/PDL-PMD-FIR-时变SOP/CPR联合/LDPC验证。
- 不修改 Skill/controller，不恢复 Ch5，不重写整篇 `thesis-framework.md` 或 Word 正文。

## 验证与回报

1. 所有正文数字与 T092 CSV/table/V046 一致；所有图表引用存在；Markdown 链接无断裂。
2. grep 确认正文无内部术语、旧 confirmation headline、统一 tau=1 或端到端已验证声称。
3. 公式与 `production_core.py`/`scaled_unitary.py` 逐项一致；B3 channel NMSE 不用于校准后机理。
4. 独立 reviewer 检查：方法身份、数学、数字、图文、引用、跨章接口、claim ceiling与硕士论文专业外观。
5. 返回文件清单、正文字符数、图表清单、关键数字、P0/P1/P2 与 terminal。成功 terminal=`CH4_COMPLETE_CHAPTER_DRAFT_READY`；否则 `CH4_COMPLETE_CHAPTER_DRAFT_INVALID`。
