# C4-1 scaled-unitary 冻结配方 fresh confirmation

> 2026-08-30 | Groundwork Step 4a-D fresh confirmation | T071 / D050 / V025
> 终态上限：只回报 frozen confirmation terminal；本报告不宣布 `THESIS_METHOD_READY`。

## 1. 事实与门控

- task-control validator：`PASS`（`rdl.task-control.v2` / epoch 12 / CP012 / `C4_SCALED_UNITARY_FRESH_CONFIRMATION`）。
- development 五个冻结 JSON 均保持只读；独立临时 reducer 从 development raw 重算 aggregate SHA256=`9c236830edc29c96edbe6698a048c910c4d6775486bc51ec2d82b460a2cc2ccb`，与冻结 aggregate 完全一致，terminal=`C4_STRUCTURED_SIGNAL / PROVISIONAL_A`。
- 原 T069 目标测试 fresh 为 `13 passed`；confirmation 主合同按 RED→GREEN 执行（RED=`5 failed`，缺失新 manifest/runner/reducer；GREEN=`5 passed`）；暂存时发现行尾哈希风险后又以独立回归完成 RED=`1 failed` → GREEN=`1 passed`。最终合并测试为 `19 passed`。
- confirmation 只运行一次：四格均为 64 个 confirmation-only windows，seed bases=`7000/7100/7200/7300`，无 tune/evaluation split、无参数搜索、无 development seed 重叠。
- B1 参数按四格固定为 `0.01/0.001/0.001/0.01`；B2 固定 `tau=1.0`；primary comparator 始终为 B2。
- raw-only fresh 内存复算与保存 aggregate 去除 `_meta` 后完全一致，scientific payload SHA256=`db0094d500ae6f651e4f5f38bd86f3b3ae25405368e5258c692cf61f0ef86dd7`。

## 2. 四格 BER 与 primary CI

BER 为 64 个 paired confirmation windows 的 pooled payload BER；差值为 `C4−B2`，负值更好。

| cell | B0 | B1 | B2（最强廉价对手） | C4 | O1 | C4−B2 mean | paired 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|
| 14 dB, Np=2 | 0.08793068 | 0.08802366 | 0.08277035 | 0.07667112 | 0.05273247 | -0.00609922 | [-0.00954738, -0.00306168] |
| 14 dB, Np=4 | 0.07928896 | 0.07931185 | 0.07178736 | 0.06990385 | 0.05725527 | -0.00188351 | [-0.00354064, -0.00019817] |
| 18 dB, Np=2 | 0.04305935 | 0.04306221 | 0.03875256 | 0.03550529 | 0.02203321 | -0.00324726 | [-0.00548053, -0.00143516] |
| 18 dB, Np=4 | 0.02407551 | 0.02412033 | 0.02216578 | 0.02104330 | 0.01726913 | -0.00112247 | [-0.00216106, -0.00026414] |

两个 Np=2 cell 合并 128 个 paired windows：`mean=-0.00467324`，95% CI=`[-0.00686385,-0.00282661]`。两格 individual CI upper 均 `<0`；两格 Np=4 CI lower 均 `<0`，没有显著退化。

## 3. Secondary 与方向一致性

| cell | C4 相对 O1 oracle headroom | development C4−B2 方向 | confirmation 方向 | 一致 |
|---|---:|---:|---:|---|
| 14 dB, Np=2 | 0.02393866 | 负 | 负 | 是 |
| 14 dB, Np=4 | 0.01264858 | 负 | 负 | 是 |
| 18 dB, Np=2 | 0.01347208 | 负 | 负 | 是 |
| 18 dB, Np=4 | 0.00377417 | 正且 CI 跨 0 | 负且 CI upper <0 | 否；变化方向有利 |

四格均保留正 oracle headroom。development 与 confirmation 的 C4−B2 点估计方向为 3/4 相同；唯一不一致的 18 dB/Np=4 从 development 的非显著轻微退化变为 confirmation 的显著改善，没有触发反向科学门。

## 4. 冻结终态与 claim ceiling

**Frozen terminal：`C4_CONFIRMED_STRUCTURED_SIGNAL`。**

判据逐项成立：两格 Np=2 mean 均 `<0`；pooled Np2 CI upper `<0`；至少一个（实际两个）individual Np2 CI upper `<0`；两格 Np=4 均无 CI lower `>0`；correctness、finiteness、hash、split、seed non-overlap、paired realization/observation 与 truth firewall 全部 PASS。

方法身份仍冻结为：短 balanced-pilot DP-(8,8)-16APSK 相干接收中的 scaled-unitary 公共增益—偏振矩阵联合估计。B2 `tau=1` 是必须如实报告的最强廉价对手；C4 与 B2 使用相同 `UV^H` 偏振方向，差别是公共尺度估计。因此证据只支持“共同尺度估计带来的有限 BER 改善”，不支持更好的偏振旋转、新估计理论、首次或 SOTA。

## 5. 唯一下一步

由另一上下文从 `confirmation_raw.json` 独立复算 terminal、CI、hash/split/firewall。当前实现上下文不得宣布 `THESIS_METHOD_READY`，不得追加第二次 confirmation，也不得扩格、换 seeds、调参数或新增损伤。
