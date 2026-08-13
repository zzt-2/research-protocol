# Task Brief: P11 Complex-LS Butterfly FIR 最后一次 bounded confirmation

> 来源: S020 / D030 | 产出位置: P11 专题治理、worker-log、corrected artifacts 与回传
> 日期: 2026-08-13
> 唯一文档: 执行方只需本任务书、仓库源码与本文列出的 owner

## 0. TL;DR

你在 `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`。

**任务**：把历史 P11 的假 SNR 标签纠正为真实注入的至少三个 SNR 条件，冻结并执行一次 complex-LS / full-label Adam / pilot RLS / blind CMA 的公平 paired confirmation，判断 complex-LS 是否能形成一个有限主张的硕士级校准方法。

**这是本轮最后一次自动方法尝试。** 若 authority 不足、需要发明新物理条件、corrected 结果失败、同任务 CMA 全面吸收、执行无效或 verifier 不通过，立即终止为 `METHOD_SEARCH_PAUSED_FOR_STRATEGIC_DISCUSSION`；不得自动转 P01、修同轴变体或另找候选。

### 最高纪律

1. 运行任何仿真前必须完整读取并执行 `sim-preflight` Skill、`thesis-lessons.md`、`stages/groundwork.md` 及当前合法 GW step owner；明确回答“当前在 GW 哪一步”。
2. 先做 authority reconciliation。若历史 P11 不能合法续接到一次 bounded Step 4a/等价补证，诚实 BLOCKED 并触发停机，不用长检索重建整条路线。
3. true SNR 必须实际进入 channel generator；设置不同 gamma 后至少一个接收统计量必须按理论方向变化。仅改 cell 标签 = EXECUTION_INVALID。
4. test 前冻结 cells、dev/test seeds、pilot fractions、method identities、primary metric、MDE/CI 和 PASS/FAIL；held-out 开始前留 immutable receipt/commit chronology。
5. runtime 只能用冻结 pilot 位置的 TX symbols 和 receiver-visible samples；payload truth、true h/SNR/turbulence/phase 只能评分或 oracle，不能进入 deployable action。
6. 不准事后挑 slice。只有预注册 slice 可承重。
7. 不称 CNN 创新、LS 首创、SOTA、全面优于 CMA或跨 SNR 鲁棒；claim ceiling 只到目标链路中的低导频线性 Butterfly FIR 校准。
8. 工作树有无关 dirty 与四个 `p05_run*.log`；不得修改、暂存或提交。不得 push。

## 1. 已知事实与 owner

- 历史 worker-log：`projects/thesis-fso/worker-logs/step-041-p11-pilot-efficient-butterfly-fir.md`。
- 根因审计：`.sessions/2026-07-23-research-direction-lab-longitudinal-test/R010-campaign-final-effect-and-root-cause-audit.md`。
- thesis-grade remap：`projects/thesis-fso/direction-lab/harvest/historical-assets-thesis-grade-remap.md`，P11 位于 B2。
- 现有代码：`projects/simulation/explore/p11-pilot-efficient-butterfly-fir/`。
- 现有结果：`projects/simulation/results/p11_pilot_efficient_butterfly_fir/`。
- 模型身份：`projects/simulation/common/_ml_equalizer.py:104` 的 `ButterflyCNNEqualizer2x2` 实际是 4 个复 FIR / 8 个无 bias 实 Conv1d，无 activation/normalization；正文不得称新 CNN。
- 历史数字仅是 **实际 20 dB 局部切片**：约 B2 LS BER `3.10e-4`、B0 full-label Adam `3.86e-4`、1% pilot goodput 约为 50% labels 的 `1.98×`。旧 9/11/13/15 dB 标签没有传入 generator，禁止复用为跨 SNR 证据。
- 历史 blind CMA 报告 BER 近 0；必须核对其 metric、phase/swap resolution、runtime information 与输出合同。只有同任务、同 fixed-label 输出、同可见信息的 CMA 才能构成吸收；任务合同不同则作为强邻居限制 claim ceiling。

## 2. 执行阶段

### A. Authority 与语义门

1. 新建或续接唯一合法 P11 专题前先查 `.sessions/_registry.yaml`；不要重复开题。
2. 沿 caller→callee 核查：gamma 参数如何进入信道、模型/训练/检测/评分身份、CMA 的 phase/swap 处理、pilot truth 边界。
3. 写出 P11 的 M-C-A 与 deployable action：
   - M：50% 连续标签 + Adam 训练的线性 2×2 Butterfly FIR；
   - C：有限 pilot 开销、至少三个真实注入 SNR 的冻结目标切片；
   - A：线性 FIR 的闭式 complex LS 可用少量 pilots 完成校准，降低监督开销而不损失 fixed-label BER。
4. 判定是否已有合法 Step 3/4a 依据可做一次 bounded confirmation。不能确认则终止，不做广泛补文献。

### B. Pre-test freeze

冻结至少：

- 3 个真实 SNR 条件，覆盖历史目标 operating range；每个条件的 gamma 必须实际进入 generator；
- 至少 weak/moderate/strong 中能由现有 source 合法支持的湍流覆盖，不为制造优势新增物理自由度；
- dev/test seeds 完全分离，paired realization；
- pilot fractions 至少含 1% 与 50%，其他点可沿历史合同但不得膨胀；
- B0 full-label Adam、B1 pilot complex LS、B2 pilot RLS、B3 dev-tuned Godard-with-z blind CMA；
- fixed-label BER primary，PI-BER secondary（若有必要），pilot-adjusted goodput 与真实运行成本 secondary；
- paired seed-cluster CI、MDE/non-inferiority margin 与 sample-size rationale；
- PASS/FAIL/blocked terminal；
- source hashes、receipt hash、`test_started=false`。

先跑小 dev/sentinel：不同 SNR 的噪声或接收质量统计必须按理论方向变化；相同 realization 在仅更改标签时不得“变化”。sentinel FAIL 直接 EXECUTION_INVALID/停机。

### C. 一次 held-out confirmation

只运行冻结 grid 一次。所有方法共享 realization、pilot positions、eval window、detector 和 scoring。CMA 独立 dev 调谐，不能故意弱化；同时不得使用 TX payload truth 做 phase/swap resolve。

### D. 判决

`P11_THESIS_METHOD_READY` 仅当全部成立：

1. true-SNR sentinel 与信息边界通过；
2. complex LS 在预注册 grid 上对 full-label Adam 非劣，paired CI 支持；
3. pilot/goodput 优势成立，不是标签或统计 artifact；
4. 至少一个预注册、机制连贯的目标切片未被**同任务同输出** CMA 完全吸收；
5. 方法链可画流程、可做 pilot-fraction 消融、可形成有限 claim。

否则根据事实记录局部科学 terminal，并把全局执行终态设为：

`METHOD_SEARCH_PAUSED_FOR_STRATEGIC_DISCUSSION`

该终态后禁止任何自动候选轮换、补跑或改名重开。

## 3. 独立验证

执行与验证必须分离。fresh-context verifier 至少核查：

- gamma 确实进入 generator，metamorphic/sentinel 有数值证据；
- freeze chronology 与 source hashes；
- raw→aggregate 独立重算；
- dev/test seed 隔离、paired realization；
- pilot-only truth 边界与 CMA 调用图；
- fixed-label/PI-BER 口径没有混淆；
- CMA 是否真为同任务吸收；
- verdict 唯一且没有 post-hoc slice；
- 无关 dirty、Skill/controller/formal thesis 未污染。

## 4. 交付与回传格式

最终只回五项：

1. authority / true-SNR sentinel / chronology 结论；
2. Adam / complex-LS / RLS / CMA 的关键 BER、goodput、paired delta 与 CI；
3. CMA 是同任务吸收、仅强邻居，还是未解决，以及依据；
4. terminal、thesis_method_disposition 与是否触发战略停机；
5. worker-log、artifact、D/V/H、verifier、commit SHA。

执行完成后通过 Codex thread 工具自动回传父任务 `019fccc3-f9f2-7b52-938f-b2b1dda09b10`，不要让用户手工中转。不要 push。

## 5. 验收

- [ ] 开跑前明确合法 GW/authority step；不够则诚实停止。
- [ ] true-SNR 注入有 caller→callee 与运行时 sentinel 双证据。
- [ ] test 前 immutable freeze，test 后不改合同。
- [ ] 比较器身份、公平性、truth boundary 全闭合。
- [ ] 只有预注册 slice 承重。
- [ ] 任一非成功终态均触发战略停机，未派下一候选。
- [ ] fresh-context verifier 完成。
- [ ] 单对话按规则统一提交；不 push；无关 dirty 未纳入。
