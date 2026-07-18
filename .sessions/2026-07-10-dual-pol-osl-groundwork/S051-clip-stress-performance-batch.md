# [S051] Clip 压力域首轮性能 batch

> 2026-07-16 | Batch 1 性能筛选 | PARTIAL（内存阻塞）

## 目标

在 μ=1e-2 的已有高风险域，检验 P95/P99 gradient clipping 是否改变 divergence/BER，而不是在安全域重复零事件。

## 记录

理论预期（跑前冻结）：

1. Godard 更新范数尾部应比 μ=1e-3 pilot 更重；P95/P99 clip 应分别影响约 5%/1% 的 block 更新。
2. 若数值失稳是主要瓶颈，baseline 应出现至少少量 divergence 或明显异常输出；clip 可能降低 divergence，但不保证 BER 改善。
3. 若三臂均无 divergence 且 fixed/PI BER 均为 0，则本批判为 **inconclusive**，不扩大统计、不写性能结论。

配置：修复后 prefix-stable generator，N=5,000,000、seeds41–45、strong α=4.2/β=1.4、fG=30、SOP=4e-7、μ=1e-2、standard Godard-z；baseline/P95=`0.0014604833857170827`/P99=`0.003110059353060399` 三臂，共享 realization/mask/window/events。

观察：divergence rate/symbol、fixed/PI BER、swap/fade/recovery/censor、clip count。首轮不做最终 Go/Kill；任何 schema/finite/mask 失败立即停止。

## 决策引用

- D045：候选族批量排跑。
- D046：prefix-stable GG generator。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

已完成 seed41/P99 独立进程 smoke：valid=4,999,936、fixed/PI=0、clip blocks=0、无 divergence；同进程多臂 runner 在第三臂前因内存被杀，未静默降 N。其余 5M 三臂未完成，故本批 PARTIAL，不作性能结论。下一步改为流式/分臂执行后再继续。
