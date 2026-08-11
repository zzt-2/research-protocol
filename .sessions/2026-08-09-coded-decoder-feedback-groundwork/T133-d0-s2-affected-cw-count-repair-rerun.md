# Task Brief: S2 affected-CW 计数修复与立即重跑

> 来源: S001 / T132 formal run | 产出位置: `projects/thesis-fso/worker-logs/step-205-d0-s2-affected-cw-count-repair-rerun.md`
> 日期: 2026-08-11

## 根因证据

完整 S2 已产生 1620/1620 unique rows，但 typed finalization 失败：1311 rows 的 `affected_cw_errors > affected_cw_total`。样例为 `4061/8`；`affected_cw_errors` 与 `information_bit_errors` 相等，证明 runner 把 bit-error count 写进 codeword-error 字段。该结果 INVALID，不是科学 FAIL。

## 唯一任务

1. 写 focused RED，复现 multi-bit errors in one affected CW 必须计为 1 CW error而非 bit count。
2. 从真实 decoded info bits 与 truth info bits 按 canonical 16×1024 CW 切分，只在 fixture affected suffix CW 集合内计 `any bit error` 的 CW 数；`information_bit_errors` 继续是全帧 bit-error count。不得 clamp/min 伪修。
3. 验证 B1/O1、B04/B08/B12 affected range 与 `affected_cw_total=12/8/4` 一致。
4. focused GREEN 后删除 INVALID S2 checkpoint/artifacts并完整重跑 exact 1620 rows；这是同一 S2 bounded repair 的数据纠正，不保留错误行作 resume。
5. 产出 summary/receipt，给 damage/headroom point、10k CI、positive cells、PASS/FAIL；B2保持 NOT_RUN。
6. 15 分钟硬停；不改 owner/schema/gate/common/S1/S3+，不 stage/commit/push。

## 否决条件

若现有 runtime 无法访问 per-CW decoded/truth info bits，或需要改变 metric/schema，立即 BLOCKED；不得从 bit count 猜 CW count。
