# Ch4 C4-2 gated-RDE 有界开发独立科学验证

> 2026-08-30 | T062 | 独立 verifier | 未运行 `run_development.py`，未读取 confirmation 结果

## 0. 结论

- **验证结论：`PARTIAL`**。
- **IMPLEMENTATION_CORRECTNESS：`PASS`**。fresh tests、correctness smoke、公式调用链、truth firewall、paired realization 与 count-match 实现均成立。
- **C4-2 SCIENTIFIC DISPOSITION：接受 `D/STOP_NO_METHOD_SIGNAL`**。三个 Round-1 cell 均无 10% oracle headroom；candidate/cheap 对 `B0*` 均退化且 paired wins 均为 0。高 AUROC 不能越过 BER/oracle 停机门。
- **是否允许轮换 C4-1：是**。Round 2 合法地未生成，winner=`none`；可按 D046/T059 轮换 C4-1，不得为 C4-2 增加第三轮、第三种 gate 或 confirmation。
- `PARTIAL` 的唯一原因是 **receipt SHA 的跨 worktree 换行可移植性缺口**；原 executor worktree 五项 hash 全部精确匹配 receipt，故不是 T059 后实质篡改，也不影响 raw→aggregate 或科学 STOP。

## 1. Fresh 命令证据

### 1.1 task-control

```text
python .agents/skills/research-direction-lab/scripts/validate_task_control.py \
  .sessions/2026-07-09-thesis-writing/T062-verify-ch4-bounded-gated-rde-development.md --repo-root .
PASS
```

控制为 epoch 8 / CP008 / `INDEPENDENT_SCIENTIFIC_VERIFICATION`。

### 1.2 两份 Ch4 tests

```text
python -m pytest \
  projects/simulation/tests/test_ch4_apsk_ring_gated_rde.py \
  projects/simulation/tests/test_ch4_apsk_ring_gated_rde_development.py -q
............ [100%]
12 passed in 2.80s
```

### 1.3 correctness smoke

`run_smoke.py::main()` fresh 执行；receipt sink 重定向为内存对象，未刷新仓库 receipt：

```text
exit code: 0
internal pytest: 7 passed in 0.37s
identity LS max abs error: 0
random-J LS max abs error: 2.289170737184863e-16
accepted updates: candidate=506, cheap=506, oracle=512, plain=512
realization hash: 815ed95330f7452a1863168514cd520ca0596ae92bad558e259769f6583b879a
verdict: CORRECTNESS_ONLY
method signal: NO_METHOD_SIGNAL
blockers: []
```

### 1.4 一次性 raw probe

独立 probe 只使用 `json/yaml/numpy/hashlib`，未导入 `run_development.py`，未生成文件：

```text
raw rows=126 = 3 cells × 6 eval seeds × 7 arms
cells=D1,D2,D3; rounds=[1]
eval seeds=54201..54206; max seed=54206
seed >=54301 rows=0; D4-D6 rows=0
18/18 cell-seed groups: 7 arms share exactly one realization hash
36/36 gated/count-matched pairs: accepted_count=source_gate_count
raw→aggregate scalar mismatches=[]
independent Round-1={winner:none, enter_round2:false,
  stop_reasons:[NO_ORACLE_HEADROOM,NO_PREREGISTERED_GATE_SIGNAL]}
```

### 1.5 工作树检查

写报告前 `git status --short` 为空，`git diff --check` 退出码 0。smoke 与 raw probe 均未改实现或结果。

## 2. Manifest、实现与 firewall

### 2.1 冻结合同

Manifest 与 T059 一致：

- Round 1：D1=`14 dB/2 pilots`，D2=`18 dB/2 pilots`，D3=`14 dB/8 pilots`；
- Round 2：D4=`14 dB/4 pilots`，D5=`18 dB/4 pilots`，D6=`18 dB/8 pilots`；
- payload=`8192`，block=`256`；
- tune=`54101–54103`，eval=`54201–54206`，confirmation floor=`54301`；
- raw 只含 Round 1 的 126 行，最大 seed 54206，未生成 Round 2 或 confirmation 行。

四个 arm 的 tuning ledger 均恰有 9 个配置；独立重做 1% tie-break 后，选择与 ledger/raw 一致：plain/oracle `mu=1e-3`，cheap `mu=3.16e-4,tau_r=.8`，candidate `mu=3.16e-4,tau_r=tau_d=.8`。eval rows 不含 tune seeds，且每个 arm 只出现冻结配置。

### 2.2 canonical update、gate 与 truth firewall

- `_run_rde` 对 plain/cheap/candidate/oracle 统一用 `canonical_nearest_radius(z)` 的 radius 进入 `canonical_rde_step`。
- cheap gate 只读 canonical native-ring residual；candidate gate 只读 nearest-point ring residual 与 nearest-symbol decision distance。
- oracle 的 TX label 只参与 gate equality；update radius 仍从接收输出 `z` 的 canonical nearest radius 得到，`mu` 来自独立冻结 grid。deployable arm 的签名不接收 TX symbols、Jones truth、true SNR 或 evaluation BER。
- `wrong_ring=(predicted_label>=8)!=(truth_label>=8)`；ring AUROC 用 native-ring score 对 wrong-ring，decision AUROC 用 decision score 对 wrong-symbol，combined AUROC 用双门归一化最大分数对 wrong-symbol。D2 六个 candidate row 的 wrong-ring 正样本均为 0，故 ring AUROC=`N/A` 合法。

### 2.3 paired realization 与 count-match

每个 cell-seed 的 7 个 arm 均共享同一 `realization_hash`；18 个 cell-seed 对应 18 个唯一 realization。`count_matched_masks` 按每偏振、每 256 symbols 分块，以独立确定性 RNG 抽取 source gate 的实际 count；`_count_matched` 复用对应 gated arm 的 `mu`。fresh test 覆盖 per-pol/per-block invariant；raw 对全部 36 个 source/count-matched 对确认 frame-total count 三方相等：

| cell | seed | cheap=CM | candidate=CM |
|---|---:|---:|---:|
| D1 | 54201 | 15076 | 15244 |
| D1 | 54202 | 14958 | 15136 |
| D1 | 54203 | 15005 | 15177 |
| D1 | 54204 | 15303 | 15483 |
| D1 | 54205 | 15259 | 15387 |
| D1 | 54206 | 15067 | 15199 |
| D2 | 54201 | 16114 | 16125 |
| D2 | 54202 | 16099 | 16099 |
| D2 | 54203 | 16131 | 16131 |
| D2 | 54204 | 16203 | 16205 |
| D2 | 54205 | 16175 | 16177 |
| D2 | 54206 | 16121 | 16121 |
| D3 | 54201 | 15271 | 15460 |
| D3 | 54202 | 15191 | 15329 |
| D3 | 54203 | 15117 | 15315 |
| D3 | 54204 | 15302 | 15471 |
| D3 | 54205 | 15296 | 15435 |
| D3 | 54206 | 15240 | 15422 |

## 3. Raw 独立重算

每个 cell-arm 的总 bit 数均为 `393216=6×2×8192×4`。Jeffreys BER 独立按 `(errors+0.5)/(bits+1)` 计算；gain 为相对本 cell `B0*=min(LS-only,tuned plain)`；wins 为 6 个 paired eval seed 中严格优于 `B0*` 的个数。AUROC 是 raw 中逐 seed AUROC 忽略 `N/A` 后的算术均值。

| cell | arm | errors | Jeffreys BER | gain vs B0* | wins | ring / decision / combined AUROC |
|---|---|---:|---:|---:|---:|---|
| D1 | plain (B0*) | 10844 | 0.02757892 | 0 | 0 | .973/.794/.661 |
| D1 | LS-only | 14805 | 0.03765224 | -36.527% | 0 | .500/.500/.500 |
| D1 | oracle | 10842 | 0.02757383 | +0.018% | 3 | .973/.794/.661 |
| D1 | cheap | 11470 | 0.02917092 | -5.773% | 0 | .964/.785/.657 |
| D1 | candidate | 11586 | 0.02946592 | -6.842% | 0 | .961/.786/.661 |
| D1 | CM-cheap | 11553 | 0.02938200 | -6.538% | 0 | .964/.787/.658 |
| D1 | CM-candidate | 11531 | 0.02932605 | -6.335% | 0 | .964/.787/.658 |
| D2 | plain (B0*) | 1968 | 0.005006142 | 0 | 0 | N/A/.928/.692 |
| D2 | LS-only | 3139 | 0.007984141 | -59.502% | 0 | .500/.500/.500 |
| D2 | oracle | 1971 | 0.005013771 | -0.152% | 1 | N/A/.928/.692 |
| D2 | cheap | 2130 | 0.005418128 | -8.232% | 0 | N/A/.922/.685 |
| D2 | candidate | 2132 | 0.005423214 | -8.333% | 0 | N/A/.921/.685 |
| D2 | CM-cheap | 2123 | 0.005400326 | -7.876% | 0 | N/A/.922/.685 |
| D2 | CM-candidate | 2122 | 0.005397783 | -7.825% | 0 | N/A/.922/.685 |
| D3 | plain (B0*) | 9103 | 0.02315134 | 0 | 0 | .981/.818/.668 |
| D3 | LS-only | 11098 | 0.02822487 | -21.916% | 0 | .500/.500/.500 |
| D3 | oracle | 9108 | 0.02316405 | -0.055% | 1 | .979/.818/.668 |
| D3 | cheap | 9427 | 0.02397531 | -3.559% | 0 | .974/.813/.667 |
| D3 | candidate | 9490 | 0.02413553 | -4.251% | 0 | .973/.814/.671 |
| D3 | CM-cheap | 9473 | 0.02409230 | -4.065% | 0 | .974/.814/.668 |
| D3 | CM-candidate | 9481 | 0.02411264 | -4.152% | 0 | .974/.815/.668 |

关键 cell 结论：

| cell | B0* arm / BER（raw） | B0* errors | oracle headroom | candidate gain | cheap gain | underpowered |
|---|---|---:|---:|---:|---:|---|
| D1 | plain / 0.02757772 | 10844 | +0.0184% | -6.842% | -5.773% | false |
| D2 | plain / 0.005004883 | 1968 | -0.1524% | -8.333% | -8.232% | false |
| D3 | plain / 0.02315013 | 9103 | -0.0549% | -4.251% | -3.559% | false |

三格的 `B0*` error count 均远高于 100，因此均非 `UNDERPOWERED`。raw 重算与 aggregate 中所有相关 scalar（errors、BER、gain、wins、三类 AUROC、B0*、oracle headroom、underpowered）零不一致。

## 4. Round-1 停机复判

独立按冻结规则执行：

1. candidate 与 cheap 在三格相对 `B0*` 均为负增益，paired wins 均为 `0/6`，两个 arm 均不满足进入 Round 2 的 BER 路由。
2. candidate combined AUROC 为 `.661/.685/.671`，cheap ring AUROC为 `.964/N/A/.974`；score 有判别力，但 AUROC 只是机制代理，不是 BER/oracle 门的替代品。
3. oracle headroom 为 `+0.0184%/-0.1524%/-0.0549%`，三格均 `<10%`，直接触发 `NO_ORACLE_HEADROOM`。
4. 无 gated arm 形成预注册正信号，故 `winner=none` 与 `NO_PREREGISTERED_GATE_SIGNAL`；Round 2 必须停止。
5. count-matched 不是本次 STOP 的主因：没有任何相对 `B0*` 的 apparent gain 可供“吸收”。

因此唯一合法结论为：`winner=none`、`D/STOP_NO_METHOD_SIGNAL`、`NO_ORACLE_HEADROOM`、`NO_PREREGISTERED_GATE_SIGNAL`。这是 **C4-2 科学 STOP**，不是 correctness 失败。

## 5. 问题（按严重度）

### Important — receipt SHA 跨 worktree 不可移植（不影响科学结论）

当前 verifier worktree 把部分文本文件物化为 CRLF；receipt 的 SHA 则来自原 executor worktree。当前字节直接 hash 时，manifest/driver/development-test 与 receipt 不同，而 core/report 相同，形成混合换行约定。

只读核对原 executor worktree `C:\Users\zzt\.codex\worktrees\d071\research-protocol` 后，五项均与 receipt **精确一致**：

| artifact | executor SHA-256 / receipt |
|---|---|
| manifest | `ff5419eeb11e3553f3ad8b1084552c92abe41fe96d80f23e5a97d7e41effacdd` |
| driver | `1e8309e0d1c1d3b1de89046136ccdd14e2ab6699a9276a05bbc38d33fd058f10` |
| development test | `187c100c0c6c1d7d6f0d2cf8d5bfe1bafbe9a5189c21ba3f05525ee41f4beced` |
| core | `6dbe14d0d7cd6eb8cf34286a2e8767eb4d0842a5c5339f74195c4c7af8239db2` |
| report | `fd70a1ce27dd419a32705857bd85e89eb47a46ff8c4b361c97cd0ffa287980dd` |

manifest/driver/test 在当前 worktree 归一化为 LF 后也分别等于 receipt SHA；git 工作树 clean，且 HEAD 内容无语义 diff。因此这是 provenance portability/reporting gap，不是 stale science 或篡改。已停路线不值得为此重跑矩阵或改 hash。

**Critical/High 科学问题：无。**

## 6. 唯一下一动作

主控将 C4-2 登记为已独立接受的 `D/STOP_NO_METHOD_SIGNAL`，随后按 D046/T059 **轮换 C4-1**；不得修补 C4-2 hash、重跑 development matrix、读取 confirmation seeds、增加第三轮或自行改 gate。
