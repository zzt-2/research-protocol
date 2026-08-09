# Task Brief: RML-FSTS Step 3.5 独立终验

> 来源: S003 | 产出位置: `projects/thesis-fso/worker-logs/step-3-5-rml-independent-verifier.md`
> 日期: 2026-08-09
> 唯一文档: 执行方只需本 T 与目标 worktree；fresh context，不继承实现者判断

## 0. TL;DR（执行方先读）

你在 `D:/code/study/research-protocol/.worktrees/rdl-method-production-v2`。本轮声称只执行 mandatory Step 3.5，并以“证据阻塞”停止。
**你的任务**：独立核验 scope、检索/引用链、identity/fulltext/SHA、动作分类、cheap lookup、terminal、current views、禁区与 p05；按 P0/P1/P2 报告。不要修改任何文件，除指定 verifier log。

**最高纪律**：
1. 不相信 R004/D007 的总结；从 raw receipts、实际文件、git diff 与 hashes 反向核验。
2. abstract/metadata 不能替代全文 action；缺全文项应保持 UNKNOWN。
3. exact collision、generic multi-lag、offline optimization、conditioned lookup equivalent、architecture adjacent 必须逐类审查。
4. 终态只能是 Q1存活闭包 / Q1被关闭 / 证据阻塞之一；检查证据是否唯一支持当前“证据阻塞”。
5. 不修文件，不运行搜索/下载，不进入 Step4a，不触碰 p05。

## 1. 必读与证据

1. 本专题 `topic-index.md`、S003、R004、D006-D007、H004、V003
2. `projects/thesis-fso/literature_notes_rml_fsts.md`、`master-state.md`、`.sessions/_registry.yaml`
3. T002-T009 worker-logs
4. `search-archive/2026-08-09/` 下所有 `rml-fsts-step3-5-*receipt.json` 与其指向 raw
5. `papers/index.json`、T004/T006 qualified content/read-notes 的实际 SHA/bytes/title/DOI/action lines
6. `git status/diff` 与四个 p05 baseline

## 2. 强制验证 10 项

1. scope-change 授权只到 Step 3.5，D006/voice/topic 一致，未进入 Step4a。
2. R1 keyword matrix=8/8、actual sources≥2、R2/R3 轮次与超时语义真实。
3. Wang+Enhanced forward/backward citation chain 4/4，返回/去重/筛查数字可复算，S2-only 处理正确。
4. 每篇承重论文有 identity/fulltext/path/SHA/bytes/action evidence；全文不可得项未伪承重。
5. exact collision 与 generic multi-lag/offline/adjacent 区分正确。
6. dev-frozen modulation/TS-length/receiver-power-conditioned single-lag lookup 被保留且未包装成 adaptive。
7. terminal 是否由证据唯一支持；是否诚实避免“未找到=新颖”。
8. 未进入 Step4a/实验/仿真/MVE/设计实现，`common/`/`params.py`/正式论文/dormant campaign 无 diff。
9. topic/literature/master/registry/S003/R004/D007/H004 current views 一致，object/package failure=`0/0`。
10. 四个旧 `p05_run*.log` size/mtime/SHA 与基线一致且未暂存；无工具 cache/临时副作用。

## 3. 额外机械检查

- 解析所有 JSON receipts 与 registry YAML；重算 receipt 指向 raw 的 SHA256/bytes/count。
- `git diff --check`；列出 tracked/untracked/staged。
- 检查 `papers/index.json` 两个新增 success entry 的路径/title/status/read-note 与 actual files 一致。
- 检查被忽略 receipts/raw 是否存在；不要因为 gitignore 就跳过。

## 4. 产出格式（强制）

1. `# Independent Verification`
2. `## Verdict`：PASS/PARTIAL/FAIL + P0/P1/P2 counts
3. `## Ten-gate table`：每项 PASS/FAIL、方法、原始证据
4. `## Mechanical evidence`：命令输出/计数/hash
5. `## Findings`：每条 P0/P1/P2，说明为何承重、最小修复
6. `## Allowed disposition`：当前 terminal/Step4a entry/commit permission

P0=科学或范围完整性破坏；P1=承重证据/一致性缺陷；P2=非承重可读性/轻微治理问题。无 finding 时明确 `none`。

## 5. 验收

- [ ] 10 项逐项有实际验证证据，不接受 checklist 自述。
- [ ] receipt/hash/count 可复算。
- [ ] verdict 明确说明是否允许统一 commit、是否开放 Step4a。
- [ ] 仅新增指定 verifier log。

## 附：产出回传位置

`projects/thesis-fso/worker-logs/step-3-5-rml-independent-verifier.md`
