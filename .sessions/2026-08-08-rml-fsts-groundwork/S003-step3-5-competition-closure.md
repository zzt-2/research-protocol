# [S003] RML-FSTS mandatory Step 3.5 竞争闭包

> 2026-08-09 | Groundwork Step 3.5 | IN_PROGRESS
> 2026-08-09 续接 | Groundwork Step 3.5 | EVIDENCE_BLOCKED
> 2026-08-09 主控接收 | Groundwork Step 3.5 | PROVISIONAL_SURVIVOR

## 目标

按 `stages/gw-supplement.md` 完成 Q1 的 mandatory Step 3.5 文献与竞争闭包，独立验证后统一提交一次；到 Step 3.5 canonical terminal 停止，不进入 Step 4a。

## 记录

- H003 接收验证通过：Step 3 的 5/5 receipt、修正后 Q1 M-C-A、四判据 4/4、Wang/Enhanced 角色分账与 Step 3.5=`NOT_STARTED` 均有确定性证据。
- Registry 检查通过：本专题依赖 `2026-08-08-ch4-reference-method-extension`（dormant、产出已迁移），`conflicts_with=[]`。
- 用户显式授权将当前范围从 Step 3 扩展到 mandatory Step 3.5；D006 与 topic-index scope-change record 已登记。
- 四个既有未跟踪 `p05_run*.log` 已记录 size/mtime/SHA256 保护基线；本轮不得修改或暂存。
- 本轮科学问题、FACT/INFERENCE/UNKNOWN 与 conditioned single-lag strongest cheap alternative 按用户提示冻结；只裁竞争边界，不比较数值胜负。
- T002 完成本地 21,806 条索引盘点；T003 完成 8/8 matrix、三类真实来源与 Wang/Enhanced 4/4 双向引用链；T004 修复 Tang/WiSEE provenance 并全文排除 exact action。
- R1 新增 must/should=`3/3` 后进入 bounded R2。T005 的 3 篇 must 全文均不可得；T006 的 3 篇 should 中 2 篇 qualified全文为 architecture-adjacent、1 篇阻塞；T007 的 4 项关键旧债务在每篇 4 个不同通道后仍不可得。
- T008 R2 的前三条 query 共 63 条，48 个新标题全排除、new must/should=`0/0`；Q4 超时。T009 R3 源限定补查仍超时，`round_limit_reached=true`，禁止 R4。
- R004/D007 将 Step 3.5 终止为 **证据阻塞**：qualified evidence 未确认 exact collision 或 cheap lookup 等价，但 8 项关键全文不可得，不能闭合 novelty/competition boundary，Step 4a 不开放。
- T010/V004 fresh-context 独立终验 10/10 gates PASS，P0/P1/P2=`0/0/0`；唯一合法 terminal=`EVIDENCE_BLOCKED`，Step 4a=`NO ENTRY`。
- 四个 `p05_run*.log` 的 size/mtime/SHA256 与启动基线一致，始终未跟踪、未暂存。
- 主控接收审查发现 D007/V004 terminal 过严：框架三轮上限不要求所有候选全文齐备；8 项也不是等强 exact blocker。
- 共享 canonical 已有 Optics Communications 130981 全文与 read-note，执行阶段因只查 worktree stale metadata 误报 unavailable；正文排除 condition→lag/`B_L`/window collision。
- D008/V005 将 Q1 修订为带全文限制的 provisional survivor；当前只开放后续 Step 4a 讨论入口，本轮仍未执行 Step 4a/实验。

## 决策引用

- D006：仅将当前范围扩展到 mandatory Step 3.5，并在 canonical terminal 停止（新建）。
- D007：Step 3.5 终止为证据阻塞且不开放 Step 4a（新建）。
- V004：Step 3.5 独立终验 PASS，确认唯一 terminal 与提交边界。
- D008/V005：取代 D007/V004 的 terminal 科学语义；保留其机械证据与检索事实。

## 范围确认

- 本轮是否在 scope boundary 内：是（见 D006 与 topic-index 2026-08-09 scope-change record）。

## 后续

主控接收修订已完成。下一科学动作是用户授权后在新对话只执行 Step 4a feasibility；必须携带 cheap conditioned single-lag comparator 与全文限制，不得把 provisional survivor 当 Go。
