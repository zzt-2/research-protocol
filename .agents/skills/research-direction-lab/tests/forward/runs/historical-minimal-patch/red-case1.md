# RED Case 1 — scale/action

> baseline bundle: `91f306ef72b54dc883b52a9683629b4dff54a0f6ce985d22bd34c33e3822f1ab`
> fresh context, read-only, raw adjudication reproduced verbatim below

裁决：**现在既不应扩更多 cells/seeds，也不能直接认定为 `METHOD_SIGNAL`。应暂列为 `UNRESOLVED_DIAGNOSTIC_CANDIDATE`，先对既有数据做一次有界的统计与比较器裁决。**

证据：

- 机制信号很强：7 cells × 20 fresh seeds、140 pairs 中，G1 在 collapse 层相对 CMA 的 PI-SER 差为 −0.5598，95% CI [−0.6947, −0.4064]，12 help / 0 hurt；healthy 最坏退化为 0；always-on scalar 的最坏 healthy 退化为 0.0156–0.0195；G1 相对 M4 改善 −0.0355，95% CI [−0.0466, −0.0243]。
- 实现边界基本合理：仅用 128-symbol prefix 冻结 gate/scale，scored suffix 不反馈；16QAM 平均功率确为 1，`sqrt(Ps/Pz)` 公式成立；1120 行原始数据键唯一且无空 PI-SER。
- 但正式 Gate 6 的裁决没有闭合。执行代码声称做 seed-cluster bootstrap，实际在 `run_g1_confirm.py:397-423` 对 pair 位置重采样。结果文件后加的“正确”CI [0.50, 0.6579] 又把单类 seed 的 balanced accuracy 固定成 0.5；而原始数据实际有 5 个、并非文档所称 3 个 seed 同时含 healthy 与 collapse。按通常的 cluster bootstrap——重采样 seed、合并其 pair 后重算 balanced accuracy——对现有 rows 的只读复算得到 95% CI 约 [0.8849, 1.0000]。因此当前 PASS/FAIL 取决于未明确的 estimand，而非新增样本能直接解决。
- 语义烟测未进入终端产物：`result.json` 的 `smoke_results` 是空对象，且 runner 在 `run_g1_confirm.py:793` 明确把 `{}` 写入结果。扩大样本前必须补齐可审计的 smoke 证据。
- 比较器仍有缺口：always-on scalar 是任务匹配的对照，但 D4 在 `methods.py:353-378` 直接返回未改变的 post-CMA stream，本质上不是同层输出归一化比较器。还需裁定一个明显的低成本同任务替代，例如 clipped/soft-gated scalar，是否能同时取得恢复与安全性。
- collapse 证据范围窄：20 个 recoverable-collapse pairs 中 19 个来自 SNR20/25 两个 cells；唯一的 SNR15 collapse 未触发 gate。盲目增加相同 cells 的随机 seeds 主要提高精度，不能证明跨边界机制稳定。

扩大前必须完成的检查：

1. 明确 Gate 6 的统计量：是“重采样 seed 后 pooled bacc”，还是“仅在双类 seed 上计算 per-seed bacc”；禁止用缺失类别记零的隐式规则。
2. 由独立上下文从现有 raw rows 重算 Gate 6，并修正“双类 seed 数量”事实。
3. 持久化并核验 semantic smoke：prefix/suffix 隔离、healthy identity bit-equality、scale 公式、无 trivial/no-op 伪收益。
4. 补齐同任务、同信息、独立调参的廉价 conventional extension；D4 identity 输出不能承担该角色。
5. 若之后扩展，采用单独预注册的 targeted atlas，覆盖 gate 阈值附近、更多 SNR/`f_g`/长度，并确保每个统计 cluster 对两类都有可识别支持；不得作为当前合同失败后的 post-hoc rescue。

下一合法动作：**仅对现有产物执行一次 `BOUNDED_EVIDENCE_ADJUDICATION`，不跑新仿真。**若 pooled seed-cluster estimand 被确认符合原合同，且 smoke 与 comparator 缺口闭合，则可接受 `METHOD_SIGNAL`，但 claim ceiling 仍为 `CANDIDATE/LOCAL_SLICE`，随后进入 promotion preflight；若原意确为 equal-weight per-seed bacc，则保留 `G1_FORMAL_CONFIRM_NO_GO / mission_method_delta=NONE`，作为诊断/harvest 资产并轮转。当前合同已禁止第二次 repair、换 cells 或加 seeds 救活本次 verdict。
