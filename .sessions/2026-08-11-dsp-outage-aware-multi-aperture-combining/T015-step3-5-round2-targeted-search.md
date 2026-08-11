# [T015] Step 3.5 Round 2 定向补查

> 2026-08-11 | owner: Step 3.5 主线程 | timebox: 15 min

## 输入事实

- Round 1 query matrix：8 queries，45 unique，MUST=0、SHOULD=0。
- Round 1 citation chains：121 unique，新增 5 MUST + 5 SHOULD，主要债务是直接多孔径自适应竞品与 branch-validity/selection 边界。
- Q001 是 `receiver-visible branch-local validity -> bounded reliability/admission/abstention -> combined sequence + no-valid flag`，位置在 Wang branch-local FS/alignment+phase-correction 与 MRC 之间。

## 唯一目标

做 Round 2 定向补查，验证上述窄 action 是否仍有遗漏。不得下载、精读、判 terminal。

## Query matrix

使用仓库 `tools/search`，2 个实际贡献源为目标，查询应覆盖且可按工具语法拆成 4–6 组：

1. `("branch validity" OR "lock aware" OR "synchronization confidence") AND (MRC OR "diversity combining") AND (optical OR coherent)`
2. `("frame synchronization confidence" OR "phase validity" OR "cycle slip detection") AND (branch selection OR branch admission OR combining)`
3. `(abstaining OR bounded OR robust OR outlier OR invalid branch) AND (MRC OR "maximal ratio combining")`
4. `("DSP outage" OR "receiver outage") AND (multi-aperture OR distributed aperture) AND coherent combining`
5. 必要时用 Round 1 新 identity/术语（dynamic channel tracking、aperture selection、modulus-normalized adaptive cost）做 1–2 个定向 query。

## 筛选纪律

- 逐条语义筛选，不能只依赖 relevance score。
- 对每个 retained 给 input/trigger/action/output 可见部分，以及 MUST/SHOULD/MAY/REJECT。
- 不能从题目推断 exact action；abstract 缺失的承重 direct identity 标 unresolved acquisition debt。
- 与 Round 1/citation shortlist 去重。最终明确本轮 `new MUST` 和 `new SHOULD` 数。
- 若 new MUST/SHOULD=0，标 `ROUND2_SEARCH_CONVERGED`；否则列给下一次 acquire/read/Round3 的精确债务。

## 输出

- raw receipts 存 `search-archive/2026-08-11/step3-5-dsp-r2-q*.json`。
- worker log：`projects/thesis-fso/worker-logs/step-3-5-dsp-outage-round2-targeted.md`。
- 不修改专题控制文件、不提交、不 push。
