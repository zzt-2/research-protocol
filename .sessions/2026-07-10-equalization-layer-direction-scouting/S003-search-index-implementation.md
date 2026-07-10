# [S003] 档 C 实施：tools/search 加自动索引 + 一次性回填 + 均衡层 seed 生成

> 2026-07-10 | 框架层改进（落在本专题，所有专题受益）| 状态：完成（已验证）
> 续接：S002（盘库发现"扔那不看"结构根因）

## 目标

回应用户 S002 末选的"档 C：治本改 tools/search"。给 `tools/litsearch` 加自动索引机制 + 一次性回填历史 3.6 万条 + 从索引生成均衡层种子。**本对话内完成**。

## 记录

### 1. 改动清单（3 个文件）

| 文件 | 类型 | 改动 |
|---|---|---|
| `tools/litsearch/search_index.py` | **新建** | `_dedup_key` / `_result_to_record` / `_merge` / `_load_index` / `_write_index` / `update_global_index_from_results` / `update_global_index`。失败不阻塞主流程（try/except + stderr 警告）|
| `tools/litsearch/search_pipeline.py` | **改** | `_auto_save` 末尾（line 478 后）加 `from .search_index import update_global_index; update_global_index(archive_file, output_data)`，外层 try/except 兜底 |
| `tools/backfill_index.py` | **新建** | 一次性回填脚本。`--dry-run` / `--since YYYY-MM`。幂等。扫 `search-archive/*/*.json` → 重建索引 |

### 2. 关键设计决策

**去重键**：DOI 优先（小写化）→ 否则 title 前 80 字符小写去标点。验证：JLT 2023 multi-aperture（DOI 10.1109/JLT.2023.3276637）三条不同查询正确合并成一条，hit_count=3，queries 聚合 3 条。

**abstract 完整存**（非截断）：原计划 abstract_short 前 200 字，验证发现 equalization 关键词首次出现位置**中位数在 574 字**——截 200 字丢 73% 匹配。改完整 abstract，JSONL 从 18MB → 35MB（仍可 grep/Python 扫）。

**合并策略**：queries/dates/sources 并集（保序去重），citation_count 取较大，其他字段取最新非空。验证：FAKE 测试论文插入后 JLT citation_count 正确更新为 999（测试后已清理）。

**失败安全**：`update_global_index` 异常只 stderr 警告，不影响检索主流程。JSONL 损坏可 `python tools/backfill_index.py` 重建（幂等，多次运行结果一致）。

### 3. 回填 + 验证结果

```
扫描文件数：    2084
失败文件数：    3
条目总数（去重前）：36823
唯一论文数（去重后）：19166   ← 全局索引规模
去重率：        1.9x
耗时：          0.9s
文件大小：      35 MB
```

**3 项验证全过**：
1. **抽样**：JLT 2023 multi-aperture（DOI 10.1109/JLT.2023.3276637）在 JSONL 里，hit_count=3，3 条 queries 正确聚合，first_seen 2026-05-29 / last_seen 2026-05-29 正确
2. **FSO×均衡计数**：JSONL 扫出 130 篇（S002 盘库 142，差 12 = 去重后 DOI 合并，合理）
3. **增量集成**：直接调 `_auto_save` 测试，`[存档]` 行后跟 `[索引] +1 新 / 0 更新` 行，索引自动更新（JLT hit_count +1，FAKE 新论文正确插入，测试后清理）

### 4. 均衡层 seed.md（子 agent 生成）

派子 agent 从 JSONL 扫 FSO×均衡 → `search-archive/_index/by-topic/equalization-seed.md`（26KB，199 行）：
- **117 篇** FSO×均衡唯一论文（134 原始 - 17 离题剔除）
- **8 子地带**：multi-aperture coherent combining 14 / OAM-MIMO 25 / 偏振 PolDemux 17 / DNN/NN 13 / ISI 11 / OFDM-FSO 6 / AO-DSP 5 / 其他 26
- **死地标记**：🔴 OAM-MIMO 均衡族（2014-2026 跨 12 年成熟饱和）
- **3 核心论文**：JLT 2023 multi-aperture MIMO 2N×2（引 13）/ TCCN 2026 Bootstrapping blind VAE（引 0，新）/ Light Sci & Appl 2023 Tbit/s feeder links coherent+AO（引 102）
- **核查**：子 agent 标注基本准确（"引 134"是去重前，去重后 102），未编造
- **落盘率 0%**：117 篇里 0 篇下全文——确认 S002 盘库判断（检索到、评估了、但没下）

### 5. AGENTS.md 更新

文件路径规则表加 3 行（守"AGENTS.md 只加索引行"规则）：
- 全局论文索引 | tools/search 自动维护 | search-archive/_index/all-papers.jsonl
- 索引一次性回填 | tools/backfill_index.py | 重建 all-papers.jsonl
- 专题种子视图 | 手动从索引生成 | search-archive/_index/by-topic/{topic}-seed.md

## 决策引用

- 无新建 D###（机制改动，非方向决策）
- 引用既有：S002 盘库结论 / INVARIANT 6（地勘只找清单不判缝）/ INVARIANT 17（规划完才进阶段 1）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（档 C 是 S002 复用方案的执行，服务阶段 1 地勘）
- 档 C 同时是框架层改进，按 plan 在 framework-evolution 加一条索引（**待办**，未在本轮做）
- 守 INVARIANT "不改框架文件"：未改 stage/glossary/templates，只改 tools/ + AGENTS.md 索引行

## 后续

**已完成**：
- ✅ tools/search 增量索引 + 一次性回填 + 均衡层 seed 生成
- ✅ AGENTS.md 加 3 行索引
- ✅ 验证（抽样 + 计数 + 增量集成 + 清理测试污染）

**待办（不在本轮）**：
- framework-evolution 专题加索引行（"search-archive 索引机制"）—— 跨专题引用
- 阶段 1 第 1 批地勘：PROMPT-001 组 1 改为"seed.md 起步 + 补 2026 下半年新论文"，省 1 个对话
- 本对话末尾统一 commit（守自动提交规则）

**纪律提示（给后续对话）**：
- 索引机制已上线，下次 `bash tools/search "..."` 自动更新索引，不用手动跑 backfill
- JSONL 损坏 / 想重建 → `python tools/backfill_index.py`（幂等）
- 专题起步想用索引 → 派子 agent 从 `all-papers.jsonl` 扫自己专题的关键词 → 生成 `{topic}-seed.md`

### 6. 后续修订（用户 2026-07-10 拍板，同对话续接）

用户核查后指出："已有的这一批质量不知道咋样，最好仅仅是当做参考，让新对话知道该怎么检索。后续再大规模检索？"

**核查数据支持用户判断**：
- 117 篇 FSO×均衡里 **venue 质量**：Trans/Letters 16（12%）/ 期刊 23（18%）/ 会议 18（14%）/ **unknown-preprint-web 73（56%）**
- **年份很新**（2025-2026 占 38%）+ **核心相关度不低**（标题同时含 equaliz+FSO 的 55 篇占 42%）——不是过时货，但 venue 参差
- **16 篇 Trans/Letters 质量硬**：JLT 2010 Pol-Mux coherent 引 93（领域奠基）/ OL 2016 OAM-MIMO 引 97 / TCCN 2026 Bootstrapping / TCOMM 2026 ISI in IRS-FSO

**修订执行**（用户选"当地勘参考地图"）：
1. `equalization-seed.md` 文件头说明改：从"种子清单"→"地勘参考地图（不是种子）"，加 56% unknown 警示 + 16 篇 Trans 硬核说明 + ✅当导航/❌不当种子/❌不跳新检索 三条用法
2. `PROMPT-001-landscape-preflight.md` 加段"## 开工前必读：地勘参考地图"——新对话开工第一步读 seed.md 的 16 篇 Trans + 8 子地带分类 + 🔴 死地标记，**然后仍从零跑组 1-3 检索**，跑完交叉核（新检索 Trans vs seed / seed 🔴 死地新检索确认 / 两表对不上重点追）
3. **关键纪律**：seed.md 是子 agent 启发式词频归类（非定论）+ venue 弱源标"待精读确认"，新检索时以工作对话自己判断为准，seed 只作交叉核

**这一步的价值**：尊重了用户"质量参差"判断 + 不浪费 16 篇硬核 Trans + 8 子地带死地标记的导航价值 + 守 INVARIANT 6/17（地勘只找清单不判缝 + 规划完才进阶段 1）。
