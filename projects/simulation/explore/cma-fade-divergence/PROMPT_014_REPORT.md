# PROMPT-014 报告：盲 VQ-VAE 公平比较首轮截断

## TL;DR

盲 VQ-VAE 的实现、无标签边界、shared-realization 比较、双口径指标与 checkpoint 合同均已通过测试和独立代码审查；但正式实验只完成 11/30 cells，且其中 1 个 cell 违反预先冻结的训练 loss sanity。当前结果不能判定盲 VQ-VAE 是否正式优于 CMA，也不能解除监督公平性债务。

## VQ-VAE 实现

论文原文核对显示，Qin 的接收端使用固定已知调制星座作为码本，损失为重建误差与 commitment loss 之和（rho=1），不是学习 512×64 码本的通用 VQ-VAE。当前实现采用固定 QPSK 码本、straight-through estimator、29-tap 2×2 complex-FIR encoder/decoder；这是 1-sps 线性适配，不等同于原文 2-sps、四实通道 Hammerstein 结构。

盲性边界由接口与测试共同约束：训练仅接收前 50% 的 rX/rY，不接收 sX/sY、bits 或标签；CMA、VQ-VAE、监督 ML、oracle 与 raw diagnostic 共用一次信道 realization，后 50% 统一计算 fixed-label 与完整偏振排列/四相位消歧的 PI-BER。联合回归为 48 passed，独立审查为 Spec PASS / Quality PASS。

## 首轮正式运行

固定参数为 N=2,000,000、strong turbulence、20 dB、SOP=4e-7、f_G={30,100,1000}、seeds=1000–1009。正式运行完成 11 个唯一 cells，签名和 7 组件 SHA 一致，JSON 严格解析与数值有限性检查通过。

当前子集的 VQ-VAE/CMA PI-BER 均值及配对胜场为：f_G=30，0.04643/0.12288、2/2；f_G=100，0.05396/0.15409、2/2；f_G=1000，0.01063/0.11132、7/7。由于各频点尚未达到 10 seeds，这些数字只用于检查运行方向，不是正式性能结论。

## 截断原因

f_G=1000、seed=1004 的 VQ-VAE total loss 从 0.02049 增至 0.19909，触发 `loss_decreased=false`；finite、码本利用率 4/4 和非坍缩检查仍通过，该 cell 的 VQ-VAE PI-BER 为 0.02071，CMA 为 0.10562。

独立复算显示，前/后 100 批 total loss 均值为 0.04901/0.23269；reconstruction 从 0.01806 降至 0.01357，commitment 从 0.03095 升至 0.21912。训练实现每次顺序读取不同时间 batch，因此首批与末批不是同一个固定 probe。`final < initial` 既已在该 cell 字面失败，也不能被解释为同数据上的收敛证据。按预先冻结的规则，保留该 trial 后补齐 30 cells 最终只能得到 INVALID，故在 11/30 处停止，未事后修改 gate。

## 判定与建议

本轮结论为 PARTIAL/首轮候选被拒，不是“VQ-VAE 方法已证伪”。公平性债务仍未解除。若继续，应在查看新结果前先冻结“同一固定 probe 上的训练前/后重建与 commitment 指标”，改变代码 SHA 后从 0 重跑完整 30 cells；旧 11 cells 不得与新 gate 混合。

## 产出路径

- `projects/simulation/common/_vae_equalizer.py`
- `projects/simulation/common/_dual_pol_channel.py`
- `projects/simulation/explore/cma-fade-divergence/vae_vs_cma_blind.py`
- `projects/simulation/results/cma-fade-divergence/vae_vs_cma_blind_part_{a,b,c}.json`（gitignored，11/30）
