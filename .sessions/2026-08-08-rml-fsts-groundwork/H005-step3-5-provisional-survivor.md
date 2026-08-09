# Handoff: RML-FSTS Step 3.5 主控接收纠偏完成

> 来源: S003 | 交接目标: 用户授权后在新对话只执行 Step 4a feasibility
> 日期: 2026-08-09

## 已完成边界

Step 1–3.5 已完成。D008/V005 保留 R004/D007/V004 的检索、引用链、全文读取与三轮止损事实，但撤回 blanket `EVIDENCE_BLOCKED / NO ENTRY`：共享 canonical 已有 Optics Communications 130981 全文，其动作是固定 STFT/FFT coarse FOE，不是 condition→lag/`B_L`/window selector。Q1 当前为 `PROVISIONAL_SURVIVOR_WITH_FULLTEXT_LIMITATIONS`，Step 4a 尚未启动。

130981 的有效全文增量 read-note 是 `papers/_read_notes/_B5-short-time-spectrum-cfo-increment.md`；DOI 同名旧 note 仍保留为 stale 下载失败历史，不得用其否定 shared canonical 全文。

## 不要做什么

- 不把 provisional survivor 写成首次、novelty closure、Go、METHOD_SIGNAL 或方法成立。
- 不在本对话补跑 Step 4a、smoke、仿真、MVE、方法设计或实现。
- 不把 offline conditioned lookup 包装成 adaptive method。
- 不因一篇后续全文出现碰撞而改写旧 receipts；用新 D/V 血缘修订当前状态。

## 必读

1. 本专题 `topic-index.md`
2. `decisions.md` D008 与 `verifications.md` V005
3. `R004-step3-5-competition-closure.md` 的 D008 amendment
4. `projects/thesis-fso/literature_notes_rml_fsts.md`
5. `stages/gw-feasibility.md`

## 下一步干什么

用户确认后，新对话完整读取 `stages/gw-feasibility.md`，只执行 Step 4a。先做 A0/semantic smoke，判断目标 receiver-visible condition 是否真的改变最优 lag/ranking，并把 dev-frozen modulation/TS-length/receiver-power-conditioned single-lag lookup 作为最强廉价 comparator。

## 纪律（和下一步直接相关）

- provisional survivor 不是首次、novelty closure、Go、METHOD_SIGNAL 或方法成立。
- SSRN 6293357 保持高风险 action-level UNKNOWN；ACP/IPOC 10809664 是次级 comparator 债，取得全文后可回填或推翻当前边界。
- 不把 offline curve lookup 包装成 adaptive method；候选必须产生超出 conditioned single-lag lookup 的 receiver-visible action 增量。
- Step 4a 先做最小 semantic smoke/headroom，不直接搭完整 testbed或跑正式 MVE。
- 四个 `p05_run*.log` 继续保持未跟踪且不动。

## 接口变更（如有代码改动）

无代码改动。

## 失败数据附录（如涉及路线失败）

无 research-object/method-package failure。D007 的 blanket blocker 是主控接收语义错误，不计科学失败；具体根因为漏查共享 130981 全文，并把不同相关性层级的 8 项缺件等强化。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| SSRN 6293357 全文 | exact-action boundary | 高风险 UNKNOWN | 用户/作者/正式版本全文可得后 action read |
| ACP/IPOC 10809664 全文 | strongest comparator coverage | 次级债 | 校园网/IEEE blit 合法取得后回填 |
| Cheng/OE/Dong 缺件 | competition limitation | 非阻断边界债 | 获得全文后更新 claim ceiling |
| target crossover/headroom | Step 4a problem truth | 未验证 | Step 4a semantic smoke |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 当前结果 |
|---|---|---|---|
| Step 3.5 closure | matrix + ≥2源 + 双向链 + 3轮上限/0新增 | `gw-supplement.md` | PASS，带 timeout caveat |
| Exact collision | qualified evidence 中无确认 exact action | R004/D008 | 0 confirmed，不作首次声称 |
| Step 4a cheap comparator | conditioned single-lag lookup 必须存在 | topic invariant 2 | 待执行 |

---
## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证 130981 shared canonical 路径/SHA/action 与 D008 一致
- [ ] 已验证 Q1 当前仅为 provisional survivor，Step 4a=`NOT_STARTED`
- [ ] 已检查 `_registry.yaml` 的 depends_on/conflicts_with
- [ ] 已确认本轮不提前进入 Contract/Execute

## 下一轮

等待用户授权。授权后新对话只执行 Step 4a feasibility，并在 Step 4a terminal 停止。
