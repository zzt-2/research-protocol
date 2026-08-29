# Step 083: Ch4 historical-observation corrected-demapper replay

> 2026-08-30 | T083 / D062 / V037 / CP024 | 实现者记录

## 事实

1. 起飞 task-control validator=`PASS`；只执行 A1 exact replay，未建立新 RNG、未加入 B3_PSC、未运行 A2/smoke/production。
2. TDD RED：新建测试后、实现前 focused=`5 failed`，失败原因均为 `demapper_replay_*` manifest/runner/reducer 尚不存在。
3. TDD GREEN：focused=`5 passed in 4.03s`；包含单窗 identity、完整 256-window identity census、机制量、paired bootstrap/gate 与 manifest-hash fail-closed。
4. 固定 4×64 replay 只运行一次。全部 `256/256` seed/gain/realization hash/observation hash/payload-bit identity 通过；五臂机制量 `1280/1280` 行与 T071 raw 在绝对容差 `2e-15` 内一致。
5. T071 四个 historical artifact 的 SHA-256 在任务前后不变；新 raw 只允许 corrected demapper 引起 `bit_errors/BER` 变化，runtime 可变。
6. raw-only reducer 以 window 为 paired unit；每个 named comparison 重置 PCG64 seed=`2026083005`，resamples=`5000`，quantiles=`2.5%/97.5%`。

## 历史 authority SHA-256

| artifact | SHA-256 |
|---|---|
| `confirmation_manifest.json` | `18c93796ff3e7e0ebf0bf05ee71c94bfd4027218b31a60d0d917d26581aa8a65` |
| `confirmation_raw.json` | `55c31e36b7d11e5d0b9e8225805596e0f0f7b127cde26874c7b0b217b0e23101` |
| `confirmation_aggregate.json` | `78e6795b17b1cfcbe5ee297c001e6e92bd81a6576c54ed317aeda526acbd17c9` |
| `confirmation_receipt.json` | `7508f61a6f30ade11e3770b819fcbda028726b8ef42f0c40e7152ad9b90be1e2` |

## Corrected replay 数字

| cell | B2 errors/bits | B2 BER | C4 errors/bits | C4 BER | mean(C4-B2) | 95% CI | C4 window wins |
|---|---:|---:|---:|---:|---:|---:|---:|
| `snr14_np2` | 178610/2097152 | 0.0851678848 | 161245/2097152 | 0.0768876076 | -0.0082802773 | [-0.0121246457, -0.0049545288] | 51/64 |
| `snr14_np4` | 153540/2097152 | 0.0732135773 | 145707/2097152 | 0.0694785118 | -0.0037350655 | [-0.0056052446, -0.0019459724] | 46/64 |
| `snr18_np2` | 84450/2097152 | 0.0402688980 | 74744/2097152 | 0.0356407166 | -0.0046281815 | [-0.0072456598, -0.0023582816] | 35/64 |
| `snr18_np4` | 47812/2097152 | 0.0227985382 | 44171/2097152 | 0.0210623741 | -0.0017361641 | [-0.0030241013, -0.0006393552] | 28/64 |

Pooled Np=2：clusters=`128`，mean(C4-B2)=`-0.0064542294`，95% CI=`[-0.0086839616,-0.0043308616]`，C4 wins=`86/128`。

## Gate

- pooled Np2 CI upper=`-0.0043308616 < 0`：PASS；
- `snr14_np4` CI lower=`-0.0056052446 <= 0`：PASS；
- `snr18_np4` CI lower=`-0.0030241013 <= 0`：PASS；
- identity/schema/source-hash/truth-firewall/raw-only：PASS。

因此 frozen terminal=`DEMAPPER_REPLAY_PASS`。该终态只说明 corrected global-ML scoring 下历史 C4-vs-B2 承重信号仍存在；它不等于 A2/B3_PSC 已通过，也不是正式论文结论。

## 命令与验证

| 命令 | 结果 |
|---|---|
| `python -m pytest .../tests/test_demapper_replay.py -q`（RED） | `5 failed`（预期缺实现） |
| 同 focused（GREEN） | `5 passed in 4.03s` |
| `python .../run_demapper_replay.py` | `4×64` 完成，raw 由 `save_results()` 写入 |
| `python .../reduce_demapper_replay.py` | aggregate/receipt 由 `save_results()` 写入，terminal PASS |
| 新测试 + confirmation/development/scaled-unitary/demapper 邻接测试 | `27 passed in 5.45s` |
| `python -m py_compile` 三个新 Python 文件 | PASS |
| T083 task-control validator | PASS |
| JSON parse/hash/count + historical immutable | `4 cells / 256 windows / 1280 rows`，PASS |
| `git diff --check` | PASS（仅报告共享 worktree 既有 CRLF warning） |

## 精确文件清单

1. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/demapper_replay_manifest.json`
2. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/run_demapper_replay.py`
3. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/reduce_demapper_replay.py`
4. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/tests/test_demapper_replay.py`
5. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/demapper_replay_raw.json`
6. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/demapper_replay_aggregate.json`
7. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/demapper_replay_receipt.json`
8. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/.gitattributes`（主控在实现完成后仅补四个新 JSON 的稳定 EOL 规则）
9. `projects/thesis-fso/worker-logs/step-083-ch4-historical-demapper-replay.md`

共享 worktree 的既有 modified/untracked 文件未清理、未覆盖、未纳入本任务。未 commit、未 push。

## 约定变更

T071 cells/seeds/arms/signal model/mechanism metrics 保持不变；唯一允许变化是 corrected demapper 的 BER scoring。实现后发现 `core.autocrlf=true` 会使新 JSON 在 fresh checkout 后产生字节 SHA 漂移，主控据此在 T083 白名单和 seam `.gitattributes` 中补入与实际生成格式一致的规则：manifest=`LF`，raw/aggregate/receipt=`CRLF`。该修复不改变 JSON 语义、样本、数字或 gate。

## 终态

`DEMAPPER_REPLAY_PASS`

下一步只允许未参与实现的 reviewer 独立解析 raw、重算 identity/counts/CI/terminal；实现者不宣布 A2 已开放。
