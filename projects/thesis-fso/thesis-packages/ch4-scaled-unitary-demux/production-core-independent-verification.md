# Ch4 production core independent verification

> 2026-08-30 | T084 / D063 / V038 / CP025 | independent code/science review

## Terminal

`PRODUCTION_CORE_CORRECTNESS_INVALID`

P0/P1/P2=`0/1/1`。实现的生成路径、数学公式和 frozen tests 均通过；但消费侧 `_validated_latent` 接受被篡改的 RNG namespace 与 turbulence authority snapshot，未闭合 T084 要求的完整可复现 provenance contract。该问题修复前不得开放 A2。

## Findings

### P1 — latent validator 未验证 namespace/authority 元数据

`make_latent_window()` 生成的七个 SeedSequence 子流本身正确：独立 oracle 对 moderate/latent 123 的七个 component 逐一按 entropy=`20260830`、spawn key=`[84,1,1,123,component_code]` 重建，七个数组/标量、七个 spawn key 和 exact replay 全部一致。

但 `_validated_latent()` 只检查 `rng_namespace` 与 `turbulence` 字段存在，不检查：

- namespace 的 key set、bit generator、entropy 与完整 spawn key；
- spawn key 中的 scenario code / latent ID / component code 是否与窗口身份一致；
- turbulence snapshot 是否等于 `SimulationConfig().turbulence` 当前 authority，或其 scenario 是否一致。

独立 mutation probe 把 `payload_bits.spawn_key` 改为 `[999,999]`，`observe_latent()` 仍成功；另把 moderate snapshot 的 `alpha` 改为 `999`，同样仍成功。虽然数值 latent hashes 未变，但正式 seam 会接受与实际随机总体/物理 authority 矛盾的 provenance。T084 明确要求完整 namespace、exact replay 与 invalid input fail-closed，因此这是 correctness gate 的 P1，而不是只改文档即可消除的问题。

最小修复边界：在 `_validated_latent()` 内从 `scenario + latent_id` 重新构造 expected namespace，要求七个 component 精确相等；重新解析 `_resolved_turbulence(scenario)` 并要求 snapshot 精确一致。补两个先 RED 的 mutation tests，不改 RNG、参数或科学设计。

### P2 — B3_PSC 的 `channel_nmse` 必须限定为继承的 B2 estimator metric

B3_PSC 正确地保留 B2 `h_hat`，同时把最终 payload inverse action 改成 `a W_B2`。因此 `score_action()` 对 B3 的：

- `channel_nmse` 衡量的是 calibration 前、继承自 B2 的 channel estimate；
- `inverse_residual` 衡量的是 calibration 后实际执行的 `a W_B2`。

这不是公式错误，也不要求把 `h_hat` 人为改成 `h_hat/a`；当 `a=0` 时后者甚至没有合法定义。但两项不能被共同解释成同一个“最终等效 channel estimate”的机制量。正式 Fig. 4-4 若不画 B3 的 channel-NMSE，本问题只需在 comparator/metric contract 说明；若画 B3，必须标成 inherited pre-calibration B2 NMSE，并用 inverse residual 表示 PSC 的实际动作效果。当前代码字段没有这一语义标签，故记 P2 claim/plot boundary，不单独阻塞 correctness。

## Independent oracle results

### RNG namespace、latent replay 与 SNR/Np pairing

- 自建 PCG64/SeedSequence oracle，没有调用任务测试 helper。
- moderate / latent 123 / payload 13 / max pilots 16：七个 namespace=`7/7`、七个 component exact=`7/7`、第二次 latent replay exact PASS。
- 7 dB/Np2 与 31 dB/Np16 共用全部 latent hashes；pilot noise 为同一冻结前缀，payload latent 不变。
- analytic noise-scale ratio=`15.8489319246111`，等于 `sqrt(10^2.4)`；逐元素重建 `Yp/Y` 最大误差在 `2e-15` 容差内。

### Authority、pilots 与 receiver identities

- `SimulationConfig().turbulence` 直接解析：weak `(11.6,10.1)`、moderate `(4.0,1.9)`、strong `(4.2,1.4)`。
- rounded-parameter GG scintillation indices 独立计算为 `0.193752134 / 0.907894737 / 1.122448980`；kernel 未硬编码 Rytov variance 第二份 authority。
- Np=`2/4/8/16` 的 `Xp Xp^H=Np I` 全部 exact PASS。
- B2 tau=1 与 C4 的 `W × public_scale` 均等于独立 SVD 构造的 `V U^H`。
- deployable `receiver_action` 签名恰为五个 observation-only 参数；源码无 `h_true/bits/decision/truth`。

### B3_PSC closed-form oracle

- 正常有限样本：独立闭式标量 `a=0.999832217636138`；`W_B3=aW_B2`、`Z_B3=aZ_B2`、B2 `h_hat`/tau identity 全部 PASS。
- negative numerator：返回 constrained optimum `a=0`。
- zero denominator、nonfinite denominator/input、finite-input overflow-to-nonfinite scalar 三类均 fail closed，`3/3` PASS。
- bad tau 的 None/bool/out-of-range/nonfinite paths 均拒绝。

### Structure mismatch oracle

自建 Haar `U,V`，`g=1.37`，delta=`0/.05/.1/.2/.3/.4`：

- 独立公式逐元素一致；
- `||H||_F^2/2=g^2` 全部通过；
- singular-value ratio 依次为 `1.000000000, 1.105263158, 1.222222222, 1.500000000, 1.857142857, 2.333333333`，与 `(1+delta)/(1-delta)` 一致且严格递增。

## Frozen verification commands

| 验证 | 结果 |
|---|---|
| T084 focused three-file pytest | `29 passed in 1.28s` |
| independent inline oracle | 数学/生成路径 PASS；metadata mutation probe 暴露 P1 |
| `python -m py_compile production_core.py tests/test_production_core.py` | PASS |
| T084 task-control validator | PASS |
| exact T084 scope | 仅 implementation/test/worker-log 三个未跟踪文件；`scaled_unitary.py/common/params` 无 T084 diff |
| scoped `git diff --check` | PASS |
| worktree-wide `git diff --check` | exit 0，仅共享既有 papers CRLF warning |

## Scope

本 reviewer 只新增本报告；未修改实现或测试，未运行 BER、A2、smoke、tuning 或 production，未 commit/push。

## Gate interpretation

生成路径和核心数学不变量值得保留，不需要换设计。下一动作只能是一次最小 correctness repair：补 namespace/authority consumption validation 与 RED mutation tests，然后由 fresh reviewer 重跑同一 oracle。P1 清零前不得把 frozen-test GREEN 转述为 `PRODUCTION_CORE_CORRECTNESS_PASS`。

---

## Repair recheck — 2026-08-30

> 本节追加 fresh repair evidence；上方初审 `INVALID / 0-1-1` 保留为历史，不覆盖。

### Fresh terminal

`PRODUCTION_CORE_CORRECTNESS_PASS`

Fresh P0/P1/P2=`0/0/1`。唯一 P2 是已经披露的 B3_PSC metric-semantics 边界，不阻塞 production-core correctness；P1 provenance blocker 已由消费侧 fail-closed 修复并经独立 exploit 重放清零。

### 原 exploit 独立重放

Reviewer 没有调用 task test helper，自行复制 fresh moderate latent 并逐项篡改；`observe_latent()` 对下列 `17/17` 情形均抛出 `InvalidEstimate`：

- RNG namespace：替换 component key、修改 entropy、修改 bit generator；
- 完整 spawn key：分别修改 scenario、latent ID、component 三个 identity word；
- turbulence snapshot：修改 scenario、alpha、beta、scintillation index、authority 五个字段；
- latent ID：`-1`、bool、字符串、非整数 float、`2^32` 越界值，以及与 namespace 不一致的 `124`。

这证明修复不只覆盖初审的两个具体样本，而是闭合了 component set、metadata schema、完整 namespace identity、central authority snapshot 和 uint32 latent identity。

### Fresh independent positive oracles

1. **七流 namespace/exact replay**：moderate / latent 321 / payload 11 / max pilots 16；按 entropy=`20260830` 和 spawn key=`[84,1,1,321,component_code]` 独立重建 bits、Q、GG gain、pilot noise、payload noise、mismatch left/right，namespace=`7/7`、component exact=`7/7`、second latent replay PASS。
2. **SNR/Np pairing**：5 dB/Np2 与 35 dB/Np16 共用全部 latent hashes，pilot noise 为冻结前缀，payload latent 不变；analytic noise-scale ratio=`31.6227766016838=sqrt(1000)`，`Yp/Y` 独立逐元素重建 PASS。
3. **Authority/Gram**：weak/moderate/strong 三档仍从 central params 解析；Np=`2/4/8/16` 的 `XpXp^H=NpI` exact PASS。
4. **B3/UVH/firewall**：正常闭式 PSC 标量=`0.999832217636138`，negative numerator=`0`，zero/nonfinite/overflow 三条 fail-closed=`3/3`；B2 tau=1 与 C4 共用独立 SVD 的 `VU^H`；receiver API/source truth firewall PASS。
5. **Mismatch**：delta=`0/.05/.1/.2/.3/.4` 的独立公式、平均 Frobenius power 与 analytic singular ratio 全部 PASS；ratios=`1.000000000,1.105263158,1.222222222,1.500000000,1.857142857,2.333333333`。

### Frozen verification rerun

| 验证 | fresh 结果 |
|---|---|
| production-core + demapper + scaled-unitary focused suite | `46 passed in 1.33s` |
| `python -m py_compile` core/test | PASS |
| T084 task-control validator | PASS |
| T084 scoped `git diff --check` | PASS |
| exact scope | implementation/test/worker-log + 本 reviewer 报告；无 `scaled_unitary/common/params` diff |

### P2 disposition

B3_PSC 保留 B2 `h_hat`、对最终 action 使用 `aW_B2` 的设计仍成立。`channel_nmse` 只表示 inherited pre-calibration B2 estimate，`inverse_residual` 才表示 post-calibration action；该边界已写入 worker log 与本报告。后续若正式机制图包含 B3，必须沿用此标签；不得把 inherited NMSE 解释为最终 calibrated equivalent-channel estimate。此项为非阻塞 P2，不要求改算法。

### Gate conclusion

PASS 只表示 production core 的接口、随机性、authority、receiver 公式、invalid-path 和可复现性 correctness 已闭合。它不表示 A2/B3_PSC 科学比较、BER、smoke、tuning 或 production 已运行；后续只能由主控另开固定 A2 bridge checkpoint。
