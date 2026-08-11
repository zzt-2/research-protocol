# [T014] Step 3.5 Zhang 2023 定向全文精读

> 2026-08-11 | owner: Step 3.5 主线程 | timebox: 15 min

## 派遣标题

Flexible Phase Synchronization for Coherent Free-Space Optical Communications Based on Adaptive Fractionally-Spaced Blind Equalization Combined With Adaptive Kalman Filter

## 目标

精读现有全文 `papers/downloads/2026-07-08/10301506.md`，闭合与 Q001 有关的 exact action signature，并核其对 Sun 2019 的一手引用语境。

## 冻结 Q001

M=Wang branch-local FS/alignment+phase-correction→MRC；C=pre-MRC 支路功率与 FS/phase validity 异质；A=校正不等于 validity，invalid 支路仍可能非零进入 MRC。候选输出仅为 branch-local validity→bounded reliability/abstention→combined sequence+no-valid flag。

## 必须抽取

- title/identity 自检；input；branch 位置/处理顺序；trigger；weight/admission/abstention；no-valid flag；statefulness；output。
- 明确 Zhang 自己的方法与 Sun 引文分别支持什么，不得向 Sun 投射 Zhang 动作。
- 对 Q001 分类只能是 exact collision / cheap absorption / neighbor / unresolved，并逐字段说明。
- 按当前 literature owner/read-log 的既有格式产出新全局 read note；本轮定向精读无需重做已在 Step 3 完成的 7 子表/实验完备性总表，但动作签名必须给原文行号。
- 写 `projects/thesis-fso/worker-logs/step-3-5-zhang-2023-exact-action.md`。

## 禁止

- 不判 Step 3.5 terminal，不设计方法、不实现、不仿真、不进 Step 4a。
- 不修改 D/V/H/master/registry，不提交、不 push。
