# T010: Fresh-context Step 3 verifier

> 2026-08-11 | assignee: independent verifier | timebox: 15 minutes

## 目标

独立核验 Step 2 narrow repair 与 Step 3 五篇全文综合是否满足本轮合同。不得依赖主线口头结论，不得实现、仿真、搜索或下载。

## 必读

- `stages/groundwork.md`, `stages/gw-read.md`, `stages/glossary.md`, `domain-comms.md`
- 专题 `topic-index.md`, `decisions.md`, `S003-step2-repair-and-step3-read.md`
- `R002-step2-acquisition-coverage.md`, `R003-step2-acquisition-receipt.md`, `R004-step3-direct-competitor-synthesis.md`
- `projects/thesis-fso/literature_notes_dsp_outage_multi_aperture.md`
- T007–T009 与三个 `projects/thesis-fso/worker-logs/step-3-dsp-outage-read-*.md`
- 五篇 `papers/_read_notes/`：Johst 2024、Wang 2023、Liu 2023、Tu 2020、Yang 2022
- `projects/thesis-fso/read-log.md`, `projects/thesis-fso/master-state.md`, `.sessions/_registry.yaml`

## 核验清单

1. Step2 repair：JLT title/DOI/path/SHA/lines 是否闭合；qualified=5 是否由五篇真实全文组成；2019 未被当全文。
2. 五篇 identity/title gate 与每篇 14+字段、7结构段、通信参数、实验完备性是否齐全；2–3 个 writing architecture 是否存在。
3. 动作矩阵是否准确区分：2019 broad unknown、JLT estimator-changing、Johst hard discard、Tu known-OSNR admission、ICCC pilot-attenuation soft weight、Wang post-DSP MRC。
4. Q001 的 M/C/A 与 glossary 四判据是否具体、可证伪、baseline 合法；是否把 strongest cheap comparator 纳入且没有 EGC strawman。
5. 2019 limitation 是否始终为 exact action `UNRESOLVED`，且仅在 Q001 存活时移交 Step 3.5。
6. 范围是否严格停在 Step 3：无 Step3.5/4a、算法公式、实现、仿真、Go/Kill/METHOD_SIGNAL。
7. read-log/topic/master/registry/D003/D004 是否一致；检查重复 read-note/casing/path 问题与 `git diff --check`。

## 输出

只创建 `projects/thesis-fso/worker-logs/step-3-dsp-outage-independent-verifier.md`，给：

- verdict=`PASS|FAIL|PARTIAL`
- critical/major/minor counts
- 每个 finding 的文件+行或锚点
- terminal 是否被证据支持
- scope violation count
- 可机械执行的修复建议（若有）

不得修改其他文件。回执只给 verdict/counts/output path。
