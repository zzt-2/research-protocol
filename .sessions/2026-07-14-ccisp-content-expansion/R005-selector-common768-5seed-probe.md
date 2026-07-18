# [R005] selector common-768 公平口径 5seed 探索——前因后果 + 数字

> 2026-07-15 | 关联：R004 / D005(写作专题) / D008 / D009 | 阶段：只读验证 + 探索性 5seed
> 任务：验证 R004 揪出的 Fig.5 口径问题在公平 common-768 口径下 selector 真实增益是多少

## 调研问题

R004（本专题，2026-07-15）审计出 Fig.5（selector BER reduction 2.3/2.0/1.3 dB）用的是 mixed 口径（selector 选 DA 时错误计数在 768 解码位上累加、选 NDA 时在 1024 全部位上累加、两边都除 1024 但比值约掉），实际是 branch-dependent error-count ratio 不是公平 BER。R004 给了病态退化证明：即使 selector 毫无本事，只要选了 DA 窗也会机械白送最多 1.249 dB。

主控（本对话）基于 R004 + 现有 data-BER 口径旁推："公平 common-768 口径下 selector 增益大概率从 2.3/2.0/1.3 缩水到 0.1–0.7 dB"。用户拍板"开新对话跑 5seed 看情况，别推断"。

本 R005 记录：(1) 这件事的完整前因后果（为什么反复拉扯这么久）；(2) 5seed × 9点验证结果；(3) 数字对删图/保图决策的影响。

---

## 第一部分：完整前因后果（"当时咋想的" + "为啥稍微改就差那么多"）

### 时间线（同一根问题被审了三次，每次只审一半）

| 日期 | 记录 | 审了什么 | 结论 | 漏了什么 |
|---|---|---|---|---|
| 2026-07-09 | 写作专题 D001/D002 | 切换代码三个 bug（混合分母/判据脱钩/oracle 对照）| 修 bug 重跑，切换 vs 固定 NDA 低 SNR +1.3~2.3dB | mixed 口径的 selector-output 图未单独审计 |
| 2026-07-11 | 写作专题 D005 | **branch-winner 口径**：full(ne_d/1024) 给 DA 打 0.75 折，data(ne_d/768) 才公平 | 选对率 13/29→26/29 反转，"跨场景选优"framing 成立 | **只审 branch-winner，没审 selector-output 增益图**（Fig.5 用的另一种 mixed 口径，病根相同形式不同）|
| 2026-07-11 | 写作专题 R008 | 基于 D005 把切换叙事升为"自适应选优" | 误称"全 data 口径核查"（1.3~2.3dB 实为 net/mixed 口径）| 口径标注错误传到 W002 正文 |
| 2026-07-14 | 本专题 D003→D004 | D003 暂停 switching 全口径，D004 恢复 data-BER | 又只恢复 branch-winner 的 data 口径 | Fig.5 mixed 口径仍未解决 |
| 2026-07-15 | 本专题 R004 | **selector-output 口径**（端到端调用链追踪）| Fig.5 metric BLOCKED；病态退化证明 1.249dB 白送 | 终于挖到根——同一 population 问题在三个对象(branch-winner/selector-output/net-gain)上，前两次只审了 branch-winner |
| 2026-07-15 | 本 R005 | 5seed 实跑 common-768 验证 | 见下 | — |

### 根因（一句话）

**同一个 768/1024 population 不统一问题，存在于三个对象，但前 4 次审计每次只审了 branch-winner（"哪个估计器赢"），没审 selector-output（"切换输出增益图"）。** D005 修了 branch-winner 后大家以为"口径问题解决了"，没做全局扫描。

同型根因（D004 教训原话）："数字口径的物理含义没有用代码逐行验证，凭字段名或印象判断"。`switch_ber_mean` 字段名听着像"切换 BER"，但 numerator population 随 branch command 在 768/1024 间跳——字段名掩盖了 population 不统一。R004 能揪出来是因为做了端到端调用链追踪（paper claim→caller→callee→metric/state），不是只看字段名。

### "为啥稍微改口径差那么多"——不是改没了，是原来数字里有虚的部分

**真实的物理增益从一开始就不大。** Fig.5 原报的 2.3/2.0/1.3 dB 里有一部分是口径白送的，不是 selector 赚的。

**病态退化（R004 §3 + 5seed 验证坐实）**：假设 selector 完全没用，DA/NDA 每 bit 错误率都是 `p`，selector 全选 DA：
- NDA BER = 1024p/1024 = p
- SW BER = 768p/1024 = 0.75p
- Fig.5 增益 = 10log10(p/0.75p) = 10log10(4/3) = **1.249 dB**（白送，跟 pilot overhead 同数）

改 common-768 后：
- NDA common-768 BER = 768p/768 = p
- SW common-768 BER = 768p/768 = p
- 增益 = 0 dB（白送消失）

**5seed 验证精确坐实**：strong@5 mixed = +1.315 dB ≈ 病态地板 1.249 dB，说明该点 mixed 正值几乎全是机械白送；扣掉后 common-768 只剩 +0.085 dB（≈真实选择信号接近零）。差值列（+0.8~+1.2 dB）系统性落在 1.249 附近，与 R004 结论一致。

---

## 第二部分：5seed × 9点 验证结果（核心数字）

> 脚本 `_a4_switch_common768_probe.py` / 数据 `_a4_switch_common768_probe.json`
> 只加 common-768 位计数，未改 estimate/decide/demod/判据/参数。TL-23 守门 0 违例。24 秒跑完。

### mixed vs common-768 增益对比

| 场景 | SNR | mixed gain (dB) | common-768 gain (dB) | 差值 (dB) |
|---|---:|---:|---:|---:|
| weak | 5 | +1.699 | **+0.587** | +1.112 |
| weak | 10 | +2.279 | **+1.248** | +1.031 |
| weak | 15 | +0.876 | **+0.457** | +0.419 |
| moderate | 5 | +1.570 | **+0.381** | +1.189 |
| moderate | 10 | +1.956 | **+0.830** | +1.126 |
| moderate | 15 | +1.030 | **+0.437** | +0.594 |
| strong | 5 | +1.315 | **+0.085** | +1.230 |
| strong | 10 | +1.343 | **+0.192** | +1.151 |
| strong | 15 | +0.909 | **+0.107** | +0.802 |

### Sanity check（PASS）

mixed 口径三个锚点全部精确复现，证明代码改对了：
- weak@10 +2.279（目标 ~2.3）✓ / moderate@10 +1.956（目标 ~2.0）✓ / strong@5 +1.315（目标 ~1.3）✓

### 数字解读

common-768 增益分布：
- **weak/moderate 中 SNR（5/10dB）真实增益 +0.38~+1.25 dB**——selector 真有本事，低 SNR 区 NDA 升幂崩溃 selector 切 DA 避险
- weak/moderate 高 SNR（15dB）+0.44~+0.46 dB——中等，DA/NDA 接近边际收益变小
- **strong（5/10/15dB）+0.085~+0.19 dB——接近零**。R004 病态退化坐实，strong@5 mixed 1.315dB 几乎全是白送

符合物理直觉：strong 湍流 deep fade 严重 DA/NDA 都受罪切换救不了多少；weak/moderate 低 SNR 区 NDA 升幂崩溃是硬伤 DA 有 pilot 撑着，切换确实避险。

---

## 第三部分：对决策的影响

### 删图(路线3)的问题

会丢掉 weak/moderate 低 SNR 区 +0.4~+1.25dB 的真实增益证据——这是 selector 唯一能正当声称的性能贡献，删了就真没 selector 性能证据了。

### 全 9 点保图(路线4 原方案)的问题

strong 三点 0.085~0.19 dB 写进图很难看，审稿人会问"strong 那三点几乎为零意义是什么"。

### 5seed 数字暴露的第三条路（主控建议，待用户拍）

Fig.5 **不删但只画 weak/moderate 的 6 点**（真实增益 0.4~1.25dB），strong 不进这张图。正文 §IV-C 叙事从"selector 全场景 BER reduction"收窄为"selector 在 NDA 升幂失效的低 SNR 区提供避险增益"。strong 场景 selector 价值低是 deep fade 限制，§IV-B 一句话带过不硬凑进性能图。

### 论文承重墙不受影响（用户最关心的"方法是不是不行了"）

- selector 在 weak/moderate 低 SNR 区**行**（0.4~1.25dB 真实避险增益）
- selector 在 strong 区作为性能增益**弱**（但这不影响论文，strong 的分量由 D009 的 NDA-vs-DA 1.9dB/3.1dB 承担，那个数字真实口径规范独立成立不走切换代码）
- 论文最大数字（NDA-vs-DA 1.9/3.1dB，D009）在 §IV-B 不在 §IV-C，跟 Fig.5 毫无关系，**不受 selector 口径问题影响**

---

## 结论

1. **R004 技术审计成立**——Fig.5 mixed 口径问题真实，病态退化证明 + 5seed 验证双坐实。
2. **selector 不是废物**——公平口径下 weak/moderate 低 SNR 区有 0.4~1.25dB 真实避险增益。
3. **selector 也不是性能明星**——strong 区几乎为零，原 mixed 口径的 1.3dB 大部分是白送假象。
4. **论文立得住**——核心价值是"系统表征+crossover 发现+量化对比"(§IV-B)，切换规则是适配机制，承重墙不靠 selector 增益图。
5. **建议第三条路**——Fig.5 只画 weak/moderate 6 点，升级 30seed 收窄 CI，正文收窄为"低 SNR 避险增益"叙事。待用户拍板。

## 对决策的影响

- 不新建 D###（5seed 是探索性验证，数字待 30seed 定稿后才进决策；本 R005 只记录事实）
- 待用户拍板"第三条路"后，建 D011：Fig.5 改为 weak/moderate 6 点 + common-768 口径 + 避险叙事
- 若用户选删图，D011 改为"删 Fig.5 + §IV-C 整段 + 收窄 selector 性能声称"
- 影响上游写作专题 D005（branch-winner 口径审计正确但 selector-output 漏审，需在 D005 追加注释指向 R004/R005）

---

## 追加（2026-07-15）：30seed × 9点 定稿结果

> 脚本 `_a4_switch_common768_30seed.py` / 数据 `.json`，161 秒，TL-23 守门 0 违例。

| 场景 | SNR | common-768 gain (dB) | CI95 下界 | CI95 上界 | 显著? |
|---|---:|---:|---:|---:|---|
| weak | 5 | +0.698 | +0.668 | +0.728 | ✅ |
| weak | 10 | +1.256 | +1.220 | +1.292 | ✅ |
| weak | 15 | +0.536 | +0.443 | +0.629 | ✅ |
| moderate | 5 | +0.470 | +0.447 | +0.493 | ✅ |
| moderate | 10 | +0.867 | +0.831 | +0.903 | ✅ |
| moderate | 15 | +0.474 | +0.395 | +0.554 | ✅ |
| strong | 5 | +0.075 | +0.053 | +0.096 | ✅(≈0) |
| strong | 10 | +0.138 | +0.098 | +0.178 | ✅(≈0) |
| strong | 15 | +0.101 | +0.053 | +0.149 | ✅(≈0) |

**全 9 点 CI95 下界为正**（统计显著）。weak/moderate 6 点真实避险增益 0.47–1.26dB；strong 3 点 CI 显著但绝对值≈0（0.075–0.138dB），mixed→c768 差值贴近病态地板 1.249dB 坐实 R004 结论。

**用户拍板（2026-07-15）**：方案 B——Fig.5 全 9 点 + common-768 口径 + "避险增益随湍流递减，strong 收窄至零"叙事。不删图不藏 strong。待建 D011 执行。

5seed→30seed 稳定性：weak@10 2.279→2.296(mixed)/ 1.248→1.256(c768)，口径未改错。
