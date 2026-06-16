# [S007] N1 相干 FSO PCS gain 数据门控——门控解除，N1 升级倾向 PASS

> 2026-06-16 续 5 | 阶段: 方向探索（N1 Groundwork 前置数据门控）| 状态: 门控解除，N1 可进 Groundwork
> 来源: H005 任务块 N1（对话乙）| 方法: D005 门控逻辑 + tools/search 检索 + 子 agent 精读 + 主对话交叉验证
> 注: 原拟编号 S006，与对话甲（A3 Groundwork §B）的 S006 冲突，改 S007

## 目标

执行 H005 任务块 N1：派子 agent 检索 + 精读，确认相干 FSO（intradyne，非 IM/DD）下 PCS shaping gain 是否存在且 ≥1 dB。补到→解除门控，N1 可进 Groundwork；补不到→N1 降级"数据不足"。本轮**只做门控判定，不进 N1 Groundwork**（D005 强制：门控未解除前不进）。

## 记录

### 接收 H005 验证（Trigger 5）

按 H005 接收方验证清单，主对话交叉验证 3 条关键事实声称（全部 PASS）：
- **声称1** Elzanaty 是 IM/DD（非相干）→ PASS：content.md L43 "For FSO systems, the IM/DD is preferable over coherent modulation techniques"
- **声称2** cite=81 踩 TL-03 → PASS：Semantic Scholar abstract 直证（curl 重验 citationCount=42 非 81，"moving average channel estimator" + "55-m link" + "raining periods"）
- **声称3** Paillier AGC 信号+噪声等比放大 → PASS：content.md L177 "the multiplicative gain of the AGC loop impacts equally the signal and the noise... in deep fades, both the signal and the noise are amplified"

### 执行实况

1. **检索**（主对话 `tools/search`，2 条查询，JSON 存 `search-archive/2026-06-16/`，slug 加 `-n1-gain-preflight` 后缀避免覆盖）：
   - `probabilistic constellation shaping coherent free-space optical QAM turbulence`（71 去重 → 30 篇）
   - `Maxwell-Boltzmann probabilistic amplitude shaping coherent optical wireless turbulence gamma-gamma gain`（38 去重 → 30 篇）
   - Semantic Scholar API 踩 429 速率限制（S005 教训重演），改用 `tools/search` 多源（Exa+OpenAlex+arXiv+S2）绕过

2. **下载 4 篇关键论文**（多路径）：
   - Tian 2021（MDPI OA）：`tools/download --doi` 失败 → 构造单篇 JSON 带 url 字段 → Firecrawl scrape 成功 → `papers/doi/10.3390_app11219805/`
   - cite=35 Rode 2023（arXiv 2212.03839）：`tools/download --arxiv` 成功 → `papers/arxiv/2212.03839/`
   - Zahr 2024 JSAC（IEEE closed）：`tools/blit --source ieee --download` 成功 → `papers/downloads/2026-06-16-n1/10436131.pdf` → convert
   - Deng 2026 LPT（IEEE closed）：`tools/blit --source ieee --download` 成功 → `papers/downloads/2026-06-16-n1/11313238.pdf` → convert

3. **子 agent 精读**（≤600s 内完成，1 agent 读 4 篇，逐篇提取检测类型/信道/调制/整形/gain dB/baseline/强湍流分离）

4. **主对话交叉验证**（AGENTS.md 强制）：grep Tian content.md 逐字验证 1.3 dB / 1.5 dB / 0.3-0.4 dB 三个 gain 数字，全部与子 agent 报告一致

### 门控判定：解除（RELEASE）

**决定性证据：Tian et al. 2021（MDPI Appl. Sci., DOI 10.3390/app11219805）** —— 正是 N1 假设的精确场景（相干 FSO + 16-QAM + Gamma-Gamma 湍流 + 概率整形），正文报：

| 指标 | gain（PS H=3.7964 vs uniform 16-QAM）| 阈值 |
|---|---|---|
| post-FEC BER @ 1e-2 | **1.3 dB** | ≥1 dB ✓ |
| SER @ 4e-1 | **1.5 dB** | ≥1 dB ✓ |
| AIR @ 1.8 bit/sym | 0.3-0.4 dB | <1 dB（信息论增量小）|

**D005 门控阈值（≥1 dB）满足**。N1 从 S005/D005 的"存疑（数据门控）"升级为"**倾向 PASS（门控解除，可进 Groundwork）**"。

### 四个限制（门控解除但不无条件 PASS，N1 Groundwork §B 必须复核）

1. **gain 随 SNR 递减**：Tian 正文"With the increase of the SNR, the shaping gain decreases gradually. Eventually, the PMF approaches the uniform distribution." → 高 SNR（弱湍流）gain 趋零。**N1 gain 主要在低-中 SNR（中-强湍流）区**
2. **AIR gain（0.3-0.4 dB）远低于 SER/post-FEC BER gain（1.3-1.5 dB）**：1.3-1.5 dB 含 FEC 协同。**N1 报 gain 应报 SER/post-FEC BER（1.3 dB），非 AIR**
3. **强湍流（σ²_R > 1）gain 未单独列表**：Tian sweep weak→strong 未按 σ²_R 数值隔离。文本暗示弱湍流 gain 大但与"随 SNR 递减"矛盾——实际可能是**中湍流 gain 最大**，需 Groundwork 复核
4. **单一来源**：Tian 是长春光机所 Wu Zhiyong 组单篇。1.3 dB 需 N1 Groundwork 用 Elzanaty blind 框架独立复现

### cite=35（Rode 2023）降级

fiber AWGN + Wiener 相位噪声，无湍流，gain ~0.1 bit/symbol BMI（非 dB）。**不适用 FSO 门控**，从"N1 关键论文"降级为"PCS+CPE 方法参考"（differentiable BPS + GeoPCS 方法论可迁移，gain 数字不能用于 N1 FSO 门控）。D005 对 cite=35 的疑虑由 R007 确认。

### 其他检索命中（未精读，N1 Groundwork Phase B 可补）

- L8/L9 "Super-Gaussian vs MB in coherent FSO turbulence"（c=1）：4% distance improvement（≈0.17 dB）——PS 分布族内部对比，小
- L13 Zahr 2024 JSAC：coherent 低阶 ASK shaping gain "limited"（负证据：coherent 低阶 PS gain 小，Tian 的 1.3 dB 依赖 16-QAM + FEC 协同）
- L4 OFC 2024 Th3C.5 "PCS + interleaving strong turbulence 65dB link-loss"：未精读，强湍流场景

## 决策引用

- **D005（门控解除，不新建 D006）**：D005 否决条件第 1 条满足（"补检索确认存在相干 FSO PCS gain 论文 ≥1 dB → 门控解除"）。**D006 预留给降级路径，本轮走解除路径不新建**。详细证据与门控逻辑见 R007
- D001：执行（后续阶段链 Groundwork §B）
- D004：参照（A3+N1+2.2 互锁三章主轴，N1 物理可行性基础增强）
- 无新决策（门控解除是 D005 预设的"释放"分支，非新方向决策）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。N1 gain 数据门控是 D005 的强制前置，属"系统性扫描找方向"原始目标的 Groundwork 前置筛选。**未进 N1 Groundwork**（D005 强制：门控判定与 Groundwork 分离），未碰 MVE/Contract/Execute，未改仿真代码/开题报告
- 范围变更：无新增

## 后续

### 当前候选总览更新（S005 → S007）

- **A3（导频抗 deep fade）= §B PASS**（S006 对话甲判定，升级自 S005 倾向 PASS）：Groundwork §B 正式通过，可进剩余步骤。详见对话甲 S006/D006
- **N1（静态 PCS 适配湍流 SNR 分布）= 倾向 PASS（升级）**（S005 存疑 → S007 门控解除）：无物理死锁 + TL-03 边界已厘清（Elzanaty blind）+ **gain 数据确认存在（Tian 1.3 dB，门控解除）** + 主导损伤针对性强。缺口=Groundwork §B 复核 R007 四个限制
- **2.2（自适应频谱效率闭合解）= 保底**：纯解析，不变
- **关键变化**：两候选（A3/N1）现在都倾向 PASS，各有 Groundwork 内可闭合的缺口。保底骨架 2.2 不变

### N1 下一步（进 Groundwork，非本轮）

1. 读 `stages/groundwork.md` + `gw-feasibility.md §B`（框架文件规则）
2. N1 §B 空白零假设：N1 比 Tian 2021 强在哪？（Tian = 启发式 PSO 全搜索 + 单一 MB；N1 若锚 Elzanaty blind 离线设计 + D004 切法③仰角确定性排程 = 增量）
3. 复核 R007 四个限制（gain 随 SNR 递减 / AIR vs BER / 强湍流隔离 / 单一来源）
4. 未到 MVE

### 两对话汇总（H005 收尾）

H005 任务块 A3（对话甲）+ 任务块 N1（本轮，对话乙）完成后，主对话（新开或合并收尾）汇总：
- A3 §B 判定（对话甲产出）+ N1 门控解除（R007/S006 本轮产出）
- 更新候选总览 → 决定互锁三章是否成立 / 保底骨架是否调整
- 两候选都倾向 PASS，互锁三章物理可行性基础增强，但仍需各自 Groundwork §B 通过（S004 教训：互锁是结果非前提）

### 不要做

- ❌ 把 Tian 1.3 dB 当 N1 既得 gain（Tian 是他人工作，N1 需独立增量；1.3 dB 是"领域已证 gain 存在"锚点）
- ❌ 忽略"gain 随 SNR 递减"（高 SNR 报 gain 会得 <0.5 dB 错误结论）
- ❌ 用 cite=35 fiber gain 作 N1 FSO gain 锚点（信道不兼容）
- ❌ 在 N1 Groundwork §B 未过前锁"互锁三章"叙事
