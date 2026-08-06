# Task Brief: Q2 canonical 判据 3 与廉价 comparator 独立裁决

> 来源: S001 | 产出位置: `projects/thesis-fso/worker-logs/step-3-5-q2-baseline.md`
> 日期: 2026-08-06
> 唯一文档: 执行方可读取现有 7 CORE notes、搜索索引与框架 owner

---

## 0. TL;DR（执行方先读）

**你的任务**：独立判断 Q2 是否存在“具体、近期、task-matched baseline M”，并核查最强廉价 comparator 的文献身份；不要把“共同失锁尚未实验证实”继续当判据 1 FAIL。
**产出**：证据表写入指定 worker log。

**最高纪律（违反一条就废了）**：
1. 判据 1按 glossary：M/C/A 明确、句子级、可解即可；A 可证伪，不要求已由 Step 4a/MVE 证实。
2. 判据 3必须是一篇/一套可引用的 2019+ task-matched baseline；不得用 Gu+Paillier+Valjus 跨论文拼接伪造 integrated baseline。
3. 区分文献已有 baseline 与主线构造的 fair cheap comparator contract；后者不能自动满足判据 3。
4. 只检索和裁决，不改 canonical 文件、不实现、不仿真、不提交。

## 1. 背景

Q2：M=`timing loop + carrier loop 独立 maintenance/reacquisition，候选 cheap extension 为 shared freeze + fixed known-preamble restart`；C=`≥2-sps RRC coherent OSL，SCO/drift、CFO/Wiener PN 与 dynamic deep fade`；A=`fade 可使 timing/carrier 检测器共同或异步失锁，且廉价 shared-freeze/fixed-restart 可能不足`。现有 D005 把 A 未经实验证实误作判据 1 FAIL，需纠正；判据 3必须独立裁决。

## 2. 任务详情

### 2.1 要回答的问题

- 现有 7 CORE 或本地索引中是否有 2019+ integrated timing+carrier maintenance/reacquisition baseline？
- 若需补检索，是否出现具体 task-matched baseline，还是仍只有单环/综述/顺序模块拼接？
- `polyphase/Farrow timing bank + sequential Le Bidan/Sun/FSTS/STSB chain` 是否是 Q1 最强廉价 comparator；Q2 的 shared-freeze+fixed-restart 是否仅为主线构造的 fair comparator contract？

### 2.2 执行方式

1. 逐字读取 `stages/glossary.md` L22-31、现有 Step 3 report、literature notes 与相关 read notes。
2. 确定性搜索本地索引；必要时用项目 `tools/search` 补一轮 task-matched query并落盘。
3. 对候选逐一列 information/action/output/timing/task fit 与年份/venue/DOI。

### 2.3 产出格式（强制）

```markdown
# Q2 baseline adjudication
## Canonical 判据 1 重判
## 候选 baseline 表
| paper/system | year | DOI | information | action/output | integrated? | task fit |
## 判据 3 verdict
## Q1 最强廉价 comparator closure
## Q2 cheap comparator contract 边界
## 结论
```

## 3. 已知陷阱

- `分别讨论 timing 和 carrier` 不等于 integrated baseline。
- 一套工程上可构造的组合链不等于近期文献 baseline M。
- 未经实验验证的 A 仍可满足 Step 3 判据 1，只是留给 Step 4a。

## 4. 验收

- [ ] 判据 1未再要求 MVE/量化失效证据。
- [ ] 判据 3逐候选 task-fit 核查并给出明确 PASS/FAIL。
- [ ] 无跨论文拼接伪造 baseline。
- [ ] Q1/Q2 cheap comparator 边界清楚。

## 附：产出回传位置

`projects/thesis-fso/worker-logs/step-3-5-q2-baseline.md`
