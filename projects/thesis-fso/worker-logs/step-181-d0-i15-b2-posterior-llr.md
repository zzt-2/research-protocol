# Step 181 — D0 I15 B2 posterior / LLR / one-way decode

> 2026-08-11 | author implementation | DONE

## 边界

- 只修改 `projects/simulation/explore/coded-decoder-feedback/b2.py` 与 `projects/simulation/tests/test_d0_b2_math.py`。
- 未修改 `common/`、参数、session、owner/freeze/codec/receiver 文件；未运行 science、I05 或 benchmark；未 stage/commit/push，未触碰 `p05_run*.log`。

## 实际代码

- 新增 nearest-pilot earlier-tie 选择与局部 pilot log-domain forward/backward posterior；`p_s=0` 保持 exact identity/Dirac，无 epsilon。
- 新增四状态 exact logsumexp、状态内 16QAM bit-set max-log LLR；支持 state permutation、received-only rotation inverse label shift、coordinate rotation no shift 与 uniform-state bit identities。
- 新增 `run_b2`，输出每偏振 6144×4 LLR，并对 X/Y 各调用一次 `decode_fresh`；无 callback、redecode、message/warm-state reuse。

## RED → GREEN

- RED：`python311 -m pytest projects/simulation/tests/test_d0_b2_math.py -q` → B201–B205 通过，B206–B212 因目标 API 缺失按预期 7 failed / 5 passed；命令耗时 `1.576s`。
- 初次 GREEN：`12 passed`，命令耗时 `1.421s`；发现 Dirac all-impossible 中间值产生 1 条 `log(0)` warning。
- 窄修：用 masked `np.log(..., where=total>0)` 保留 exact `-inf` 且消除 warning。
- 无 warning GREEN：`12 passed in 0.62s`，命令耗时 `1.469s`。
- 最终 fresh 验证：`py_compile` + B201–B212 整文件 + `git diff --check`，`12 passed in 0.49s`，合并命令耗时 `1.596s`，exit 0。

## 接收证据

- `b2.py` SHA256：`b1108f5ff5188d9adcc4e5f3b69c74e212926585df145ce4b458beb1cb839cf8`
- `test_d0_b2_math.py` SHA256：`33e734c36058ce1a55f109fb24845eb0547e2ad48b9890a87397ef6e6f293fc6`
- 负向源码扫描词：`epsilon|callback|redecode|message_state|warm_state|truth|payload|final_correct`；`b2.py` 0 命中。
- B212 dynamic spy：2 个调用，candidate IDs=`B2:X/B2:Y`，每次 shape=`(16,1536)`，每偏振恰好一次。

## 裁决

- P0/P1/P2：`0/0/0`（作者门，不代替独立验收）。
- 科学状态未改变：D0 science `NOT_RUN`，method signal `NONE`。
- 下一接口：I15 final bytes 进入本批唯一独立代码验收；PASS 后由主控继续下一个实际代码任务。

## 新 P1 窄修 receipt

> 2026-08-11 | reviewer-directed boundary repair | DONE

- 新增两个最小负向测试，覆盖 4 个非法输入变体：nonfinite `state_rotations`，以及 per-pol CW IDs 长度非 16、重复、非字符串。
- RED：focused `2 failed / 12 deselected`，`1.787s`。rotation 被错收并产生 NaN warning；单 ID 到达 decoder spy，证明验证缺失。
- 修复：`data_llr` 在计算前拒绝 nonfinite rotations；`run_b2` 在任何 LLR/decode 前要求每偏振 exact 16 个 unique non-empty plain-string IDs。
- Focused GREEN：`2 passed / 12 deselected`，`1.129s`。
- Final GREEN：`py_compile` + B201–B212 整文件 + `git diff --check`，`14 passed in 0.58s`，合并命令 `1.931s`，无 warning。
- 负向变体 4 项，最终错收/错拒=`0/0`；P0/P1=`0/0`（作者窄修门）。
- final `b2.py` SHA256：`d62c87619a012e0e71843ecf5d88973ab7c77dfe2465924bab39cc6d67b0f864`。
- final `test_d0_b2_math.py` SHA256：`612b10d775337592388a145e947163b925360f8379f6a2a6cd643f43c3355675`。
