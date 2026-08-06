# Task Brief: Step 3.5 focused Round 2 convergence search

> 来源: S001 | 产出位置: `projects/thesis-fso/worker-logs/step-3-5-sync-search-r2.md`
> 日期: 2026-08-06
> 唯一文档: 执行方可读取 T005/T006/T008 worker logs 与 Round 1 JSON

## 0. TL;DR（执行方先读）

只执行一个 focused Round 2，用 Round 1 已暴露的 semantic gap 检查是否仍有新增 must/should；不重跑
Round 1，不做 acquisition，不启动 Round 3。产出新增相对 R1+引用链+已读论文的确定性去重表。

最高纪律：仅使用 `tools/search`，最多 3 个 query；至少请求 S2/OpenAlex/arXiv；全部落
`search-archive/2026-08-06/step35-r2-*.json`；摘要只筛查；不改 canonical；不提交。

## 1. Query 冻结

1. `single objective joint frame sampling phase carrier frequency offset coherent optical`
2. `fractional delay frame frequency joint estimator single carrier coherent optical burst`
3. `preamble joint burst arrival sampling phase carrier frequency offset estimator`

不得加第 4 个 query。若工具超时，只补缺项，不重跑成功项。

## 2. 判定

- known set：T005 的 80 unique、T006 43 citation entries、T008 P1/P2/P3。
- 新 must：摘要明确 coherent optical 且同一 estimator/objective 涉及 frame/burst position + fractional
  sample timing/phase + CFO。
- 新 should：缺一动作但为 2019+ direct coherent optical estimator/preamble competitor。
- 只列真正新增；重复 DOI/arXiv/title 计 0。

## 3. 产出

写命令、3 个 JSON、raw/unique、相对 known-set 新增 must/should 表、semantic 分类、Round 2 新增数与
是否达到新增=0。若非 0，只记录给主线决定 Round 3，不自行继续。

## 4. 验收

- [ ] 恰好最多 3 query，无 R1 重跑。
- [ ] 相对 known set 确定性去重。
- [ ] 新增 must/should 有 DOI/arXiv 与 abstract-supported reason。
- [ ] 无 canonical/代码/实验改动。
