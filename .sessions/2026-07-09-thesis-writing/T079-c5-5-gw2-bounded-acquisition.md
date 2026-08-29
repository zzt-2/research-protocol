# Task Brief: C5-5 reliability-driven LDPC budget 候选级 Groundwork Step 2 有界获取

> 来源: S028 / D058 / V033 / T078 | 产出位置: `projects/thesis-fso/apsk-soft-receiver-groundwork/c5-5-step2-coverage-report.md` 与合格全文池
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 20
  action_class: C5_5_GW_STEP2_BOUNDED_ACQUISITION
  mission_checkpoint: CP020
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

为既有 `Q-C5-5` 完成一个最多 3 篇的候选级 GW Step 2 acquisition。优先合法取得并验证 DOI `10.1109/ACCESS.2019.2899106`（residual-decaying informed dynamic scheduling）；再按精确缺口至多取得 2 篇近期 primary fulltexts，覆盖 reliability/stall-aware BP iteration-budget allocation、adaptive maximum iterations 或 ordinary syndrome/CRC early termination 的直接动作与公平比较。

本任务只回答 Step 3 是否有合格全文输入；不得精读形成 Q# 新结论、判 exact collision、改写 T078 terminal、实现、仿真或进入 Step 3。

## 开始前强制读取

1. 根 `AGENTS.md`、`research-direction-lab`、Groundwork Step 2/acquisition 规范与 `tools-guide.md`；运行 task-control validator。
2. 本 brief、topic-index CP020、D058/V033、T078 主报告与 worker log。
3. `projects/thesis-fso/direction-lab/harvest/ldpc-receiver-authority.md`、T041 search archive、现有 C5-5 Step 1 collision/absorption ledger。
4. 本地 `papers/index.json`、`papers/_read_notes/` 与 `papers/**/content.md`；先复用现有资产，不重复下载。

## 获取边界

- **P0 必取**：DOI `10.1109/ACCESS.2019.2899106` 的 canonical fulltext；核对 DOI、题名、版本、来源、content quality，不能只保存 landing page/abstract。
- **P1 至多两篇**：只补 direct action 缺口，关键词围绕 `LDPC reliability-aware iteration allocation`, `adaptive maximum iterations`, `early termination`, `informed/residual scheduling`, `equal complexity/edge updates`。不得扩成一般 LDPC decoding 综述池。
- 至多 4 个聚焦 `tools/search` query；只用项目 `tools/download` 获取，用 `tools/convert` 转换 PDF。主线程不直接 WebSearch。
- 合格全文目标 2–3 篇；至少 1 篇 direct scheduling、至少 1 篇可审 early-stop/iteration-budget comparator。2019 paper 若本身同时覆盖两桶，可只再补 1 篇近期 comparator。

## 每篇只记录 acquisition schema

1. canonical identity、DOI/arXiv/正式性与 meta 来源；
2. local fulltext/readable content 路径、页数/文本质量、公式/算法/实验段是否存在；
3. 仅按全文快速定位标记 `direct scheduling / iteration budget / early-stop comparator / related`，不做承重方法解释；
4. Step 3 必须精读的问题：input/state、action granularity、stop/budget rule、baseline、equal-update口径、overhead、与 `Q-C5-5` 九字段碰撞；
5. duplicate/identity mismatch/paywall/abstract-only 一律不计 qualified。

## Terminal

1. `STEP2_C5_5_READY_FOR_STEP3`：取得 2–3 篇合格全文，含 direct scheduling 与可审 early-stop/iteration-budget comparator，并冻结明确 Step 3 read pool。
2. `STEP2_C5_5_READY_WITH_CLASSIC_LIMITATION`：2019 direct fulltext 合格，但只取得经典/非近期 comparator；允许 Step 3，claim ceiling 预先收窄并保留 recent-neighbor debt。
3. `STEP2_C5_5_EVIDENCE_BLOCKED`：P0 direct fulltext 无法合法取得且没有动作等价的 primary substitute，或内容不足以精读；列唯一 blocker，关闭本包，不实现、不仿真。

## 交付与验证

- 主报告：`projects/thesis-fso/apsk-soft-receiver-groundwork/c5-5-step2-coverage-report.md`。
- 必要 search/archive、paper/meta/content/read-note/index 增量与 usage log；不得修改 `.sessions/`、Skill/controller、仿真/decoder 代码、论文正文、旧报告或旧结果。
- 报告 facts-first，给 pool arithmetic、qualified ledger、coverage、identity/content-quality checks、terminal、冻结 Step 3 read pool 与唯一下一步。
- 墙钟 60 分钟；先本地复用，再 bounded search/acquisition。运行 task-control validator、identity/meta/content-quality audit、路径白名单与 `git diff --check`；一次 commit、不 push。
