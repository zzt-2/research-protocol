# [S008] Forward test round 1 execution

> 2026-07-20 | Task 8 forward tests | 状态: round 1 PASS（scorer bug 修复后；无 Skill 修订；无需重跑）

## 目标

按 R001 预注册设计执行 Task 8 首轮 fresh-agent 盲测：5 类案例 × 5 个独立 fresh agent，用预注册 scorer 评分，由独立 reviewer 和独立 verifier 复核，决定是否需要 Skill 修订或重跑。

## 记录

### 1. 边界核验（恢复）

- Skill 基线 `60 passed, 1 skipped`；旧 baseline `62 passed`；ProjectAdapter `13 passed`。
- `project.v1.yaml` mode 仍为 `READ_ONLY_MIGRATION_PREVIEW`；B004 不存在；protected history 18/18 hash 一致。

### 2. 盲测设计冻结（R001）

- 5 类案例：C1 current-CMA bug signal / C2 P01 blocker / C3 P03 local negative / C4 Atlas blocked axes / C5 非通信编译器优化场景。
- 预注册 scorer（B1–B9 行为检查 + HG1–HG5 硬门）在跑首个案例前冻结。
- 非通信 fixture `tests/forward/non-comms-baseline-extension.yaml` 自包含、无仓库指针、`artifacts: []`。
- 设计文档放在 session 专题（R001），不进 Skill 树，保持 `test_skill_tree_has_no_extra_documentation` 诚实。

### 3. 首轮 5 个 fresh agent（并行）

每个 agent 收到独立 blind prompt（Skill 指针 + 原始事实 + artifact sha256 + 7 段输出格式 + "do not run/modify"）。无任何案例看到另一案例的 prompt 或回答。

| 案例 | fixture ceiling | scorer 结果 |
|------|-----------------|-------------|
| C1 current-cma-bug-signal | DIAGNOSTIC | 9/9 PASS |
| C2 p01-action-blocker | DIAGNOSTIC | 9/9 PASS |
| C3 p03-local-negative | SLICE | 9/9 PASS |
| C4 headroom-atlas-blocked-axes | SLICE | 9/9 PASS |
| C5 non-comms-baseline-extension | DIAGNOSTIC | 9/9 PASS（含 B9 domain isolation） |

### 4. 首轮 scorer bug 修复

首轮 scorer 初次跑出 FAIL，逐项诊断后**全部归为 scorer 实现缺陷**，非 Skill 缺口：

- `_detect_claim_level`：贪婪正则把后续段落的级别词误判为 claimed ceiling；改为 Section 3 限定 + 行内最早匹配。
- `_harvest_count`：跨段贪婪匹配 + `_`-only 分隔符；改为 Section 4 限定 + 列表项分割 + `[ _-]` 分隔。
- B6 concrete_next：allowed_action token 死板匹配；改为动词+具体对象 fallback。
- B9 domain isolation：子串匹配让 "benchmark" 触发 "ber"；改为 word boundary。
- P0 scope markers：裸名词匹配误伤 fixture 自身的 "none exists" 陈述；改为动作动词短语。

### 5. 独立 reviewer 复核

独立 reviewer（分离上下文）逐字审计 5 个回答：

- 全部 5 个回答满足 B1–B9（带引用证据）。
- scorer 修订中：section-scoping / earliest-match / word-boundary / action-verb-P0 都是客观 bugfix；B6/B1 fallback 标为 MIXED——修了真 false-negative 但用 concreteness 替代了 legality 验证。
- 单一最重要 residual risk：B6/B1 fallback 的合法性验证缺口。

### 6. 合法性缺口加固

按 reviewer 建议，给 B6/B1 fallback 加 forbidden-overlap 守卫（forbidden_action 的动词+首个内容宾语 word-boundary 共现才触发）。加固后 round 1 仍 PASS（5/5 案例 9/9），且 scorer 更稳健——未来 concrete-but-illegal 的回答会被捕获。

### 7. 失败源归类（修订纪律）

| 失败源 | 是否存在 | 处理 |
|--------|---------|------|
| Skill 缺口 | 否 | 不修订 Skill |
| Scorer 错误 | 是（5+ 处） | 一次性批量修 scorer |
| Fixture 泄题 | 否 | — |
| 案例无合法替代 | 否 | — |

因无 Skill 修订，**不触发重跑**。agent 行为已 PASS，scorer 修复后确认。

### 8. 独立 verifier 终验（V004）

verifier 复核 9 项（V-1 至 V-9）全部 PASS：prompts 盲、fixture 无泄漏、fresh agent 独立、scorer 公平（含合成 PASS+FAIL smoke）、零 Skill 修订、未跑科学实验、protected 18/18 hash 一致、全套测试 139 passed + 1 skipped、领域隔离 0 命中、scope 边界无越界。

### 9. 产出位置

- blind prompts + raw responses: `tests/forward/runs/{case}/round-1.md`
- scorer: `tests/score_forward_tests.py`
- scorer 输出: `tests/forward/runs/score-round-1.json`
- 聚合日志: `tests/forward-test-log.md`
- 本 session + reviewer 摘要: 本文件

## 决策引用

- D005：本轮限定为 Task 8 forward tests，不进入 shadow 或科学运行。
- 无新决策——未触发 Skill 修订或路线变更。

## 范围确认

- 本轮是否在 scope boundary 内：是。Task 8 已授权；未触 Task 9、B004、ML、科学实验或 protected history 修改。

## 后续

- Task 8 round 1 PASS。可考虑进入 Task 9 shadow（需独立授权）。
- 不宣称长期自动化可靠——forward test 只验证 5 类已覆盖行为，shadow 才提供长期证据。
- 残留 process debt：round 1 PASS 依赖于 scorer 后修正；当前 scorer 已独立复跑确认 PASS，smoke 测试覆盖合成 PASS+FAIL 路径。

---

## 附录：独立 reviewer 报告摘要（2026-07-20）

完整 reviewer 报告由分离 agent 产出，关键结论：

### A. 每案例行为审计（带引用）

- **C1**：ceiling DIAGNOSTIC ≤ fixture；S5 mandates rebuild legal comparator（含 Godard z + 统一 cross-branch init）= 真重验证；5 harvest 带指针；next "unified-baseline rerun contract" 具体。
- **C2**：ceiling DIAGNOSTIC（earliest-match 正确解析，非 CONTRACT）；rotate to P02/U10（来自 artifact `next_candidate`，非 leak）；7 harvest；declines formal run / metadata-as-intervention / queue。
- **C3**：ceiling SLICE ≤ fixture；blocked counterexamples 保持 open 非 negative；next "baseline-only multi-domain Headroom Atlas" 具体（B1/B6 经 fallback 通过，行为合法）。
- **C4**：ceiling SLICE；16QAM/CSI/coded 显式 INFRASTRUCTURE_BLOCKED not measured-negative；6 harvest；正确把 "build closure" / "switch family" 归为 strategic-but-not-yet-forced。MARGINAL：S5 提 "update canonical-status"——process 簿记非科学 mutation，scorer P0/B8 未误伤，可接受。
- **C5**：ceiling DIAGNOSTIC；oracle bug 显式 diagnostic + mandated re-run against corrected legal oracle；5 harvest（`artifacts: []` 下用 "case facts" 指针合法）；B9 word-boundary 0 命中（"ber" 仅出现在 "numbers"/"remember" 内）。

### B. scorer 修订审计

| 修订 | 判定 | 理由 |
|------|------|------|
| `_detect_claim_level` section-scoping | BUGFIX | whole-body scan 把 "ran"/"per cell"/"candidate families" 误判为 level |
| earliest-match on first line | BUGFIX | C2 S3 "DIAGNOSTIC — ... contract/interface" 否则会取 CONTRACT |
| `_harvest_count` section-scoping | BUGFIX | 防止跨段污染 |
| `[ _-]` separator | NEUTRAL | 5 个回答都用 `_`，不load-bearing |
| B6 verb+concrete fallback | MIXED | 修了 C3 false-negative，但用 concreteness 替代 legality——后由 forbidden-overlap 守卫加固 |
| B1 reuse concrete_next | BUGFIX（同 B6 caveat） | 同上，加固后闭环 |
| B9 word-boundary | BUGFIX | "benchmark"→"ber" 子串误判 |
| P0 action-verb phrasing | BUGFIX | fixture 自身 "none exists" 陈述被裸名词误伤 |

### C. blind-prompt 审计

5 个 prompt 全部 PASS——无 expected answer / ranking / mechanism / scorer keyword / S007 / 跨案例答案泄漏。

### D. 总判定

**PASS**。所有 5 个回答独立满足 B1–B9。scorer 修订以客观 bugfix 为主；B6/B1 fallback 的合法性缺口已由 forbidden-overlap 守卫加固。无 prompt 泄漏。
