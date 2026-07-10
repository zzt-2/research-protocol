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
