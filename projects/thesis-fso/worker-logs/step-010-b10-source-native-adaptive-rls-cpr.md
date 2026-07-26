# T010 B10 source-native adaptive RLS CPR worker log

> 2026-07-26 | Phase C2 turn 1 | `PARTIAL_CONTINUE`

## 本段范围

- task-control validator 起飞 PASS。
- 将 `source-contract.yaml` 从 formal D020/C1 迁移到 formal D021/C2 validation-only，保留 Phase-B confirm 历史及 `phase_c1_method_contract`。
- 将 `contract.yaml` 激活为 `C2_VALIDATION_AUTHORIZED`，只开放 validation；held-out 与 performance conclusion 保持关闭。
- 按 TDD 新增并实现 deterministic primitives：30-setting canonical mapping、2250 integer keys、30-row strict-prefix checkpoint validation、17-file raw-byte SHA256 bundle、canonical-prefix SHA、atomic temp+fsync+replace、B* exact-tie deterministic selection。
- 未运行 source smoke、validation seed、test seed、held-out 或 Phase D。

## 命令与结果

1. `python C:\Users\zzt\.agents\skills\research-direction-lab\scripts\validate_task_control.py .sessions\2026-07-23-research-direction-lab-longitudinal-test\T010-b10-source-native-adaptive-rls-cpr.md`
   - PASS。
2. `PYTHONUTF8=1 python -m pytest ... -k "expected_keys or checkpoint_requires or hash_bundle or exact_tie or c2_authorization_migration or v025_contract"`
   - RED：6 failed，缺少 C2 primitives / 合同尚未激活。
3. `PYTHONUTF8=1 python -m pytest ... -k atomic_checkpoint_replace_failure`
   - RED：1 failed，`atomic_save_validation` 尚不存在。
4. 实现后重跑同一 deterministic selection：
   - GREEN：`7 passed, 30 deselected`。
5. `git diff --check`
   - exit 0；仅出现工作树既有 CRLF 提示。
6. protected-path diff：
   - `common/**`、`params.py`、T006/T008/T009 零改动。

## 安全点

合同与首批 deterministic primitives 已闭合；尚未实现/验证全局 setting score、
SNR-freeze objective 与 validation comparison runner，因此本段停止，不消费任何
scientific seed。既有两份 Phase-B artifacts 未更改。

## 后续

- 继续 TDD：setting score、primary freeze、pooled/effective BER、共同/无共同
  crossing 的三点 SNR window、checkpoint stale-hash/prefix-deep-equality。
- deterministic gates 全部通过后，才评估是否启动 C2 validation。

> 2026-07-26 | Phase C2 turn 2 | `PARTIAL_CONTINUE`

## Turn 2 deterministic closure

- task-control validator：PASS。
- TDD RED：剩余 setting/SNR/hash/prefix/aggregate primitives 为 `5 failed`；
  validation-cell/runner 为 `2 failed` 与 `1 failed`。
- TDD GREEN：
  - 剩余 primitives：`5 passed, 37 deselected`；
  - cell/aggregate：`2 passed, 42 deselected`；
  - runner checkpoint：`1 passed, 44 deselected`；
  - 完整 T010 定向测试：`45 passed in 2.61s`。
- `git diff --check` exit 0；validation raw/aggregate 均 `NOT_IGNORED`。
- 实现全局 setting score、P2/P3 primary tie、pooled/effective BER、
  common/no-common 3-point SNR window、stale 17-file hash 拒绝、
  prefix deep-equality/SHA、complete-only aggregate gate、30-row cell evaluator
  与 resumable validation runner。

## Turn 2 scientific checkpoint

- 命令：通过隔离模块调用 `run_validation(max_cells=1)`。
- 实际消费：validation seed `131001`，仅 weak / 14 dB 的首个 canonical cell。
- 结果：30 rows；first key `[0,0,0,0,0]`，last key `[0,0,0,5,2]`。
- checkpoint：`artifacts/validation-raw.json` 原子落盘；17-file hash、
  strict prefix、legacy debt 均复核 PASS；`directory_fsync=UNSUPPORTED_PLATFORM`。
- aggregate 未生成；held-out/test/source smoke 均未消费；临时文件数 0。

## Turn 2 安全点

完整 deterministic closure 已 GREEN，validation 停在合法 30-row cell 边界。
下一 turn 从 row 30 / cell 1 恢复，只追加 canonical 未运行 cells；全 2250 rows
完成前禁止 aggregate、排名与设置冻结。

> 2026-07-26 | Phase C2 turn 3 | `PARTIAL_CONTINUE_WITH_RUNTIME_ANOMALY`

## Turn 3 resume preflight

- task-control validator：PASS。
- 原 checkpoint：30 rows，17-file exact hash、strict prefix、legacy debt、
  heldout=false、directory-fsync 标记均 PASS。
- 未修改 code/tests/contracts；继续使用已冻结 source hash。

## Turn 3 validation execution

- 请求：`run_validation(max_cells=30)`。
- 耗时：526.2 s。
- 成功新增 27 个完整 cells / 810 rows；总计 28 cells / 840 rows。
- 已完成范围：
  - weak：全部 25 cells，即 SNR `[14,17,20,23,26] dB` × seeds
    `131001–131005`；
  - moderate：14 dB × seeds `131001–131003`。
- 最后合法 key：`[1,0,2,5,2]`。
- 下一 canonical key：`[1,0,3,0,0]`。

## Turn 3 anomaly 与安全点

- 在 moderate / 14 dB / seed `131004` 的 P1 setting 0 开始执行时，
  `source_native_rls.py` 抛出
  `ValueError: source-native identity requires finite positive CFO slope`。
- 失败 cell 未写入、未修补、未覆盖；按 checkpoint 合同立即停止。
- checkpoint 复核：840 rows、17 hashes、strict prefix PASS；temp files=0；
  aggregate 不存在；held-out/test/source-smoke 未运行。
- `git diff --check` exit 0；protected/common/params/旧包零改动。

> 2026-07-26 | Phase C2 systematic debugging Phase 1 | 仅诊断

## 失败 cell 确定性复现

- cell：moderate / 14 dB / seed `131004`。
- 独立重建 2 次：
  - RX SHA256 均为
    `c6a14e779311b96a7350d750a7a737bfc4007b97c4343f048c2f4e953d921c5f`；
  - GG SHA256 均为
    `3d7cc0b1cf3a532a23d6c592b7bd77df70d1360b1191ca1a22a83c4bbfbdf790`；
  - 全部诊断数字和 traceback 完全一致。
- traceback：

```text
Traceback (most recent call last):
  File "<stdin>", line 24, in diagnose
  File ".../source_native_rls.py", line 74, in run_source_native_rls
    raise ValueError("source-native identity requires finite positive CFO slope")
ValueError: source-native identity requires finite positive CFO slope
```

## 数据流证据

### 真实相位与输入幅度

- 合同 CFO slope：`+0.0025132741228718345 rad/symbol`；
  含 PN 的前 128 symbol true-phase LS slope：
  `+0.0027734092386368595`。真实符号约定为正。
- pilot GG：均值 `0.2427183`，min `0.2424893`，无 `h<0.1`；
  GAR block=100 导致前 100 个 pilot 共用一个 h，后 28 个共用另一个 h。
- pilot RX amplitude：min/p05/median/mean/max =
  `0.1067/0.1805/0.5017/0.5060/1.0339`。
- 14 dB 经该 fade 后的 mean effective Es/N0 约 `7.851 dB`；
  最低星座点的无噪声场幅约 `0.2203`，complex noise RMS `0.1995`。

### angle / unwrap

- raw first/last：`0.14821 / 0.000529 rad`；
  unwrap first/last：`0.14821 / -6.282656 rad`。
- raw wrap jump 数：1；unwrap `|step|>π/2` 数：3；
  max unwrap step：`3.06684 rad`。
- 关键 false branch：
  - 7→8：RX amplitude 降到 `0.1067`，raw
    `-0.4179→+3.0458`；`np.unwrap` 选成
    `-0.4179→-3.2374`；
  - 8→9：随后到 `-6.3042`，而 true phase 仅
    `0.02584→0.03455`；
  - 该错误 branch 使其后观测整体少 `2π`。
- observed unweighted LS slope：`-0.0138504`，已在进入 RLS 前反号。

### RLS 与方法初始化

- λ=.98/.99/.999 的最终 `h[1]` 分别为
  `-0.0062947/-0.0109464/-0.0164973`；三者均保持负号。
- λ=.98 关键迭代 h1：k1 `+0.03743`、k2 `-0.07404`、
  k8 `-0.18994`、k16 `-0.53336`、k64 `-0.04671`、
  k128 `-0.0062947`。
- P1 与 P2 使用相同 pilot/observed/h0/P0/λ=.98，均在 pilot 门失败；
  P3 用同一 pilot/observed/h0/P0、λmax=.999，也在同一门失败。
  因此异常早于 DD gating/adaptive forgetting。

## 相邻成功 cell 对照

- moderate / 14 dB / seed `131003`：
  - true-phase LS slope `+0.00222638`；
  - pilot GG mean `1.476998`，pilot RX median `1.25641`；
  - raw wrap jump 0，observed LS slope `+0.00156570`；
  - RLS h1 λ=.98/.99/.999 =
    `+0.00234342/+0.00191140/+0.00162253`；
  - P1/P2/P3 pilot initialization 均通过。

## 单一 root-cause hypothesis 与 falsifier

**Hypothesis**：失败来自 moderate fade 将 pilot 的有效观测 SNR 降至约
7.85 dB；第 8 个低幅 pilot 的接收点被噪声推到 angle branch 附近，
`np.unwrap` 产生一个虚假的 `-2π` branch。因而 unweighted LS 在 RLS 前已经
得到负 slope，RLS 只是忠实拟合受污染的 observable sequence。证据不支持
runner、RLS递推或正/负符号约定是首发根因。

**Falsifier**：在保持同一 frozen RX bytes 不变的只读分析中，如果能证明
`np.unwrap(angle(rx/pilot))` 的 branch 与真实连续相位同支，或在送入 RLS 前的
独立 unweighted LS slope 为正且只有 RLS 输出转负，则本假设被推翻，根因应转向
RLS递推；若同 RX/参数重复生成不同 bytes，则应转向 runner/RNG。

本段未提出或实施修复，未运行 validation continuation，未改 raw/aggregate。
