# [T016] Step 3.5 independent fresh-context verifier

> 2026-08-11 | owner: Step 3.5 主线程 | timebox: 15 min

## 验证范围

独立核查本专题 Step 3.5 最终产物，不修改科学结论或控制文件：S004、R005、D005/D006、H004、topic-index、master-state、registry、literature owner/read-log、T011–T015 worker logs、Zhang canonical note、raw search/citation receipts、acquisition metadata。

## 必查

1. 机械计数：Round1 8 receipts/115 raw/45 unique；citation 7 receipts/134 raw/121 unique；Round2 6 receipts/6 raw/4 unique；最后一轮 new MUST/SHOULD=0/0。
2. 来源：Step3.5 整体至少 S2+OpenAlex 两个实际贡献源；不能把限流/0结果写作贡献。
3. Identity/content：Zhang title/DOI/SHA/line pointers；Sun/Xie/Chen/Qiu/Li fulltext availability 与 metadata/receipt 不得冒充全文。
4. 动作语义：R005 的 input/position/trigger/action/no-valid/state/output 分类是否由一手支持；`EVIDENCE_BLOCKED` 是否符合“无 confirmed collision，但承重 direct exact-action 仍不确定”。
5. Scope：Step4a/implementation/simulation/method design=0；完整 post-all-FS/CE/CPE 仍 excluded；coded/b3/unrelated dirty files 未改。
6. 控制面：topic/master/registry/literature/H004 一致；D004→D006 血缘；H004 模板完整。
7. Git：列出本任务应提交文件与必须排除的 unrelated dirty/p05/coded/pycache/profile/index 文件；`git diff --check`。

## 输出

- 写 `projects/thesis-fso/worker-logs/step-3-5-dsp-outage-independent-verifier.md`。
- verdict 仅 `PASS` / `PARTIAL` / `FAIL`，给 critical/major/minor 数字和逐项证据。
- 不修文件、不提交、不 push。
