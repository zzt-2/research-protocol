# Decisions — Research Direction Lab 长程真实运行测试

## D001: Phase 2 首包续接合法 B1 carrier，不跳转 C15

> status: active
> date: 2026-07-26
> 取代：无
> 扩展：formal D013 / system D018 / mission CP007
> 被取代：无
> 依据：`projects/thesis-fso/master-state.md` 当前控制面与 FR-22 + T007 phase-1 critic
> 触发原话：无（技术纠偏；用户只要求交付下一提示词）

### 决策

Phase 2 第一包为 B1 adaptive phase-window 的 **identity-repaired method-production
package**。C15 虽有现成代码，但未完成当前 formal owner 要求的新候选 Step 1–3；
直接运行会违反 FR-22。它保留为后续 candidate，不以“portfolio 可运行”冒充
“formal 已授权”。

B1 已有 Step 1–3 与 formal D013，且 T007 的当前 oracle 诊断仍显示约 0.4–1.0 dB
局部空间；其 Kill 未被主控接收。T008 只关闭五个已知身份缺口，若合法空间仍在，
同一包必须完成三个 receiver-visible 方法及 fresh-seed paired comparison。

### 正向方法合同

- `positive_method_target`：receiver-visible、低复杂度 adaptive phase-window CPE。
- `minimal_construct`：physics-ratio rule、validation lookup+hysteresis、
  confidence-safe selector。
- `fair_comparator`：validation-frozen global fixed window；per-condition fixed 作强对照。
- `primary_packaging`：面向 GG block-SNR 与 Wiener phase-noise 联合变化的自适应窗。
- `fallback_packaging`：合法 fixed-window 选择与 receiver-observability 工作区边界。
- `next_positive_action`：执行 T008；identity 修复后同包跑方法，不再单独派纯修复包。

### 已知五个缺口

1. B* 疑似按 seed/test truth 重选，而非 validation 全局冻结；
2. required-SNR 使用硬编码 log-BER slope，而非真实 SNR 曲线；
3. oracle/B* 候选集合与选择身份未完全闭合；
4. observability 缺 held-out exact-window accuracy 与 majority-fixed 对照；
5. 仅凭当前特征 `|rho|<0.5` 把 0.4–1.0 dB diagnostic headroom 提前 Kill。

### 边界

- 只在 GW Step 4a；不进 Step 5/Contract/Execute。
- executor 不更新 formal/current/master/mission owner。
- 任一 identity 无法闭合则 `BLOCKED_IDENTITY`，不作科学裁决。
- headroom 存在但方法不胜则 `METHOD_FAIL_WITH_SPACE`，不 Kill 整个 family。
- 不修 Pilot-Jones、B10/B12、C15 或 dormant science-scout。

