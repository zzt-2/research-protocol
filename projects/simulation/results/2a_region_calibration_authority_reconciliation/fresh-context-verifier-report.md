# Fresh-context verifier report — 2A authority reconciliation

> 2026-08-07 | read-only independent subagent | VERDICT=`PASS` | P0/P1/P2=`0/0/0`

Verifier 未继承执行对话上下文、未参与实现或裁决、未修改 worktree。以下结论由主线程按 verifier 返回原样
登记。

## 九项检查

1. **授权来源 — PASS**：用户的“行”被准确记录为对主控完整受限方案的转述授权，没有伪造成用户逐字
   复述；“这种东西，不太能写吧？”准确关联 D038。
2. **三对象分账 — PASS**：P01 adapter、P02 scalar retune、T004 online map 在 D038、authority、package、
   inventory 与图中均独立。
3. **region identity / truth / scalar — PASS**：P02 caller 签名
   `decide_adapter_weakretune(raw, gamma_hat_db, gamma_hat_lin, b)`，无 region/scene/true-SNR 参数；truth 只
   定义 `TARGET_CELLS=[weak@5,7,9]`；所有 cell 共用冻结 `ref_snr_db=11`，distinct actions=`1`。六门仅
   truth-not-in-decide 通过。
4. **chronology — PASS**：P01 dev `0–9`、held-out `30–49`；P02 dev `50–59`、held-out
   `60–70 ∪ 81–99`，均互斥。P02 首批 20 seeds 为 `60–70 ∪ 81–89`，观察结果后追加 `90–99`，不是
   pristine one-shot 30-seed confirmation。
5. **raw→aggregate — PASS**：P01 恢复 4/5，material safety failure 1/15；`weak@9=-0.3228487286 dB`，
   CI `[-0.3567860861,-0.2889113710]`。P02 weakretune-adapter=`+0.4538673652 dB`，cluster CI
   `[+0.4340368738,+0.4736978566]`；cand_rank-weakretune=`-0.0960851354 dB`，cluster CI
   `[-0.1027456689,-0.0894246019]`；branch occupancy 非零 `207/210`，且已披露无逐窗 command trace。
6. **comparator / dev-vs-heldout — PASS**：T004 dev-only 6-cluster 表为 B0=`0`；B1=`+0.1368759553`
   CI `[0.0511724323,0.2225794782]`；B2=`+0.3084554511` CI `[0.1745499332,0.4423609690]`；
   M=`+0.2674971826` CI `[0.1371888329,0.3978055322]`；M-B2=`-0.0409582685 dB`。没有把它写成
   held-out claim。
7. **未运行新 held-out — PASS**：T004 receipt 为 `test_started=false`、`heldout_artifacts_absent=true`、
   `heldout_never_run=true`；commit tree 无 chronology/raw/summary held-out。T009 为 deterministic-only，
   `bounded_confirmation_run=false`，三份输出复跑前后 SHA-256 相同。
8. **owners / package / terminal — PASS**：D038、CP021、epoch 34 control、registry、inventory 2A、authority、
   package、worker log 与 SVG 均闭合到唯一 `SUPPORTING_ONLY`；T004 `REJECT` 与 D036 Ch5 scheduling
   authority 独立保留。
9. **范围边界 — PASS**：未见 `common/`、`params.py`、CCISP 本体或论文正文修改。四个既有
   `p05_run*.log` 仍为 untracked/unstaged，必须继续排除在最终提交之外。

## 原始命令证据

```text
python -m pytest projects/simulation/results/2a_region_calibration_authority_reconciliation/test_recompute_existing_evidence.py -q
...                                                                      [100%]
3 passed in 2.44s
```

```text
python projects/simulation/results/2a_region_calibration_authority_reconciliation/recompute_existing_evidence.py
{"terminal": "SUPPORTING_ONLY", "semantic_gate": false}
HASH recomputed-evidence.json BEFORE=66CF3BE1C860ECA8293489CE4582FB9CF477A181B156DC052BA5CCDF1BEBAEB9 AFTER=66CF3BE1C860ECA8293489CE4582FB9CF477A181B156DC052BA5CCDF1BEBAEB9 IDENTICAL=True
HASH p01-harm-cells.csv BEFORE=9A85854C2C85BCA209AC78D54FE61A24D256A8951CE5E06F7164EBF519C23A8A AFTER=9A85854C2C85BCA209AC78D54FE61A24D256A8951CE5E06F7164EBF519C23A8A IDENTICAL=True
HASH original-global-region-table.csv BEFORE=D0BAA3DF7E6FFD58933C3861D00197A0B5CB3D351045F485ED0A3659A63B10D5 AFTER=D0BAA3DF7E6FFD58933C3861D00197A0B5CB3D351045F485ED0A3659A63B10D5 IDENTICAL=True
```

```text
JSON PASS: recomputed terminal=SUPPORTING_ONLY semantic_gate=False bounded_confirmation_run=False; T004 test_started=False heldout_absent=True heldout_never_run=True
YAML PASS: registry active/conflicts=[]; inventory 2A=SUPPORTING_ONLY, P02 method_like=false/chapter_capable=false; task epoch33/CP020; current epoch34/CP021
XML PASS: SVG parses and contains P01/P02/T004, runtime-region failure, pre-test REJECT, SUPPORTING_ONLY
CSV PASS: p01-harm-cells.csv rows=5
CSV PASS: original-global-region-table.csv rows=4
CONSISTENCY PASS: D038/CP021/topic/inventory/package/authority/worker/SVG terminal=SUPPORTING_ONLY
git diff --check: exit 0 (only LF→CRLF working-copy warnings)
```

## 终验结论

`PASS`。本轮唯一合法 terminal 为 `SUPPORTING_ONLY`；没有承重事实缺口或需修复的 P0/P1/P2。
