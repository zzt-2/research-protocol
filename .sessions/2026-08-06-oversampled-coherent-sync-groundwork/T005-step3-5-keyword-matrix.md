# Task Brief: Step 3.5 系统关键词矩阵与竞争者筛查

> 来源: S001 | 产出位置: `projects/thesis-fso/worker-logs/step-3-5-sync-search.md`
> 日期: 2026-08-06
> 唯一文档: 执行方可读取本 worktree 的框架、现有 Step 1–3 证据与搜索工具

---

## 0. TL;DR（执行方先读）

你在 `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`。
**你的任务**：只围绕 Q1 完成最多三轮 Step 3.5 系统关键词矩阵检索，筛出真正同信息、同动作、同任务的竞争者。
**产出**：结构化 worker log，写到上述路径。

**最高纪律（违反一条就废了）**：
1. 使用项目 `tools/search`，搜索结果必须落到 `search-archive/2026-08-06/`；不得改 canonical 会话/项目状态文件。
2. 明确区分 generic shared-preamble/resource reuse、sequential timing/frame/CFO、真正 joint `(frame, τ, CFO)` estimator。
3. abstract 只用于筛查，不得作为 exact-action novelty/collision 的全文裁决。
4. 最多三轮；最后一轮新增必读/建议读为 0 才称收敛，否则记录未覆盖项。
5. 不进入 Step 4a、不写代码、不跑仿真、不修改 protected paths、不提交。

## 1. 背景

Canonical Q1：M=`Le Bidan 2-sps 顺序 acquisition chain + Sun/Wang frame–FOE`；C=`RRC、≥2 sps coherent FSO，fractional timing、frame、CFO 同时未知`；A=`顺序 timing-first 处理在同时未知状态下可能传播误差或产生错误峰/误锁`。Q1 已按 glossary 四判据成为 Step 3 survivor；Step 3.5 只做竞争闭包，不证明方法可行。

## 2. 任务详情

### 2.1 要回答的问题

- 构造方法变体×问题场景/动作语义矩阵，至少三类方法变体、每类至少两个组合。
- 检索是否已有同 receiver-known sample-level information 下直接输出联合 `(frame, τ, CFO)` 的 estimator。
- 识别最高相关 direct competitor，并给出 DOI/arXiv/venue/year/abstract 支持的动作分类。
- 给出新发现论文的 `必读/建议读/排除` 分级；高相关项必须指出 acquire→read 需求。

### 2.2 执行方式

1. 先读 `stages/gw-supplement.md`、`projects/thesis-fso/literature_notes_oversampled_sync.md` 和 Step 3 report。
2. 使用 `tools/search` 覆盖至少两个来源；每轮记录完整 query 矩阵、输出 JSON 路径和新增候选数。
3. 对 web/search 断言用 Semantic Scholar/OpenAlex/DOI abstract 交叉验证。
4. 只写 worker log；不得替主线裁决 survivor 或 terminal。

### 2.3 产出格式（强制）

```markdown
# Step 3.5 Q1 keyword-matrix search
## 执行环境与命令
## 关键词矩阵
## Round 1/2/3
| query | sources | archive JSON | raw/unique | new must/should |
## 候选表
| title | year | DOI/arXiv | abstract-supported action | class | relevance | acquire/read |
## 三类语义边界
## 收敛与未覆盖项
## 结论（只陈述检索事实，不做 Step 4a 判断）
```

## 3. 已知陷阱

- 标题含 `joint synchronization` 不等于 joint `(frame, τ, CFO)` action。
- 同一 preamble 分区做 clock 与 frame/FOE 仍是 resource reuse / sequential。
- `frame+CFO` 已被多篇占用，不能据此声称 exact collision。

## 4. 验收

- [ ] 矩阵满足 ≥3 方法变体且总组合 ≥ 方法变体数×2。
- [ ] 搜索源 ≥2，所有结果有 archive JSON。
- [ ] 每个高相关候选有 DOI/arXiv 与 abstract 交叉验证。
- [ ] 最多三轮并明确收敛状态。
- [ ] 没有修改 canonical 状态、代码、实验和 protected paths。

## 附：产出回传位置

`projects/thesis-fso/worker-logs/step-3-5-sync-search.md`
