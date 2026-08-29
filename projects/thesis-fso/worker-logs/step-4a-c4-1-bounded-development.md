# Step 4a — C4-1 scaled-unitary correctness 与有界 BER

> 2026-08-30 | T069 / D049 / T068 / V023 | CP011 / epoch 11
> Status: `PASS / C4_STRUCTURED_SIGNAL / PROVISIONAL_A`

## 范围与门控

- validator：PASS；base `9a31d5d73e87c37417840a66767a20d8df0f8e36`。
- 只新增独立 seam、对应 tests、指定 Groundwork 报告、本 worker log 与必要 usage log。
- 未改 common/params、Ch3/Ch5、Skill/controller、论文正文；未检索论文、扩参数网格或运行 confirmation。

## RED/GREEN 与正确性

```text
RED core: 6 failed（scaled_unitary.py 尚不存在）
GREEN core: 6 passed
RED standalone-import regression: 1 failed（common 内部顶层 params 导入缺 SIM_ROOT）
GREEN final seam suite: 13 passed in 3.98s
C0/C1/C2/C3/C4/C5: PASS/PASS/PASS/PASS/PASS/PASS
correctness repair rounds used: 0
```

首次 BER runner 在生成任何 window/raw 前退出；最小路径修复后全量测试通过，manifest 未变化。

## 冻结批次与 reducer

```text
cells=14/18 dB × Np=2/4
windows=64/cell (32 tune + 32 evaluation)
payload=4096 symbols/pol/window
seed bases=6000/6100/6200/6300
B1 eta=0.01/0.001/0.001/0.01
B2 tau=1/1/1/1
raw-only checks=9/9 PASS
bootstrap=PCG64 seed 2026083003, 2000 resamples
```

核心 paired CI（C4 − strongest B1/B2）：

```text
14dB,Np2  [-0.0106374741, -0.0004005194]
18dB,Np2  [-0.0063127518, -0.0000006914]
14dB,Np4  [-0.0038831949, -0.0003260136]
18dB,Np4  [-0.0007823706, +0.0011769772]
```

B2 − B0 在四格 CI 均严格小于 0；cheap winner 信号未隐藏。完整 arm/cell BER、NMSE、residual 与 bit counts 见 Groundwork 报告和 aggregate。

## 终点

```text
TERMINAL=C4_STRUCTURED_SIGNAL
GRADE=PROVISIONAL_A
WINNER=C4
ONLY_NEXT_STEP=fresh confirmation of frozen C4 recipe
```

未满足项：fresh confirmation、最终章节声称、LDPC/FER、额外场景均未执行，也未获本任务授权。
