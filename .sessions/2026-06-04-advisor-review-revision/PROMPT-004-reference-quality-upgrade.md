# PROMPT-004: 参考文献质量升级（换 trans 级）

> 创建: 2026-06-04 | 优先级: P1（高复杂度）
> 依赖: P-001（预装规范 B9/B10 已就绪）
> 后续: P-012（#54 格式修正，依赖本 PROMPT 完成质量升级后做 GB7714-87 格式修正）
> 对应批注: #54（"所引用期刊水平低，应以 trans 为主"）

## 目标

将 `毕设/开题报告/kaiti-report.md` 中引用的参考文献质量升级至导师要求的"以 trans 为主"标准。具体产出一份替换清单（旧引文 → 新引文 + 替代理由），并更新 `毕设/写作材料/references.bib` 和 `kaiti-report.md` 中的引用。

**本 PROMPT 只负责质量评估和替换，不负责格式修正。** 格式修正（GB7714-87）由 P-012 完成。

## 背景

### 导师原话

批注 #54："所引用期刊水平低，应以 trans 为主" + "格式不符合学校规范"

### 现状

- `kaiti-report.md` 使用 Pandoc `@citekey` 格式引用，bib 文件路径为 `../写作材料/references.bib`
- bib 文件共 1371 行，约 90+ 条期刊引文
- 经初步扫描，存在以下低影响因子/非 trans 级期刊：Sensors, Photonics (×3), J. Opt. Commun., Cogent Engineering, International Journal of Communication Systems, Aerospace, Mathematics (×2), Satellite, CEAS Space Journal, Journal of Optics (×2), Wireless Personal Communications, Journal of Physics: Conference Series, Scientific Reports, IEEE Access, Optik (×2), Applied Optics, International Journal of Information Technology 等

### P-001 预装规则（B9，已就绪）

- 主引期刊：IEEE Trans. Commun. / JLT / TWC / OL / JOCN 等 IEEE Trans 系列
- 允许保留：SPIE / OFC / Optics Express / Opt. Lett. 等顶会顶刊
- 低 IF 期刊引文需逐条评估：不可替代贡献 → 保留；能找到 trans 级替代 → 替换

### 用户决策

- **允许保留**：SPIE / OFC / Optics Express / Opt. Lett. 等顶会顶刊
- **需要替换**：Sensors, Photonics, J. Opt. Commun. 等低影响因子期刊
- **替换标准**：检查该论文是否有不可替代的贡献（如该子领域唯一相关工作 → 保留），否则找 trans 级替代论文

## 必读文件（按优先级）

1. **`毕设/写作质量规范.md`** — B9（参考文献质量门槛）和 B10（GB7714-87）规则，确认替换标准
2. **`毕设/写作材料/references.bib`** — 全部 bib 条目，agent 需要提取所有期刊名并分类
3. **`毕设/开题报告/kaiti-report.md`** — 正文，确认每条引文在文中的引用位置和上下文（判断不可替代性时需要）
4. **`.sessions/2026-06-04-advisor-review-revision/PROMPT-001-preload-standards.md`** — B9/B10 规则原文
5. **`.sessions/2026-06-04-advisor-review-revision/S001-review-planning.md`** — 批注 #54 的上下文

## 子 Agent 策略

### Agent 1：提取 + 分类（主对话直接执行或轻量子 agent）

- 读 `references.bib`，提取所有 `journal` 字段
- 按以下三级分类：

| 类别 | 标准 | 处理方式 |
|------|------|---------|
| **Tier-1: trans 级** | IEEE Trans 系列、JLT、OL、JOCN、JSTQE、AOP、IEEE Commun. Mag. 等 | 保留不动 |
| **Tier-2: 允许保留的顶会顶刊** | SPIE、OFC、Optics Express、Opt. Lett.、IEEE Photonics Tech. Lett. | 保留不动 |
| **Tier-3: 需评估的低 IF 期刊** | Sensors, Photonics, J. Opt. Commun., Cogent Engineering, Aerospace, Mathematics, Satellite, CEAS Space J., J. Optics, Wireless Personal Commun., J. Phys. Conf. Ser., Scientific Reports, IEEE Access, Optik, Appl. Opt., Int. J. Commun. Syst., Int. J. Inf. Technol., IJICS 等 | 逐条评估 |

- 对 Tier-3 条目，记录 citekey、论文标题、期刊名、在 kaiti-report.md 中的引用位置和上下文

### Agent 2：不可替代性评估 + 替代论文检索（第 1 批，3-5 篇）

- 对 Agent 1 识别的 Tier-3 引文的前 3-5 篇：
  - 读该引文在 kaiti-report.md 中的引用上下文
  - 判断：该论文是否提供了不可替代的贡献？（如是该子领域唯一相关工作、提出了独特方法、包含关键数据等）
  - 对需替换的引文，用 `bash tools/search` 检索同主题的 trans 级替代论文
  - 验证替代论文 abstract 确实覆盖相同主题
  - 产出：保留/替换判定 + 替代论文候选

### Agent 3：不可替代性评估 + 替代论文检索（第 2 批，3-5 篇）

- 与 Agent 2 相同流程，处理剩余的 Tier-3 引文
- 如果 Tier-3 引文超过 10 篇，再开 Agent 4 处理剩余

### 并发控制

- Agent 2 和 Agent 3 可并行
- Agent 1 必须先完成（Agent 2/3 依赖分类结果）
- 一次最多 3 个子 agent 同时运行

## 工作步骤

### Step 1：提取所有期刊引文并分类 [检查点：分类表完成]

1. 读 `references.bib`，提取全部 `journal` 字段值
2. 去重，得到期刊名列表
3. 按 Tier-1/Tier-2/Tier-3 三级分类
4. 产出分类表（Markdown 表格：citekey | 标题 | 期刊 | Tier）

**检查点**：分类表完整，Tier-3 条目全部识别，无遗漏。

### Step 2：提取 Tier-3 引文的引用上下文 [检查点：上下文表完成]

1. 对每个 Tier-3 citekey，在 `kaiti-report.md` 中搜索 `@citekey` 出现位置
2. 记录引用上下文（引用所在段落的一句话摘要 + 该引文支持什么论点）
3. 产出上下文表（citekey | 引用位置 | 支持的论点 | 一句话摘要）

**检查点**：每个 Tier-3 citekey 都有引用上下文记录。

### Step 3：逐条不可替代性评估 [检查点：判定表完成]

对每个 Tier-3 citekey，按以下标准逐条评估：

| 判定 | 条件 | 动作 |
|------|------|------|
| **保留** | 该论文是该子领域唯一相关工作，或提出了被广泛引用的独特方法/数据 | 标记保留，附保留理由 |
| **替换** | 存在同主题的 trans 级论文可覆盖相同论点 | 进入 Step 4 检索替代 |
| **待定** | 不确定是否有替代，需检索确认 | 进入 Step 4 检索确认 |

评估维度：
- (a) 该论文在 Google Scholar 的被引次数（高被引 → 更可能是子领域核心工作 → 倾向保留）
- (b) 引用该论文支持的论点是否可以用其他论文替代
- (c) 该论文的研究主题是否在该领域有大量同类工作

**检查点**：每个 Tier-3 citekey 都有判定结果（保留/替换/待定）和理由。

### Step 4：检索替代论文 [检查点：替代候选确认]

对判定为"替换"或"待定"的引文：

1. 用 `bash tools/search` 检索同主题 trans 级论文，检索策略：
   - 提取原论文的核心关键词（如 "channel estimation FSO turbulent"，"carrier phase recovery coherent"）
   - 加上目标期刊限定词（如 "IEEE Transactions", "Journal of Lightwave Technology"）
   - 每篇替代候选需验证 abstract 确实覆盖相同主题
2. 对每个待替换引文，选出最佳替代候选（1 篇即可，不需要多个选择）
3. 产出替代候选表（旧 citekey | 旧论点 | 新论文 citekey | 新论文标题 | 新期刊 | 覆盖度确认）

**检索工具**：
- 英文文献：`cd /mnt/d/code/study/research-protocol && bash tools/search "<query>"`
- 需要检索的替换论文预计 5-10 篇
- **禁止主对话直接调用 WebSearch / webReader**（检索必须在子 agent 中执行）

**检查点**：每个需替换的引文都有确认的替代论文，替代论文 abstract 已验证覆盖相同主题。

### Step 5：更新 bib 文件和正文 [检查点：更新完成]

1. 将替代论文条目写入 `毕设/写作材料/references.bib`（新增条目，不删除旧条目，旧条目标记注释 `% REPLACED by {new_key} for PROMPT-004`）
2. 更新 `kaiti-report.md` 中的 citekey 引用（旧 key → 新 key）
3. 保留的 Tier-3 引文不做任何修改

**检查点**：bib 文件中旧条目已注释标记，新条目已添加；正文中 citekey 已替换。

### Step 6：产出替换清单 [检查点：清单完整]

最终产出一份完整替换清单（Markdown 表格），包含：

| 旧 citekey | 旧期刊 | 判定 | 新 citekey | 新期刊 | 替代理由/保留理由 |

## 质量检查

### 替换覆盖度验证

对每条替换，确认：
- [ ] 新论文的 abstract 确实覆盖旧论文在正文中支持的论点
- [ ] 新论文发表在新期刊的影响因子 ≥ 旧论文（或新期刊为 IEEE Trans 系列）
- [ ] 新论文的发表年份合理（优先近 5 年，如领域较老则放宽）

### 全局验证

- [ ] Tier-3 引文全部有判定结果，无遗漏
- [ ] 替换后 kaiti-report.md 中无悬空 citekey（每个 `@key` 都能在 bib 中找到）
- [ ] bib 文件中无重复条目
- [ ] 未修改任何 Tier-1 / Tier-2 引文
- [ ] 未修改任何引用格式（格式修正留给 P-012）

### 统计

替换完成后统计：
- Tier-1 引文数量（保留）
- Tier-2 引文数量（保留）
- Tier-3 保留数量 + 保留理由
- Tier-3 替换数量 + 替代论文
- 替换后 trans 级引文占比（目标：>60%）

## 不要做什么

1. **不要修改引用格式** — GB7714-87 格式修正由 P-012 负责，本 PROMPT 只做质量升级
2. **不要删除引用** — 只加不删。旧 bib 条目注释标记保留，不物理删除
3. **不要修改 Tier-1 / Tier-2 引文** — trans 级和允许的顶会顶刊不动
4. **不要在主对话调用 WebSearch / webReader** — 检索必须在子 agent 中执行
5. **不要同时处理格式问题** — 格式和质量是两个独立维度，分步处理
6. **不要凭印象判定期刊等级** — 每个 Tier-3 期刊的 IF 需有依据（可用子 agent 查）
7. **不要盲目替换高被引论文** — 被引次数高的低 IF 论文可能是该子领域的奠基工作，倾向保留

## 产出

### 必须产出

1. **分类表** — 全部引文的 Tier-1/2/3 分类（citekey | 标题 | 期刊 | Tier）
2. **替换清单** — 旧引文 → 新引文的完整对应表（旧 citekey | 旧期刊 | 判定 | 新 citekey | 新期刊 | 理由）
3. **更新的 bib 文件** — `毕设/写作材料/references.bib`（新增条目 + 旧条目注释标记）
4. **更新的正文** — `毕设/开题报告/kaiti-report.md`（citekey 替换）

### 更新 S001

- 在 S001 的对话映射表中标记 P-004（#54 质量）已完成
- 更新 topic-index.md 的进展线索

## 手接要求（给 P-012 的接口）

本 PROMPT 完成后，P-012 需要以下信息才能启动格式修正：

### P-012 输入

1. **更新后的 `references.bib`** — 包含新增的替代论文条目
2. **替换清单** — 知道哪些条目是新增的（只需审查新增条目的格式）
3. **kaiti-report.md 的 citekey 映射** — 确认正文中引用已更新完毕

### P-012 注意事项

- 格式修正范围：全部 bib 条目（不只是新增的），因为导师说"格式不符合学校规范"是针对全部参考文献
- 格式标准：B10（GB7714-87），每条必须包含作者/标题/期刊全称/卷期页/年份/DOI
- 格式修正时**不要再改 citekey**（citekey 已在 P-004 中确定）
