# decode-failure-rescue — 译码失败码字门控救援诊断（GW 4a-D 有界实验）

> 权威：`.sessions/2026-08-30-thesis-advisor-text-outline/R029` + 本目录 `contract.yaml`（执行前冻结）。
> 2026-09-20 本轮授权（D051）：只读限制解除，允许最小接口扩展 + 有界小规模实验；不改正文/不换场景/不动历史模块。

## 目的

在 T077 冻结格（DP-16APSK 中湍流 15dB，5G BG2 (1024,1536) NOMS(0.75,0) 20 迭代，FER≈0.258）上回答：

1. 失败码字的结构（停滞/振荡/慢收敛/收敛错码字占比；syndrome 权重与硬判错误数分布）；
2. 纯延长迭代（常规替代）能救回多少；
3. 定向擦除（R2）/配置切换（R3）相对延长的增量；
4. oracle 置零（O1，诊断专用）的 headroom。

## 布局

- `contract.yaml` — 预注册冻结合同（臂/指标/正确性门/预算/解释边界）。**执行后不改，修订走新版本。**
- `generate_llrs.py` — 复用 `../ch5-apsk-llr-calibration/single_cell.py` 冻结链生成逐帧 exact-APP LLR 缓存（smoke/dev/eval 三 split）。
- `rescue_decoder.py` — 仪器化 NOMS 译码器（Sionna 状态步进或镜像实现，按 contract decoder.route_decision）。
- `run_experiment.py` — 按合同跑臂，写逐帧 raw + summary 到 `../../results/decode-failure-rescue/`。

## 纪律

- 不修改 `ch5-apsk-llr-calibration/`、`coded-decoder-feedback/`、`common/` 任何文件。
- 所有臂共享同一逐帧 LLR 字节；eval 不调参；真值只进评分与 O1。
- 结果落 `projects/simulation/results/decode-failure-rescue/`；worker log 落 `projects/thesis-fso/worker-logs/step-207-*.md`。
