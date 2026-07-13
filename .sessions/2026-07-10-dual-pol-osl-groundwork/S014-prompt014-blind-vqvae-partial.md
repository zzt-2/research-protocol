# [S014] PROMPT-014 盲 VQ-VAE 公平比较首轮执行

> 2026-07-13 | GW Step 4a 维度 D 补充 MVE | 状态：PARTIAL（首轮结果候选截断）

## 目标

实现 Qin 路线的盲 VQ-VAE 双偏振线性均衡器，在 N=2M、strong、20 dB、SOP=4e-7、f_G={30,100,1000}、每格 10 seeds 下，与盲 CMA 做 shared-realization 双口径公平比较；监督 ML 与 oracle 仅作参照。

## 记录

论文原文核对修正了 PROMPT-014 的简化描述：Qin 使用固定已知星座作为码本，Eq.15 为 reconstruction MSE + rho×commitment（rho=1），不存在本任务原描述中的可学习码本/独立 codebook loss。实现因此采用 Qin-faithful 的 1-sps 线性 2×2 complex-FIR 适配，不声称逐项复刻原文 2-sps、4 实通道和 Hammerstein 非线性结构。

新增 `_vae_equalizer.py`、共享双偏振信道入口 `_dual_pol_channel.py`、正式驱动 `vae_vs_cma_blind.py` 及对应测试。VQ fit 接口只接收前 50% 的 rX/rY；五种方法使用同一 realization，后 50% 统一走 2!×4×4 PI-BER 与 fixed-label BER；完整参数和 7 个实现依赖进入 SHA/签名。实现、分片、合并与恢复合同经独立 review 后为 Spec PASS / Quality PASS，联合回归 48 passed。

100k 真实 smoke：391 默认 updates，14.61 s wall，loss 0.069606→0.037657，码本 4/4、finite/non-collapse 全过。正式 N=2M 单 cell 约 95.6–143.3 s。三路并发第二批在 VQ/ML 的不同 CUDA 调用点均出现 `illegal memory access` 且未写入新 trial；清空并发后相同 cell 单路成功，故后续只能单路运行。

正式运行在 11/30 cells 时触发前置 sanity：f_G=1000、seed=1004 的 total loss 0.020492→0.199085，`loss_decreased=false`；finite、码本 4/4、non-collapse 均为 true，VQ PI 0.020713 < CMA PI 0.105624。独立复算表明 first/last 100 total mean 0.049006→0.232686，主要由 commitment 0.030951→0.219121 驱动，reconstruction 反而 0.018055→0.013566。

更关键的是，7813 个 update 按 cursor 顺序覆盖不同 batch：首批中心 [0,128)，末批 [999936,1000000)。因此 `loss[-1] < loss[0]` 不是固定 probe 上的收敛证据；其他 10 个 `true` 也不能表述为“已证明收敛”。按冻结规则，当前正式实验 gate 仍为 INCOMPLETE，但保留该 trial 后补齐 30 cells 必然进入 INVALID，不可能 PASS，故停止剩余 19 cells，不事后放宽 gate。

当前子集仅作诊断：f_G=30/100/1000 的 paired wins 为 2/2、2/2、7/7；这些不是 10-seed 正式结论。完整阶段报告见 `projects/simulation/explore/cma-fade-divergence/PROMPT_014_REPORT.md`。

### 迭代计数器

- 实现合同：2 轮独立 review，关闭 exact-grid、resume/merge、内部签名自洽等问题后 PASS。
- CUDA 执行：1 轮三路并发失败；单路复现对照成功，否决继续并发。
- 正式结果：首轮候选在第 11/30 cells 触发 sanity FAIL，按 P2/F1 截断。
- 否决条件：任一正式 cell sanity false，或首末 loss 不是同一可比 probe，即不得继续把当前候选用于 PASS/FAIL；两项均触发。

## 决策引用

- D019：PROMPT-014 首轮结果候选被拒；冻结的首末 batch loss gate 不具固定探针语义，禁止续跑后宣称正式 PASS（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是（用户明确执行已提交的 PROMPT-014，仍属 GW Step 4a 维度 D 补充 MVE；未进入 Contract）。

## 后续

需用户确认二选一：A）先冻结固定 probe 的训练前/后 loss sanity，再从 0 重跑完整 30 cells（旧 SHA 的 11 cells 不混用）；B）停止盲 VQ-VAE 方法层，仅保留“公平性债务未解除”的结论。未确认前不改 gate、不续跑剩余 cells。
