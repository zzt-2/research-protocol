# Handoff: 块D检索+召回完成，下载债务待清，块E(Step 4a)就绪

> 来源: S016 | 交接目标: 下一个对话清下载债务 + 启动块E Go/No-Go
> 日期: 2026-06-27
> 文件名: H007-blockD-recall-done-download-debt-blockE-ready.md

## 到哪了（状态）

块 D Step 3.5 **检索 + 召回 + Paillier JLT 精读完成**，master-state Step 3.5 = 🔄部分（Q# 清单 Q1-Q13 已非空，可直接进块 E）。

**已完成**：
- 盲区 A/B 定向补检索（search-archive/2026-06-27/ 7 个 JSON，全核查 PASS）
- 🔴 **发现并纠正 H004 选样漏召**：Pech 2025 + Valjus 2025 + Paillier 2019 conf 三篇旧 B1 资产早在 2026-06-16 已下载精读，但被路径依赖排除。已召回入 Q# 清单为 **Q11/Q12/Q13**（D005 务实标准重评）
- **Paillier 2020 JLT（companion[9]完整版）下载成功 + 精读完成**（arXiv LaTeX 1911.11851，笔记 `papers/_read_notes/10.1109_jlt.2020.3003561.md`）。**关键发现：条件性细化 Q12 gap**——Paillier 证明"湍流相位对载波同步可忽略"但依赖特定条件（BPSK+10GBaud+理想timing+AGC恒幅+piston~1ms慢于符号率）
- Viterbi 1983 blit 元数据获（936引，浅读够 related work 用，全文需 IEEE 订阅）
- literature_notes.md Q# 清单已更新（Q1-Q13 + Q12 条件性细化 + 综合观察线索加 Q12 务实切入点）
- 偏航检查 A-E 全过

**债务（不阻塞，可进块 E）**：3 篇论文下不到：
- Rustum 2026（`10.1049/cmu2.70148`，IET 非 OA，all_failed）
- Tang 2024（`10.1117/12.3023766`，SPIE，blit 不支持 SPIE 源）
- Mosnier 2025（`10.1117/12.3075397`，SPIE，同上）

## 下一步干什么

### 直接进块 E（Step 4a Go/No-Go）— 推荐
Q# 清单 Q1-Q13 已非空（远超 gw-read.md ≥1 条门槛），Step 3.5 检索+召回核心已完成，3 篇下不到的债务不影响 Go/No-Go 判定（Rustum DL 路径可块 E 中途按需补，Tang[50]核对可读新2 原文 references）。

对 Q1-Q13 每个 Q# 走 gw-feasibility A0/A'/A/B/D。**重点候选**：
- **Q12（Paillier 分治→条件性改进）**：盲区 A 最强 baseline 端证据。**JLT 精读后务实切入点明确**：针对 Paillier 假设不适用的条件（高阶调制/低SNR/无理想timing/强湍流快piston/上行链路）做改进，赢其分治 DPLL baseline 几 dB（D005 标准）。⚠️但必查旧 B1 时期是否试过类似角度（警惕 B1 换皮）
- **Q8（PCS+Rs 治 Doppler）**：同门范式最浓，增益 ~100Gbps 硬，但增益来自 Rs 非 PS
- Q1/Q2/Q7：全过四判据但⚠️链路（LEO-LEO 星间/利益相关）

**Step 4a 前必读**：`stages/gw-feasibility.md` 全文 + `thesis-lessons.md` TL-30/31（FR-22/24 强制门控）+ decisions.md D004-c（证据链强制 FR-26）+ D005（务实路线 INVARIANT）。

### 可选：先补 Rustum 2026（DL 独立路径对比）
若块 E 需要 DL-based 对比视角，Rustum 2026 可尝试其他下载方式（如 Sci-Hub 手动 / 学校 VPN），但非块 E 硬前置。Tang[50]核对可直接读新2 原文 references 列表（papers/blit-downloads/2026-06-26/10155111.md）查 [50] 准确标题，不必下 Tang 全文。

## 纪律（和下一步直接相关的约束）

1. **D005 务实路线是 INVARIANT**：Go=赢传统未优化 baseline 几 dB（不是 oracle 上界，FR-21 降为参考）。FR-25 Go/Kill 对手标准分离——Go 赢传统 baseline，Kill 用 oracle 上界<0.5dB 或 MVE FAIL
2. **警惕 B1 换皮**：Q11/Q12/Q13 是旧 B1 方向资产。块 E 判 Go 时必须诚实回答"这次跟被 Kill 的 B1 有什么本质不同"，不能换皮重来。若只是 B1 换壳 → Kill
3. **FR-26 证据链强制**：宣称"在 Step X"/"已读 Y"必须附证据指针（文件+行号/路径）。用 papers/ 文件做判断前必查 meta.json 来源
4. **四判据不可放水**（topic-index 不变量 3）：判据 A 降为"baseline 不够好+改进空间"但不可省
5. **主对话严禁 WebSearch/webReader**（上下文爆炸）→ 检索/精读全派子 agent，主对话只接收 ≤500 词摘要

---
## 接收方验证（续接对话时必须完成）
- [ ] 已读取 topic-index 的不变量段落（8 条，D005 务实路线是最高优先级）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] Pech 2025 + Valjus 2025 + Paillier 2019 conf 确实在 papers/ 有笔记（核查 `ls papers/_read_notes/ | grep -E '11443174|sat.1553|8978983'`）
  - [ ] Q11/Q12/Q13 确实已写入 literature_notes.md Q# 清单（核查 `grep -E 'Q1[123]' projects/thesis-fso/literature_notes.md`）
  - [ ] search-archive/2026-06-27/ 确实有 7 个 JSON（核查 `ls search-archive/2026-06-27/*.json | wc -l`）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反"明确不含"（本轮未跑 MVE/未判 Go/未改框架）

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| 3 篇论文下不到（Rustum2026 IET非OA / Tang2024+Mosnier2025 SPIE无源） | Step 3.5 补精读完整性 | blit 不支持 SPIE，IET 非 OA 确认下不到。Tang[50]核对可读新2原文 references 替代 | 块 E 需 DL 对比视角时补 Rustum（Sci-Hub/VPN）；其余不阻塞 |
| IEEE 限流 | S008 增量价值<执行成本留债 | Viterbi 用 blit 拿到元数据（浅读够），全文需 IEEE 订阅 | 需要 Viterbi 全文细节时（块 F baseline 复现阶段） |
| H004 选样漏召根因 | D003 多候选不应路径过滤 | 已纠正（Q11-Q13 召回）但根因（选样流程无"历史方向资产召回"步骤）未修流程 | 下次选样时加"检查旧方向 papers/_read_notes 有无相关资产"步骤 |

## 下一轮

1. 核查下载子 agent 产出 → blit 补关键 2 篇（Paillier JLT + Rustum）→ 精读
2. 启动块 E（Step 4a）：读 gw-feasibility.md → 对 Q1-Q13 走 A0/A'/A/B/D
3. 块 E 重点：Q12（联合建模，警惕 B1 换皮）+ Q8（PCS+Rs 同门范式）
