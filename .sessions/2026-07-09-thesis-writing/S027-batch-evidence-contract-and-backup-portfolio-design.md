# [S027] 统一批次证据合同与后备方法池设计

> 2026-08-30 | 战略讨论 / paper-writing PROPOSE | IN PROGRESS

## 目标

在不执行、不检索、不补 Groundwork 的前提下，冻结用户已经批准的统一批次证据合同，并为当前 Ch4/Ch5 暂定方法预建设计态后备池，回答“两个都不行时接下来试什么”，避免失败后临时乱找。

## 记录

### 一、已批准的证据顺序

用户批准的未来证据顺序为：

`可执行正确性门 → 冻结开发矩阵 → 自动 A/B/C/D/F 分级 → 胜者 fresh-seed confirmation`

- 首要目标是 BER/FER 明确优于正确经典 baseline。
- 只有 A 级性能路线耗尽后，才允许按预定义标准降到 B/C；不能看完数字再换主指标。
- 开发矩阵只给 `PROVISIONAL` 等级；方法冻结并通过 fresh-seed confirmation 后才给 `FINAL` 等级，避免“先宣布 A、再决定是否确认”的时序循环。
- Ch4 与 Ch5 先做单轴矩阵，最后只对各自前二名做最多四个桥接组合，避免全笛卡尔积。
- 本合同已登记为 D041，但仍没有执行授权。

### 二、机制独立性的判据

只有至少改变以下一项，才单列方法卡：receiver-visible 信息、动作处理点、输出/控制对象、目标失效机制、决定性消融/公平 comparator 或贡献类型。若输入—动作—输出、因果假设、主图和消融相同，只改正则系数、阈值、窗长、阶数、步长或相似权重公式，则只算同一方法族的开发参数。

### 三、第一版 13 张设计态方法图谱

#### Ch4：双偏振估计/均衡五族（1 主 + 4 备）

| 顺序 | 方法卡 | receiver-visible 输入 → 动作 → 输出 | 直接 baseline | 纸面判断与主要风险 |
|---|---|---|---|---|
| C4-0 主种子 | 时序正则化分布式导频 Butterfly-LS | pilots、上一块 taps、pilot innovation → 带时间项的 2×2 FIR 求解 → taps、均衡符号、残差 | 逐块独立 complex LS；固定 EMA/RLS 为廉价对手 | 时间轴清楚但未必最强；SOP 太慢或 EMA 已足够会吸收 |
| C4-1 第一后备 | scaled-unitary 物理约束 Jones-LS | pilots → LS Jones → 极分解/SVD 投影为共同幅度 × 近酉偏振旋转 → 低方差逆矩阵 | 无约束 LS | 最稳妥的硕士级结构迁移；真实 PDL/PMD 或前端失配过强会破坏约束 |
| C4-2 第二后备 | APSK 环感知半盲 Butterfly refinement | pilot-LS 初值、内外环半径、payload 软可靠度 → 高可靠样本的 ring-aware multi-modulus/DD 更新 → refined taps | pilot-only LS、标准 CMA/调好 MMA | 最可能利用新 APSK 平台产生 BER 差异；环误判会错误传播，调好 MMA 可能吸收 |
| C4-3 第三后备 | 共享支撑稀疏 Butterfly FIR | pilot regression → 四个复 FIR 的 group-sparse/共同支撑估计 → 稀疏 taps | dense 11-tap LS；正确短 FIR | 低 pilot 下可降方差；真实响应稠密或短 FIR 已够则无增益 |
| C4-4 条件后备 | pilot 残差驱动 robust IRLS | pilot residual、接收功率、残差尺度 → Huber/Tukey 重加权 → robust taps、异常度 | 普通 LS；固定门限删 pilot | 只有确有重尾/异常 pilot 才开放；纯 AWGN+块级 GG 下可能没有问题 |

说明：Kalman/RLS 与 C4-0 同属时间跟踪轴，不另虚算一个方法族；频域均衡只有平台真实含长记忆/频率选择性时才允许作为研究对象扩展；decoder 软符号重均衡归入跨层储备。

#### Ch5：软解调/译码六族（1 主 + 5 备）

| 顺序 | 方法卡 | receiver-visible 输入 → 动作 → 输出 | 直接 baseline | 纸面判断与主要风险 |
|---|---|---|---|---|
| C5-0 主种子 | 均衡残差可靠性感知 LLR 校准 | Ch4 residual/reliability → 校准已生成 LLR → calibrated LLR、decoded bits | 未校准 max-log LLR | 便宜但不能把多个缩放/clip 系数包装成多种方法；旧固定 NOMS 小效应不外推 |
| C5-1 第一后备 | APSK 径向—切向几何软解调 | 均衡符号、pilot 残差、APSK 环结构 → 分环/偏振估协方差，以 Mahalanobis 距离直接生成 bit LLR | 单一 `σ²` 的各向同性 max-log demapper | 改变似然几何而非整体缩放，最有希望明确改善 BER/FER；若残差近圆对称则停止 |
| C5-2 第二后备 | syndrome 引导最不可靠位救援 | 首轮失败码字、syndrome、posterior LLR、校验矩阵 → 小候选翻转/重初始化并短重译码 → rescued codeword | 固定 NOMS；等成本多迭代/restart | 在 waterfall 附近可能明显降 FER；大范围深衰落或普通多迭代完全吸收时停止 |
| C5-3 第三后备 | 收敛感知两阶段 NOMS | 初始 LLR、逐轮 syndrome weight、hard-decision change/LLR growth → 在两组预冻 `alpha/offset/clip` 间切换 → decoded bits、轨迹 | 独立调好的最佳固定 NOMS | 作用于译码内部、与前端校准独立；若 syndrome 轨迹不能预测切换或固定 NOMS 全吸收则停止 |
| C5-4 第四后备 | 不确定码字选择性 BICM-ID | 均衡样本、decoder extrinsic、uncertainty/syndrome gate → 仅困难码字做一次 prior-aware APP remap+decode → refined LLR/bits | 单次 BICM；等总预算全量 BICM-ID | BER/FER 潜力中高、章节外形完整，但基础设施成本高且经典邻居强 |
| C5-5 工程后备 | 可靠性优先更新与码字级预算分配 | bit-channel LLR、未满足校验、syndrome slope → 调整 layer/check 顺序与迭代预算 → bits、迭代数、时延 | 固定 layer order/固定迭代；标准 early stop | 主卖点偏相同 FER 下的复杂度/时延；适合 B/C 级兜底，不应预期大 BER 差距 |

局部 LLR 擦除/clip 归入 C5-0 的同族备选，除非它改变了明确的选择性支持集且需要不同决定性消融；否则不单列方法。

#### 跨层高风险储备（仅单章池耗尽后开放）

| 顺序 | 方法卡 | 输入 → 动作 → 输出 | 开放前提 |
|---|---|---|---|
| X-1 | decoder 软符号一次重均衡/残差抵消 | extrinsic soft symbols、Ch4 taps/residual → 一次受限 soft-DD/EM 或 residual cross-pol cancellation → re-demap/re-decode | Ch4 后确有 receiver-visible、可恢复的残余串扰/相位 headroom；hard-DD 廉价对手不能完全吸收 |
| X-2 | decoder 指标有限假设消歧 | 自然出现的 residual phase/polarization hypotheses、syndrome/接收 metric → 有限分支译码选择 → codeword | 新平台先证明确有自然 slip/ambiguity 与可恢复空间；旧 coded decoder-feedback C1 的科学失败不能被忽略或原样复活 |

### 四、暂定解锁顺序

1. 第一批只开放六张：Ch4 的 `C4-0/C4-1/C4-2`，Ch5 的 `C5-0/C5-1/C5-2`。它们分别覆盖时间、空间物理、星座统计，以及软度量、解调几何、失败后救援。
2. 第一次战略结算后，只给没有 A/B 的章节开放 `C4-3/C4-4` 或 `C5-3/C5-4/C5-5`；已经锁定胜者的章节不再扩大。
3. 每章 5–6 个机制族耗尽仍无 B，停止在该处理点继续加小变体，回战略层讨论增加真实 testbed 自由度、更换研究对象或调整论文结构。
4. 只有单章池耗尽且存在自然可恢复 headroom，才允许开放 X-1/X-2；两个跨层储备仍无 A/B 后，局部 DSP 方法搜索正式结束。

### 五、组合与时间边界

- 设计地图约 13 张，但首轮最多六张；“一大堆”是预先有路，不是同时把所有路跑一遍。
- 未来若获批执行，Ch4 候选统一接冻结的经典 demapper/decoder，Ch5 候选统一接冻结的经典 Ch4 equalizer；只让前二名做最多四个桥接组合。
- 同一方法族连续两个构造都没有 A/B 信号，关闭整个机制轴，不调第三个近邻公式。
- 第 9 周后禁止新增候选；第 10–11 周留给 fresh confirmation，第 12 周冻结证据和章节身份。

### 六、当前判断

当前两个暂定方法有资格留在第一批，但没有资格被默认成成功率最高的最终 Ch4/Ch5。Ch4 纸面上最值得与当前种子并列的是 scaled-unitary 约束 LS 和 APSK 环感知半盲 refinement；Ch5 最值得并列的是 APSK 几何软解调和 syndrome 引导失败码字救援。它们的动作点彼此不同，也与 Ch3 的功率驱动 CPR selector 保持较好的技术对象独立性。

所有方法卡目前都只是 `DESIGN_ONLY / TENTATIVE`：未检索 exact collision，未做 Groundwork，未验证增益，不得写成已经提出、可行或优于 baseline。

本表只是首版机制地图，不是字段齐全的冻结方法卡。若用户批准继续设计，每张卡还必须在任何执行授权前补齐决定性消融、预期 `PROVISIONAL/FINAL` 等级判据和逐卡停止条件；X-1/X-2 还须补直接 baseline 与成本口径。

## 决策引用

- D040：共同平台锁为 DP-(8,8)-16APSK+BICM/LDPC。
- D041：四段式证据合同（新建）。
- D042：只开放设计态机制级后备池（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：否，触及了原“不开新候选”的明确排除项；用户于 2026-08-30 明确要求为当前两个方法预建大批后备选项，已按 D042 记录仅限设计地图的 scope change。未检索、未实验、未补 Groundwork、未实现、未修改 Skill/controller/仿真代码/论文正文，也未派执行任务。

## 后续

等待用户审阅 13 张方法卡、第一批六张和分层停机规则。用户明确批准完整设计前不冻结具体方法身份；用户未另行授权执行前，不运行任何 smoke、开发矩阵或 confirmation。
