# Handoff: B 路线——pilot on/off 系统级架构选择（切换叙事升级）

> 来源: S007（切换 framing 口径审计 + 选对率反转）| 交接目标: 开新对话验证 B 路线物理可行性 + 设计 pilot 开关实验
> 文件名: H006-pilot-switch-architecture-b-route.md
> 日期: 2026-07-11

## 到哪了（状态）

S007 完成切换 framing 口径审计，核心纠正：**H005 误用 full 口径，data 口径才物理公平**。data 口径下选对率 26/29（90%），framing 基本成立。用户提出「切换什么」可以不限于当前 DA↔NDA per-block 切换，扩大到 pilot 开关 / 调制阶数 / 参数等维度。用户选定 **B 路线（pilot on/off 系统级架构选择）**——比 A（估计器切换）物理更有说服力。

**B 路线定义**：面对随时间/仰角变化的湍流强度，系统在两种架构间自适应切换：
- **强湍流模式**：发 pilot（DA 架构），付 25%（或可调）throughput 代价换相位估计精度
- **弱湍流模式**：不发 pilot（NDA 架构），全功率传信息

**S007 已做的 goodput 预检（B 路线第一步物理验证）**：
- 用现有 30seed 数据算 goodput（吞吐×(1−BER)）
- **8/8 个 DA 被选中的点，DA 架构 goodput 全输 NDA 架构**
- 根因：25% pilot overhead（1.249dB）> DA 的 BER 优势（大多 +0.06~+0.50dB，仅 weak@10 +1.50dB）
- **这不是死刑**：pilot overhead 可调（1/8 spacing = 12.5% = 0.58dB），但当前 25% 不够
- 脚本 `/tmp/switch_goodput_check.py`（确定性核查，可复现）

## 下一步干什么

**新对话首要任务 = 判断 B 路线物理可行性，不是直接跑实验**：

1. **先回答 goodput 风险**：B 在 BER 指标下成立（DA 某些条件 BER 更低），在 goodput 指标下当前 25% overhead 不成立（8/8 输）。论文用 BER 还是 goodput？如果 BER，goodput 质疑怎么放 Discussion？
2. **pilot overhead 可调性探索**：当前 1/4 spacing（25%），试 1/8（12.5%）、1/16（6.25%）等，找 goodput 交叉区——在什么条件下、多大 overhead 下发 pilot 值得？
3. **如果 B 在可调 overhead 下有 goodput 交叉区 → 设计 pilot 开关实验（回 step4a，FR-22）**
4. **如果 B 物理不可行（所有 overhead 下 NDA goodput 都赢）→ Kill B，回 A 叙事升级**

**关键纪律**：
- B 是**新方法 MVE**，必须回 step4a-mve-execution 专题走 GW Step 4a 维度 D 流程
- **FR-22**：不能跳框架直接跑实验，先回答"当前在 GW 哪一步" = Step 4a 维度 D
- **FR-21**：goodput 预检就是 B 路线的 oracle 上界精神——先算上界再跑
- **守路 1**：调 pilot overhead 找交叉区 ≠ 调参冲数字——这是设计变量搜索，但要论证不是 overfitting
- **9 天截稿**（CCISP 7/20）：B 如果 3 对话内走不通（goodput 不可行或实验来不及），必须回 A

## 纪律（和下一步直接相关的约束）

1. **D005（本轮新建）**：data 口径（ne_d/768）才物理公平，full 口径（ne_d/1024）偏袒 DA 打 0.75 折。所有 BER 对比用 data 口径
2. **D004**：fair_gain = naive + 1.249dB。B 路线的 goodput 分析本质就是 naive 口径（DA 优势 − pilot overhead）
3. **不变量 7**：故事根 = 候选 A（净增益量化归因）。B 路线如果成立，叙事从"量化归因"升级为"跨工况自适应"，但根不变（数字为根）
4. **不变量 8**：切换数字用 D002 修复版（30seed，net 口径）。B 路线需新数字（pilot 开关 goodput），不能沿用 per-block 切换数字
5. **FR-22**：B 回 step4a，新对话必须先读 `stages/gw-feasibility.md` §D + step4a 专题 master-state
6. **数据真实**：goodput 预检 8/8 输不能隐藏，必须诚实面对。B 如果只在 BER 口径成立，必须标注

## goodput 预检数据（新对话必看）

| 场景@SNR | DA BER | NDA BER | BER优势(dB) | overhead(dB) | 净值(dB) | DA goodput赢？ |
|---|---|---|---|---|---|---|
| weak@5 | 0.329 | 0.399 | +0.84 | 1.249 | −0.41 | ❌ |
| weak@10 | 0.160 | 0.226 | +1.50 | 1.249 | +0.25 | ❌(goodput仍输) |
| weak@15 | 0.048 | 0.053 | +0.48 | 1.249 | −0.77 | ❌ |
| moderate@5 | 0.353 | 0.399 | +0.54 | 1.249 | −0.71 | ❌ |
| moderate@10 | 0.200 | 0.249 | +0.95 | 1.249 | −0.30 | ❌ |
| moderate@15 | 0.080 | 0.086 | +0.27 | 1.249 | −0.98 | ❌ |
| strong@5 | 0.392 | 0.400 | +0.09 | 1.249 | −1.16 | ❌ |
| strong@10 | 0.284 | 0.288 | +0.06 | 1.249 | −1.19 | ❌ |

DA 架构吞吐 = 768 bit/block（192 data + 64 pilot）。NDA 架构吞吐 = 1024 bit/block。
goodput = 吞吐 × (1 − BER)。脚本 `/tmp/switch_goodput_check.py` 可复现。

**为什么 weak@10 BER 净值 +0.25dB 但 goodput 仍输**：BER 比 0.226/0.160 = 1.41 > 吞吐比 1024/768 = 1.33，但 goodput 比 = 768×0.84 / 1024×0.774 = 645/793 = 0.81 < 1。BER 优势的 dB 值（对数域）≠ goodput 优势的线性比值。

---
## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 不变量段落（#7 故事根 / #8 切换数字 / #9 口径方向）
- [ ] 已验证 goodput 预检数据（重跑 `/tmp/switch_goodput_check.py` 确认 8/8 DA 输）
- [ ] 已验证 data 口径选对率 26/29（重跑 `/tmp/switch_caliber_audit.py`）
- [ ] 已检查 _registry.yaml 中本专题 depends_on（step4a-mve-execution，B 实验的产出源）
- [ ] 已确认当前范围：B 路线 = 新方法 MVE，回 step4a 走 GW Step 4a 维度 D（FR-22）

## 下一轮

1. 读本文件 + S007（口径纠正全貌）+ D005（口径公平性判定）
2. **第一步：判断 B 物理可行性**——goodput 风险怎么处理 + pilot overhead 可调性是否有交叉区
3. 如果可行 → 回 step4a-mve-execution 设计 pilot 开关实验（两种信号结构：DA 架构信号 vs NDA 架构信号）
4. 如果不可行 → Kill B 回 A 叙事升级（A 用已有数据，9 天能交）
5. 守 FR-22（回 step4a）/ FR-21（goodput 预检 = oracle 上界）/ 守路 1 / 9 天截稿
