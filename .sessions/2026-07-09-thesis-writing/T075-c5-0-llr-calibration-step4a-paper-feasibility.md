# Task Brief: C5-0 pilot-residual reliability calibration Step 4a 纸面可行性

> 来源: S028 / D054 / T072 / T074 / V028–V029 | 产出位置: `projects/thesis-fso/apsk-llr-calibration-groundwork/step4a-paper-feasibility.md`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 16
  action_class: GW_STEP4A_PAPER_C5_LLR_CALIBRATION
  mission_checkpoint: CP016
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

只用本地已有证据，对 `Q-C5-0` 完成候选专属 GW Step 4a A0/A′/A/B 与 correctness contract。核心不是再论证“文献没完全一样”，而是判断目标链是否自然存在 reliability mismatch、当前 LDPC decoder 是否给全局尺度留下因果 headroom、B1/B3 是否完全吸收候选，以及后续若获授权应实现 B2 还是 B3 形态。

本任务不实现、不仿真、不跑 BER/FER、不联网检索/下载、不修改 Ch4、Skill/controller 或正式论文正文。

## 必读事实

1. `projects/thesis-fso/apsk-llr-calibration-groundwork/step3-5-exact-recipe-closure.md`
2. `projects/thesis-fso/literature_notes_apsk_llr_calibration.md`
3. `projects/thesis-fso/direction-lab/harvest/ldpc-receiver-authority.md`
4. Ch5 post-Ch4→Ch3 residual bridge、occurrence 与 C5-1 negative-development 报告/manifest；只读既有 raw/aggregate，不运行脚本。
5. `projects/simulation/explore/coded-decoder-feedback/codec.py:114-205` 与目标 APSK demapper/codec bridge：区分旧 Gray-16QAM adapter 事实和目标 DP-(8,8)-16APSK 合同，不能默认二者已统一。
6. `stages/gw-feasibility.md` A0/A′/A/B、`stages/glossary.md`、`domain-comms.md` 与 `thesis-lessons.md` TL-31–33。

## 冻结对象与 baseline ladder

- 目标链：`post-Ch4 demux → per-tributary Ch3 CPR → current-frame known pilots → demeaned residual reliability/variance → soft demapper/calibration → frozen LDPC`。
- B0：同一 mismatched demapper/auxiliary parameter，`s=1`，不得偷换为 matched likelihood。
- B1：development-only tuned one global scalar，runtime 固定；作为最强 offline 廉价吸收对手。
- B2：current-frame receiver-known pilot residual → one positive global post-demapper channel/extrinsic-LLR scalar。
- B3：与 B2 完全相同 pilots、residual statistic、sample count 与 causal window，把 `hat_sigma2` 直接 plug-in exact-APP/max-log auxiliary demapper。
- O1/B_match：真实 per-frame matched parameter/likelihood，只作 headroom reference，不是 deployable baseline。

## 必答 A0 / A′ / A / B

### A0：问题是否真实存在

1. 用已有 target-chain artifact/authority 说明 B0 的 assumed reliability 与 post-Ch4→Ch3 current-frame residual reliability 是否会自然失配；不得加入 IQ/PDL/PMD/FIR、新湍流档或 synthetic anisotropy 制造问题。
2. 四判据逐项 PASS/FAIL：现象、机制、receiver-visible 可观测性、可操作改善路径。
3. 把 operational pilot count/window 保持 `UNKNOWN` 时，说明如何成为后续 falsifier；不得拍一个只为让 estimator 有用的数字。

### A′：竞争维度与指标

1. 主维度冻结为相同 LDPC、相同码长/迭代/裁剪、相同 pilots/overhead 下的 coded BER/FER；uncoded BER、GMI/ASI、variance error、clip incidence 只作机制诊断。
2. 明确全局正缩放对 uncoded hard sign、理想 maximum-metric ordering、finite NMS/BP 与 exact APP 的不同语义；不得用 GMI/ASI 代替 coded BER/FER。

### A：因果 headroom 与 action 选择

1. 对当前本地 decoder 做解析审计：`alpha=0.75` fixed normalized min-sum、20 iterations、input/internal `llr_max=20`。证明在没有 clipping/quantization/offset 时公共正缩放的正齐次性及 hard-output invariance；列出实际可能破坏齐次性的唯一 receiver elements。
2. 回答 B0→O1 headroom 在哪条合法链上可能出现：
   - B2 若只靠 clipping/saturation 改变输出，是否被 B1 或同预算 clip tuning 完全吸收；
   - B3 exact APP 改变 bit-LLR shape 是否在目标 16APSK labeling 下形成不同于外乘 scalar 的合法 action；
   - 旧 16QAM codec 与目标 DP-(8,8)-16APSK bridge 是否存在接口 blocker。
3. 按最简真实承重 action 二选一：
   - B2 只有在不是纯齐次零效应、且未被 B1/B3 完全吸收时才能保留；
   - 若 B2 被吸收而 B3 exact-APP 仍有合法 M-C-A，则候选身份改为“导频残差驱动的逐帧辅助信道参数校准软解调”，明确是 B3 形态 classical migration；
   - 不得把 B2+B3 拼成双自由度方法，只为增加可写性。

### B：claim ceiling

沿用 T074 的强邻居与 disclosure。说明这些邻居如何限制“首次/新理论”，但不把不同目标平台的经典迁移自动 Kill。若 action 最终改为 B3，必须相应进一步降低 claim，不得沿用 B2 的 post-demapper 独立身份。

## 冻结 correctness contract（只写合同，不执行）

至少包含：

1. 16APSK bit labeling、LLR sign、noise-variance factor 与 max-log/exact-APP 手算小例；
2. B2/B3 max-log 条件内逐样本逐 bit 等价；
3. exact-APP 对 DP-(8,8)-16APSK 各 bit 的 deterministic identity/non-identity test；
4. fixed-NMS 无裁剪公共缩放 invariance，以及 clipping/quantization/offset negative/positive controls；
5. B0 matched/no-mismatch negative control、B1 offline scalar、B2/B3 同 pilots/statistic/window；
6. receiver API 不得读 true noise/SNR、payload truth 或 decoder truth；truth 只进 scorer/O1；
7. paired realization、finite outputs、seed/split isolation 与 decoder call/iteration equality。

同时给一个 correctness 后的**单格 headroom/occurrence 设计**，但不得运行：先检查 natural mismatch 与 B0→O1；无 headroom 立即停，不进入开发矩阵。

## 唯一 terminal

1. `PAPER_DIMENSIONS_PASS_B2`：自然 mismatch、非齐次作用链与 B0→O1 headroom 在纸面上成立；B2 未被 B1/B3 解析吸收。允许主控另开 B2 correctness-only seam。
2. `PAPER_DIMENSIONS_PASS_B3_MIGRATION`：B2 被齐次性/等价关系吸收，但 B3 exact-APP auxiliary-parameter recalibration 仍有合法 target-scene M-C-A。允许主控另开 B3 correctness-only seam，claim 更低。
3. `PAPER_FAIL_NO_CAUSAL_HEADROOM`：问题不存在、decoder 对候选严格不敏感、或全部合法作用被 B1/B3/固定 clipping 同预算吸收。关闭 C5-0，轮换后备。
4. `EVIDENCE_BLOCKED`：目标 APSK codec/demapper/decoder 合同或自然 residual evidence 不足以做纸面判断。列出一个最小 blocker；不实现、不仿真补洞。

任一 PASS 都只是“可做 correctness”，不是方法成立或 BER 改善。

## 时限与验收

- 墙钟 35 分钟；不外搜，不修基础设施，不扩候选。
- 独立 reviewer 只核 A0→decoder contract→吸收关系→terminal，P0/P1 必须为 0；P2 可降为明确 debt。
- task-control、source paths、唯一 terminal、`git diff --check` PASS。
- 一次 commit、不 push；回报 terminal、选定 action(B2/B3/关闭)、最强解析 falsifier、correctness 清单、单格 headroom 设计、blocker 与 commit。
