# [S003] Groundwork Step 3 全文精读

> 2026-08-12 | Groundwork Step 3 | COMPLETE / VERIFIED

## 目标

精读 9 篇 qualified 全文，统一抽取动作与复杂度合同，裁 TCOM 2016、cheap/near comparators 与 D1/D2 的边界，并只在 glossary 四判据 4/4 时形成 canonical Q001。

## 记录

### H002 接收核验

- 已核 commit `5a1ef98` 为 Step 2 终点，且 worktree 中 unrelated dirty 已单列排除。
- 已核 R004/V002/machine receipt：12 篇审计、9 篇 qualified、8 篇 CORE；A/B/C 三路线均有全文。
- 已核 P0 reference C01 与 full-mixture C02 均 qualified，C06/C07/C13 为保留 limitation，不阻断当前精读。
- 已核 registry：depends_on 为 `2026-08-08-ch4-reference-method-extension` 与 `2026-07-09-thesis-writing`，`conflicts_with: []`，与 topic-index 一致。
- 已确认当前授权只取代 D003 的 Step 3 gate，不改变原始目标，也不开放 Step 3.5/4a/实现/仿真。

### 执行边界

全文按 A reference/unwrap、B full tracker、C recent task/cheap 三组委托 fresh 子 agent；每组只返回结构化证据，主线程统一写 owner/read-log，避免并发写冲突。

### 精读与综合结果

- 三个 fresh reader 分组完成 C01/C09/C14、C02、C05/C08/C10/C11/C12，共 9/9；单 agent 均在 15 分钟约束内，只返回结构化结果、未并发写 owner。
- C05/C09/C10 公式回看 source PDF；C11 跳过 publisher chrome；C02/C08 由 source TeX 关闭 title gate。
- C02 仅在 multi-trajectory primitive capability 轴为 full-general superset；task contract 为 strong neighbor，非 exact collision。
- D2 被 cheap alternatives 分块吸收，不单列 Q；D1-shaped Q001 四判据 4/4，terminal 见 D005/R005。

## 决策引用

- D004：接受 Step 2 coverage，只授权 Step 3 全文精读（新建）
- D005：Step 3 只保留 D1-shaped Q001，D2 降为可选组件（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是（D004）

## 后续

fresh verifier V003 PASS（P0/P1/P2=0/0/0），H003 已写。Step 3.5 需新的显式授权。
