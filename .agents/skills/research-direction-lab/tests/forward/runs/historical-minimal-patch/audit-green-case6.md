---
agent_task: /root/audit_green_case6
fork_turns: none
skill_identity: working-tree-canonical
prompt: .agents/skills/research-direction-lab/tests/forward/runs/historical-minimal-patch/prompts/case6.md
---

## Raw adjudication

## 原始裁决

### 证据冲突处理

- **G1**：当前 campaign thesis map 明确将其标为 `INVALID scientific result`。`g1-safe-gated-normalization-package.md` 与 `g1-thesis-insert.md` 中全部性能数字不得作为贡献证据；仅保留为实验审计/错误统计口径反例。
- **P07**：原 P07 全部科学结论失效；只采用 P07-R 的 `PROBLEM_ABSENT_AFTER_GAIN_CALIBRATION`。增益校准后问题不存在，无方法信号。
- **P08-R**：其科学结论及数字失效；只采用 P08-R2 的 `PROBLEM_ABSENT_AFTER_RECEIVER_VISIBLE_STRONG_LLR_BASELINE`。allowlist 未提供可用的 P08-R2 性能数字，因此不引用数字。
- **P09**：`p09_test_result.json` 的 `EVIDENCE_INSUFFICIENT`、BER 和“8 eval/sym”全部被 D053 invalidation marker 推翻；终态为 `EXECUTION_INVALID/KILL_C3`，不得贡献任何正向数字或方法。
- **P11**：源码中的 `cells_problem_bearing[*].gamma_db` 未传入 `gen_channel`；后者固定使用 `params.py` 的 `GAMMA_BAR_DEFAULT=100`，即 **20 dB**。因此结果只能解释为 20 dB 局部切片，不能声称覆盖合同中标注的 9/11/13/15 dB。其合法上限是 20 dB 下“传统 complex LS 已解决”的局部边界。
- **P06、P10**：均为有效局部边界/问题消解材料，不产生方法信号或 active carrier。

### 贡献分级

- `THESIS_MAIN_METHOD`
  - 基于接收功率 CV 与有效 SNR 的逐窗 DA/NDA 自适应 CPR。
  - 可用上限：已测 16APSK、AWGN + 三档 Gamma-Gamma slice；9 dB 下相对固定 NDA 改善约 0.8–1.5 dB。
  - 这是既有论文资产，不是本 campaign 新产出。

- `THESIS_ENGINEERING_COMPONENT`
  - bit-true Q-format 与 resource proxy：仅支持局部定点实现结论；uniform Q(8,6) 已到性能地板，mixed 增益最多约 0.0166 dB。不得外推为真实 FPGA 资源、功耗或吞吐结论。
  - receiver-visible coded-chain 资产：5G NR BG2 rate-matched LDPC、3GPP bit interleaver、Gray-16QAM BICM、轨迹级 FER/oracle ladder；当前为 `PARTIAL reusable engineering`，正式论文数字仍需独立 pre-test freeze 后确认性重跑。
  - 32-symbol prefix-LS 噪声估计及信息边界验证机制：工程机制可复用，但 chronology 未闭合，只能作为有界实现组件/实验纪律。

- `SUPPORTING_MATERIAL`
  - P06：严格因果历史虽有小预测增量，但 last-value persistence 显著更强；有效局部负面与强基线边界。
  - P07-R：增益校准后 AGC/ADC 问题不存在；原 P07 数字禁用。
  - P08-R2：receiver-visible 强 LLR baseline 已解决问题；仅保留终态及 coded-chain 工程资产。
  - P10：crossover 不成立；corrected standard CMA 已解决一侧问题，另一侧优势是 swap artifact。
  - P11：仅 20 dB 下 complex LS 传统基线边界，不能作为跨 SNR 方法贡献。
  - G1、P09：只作 threats-to-validity、审计 checklist、错误记账/信息泄漏反例，不作方法或贡献数字。
  - P01–P07-R 等有效局部负面只能合并为一张边界表，不能拆成多项创新。

- `ACTIVE_CARRIER`
  - **无。**
  - 既有 DA/NDA CPR 是已完成主方法，不是当前 active carrier；本 campaign 没有产生新的 `METHOD_SIGNAL`。

### Campaign verdict

`CAMPAIGN_CLOSED_WITH_ZERO_NEW_METHOD_CARRIER`

本 campaign 形成了有效局部负面、强传统基线边界和若干有界工程资产，但没有产生新的主方法。不得把负面包数量、G1、P09、P11 partial 或失效谱系包装成第二项方法贡献。

### 是否需要另一个 package

**不需要，也不应继续追加同一 campaign 的探索 package。**

下一合法行动是按“AMC 失败”方案冻结 campaign closeout：以既有 DA/NDA 自适应 CPR 为唯一主方法，组织 bit-true 定点、receiver-visible coded-chain 与强基线边界为实现/评价扩展，并闭合 coded-chain chronology 确认性重跑或真实 FPGA 综合中的至少一项。

若毕业要求明确需要第二项主方法，应启动独立 AMC Groundwork 工作线，从 Step 1–3/3.5/4a 重新建立问题、比较器与证据合同；不能以 P12 或旧 invalidated evidence 续包替代。

### 实际读取路径

- `C:\Users\zzt\.agents\skills\using-superpowers\SKILL.md`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\.agents\skills\research-direction-lab\SKILL.md`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\.agents\skills\research-direction-lab\references\method-production.md`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\.agents\skills\research-direction-lab\references\evidence-and-claims.md`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\.agents\skills\research-direction-lab\references\thesis-harvest.md`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\.agents\skills\research-direction-lab\tests\forward\runs\historical-minimal-patch\prompts\case6.md`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\thesis-fso\direction-lab\harvest\method-production-campaign-thesis-map.md`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\thesis-fso\direction-lab\harvest\g1-safe-gated-normalization-package.md`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\thesis-fso\direction-lab\harvest\g1-thesis-insert.md`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\results\p06_causal_cross_frame_history\p06_terminal_verdict.json`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\results\p07_agc_adc_dynamic_range\INVALIDATED_BY_P07R.md`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\results\p07r_agc_adc_repair\p07r_terminal_verdict.json`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\results\p08r_coded_chain_repair\INVALIDATED_BY_P08R2.md`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\results\p08r2_receiver_info_repair\p08r2_v075_result.json`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\results\p09_16apsk_confidence_bps\INVALIDATED_BY_D053.md`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\results\p09_16apsk_confidence_bps\p09_test_result.json`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\results\p10_single_expert_router\p10_verdict.md`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\results\p11_pilot_efficient_butterfly_fir\p11_verdict.json`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\explore\p11-pilot-efficient-butterfly-fir\p11_run.py`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\explore\cma-fade-divergence\ml_long_seq_failure.py`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\params.py`
