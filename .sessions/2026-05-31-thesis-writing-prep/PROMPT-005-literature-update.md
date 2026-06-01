# PROMPT-005: 文献清单更新与 bib 同步

> 专题: thesis-writing-prep | 优先级: P0（写作前置依赖）
> Python: `~/.venvs/torch/bin/python`

## 背景

`material-chapter-literature.md` 是分章文献清单，当前 165 篇（Ch1=57, Ch2=22, Ch3=35, Ch4=33, Ch5=18）。问题：

1. **Ch1 严重不足**：绪论综述章需要 ~100 篇（目前仅 57 篇），需从 Ch2-Ch5 已有文献中上提，并补充新检索
2. **bib 不同步**：`references.bib` 有 146 条，与文献清单不完全对应（部分条目缺失、部分元数据错误）
3. **引用上下文不够**：现有"支撑论点"列太简短，写作时不知道每篇文献具体该在哪个论点怎么引用
4. **状态标注过时**：部分已下载论文仍标 ❌，新增论文未登记
5. **章节对应需要更新**：v4 目录已锁定，部分论文的"对应节"列可能需要调整

## 产出

**更新文件**（原地更新，不新建）:
1. `毕设/写作材料/material-chapter-literature.md` — 文献清单（扩充至 ~200 篇，每篇有充足引用上下文）
2. `毕设/写作材料/references.bib` — 同步更新（与文献清单 1:1 对应）

**新建文件**:
3. `.sessions/2026-05-31-thesis-writing-prep/S002-literature-update-progress.md` — 进度记录

## 必读

### 规范类
1. `毕设/TERMS.md` — 术语规范（文献分类用词）
2. `毕设/thesis-status.md` — 目录 v4 + 各章状态 + 文献统计
3. `.sessions/thesis-direction-pivot/R003-kaiti-strategy.md` — 防御性写作策略

### 现有文献材料
4. `毕设/写作材料/material-chapter-literature.md` — **本文件要更新**
5. `毕设/写作材料/references.bib` — **本文件要同步**
6. `毕设/写作材料/literature-notes-ch1-ch2.md` — Ch1/Ch2 精读笔记（776 行 85 条，新增文献的上下文可从这里提取）
7. `毕设/写作材料/material-chapter-literature.md` 底部的 R1b/R1c 统计 — 已有的中文/英文补充记录

### 搜索工具（用法详见 `tools-guide.md`）
8. `tools/search` — 英文文献检索（S2 + OpenAlex + arXiv + SerpAPI + Exa 七源聚合）
   ```bash
   cd /mnt/d/code/study/research-protocol && bash tools/search "FSO channel estimation" --doc-types journal
   ```
9. `tools/blit` — 浏览器文献检索+下载（IEEE / CNKI / 万方），Playwright 驱动
   ```bash
   # IEEE 英文（校园网 IP 自动机构认证）
   bash tools/blit "carrier phase recovery FSO" --source ieee --download papers/downloads/2026-05-31/
   # CNKI 中文期刊
   bash tools/blit "大气湍流 信道估计" --source cnki
   # CNKI 硕士论文
   bash tools/blit "载波同步 激光通信" --source cnki --doc-type master --download papers/downloads/2026-05-31/
   ```
10. `tools/guide.md` — **工具完整用法**，不确定怎么用就查这个文件

### 已下载论文索引
11. `papers/downloads/2026-05-30/` — 已下载英文论文 7 篇
12. `papers/downloads/2026-05-31-cnki-985/` — 已下载 CNKI 学位论文（董凡/闫佳欣/曾嘉/夏煜等）
13. `papers/` 下其他目录 — 之前下载的论文

## 子 Agent 策略（自适应，分阶段）

**预估总量: 18-24 个 agent。** 不要求一次全开，按批次推进（每批 ≤3 个）。Phase 1 的筛选结果决定 Phase 2 的具体 agent 数量和方向。

### 各阶段 agent 估算

| 阶段 | agent 数 | 说明 |
|------|---------|------|
| Phase 1 筛选+审计 | 3 | 并行，互不依赖 |
| Phase 2 检索 | 10-15 | 按缺口方向拆分，每批 3 个 |
| Phase 3 整合写入 | 2-3 | 文献清单 + bib 更新 |
| Phase 4 验证 | 1 | 交叉检查 |
| **合计** | **16-22** | |

### Phase 1: 筛选 + 审计（3 个 agent 并行）

**⚠️ 先筛后补。** 现有 165 篇不一定都合适——有些是旧方向残留，有些和 v4 目录不匹配，有些子方向文献堆叠过多。先清理再补充。

**Agent A1 — 相关性筛选**: 逐章审核 `material-chapter-literature.md` 中每篇文献，基于 v4 目录（thesis-status.md）和当前研究方向判断：
- 哪些文献与当前方向无关（如预补偿 7 篇，D004 已决定不做；旧方向残留）
- 哪些文献放错了章节（应该在 Ch1 但放在了 Ch2-Ch5，或反过来）
- 哪些子方向堆叠过多（如 Ch3 DL 估计论文 10+ 篇，实际 Ch3 重点不在 DL）
- 哪些文献质量不够（低引且非必要、内容重叠）
- 输出: **淘汰清单**（建议移除/降级的文献列表 + 理由）+ **重分类清单**（建议挪章节的文献）

**Agent A2 — bib 一致性审计**: 审计 `material-chapter-literature.md` 与 `references.bib` 的一致性：
- 文献清单中每个 citekey 是否在 bib 中有对应条目
- bib 中每个条目是否在文献清单中被引用
- 状态标注是否过时（已下载但仍标 ❌ 的）
- 元数据错误（thesis-status.md 列出的 11 篇 bib 元数据错误）
- 输出: 缺口清单（缺失的 bib 条目列表 + 状态修正列表）

**Agent A3 — 缺口评估**: 基于 v4 目录各章节内容，评估筛选后各章文献缺口：
- Ch1 各小节（§1.1 背景 / §1.2.1 信道估计 / §1.2.2 载波同步 / §1.2.3 不足与切入点）各需多少篇
- Ch2-Ch5 各章节各需多少篇（参照同领域论文文献密度）
- 每章缺少哪些子方向的文献（结合 thesis-framework.md 各节内容判断）
- 输出: **分章分节缺口评估 + 目标篇数**（先扣掉淘汰数，再算缺口）

**Phase 1 产出汇总（主对话拍板）**:
- 淘汰/保留/重分类决定
- 每章实际缺口数
- 检索优先级排序

### Phase 2: 补充检索（按缺口发 agent，每批最多 3 个）

**Phase 1 完成后，主对话先拍板：淘汰哪些、保留哪些、每章缺口多大。然后按缺口优先级派搜索 agent。** 每个 agent 负责 1-2 个子方向：

**搜索方式**:
- 英文: `cd /mnt/d/code/study/research-protocol && bash tools/search --query "..." --limit 20`
- 中文: `cd /mnt/d/code/study/research-protocol && bash tools/blit --source cnki --query "..." --doc-type journal`
- 学位论文: `bash tools/blit --source cnki --query "..." --doc-type master` 或 `--doc-type phd`

**重点搜索方向**（Phase 1 确认后调整，以下是初步预估）:

**批次 1 — Ch1 §1.1 研究背景（3 个 agent）**:
- S1: FSO 工程项目与应用进展（LCRD 后续、EDRS 扩展、中国实践站、日本 LUCAS 等）
- S2: 星地激光通信系统综述（2023-2026 最新综述、相干检测 vs 直接检测对比）
- S3: 相干光通信技术综述（QPSK 调制、相干接收机架构、DSP 链路综述）

**批次 2 — Ch1 §1.2.1 信道估计（3 个 agent）**:
- S4: 大气湍流信道建模（GG 分布变体、Rytov 理论、Cn² 测量、非 Kolmogorov 湍流）
- S5: FSO 信道估计方法综述（LS/MMSE/Kalman 传统方法在 FSO 中的应用）
- S6: DL 信道估计（DNN/CNN/Transformer 在 FSO 信道估计中的最新进展 2024-2026）

**批次 3 — Ch1 §1.2.2 载波同步（3 个 agent）**:
- S7: 载波相位恢复综述（VV/BPS/QPSK 分区/ML 算法对比，光纤 + FSO 场景）
- S8: LEO 多普勒频偏估计与补偿（FFT 频偏估计、导频辅助、DPLL）
- S9: 湍流对载波同步的影响（相位噪声、SNR 波动、FOE 窗口选择 — 这是缺口论证的核心方向）

**批次 4 — Ch1 §1.2.3 + Ch3-Ch5 补充（3-4 个 agent）**:
- S10: Ch1 §1.2.3 反面论据（湍流下 CPR 系统性分析的缺失、现有工作的局限性）
- S11: Ch3 级联影响（估计误差→同步性能、跨层分析、灵敏度分析文献）
- S12: Ch4 湍流下 CPR 对比实验（VV/BPS/DPLL 在非高斯信道下的对比论文）
- S13: Ch5 FPGA 实现（FOE/CPR 硬件实现、资源优化、定点化、时序收敛）

**批次 5 — 中文补充（2-3 个 agent）**:
- S14: CNKI 中文信道估计+均衡硕博论文（2023-2026）
- S15: CNKI 中文载波同步/相位恢复硕博论文（2023-2026）
- S16: CNKI 中文 FPGA/信号处理实现硕博论文（2023-2026）

注意：以上 16 个搜索方向是最大覆盖。Phase 1 筛选后可能砍掉一些（如果某方向已经充足），也可能增加一些（如果发现新缺口）。主对话根据 Phase 1 结果决定实际派几个。

**每个搜索 agent 输出**:
- 搜索结果列表（citekey, 标题, 作者, 年份, 期刊, 引用数, 摘要）
- 与现有文献去重后的新增列表
- 推荐引用位置和论点

### Phase 3: 整合更新（主对话 + 1-2 个 agent）

**主对话负责**:
- 审核搜索结果，决定哪些纳入
- 确定每篇新增文献的"对应节"和"支撑论点"（要写得具体，不能只写"FSO综述"）
- 分配 citekey（遵循 bib 格式规范）

**Agent W1**: 更新 `material-chapter-literature.md`:
- 补充新增文献到对应章节表格
- 更新状态标注（已下载的改 ✅）
- 更新汇总统计表
- Ch1 跨章文献标注（标明哪些同时出现在 Ch2-Ch5）

**Agent W2**: 更新 `references.bib`:
- 补充缺失的 bib 条目（从搜索结果提取元数据）
- 修正 thesis-status.md 列出的 11 篇元数据错误
- 确保每个 citekey 与文献清单一一对应

### Phase 4: 质量验证（1 个 agent）

- 文献清单 ↔ bib 条目数完全对应
- 无重复条目
- 每篇文献的"支撑论点"具体可引用（不是泛泛的"FSO文献"）
- citekey 格式正确
- Ch1 总数 ≥ 80 篇

## 写作要求

### "支撑论点"列的写法规范

每篇文献的"支撑论点"必须包含以下信息之一：
- **数据引用型**: "LCRD 2022 年实现 X Gbps 链路，误码率 Y" → 写作时可在 §1.1 引用具体数字
- **方法对比型**: "VV 在弱湍流下 BER 0.015%，但强湍流失败率 35%" → 写作时可在 §1.2.2 对比
- **缺口论证型**: "该文仅考虑固定湍流参数，未分析时变场景" → 写作时可在 §1.2.3 指出不足
- **理论依据型**: "GG 分布 α,β 参数推导自 Rytov 方差" → 写作时在 Ch2 模型描述引用
- **工程参考型**: "Xilinx Ultrascale+ 上实现 FOE，资源占用 Y 个 LUT" → 写作时在 Ch5 引用

### Citekey 格式

遵循 bib 文件头部注释的规则：
- 英文: `{firstauthorlastname}{year}` (如 `khalighi2014`)
- 同年同姓: `{lastname}{year}{suffix}` (如 `wang2025a`, `wang2025b`)
- 中文: `{pinyin_lastname}{year}` (如 `zhangdai2018`)
- 同年同姓: `{pinyin_lastname}{year}{suffix}`

### 条目类型

- `@article`: 期刊论文
- `@inproceedings`: 会议论文
- `@phdthesis`: 博士论文
- `@mastersthesis`: 硕士论文
- `@book`: 教材/专著
- `@misc`: 预印本/其他

中文论文保留中文 title/journal，加 `language = {chinese}` 字段。

## 已知问题

1. **11 篇 bib 元数据错误**（thesis-status.md 列出）: kaushal2016, pollock2022laserspace, pathak2024revolutionizing, capeleti2023linkbudget, param2021gg, boroson2022lcrd, sommerkorn2020edrs, fields2014edrs, cornwell2019nasa, le2012dpll, zibar2020ukf
2. **4 篇未验证论文**: chenyan2024, guanluyang2024, bpskqpsk2024switch, fsocelprediction2024 — 搜索无匹配，可能是 citekey 错误或论文不存在
3. **Ch3 预补偿论文过多**: Ch3 中有 7 篇预补偿相关（D004 已决定不做预补偿），需要清理或重新归类
4. **旧方向残留**: 可能有少量旧方向（GNN/路由/切换）的文献需清除

## 不要做什么

- 不下载/转换 PDF（只做检索和元数据整理）
- 不写论文正文
- 不修改 TERMS.md / thesis-framework.md
- 不改动文献的 citekey（除非确实有冲突）
- 不添加与论文方向无关的文献（如纯 RF 通信、可见光通信 VLC 等）
- 不在主对话调用 WebSearch/webReader（在子 agent 中调用）

## 手接要求

如果本对话做不完（可能），产出 handoff：
1. 已完成的章节更新
2. 未完成章节的缺口清单
3. Phase 1-2 的分析结果
4. 下一个对话的 PROMPT 文档
