# decisions.md — 双偏振 OSL Groundwork 专题

> 架构决策、方向选择、路线失败记录。每条有取代/被取代字段形成血缘链。

## D001: Q-DP1（动态 SOP 跟踪均衡器）No-Go — A0 §1 物理基础不足

> status: active
> date: 2026-07-10
> 取代：无
> 被取代：无
> 依据: 调研: papers/_read_notes/{sat.1553, JLT.2023.3276637, oe.498562, ICSOS.10490279}.md + 子 agent 物理量级核查（TL-27）+ feasibility_report.md Q-DP1 节

### 决策

Q-DP1（M=动态 SOP 跟踪均衡器 C=双偏振星地湍流 A=准静态 SOP 假设致跟踪滞后失效）**No-Go（Kill，有 Pivot 记录）**。

### 核心失败机制（A0 §1 性能间隙致命）

A 假设"动态 SOP 下系数跟踪滞后致偏振解复用失败"在"湍流致 SOP"这个 C 条件下**物理基础不足**：
- 现有均衡器跟踪上限 300 krad/s（DA-LMS+CMA，sat.1553§6 L778）
- 真实星地湍流致 SOP 速率：4 篇精读论文**均无实测数值**；湍流相干时间 >1ms（sat.1553 L167）→ 对应 kHz-几十 krad/s 量级
- 均衡器跟踪上限**高出 1-2 个数量级**，SOP 变化在均衡器跟踪能力范围内
- SOP 快变的真实物理来源是机械振动/热漂移/光终端抖动，**不是湍流**（sat.1553 L563；L-DP5 L176-184）
- sat.1553§6 L745 作者明言"OSL 的 SOP 旋转可能较慢 → MMSE 可行"（MMSE 上限仅 1-10 krad/s，作者认为够用）

这不是用 oracle 上界当 Go 判据（TL-32），是 A0 §1 本职：问题"M 在 C 下因 A 失效"，但 M 在 C 下根本不失效（均衡器够用），A 是错的。

### 否决了什么

- 否决"湍流致动态 SOP 跟踪失效"作为研究方向
- 否决"5 篇共识缝 = 可做方向"的推论——共识缝（全静态建模）真实，但"动态 SOP 致失效"的因果链不成立（静态假设够用）

### 可复用部分

- 物理量级核算方法（均衡器跟踪上限 vs SOP 变化速率对比）可复用于其他"动态性致失效"类假设的 TL-27 核查
- Pivot 出口记录：若 C 改为"机械振动/热漂移致 SOP 快变"（sat.1553 L563 暗示的真实来源），A 可能成立，但①脱离湍流场景设定②已被 L-DP8（JR-CMA pointing jitter）部分占点③振动速率实测数据同样缺失

### 影响范围

- feasibility_report.md Q-DP1 节
- Q-DP1 不进 Contract/MVE
- 3 Q# 优先级排序中 Q-DP1 排末位（No-Go）

### 来源

S002（本轮 Step 4a 评估）+ 子 agent 物理量级核查

---

## D002: Q-DP2（CMA fade 发散分析）Conditional Go — 空白真实但需自建时间模型

> status: active
> date: 2026-07-10
> 取代：无
> 被取代：无
> 依据: 调研: papers/_read_notes/{sat.1553, ACP.11350394, JLT.2023.3276637}.md + feasibility_report.md Q-DP2 节

### 决策

Q-DP2（M=CMA fade 发散分析+鲁棒增强 C=GG 湍流深衰落 A=发散概率未被分析）**Conditional Go**。

### 理由

- A0 通过：空白真实（sat.1553§6 L778 综述**自认**"probability of the equalizer diverging ... has not been analyzed"，领域级共识盲区非 agent 联想）
- 性能间隙方向明确（发散概率确实没人算过），机制有物理论述（sat.1553 L582 + L-DP8 L46）
- 维度 A 结构优势成立：幅度域 PDF → 时间域动力学分析的升级（glossary 判据 2 合法方法产出）
- 维度 B 空白零假设 3 项全反驳
- FR-21 oracle 上界不适用（分析型方向，产出本身就是概率界）

### Conditional 条件（风险）

1. **FR-20 参数溯源缺口**：关键物理参数（深衰落持续时间/频率）全篇缺失，需自建 GG 时间域衰落模型才能算发散概率
2. L-DP8（JR-CMA）已部分占点解决方案，但分析维度正交（L-DP8 是算法增强给静态容差点，Q-DP2 是概率界分析）
3. 发散概率的"几 dB 量级"未知——如果发散是罕见事件，工程价值可能受限

### 排除的替代方案

- 直接做"鲁棒 CMA 算法增强"（跟 L-DP8 撞车）——排除，改为分析型（发散概率界）与 L-DP8 正交

### 影响范围

- feasibility_report.md Q-DP2 节
- 与 Q-DP3 共享 GG 时间模型基建（D003）
- 排 3 Q# 优先级第 2

### 来源

S002

---

## D003: Q-DP3（跨帧 DSP 恢复）Conditional Go — 物理基础最扎实，首选方向

> status: active
> date: 2026-07-10
> 取代：无
> 被取代：无
> 依据: 调研: papers/_read_notes/{ICSOS.10490279, WiSEE.10850117, sat.1553}.md + feasibility_report.md Q-DP3 节

### 决策

Q-DP3（M=跨帧恢复机制 C=帧间湍流衰落 A=深衰落跨帧挂起恢复 open）**Conditional Go，首选方向**。

### 理由

- A0 通过且**物理基础最扎实**：跨帧真实（相干时间 >1ms ≫ 帧时长 1-74µs，差 13-1000 倍）+ 挂起真实（L-DP5 "hang-up" + L-DP6 BER>0.44 outage 实证）+ 恢复 open（L-DP5 L766-771 自承认"requires further work"）——三点文献直接支撑
- A' 竞争维度分解：Q-DP3 竞争的"深衰落恢复"维度**先验覆盖度最低**（最安全）
- 维度 A 结构优势成立：被动冻结（sat.1553 L582）→ 主动恢复（fade 检测 + 跨帧状态管理 + 快速重锁定）
- 维度 B 空白零假设 3 项全反驳
- FR-21 oracle 上界不触发 Kill（outage 从 ~50% 降到接近 0 = 量级改善远 >0.5dB 等效）

### Conditional 条件（风险）

1. L-DP5/L-DP6 的跨帧结论部分是**预期性论述**（L-DP5 湍流未显式仿真，L176-184 + L766-771 是预期分析非实测）
2. 衰落持续时间未量化（与 Q-DP2 同缺口，但 Q-DP3 对该参数依赖较弱）
3. 恢复机制的"几 dB 量级"需 MVE 验证——赢 L-DP5 被动冻结几个 dB 则 Go 成立

### 排除的替代方案

- "交织+FEC 解决跨帧"（空白零假设 a）——排除，交织治比特错误，DSP 挂起是环路锁定丢失，不同层
- "纯工程优化无理论贡献"（空白零假设 c）——排除，可产出设计准则（fade 阈值 vs 恢复时间 vs outage 权衡曲线）

### 影响范围

- feasibility_report.md Q-DP3 节
- 排 3 Q# 优先级第 1（首选 Conditional Go）
- 与 Q-DP2 共享 GG 时间模型基建
- 下一步：进维度 D MVE 验证恢复机制有效性（需先补衰落时域参数 FR-20）

### 来源

S002

---

## D004: 攒材料优先策略 — 推迟所有 MVE，全候选深精读

> status: active
> date: 2026-07-10
> 取代：无（不取代 D001-D003，是节奏调整：D002/D003 的"进 MVE"时点推迟）
> 被取代：无
> 依据: 用户原话（S003）"咱们不着急进任何一个，咱们先把它们都推到mve前，大量精读。为我们攒材料。这样后续才好办？" + profile（多挑候选保留余地 [durable] + 警惕急于推进 [durable]）+ TL-30（5 次殊途同归根因含精读不够厚）+ FR-22（精读硬门控）

### 决策

推迟所有 viable 候选进维度 D MVE。改为对全部候选先做 GW Step 3 深精读，攒够材料后再统一评估。

### 触发原话

> 触发原话: 用户（S003）"咱们不着急进任何一个，咱们先把它们都推到mve前，大量精读。为我们攒材料。这样后续才好办？"

（已登记 voice.md）

### 理由

1. **呼应用户稳定画像**——profile 两条 durable：①倾向多挑候选保留余地 ②警惕急于推进。攒材料策略同时满足这两条
2. **守 FR-22**——精读是硬门控。之前 5 次殊途同归根因之一是精读不够厚就急着试（TL-30）
3. **本轮新开 ML 方向 3 个空白点（R002）需要材料**——ML 衰落预测喂 DSP / ML 载波恢复湍流 / ML 均衡湍流，这 3 点在湍流场景几乎全空白，精读前连过四判据都不确定
4. **不急于收敛**——当前 Q-DP2/Q-DP3 已 Conditional Go 但各有风险（FR-20 缺口/预期性论述），ML 方向未立 Q#。与其逐个急着进 MVE，不如攒齐材料统一看全貌再排

### 不推翻 D001-D003

- D001（Q-DP1 Kill）：不动，物理结论不变
- D002（Q-DP2 Conditional Go）：决策本身不动，但"下一步进 MVE"时点推迟到精读材料攒够后
- D003（Q-DP3 Conditional Go 首选）：同上，首选地位和物理基础不变，进 MVE 时点推迟

### 候选池（精读对象）

| 候选 | 来源 | 状态 | 精读材料缺口 |
|---|---|---|---|
| Q-DP2（CMA fade 发散） | S001/S002 | Conditional Go，已有结构化提取 | 补深精读，攒发散机制材料 |
| Q-DP3（跨帧恢复） | S001/S002 | Conditional Go 首选 | 补深精读，攒跨帧/恢复材料 |
| ML 衰落预测→喂 DSP | R002 空白点 A | 未立 Q# | 精读 Nguyen2022/Li2023/Islam2025/Lapsiwala2025，判是否过四判据 |
| ML 载波恢复湍流 | R002 空白点 B | 未立 Q# | 精读 Hu2025/Blatter2025，判湍流场景是否成立 |
| ML 均衡湍流 | R002 空白点 C | 未立 Q# | 精读 Qin2025/Qin2026/Nasr2026，判 vs CMA 有无深衰落优势 |

### 影响范围

- 修改 topic-index 当前位置段（从"交用户确认进 MVE"改为"攒材料精读阶段"）
- 下一步工作方式变更：批量精读替代逐个 MVE
- D003 的"下一步：进维度 D MVE"改为"先精读，MVE 时点待材料攒够后定"

### 来源

S003 + 用户原话

---

## D005: 候选合并 — Q-DP2 + Q-ML1 → Q-CMA-FADE（CMA 深衰落发散：分析+ML缓解合一）

> status: active
> date: 2026-07-11
> 取代：部分合并 D002（Q-DP2 分析层并为本方向第 1 层）+ Q-ML1（方法层并为本方向第 2 层）。D002/Q-ML1 不标 superseded（各自仍可独立追溯），但优先按合并后 Q-CMA-FADE 推进
> 被取代：无
> 依据: 20 篇精读（papers/_read_notes/ L-ML5/6/14 Qin/Nasr + sat.1553§6 自认 + L-DP8 实证）+ 用户"和别人接近才好"偏好（voice.md）+ profile D005 务实路线

### 决策

Q-DP2（CMA fade 发散，分析型）+ Q-ML1（ML 均衡缓解发散，方法型）合为一条故事线 **Q-CMA-FADE**：传统 CMA 在星地 GG 深衰落下发散，产出两层贡献（发散概率界分析 + ML 均衡缓解方法）。

### 触发原话

> 触发原话: 用户（S003 讨论续）"和别人接近才好吧？"

（已登记 voice.md）——明确偏好"有竞品对标的成熟方向"而非"完全没人做"。

### 合并理由

1. **同一物理问题**：Q-DP2 和 Q-ML1 的 M-C-A 核心一致（CMA 在深 fade 发散），只是产出角度不同（分析 vs 方法）。精读 20 篇后确认两者指向同一个 sat.1553 自认空白
2. **分析+方法合一更强**：单做 Q-DP2（只分析发散）工程价值受疑（发散是罕见事件？）；单做 Q-ML1（只换均衡器）撞 Qin/Nasr 换皮。合一后"解释为什么发散 + ML 怎么缓解"是完整故事
3. **增量定位清晰**：补 Qin/Nasr 实验缺口（真实 GG 深衰落 + 发散机制），不是照搬 VAE 换场景（见 literature_notes 增量定位表）
4. **呼应用户偏好**：有活跃竞品（Qin/Nasr）= 方向被认可 + 基建现成 + 形态可发表，符合 D005 务实路线

### 增量定位（不换皮）

- Qin/Nasr 已做：单一中强湍流强度 r0=0.4mm 固定 + 报 BER/收敛速度现象
- 我们补：真实 GG 深衰落完整建模 + 发散概率 vs 衰落深度扫描 + 发散机制解释（sat.1553 自认空白）
- 不是：照搬 VAE 换场景（TL-12/D006 换皮红线）

### 四判据（全过，最强）

详见 literature_notes Q-CMA-FADE 表。

### 风险

1. GG 时间域衰落模型需自建（FR-20，继承 Q-DP2）
2. 与 Qin 小组抢位——增量定位必须扎实
3. "几 dB 量级"需 MVE 验证

### 不合并的候选（保持独立）

- Q-DP3（跨帧恢复）：纯 DSP，ML 接不进来（尺度断），独立保留为备选
- Q-ML4（双频分离）：种子，等 Q-CMA-FADE 定了再看
- Q-ML2/Q-ML3：部分过，暂搁置

### 影响范围

- literature_notes 新增 Q-CMA-FADE 合并章节
- 候选池从 5 个收缩为：**Q-CMA-FADE（首选）> Q-DP3（备选）> Q-ML4（种子）**
- 仍守 D004：不立即进 MVE，等用户确认合并 + 排序后再进 Step 4a

### 来源

S003（20 篇精读后候选合并讨论）+ 用户"和别人接近才好"偏好

---

## D006: Step B 发散概率扫描结果 — 发散由 μ 主导，补 sat.1553 空白，Q-CMA-FADE 分析层 PASS

> status: active
> date: 2026-07-11
> 取代：部分更新 D002 Conditional 条件 1（FR-20 缺口已在 Step A 补全 + 发散概率已量化）
> 被取代：无
> 依据: 验证: results/cma-fade-divergence/cma_divergence_scan_results.json (384 trials, 128 combos) + TL-20 理论预期 + TL-22 物理前提检查 + sat.1553§6.3 L778 空白

### 决策

Q-CMA-FADE Step B（CMA 发散概率扫描，分析层）**PASS**。sat.1553 §6.3 L778 自认的"probability of the equalizer diverging ... has not been analyzed"空白已补全——量化了发散概率 vs {μ, f_G, tap, 湍流强度} 的关系，给出发散条件判据。

### 核心发现

1. **发散概率由步长 μ 主导**（TL-20 理论预期验证）：
   - μ ≤ 1e-3 → P_div ≈ 0（61/128 组合零发散）
   - μ = 5e-3 → P_div 0~1.0（临界区）
   - μ ≥ 1e-2 → P_div ≥ 0.67（危险区）

2. **f_G（衰落频率）是第二驱动**：f_G=1000Hz → P_div 最高（衰落事件更频繁 → 发散机会更多）

3. **湍流深度影响弱**（TL-22 物理前提检查通过）：深衰落 h→0 时 r≈n，梯度 ∇w=μ·R²·n* 与 h 深度无关。P_div=1.0 组合计数 weak=8/moderate=5/strong=7/uplink_strong=6 不单调

4. **tap 数**：22 tap 比 11 tap 略易发散（更多自由度 → 漂移更快）

### 发散条件判据（补 sat.1553 空白）

- **安全区**（P_div≈0）：μ ≤ 1e-3
- **临界区**（P_div 0~1）：μ ≈ 5e-3，取决于 f_G/tap
- **危险区**（P_div≥0.67）：μ ≥ 1e-2 且 f_G ≥ 100 Hz

### 对 Q-CMA-FADE 方向的影响

- **分析层 PASS**：sat.1553 空白已补全，发散概率+条件判据可写入论文
- **Step C 测试场景确定**：用 μ≥5e-3, f_G≥100Hz 的发散条件作为 ML vs CMA 对比场景
- **增量定位微调**：发散条件判据应表述为 (μ, f_G, tap) 组合而非"湍流越强发散越多"——这更精确且更实用
- **D002 Conditional 条件 1 更新**：FR-20 缺口已在 Step A 补全 + 发散概率已量化，Conditional 风险 1 已解除

### 触发原话

> 触发原话: 无（技术推导，PROMPT-004 执行）

### 来源

S005（Step B 执行）

---

## D007: Step C ML vs CMA MVE 结果 — ML 零发散 vs CMA 高发散, Q-CMA-FADE 方法层 PASS, Go 判定

> status: active
> date: 2026-07-11
> 取代：部分更新 D005（Q-CMA-FADE 方法层 MVE PASS, 两层贡献完整）
> 被取代：无
> 依据: 验证: results/cma-fade-divergence/mve_cma_vs_ml_results.json (5 场景 × 5 trials = 25 runs, 三方对照 CMA/ML/oracle) + TL-20 理论预期 + C6-C8 自检 + Freire 2022 6 陷阱 checklist

### 决策

Q-CMA-FADE Step C（ML vs CMA MVE, 方法层）**PASS — Go**。ML 均衡器在 CMA 发散条件（危险区 μ≥1e-2, f_G≥100Hz）下零发散（P_div=0.0），而 CMA P_div=0.40-0.60。ML BER 接近 oracle 下界，远好于 CMA。

### 核心发现

1. **ML 零发散 vs CMA 高发散（TL-20 理论预期验证 PASS）**:
   - 危险区 (μ=1e-2, f_G=1000Hz): CMA P_div=0.40-0.60, **ML P_div=0.00**
   - 临界区 (μ=5e-3, f_G=300Hz): CMA P_div=0.20, **ML P_div=0.00**
   - 安全区 (μ=1e-3, f_G=30Hz): CMA P_div=0.00, ML P_div=0.00（简单情况, 非同族性警报）

2. **ML BER 接近 oracle 下界**:
   - 危险区: ML BER (0.007/0.0006) ≈ oracle BER (0.006/0.0003), CMA BER (0.087/0.039) 差 10×
   - 临界 300Hz: ML BER (0.001) ≈ oracle (0.0009), CMA BER (0.017) 差 17×

3. **C8 祖师爷警报: 未触发**:
   - 安全区 ML≈CMA→ 预期（安全区是"简单情况"）
   - 危险区 ML >> CMA → 差异显著, 无数学同族性

4. **发散机制解释（补 sat.1553 §6.3 L778 空白的方法层）**:
   - CMA 逐块梯度更新: 深衰落 h→0 时 r≈n, 梯度 ∇w=μ·R²·n* 噪声驱动 → 系数随机游走 → 漂移超阈值 → 不可恢复
   - ML batch 梯度下降: 梯度对整个 batch 平均 → 单个深衰落样本噪声被 batch 稀释 → 漂移 ∝ μ·σ_n/√B 远小于 CMA
   - ML 前馈推理（权重固定）不在线更新 → 不会"发散"

### Go 判定依据

- ✅ **FR-14 先验对照**: ML P_div (0.0) << CMA P_div (0.6) 在危险区
- ✅ **FR-15 贡献目标 baseline 对照**: ML BER ≈ oracle BER, 不劣于 CMA 安全区
- ✅ **C8 未触发**: 无数学同族性
- ✅ **TL-20 理论预期验证**: ML 稳定性符合预测（batch 梯度平滑噪声）
- ✅ **C6 公式溯源**: CNN 蝶形结构标 Qin 2025 L275/283, MSE 损失恋标 Freire 2022
- ✅ **C7 三方对照**: CMA / ML / oracle MMSE 全含
- ✅ **Freire 6 陷阱**: MTRS/batch≥1024/MSE/分离/BER/RMpS 全守

### 增量定位（不换皮, 守 D005/D006）

- **Qin 已做**: VAEMR vs CMA 收敛速度 200× + 5dB 功率预算（单一中强湍流 r₀=0.4mm）
- **我们补**: 发散概率界 + 发散条件判据 + ML 在发散条件下的鲁棒性对比（新测度: P_div + 恢复时间）
- **不做**: 收敛速度对比（Qin 已做过）
- **不照搬**: VAE ELBO 损失（用 MSE 监督, 结构标 Qin 来源）

### SOP 速率修正

Step B 用 SOP_RATE=1e-4 rad/sym（250 krad/s），Step C 修正为 4e-7 rad/sym（1 krad/s, sat.1553 §6.3 真实 OSL 速率）。验证：真实 SOP 下 CMA 发散仍由 μ 驱动（与 Step B 结论一致, SOP 速率不改变发散机制）。Step B 的发散条件判据（μ, f_G, tap）仍然有效。

### 对 Q-CMA-FADE 方向的影响

- **方法层 PASS**: ML 在发散条件下保持稳定, 补 Qin/Nasr 实验缺口
- **两层贡献完整**: 分析层（Step A+B）+ 方法层（Step C）全 PASS
- **Q-CMA-FADE 方向确认**: Go, 可进 Contract/Execute
- **D005 更新**: Q-CMA-FADE 从"首选候选"升级为"方向确认"

### 触发原话

> 触发原话: 无（技术推导，PROMPT-005 执行）

### 来源

S006（Step C 执行）
