# Task Brief: C4-1 scaled-unitary correctness 与有界 BER headroom

> 来源: S028 / D049 / T064 / T068 / V023 | 产出位置: `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/` 与 `projects/thesis-fso/polarization-demux-groundwork/step4a-c4-1-bounded-development.md`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 11
  action_class: C4_SCALED_UNITARY_CORRECTNESS_AND_BOUNDED_HEADROOM
  mission_checkpoint: CP011
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

在独立 seam 实现 T068 冻结的 scaled-unitary pilot-LS。先以修订后的 C0–C5 作为硬门；全部 PASS 后，立即运行一次预注册 `2 SNR × 2 pilot budget` paired BER/NMSE 开发，判断 C4-1 或 comparator ladder 中最简真实胜者是否足以成为短 pilot DP-(8,8)-16APSK 星地相干偏振解复用的 `PROVISIONAL` 经典迁移包。不得在结果后改网格、加入新损伤或声称最终方法。

## 启动门与范围

1. 先运行 task-control validator；读取 D031–D032、D041、D049、T064/T068、V023、C4-1 Step 3.5/Step 4a 报告、平台 parameter authority、`code-quality.md` 与适用 sim-preflight/TDD/verification 规范。
2. 只新增 `explore/ch4-scaled-unitary-pilot-ls/`、对应 tests、指定 Groundwork 报告与必要 usage log；不改 `common/`、`params.py`、Ch3/Ch5、Skill/controller 或论文正文。
3. `14/18 dB × 2/4 pilots` 是 D049 批准且在结果前冻结的研究设计轴，不冒充 source reproduction；不得以“再找一个更有利 SNR/pilot”扩网格。

## 冻结 IAO 与 C0–C5

- input：receiver-known balanced pilots `X_p,Y_p` 与 payload samples `y`。
- action：`H_LS=YpXp^H(XpXp^H)^-1=U diag(s1,s2)V^H`；`g_hat=(s1+s2)/2`；`P(H_LS)=g_hat U V^H`；`W=V U^H/g_hat`。
- output：`z=Wy`、`g_hat`、`rho=s1/s2`；`rho` 只作诊断，不设自适应 guard。
- C0 no-noise exact recovery；C1 balanced direct/post-LS equivalence；C2 精确验证 `P(LHR)=LP(H)R`、`W(LHR)=R^H W(H)L^H`、complex scale identities；C3 paired `delta=0` 与 `0<delta<1`，复现理论 `rho=(1+delta)/(1-delta)` 和 projection bias/residual；C4 truth firewall；C5 exact-zero/rank-deficient/NaN/Inf fail-closed。
- 任一 C0–C5 FAIL：只做最多两轮局部 correctness 修复；仍 FAIL 则 `INVALID_TESTBED` 并停止，禁止 BER。

## 有界 BER manifest

- target slice：DP-(8,8)-16APSK；每 window 静态 random `Q∈U(2)` 与一个 moderate Gamma-Gamma `alpha=4.0,beta=1.9` 公共标量 `g=sqrt(I)`；equal-branch circular AWGN；无 PDL/PMD/FIR/IQ、无时变 SOP、无 CFO/CPR、无 LDPC。
- balanced pilots：`Np∈{2,4}`，`XpXp^H=Np I_2`；payload=`4096 symbols/pol/window`；SNR=`{14,18} dB`，定义在平均发射符号能量与 AWGN 之间，fading 后不重新归一。
- 每 cell 64 windows；tune seeds=`base+0..31`、evaluation seeds=`base+32..63`，四 cell base 依次 `6000/6100/6200/6300`；所有 arms paired 共用 `Q/g/noise/pilots/payload`。
- B0 plain unconstrained LS；B1 normalized ridge，`eta∈[0,1e-3,1e-2,1e-1,1]` 且正则项=`eta*trace(XpXp^H)/2`；B2 SV-floor，`tau∈[0,0.25,0.5,0.75,1]` 且 `s_i'=max(s_i,tau*s_max)`；C4-1 scaled-unitary mean-singular projection；O1 true `H^-1` oracle。
- B1/B2 各 cell 只按 tune payload BER 选参数；并列选更强 regularization。evaluation 不参与 tuning。
- primary：payload BER 与 candidate-minus-baseline paired window bootstrap 95% CI（PCG64 seed=`2026083003`，2000 resamples）；secondary：channel NMSE、inverse residual、`rho`、oracle headroom 与 runtime。

## 终态与自动收缩

1. `C4_STRUCTURED_SIGNAL`：C4-1 相对 strongest(B1,B2) 在至少一个 `Np=2` primary cell 的 BER CI upper `<0`，另一个 `Np=2` cell 不显著退化，且四 cell 无 correctness/finiteness 问题；C4-1 为 provisional winner。
2. `SIMPLE_ROBUST_LS_SIGNAL`：C4-1 不满足上项，但 B1 或 B2 相对 B0 满足同一 primary/non-regression 门；选真实指标更强者，若不劣则优先更简 recipe。不得隐藏 cheap winner，也不得把它说成新估计理论。
3. `LOCAL_ONLY`：只有 `Np=2` 单格点估计改善但 CI 未闭合，或 Np4 回归；只记 supporting，不做 confirmation。
4. `NO_METHOD_SIGNAL`：C4-1/B1/B2 均无稳定 BER 信号或 oracle 无 headroom；关闭本短-pilot结构族，唯一下一步 C4-0，不增加损伤救场。
5. 任何信号只给 `PROVISIONAL_A/B/C/D`；fresh confirmation 与最终写作另派。

## 交付

先 manifest→RED/GREEN→C0–C5 receipt；correctness PASS 后才跑四 cell。交付 runner/tests、manifest、raw/aggregate/receipt、facts-first Groundwork 报告和 usage log。fresh 运行 validator、全部新旧相关 tests、raw-only reducer、hash/split/firewall 与 `git diff --check`。一次 commit、不 push；回报每臂各 cell BER/NMSE、paired CI、terminal、grade 和唯一下一步。
