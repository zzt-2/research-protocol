# [R006] Step 4a defect smoke scientific disposition

> 2026-08-12 | 关联：2026-08-11-dsp-outage-aware-multi-aperture-combining / D007–D008

## 调研问题

在 receiver-visible、paired realization、dev/test 分离且 strongest cheap comparator 冻结的合同下，Wang-style branch-local FS/phase-correction→MRC 是否自然发生高功率 DSP-invalid 支路，并产生足够 damage、cheap residual room 与 validity information increment？

## 发现

### A0/A′/A/B

Q001 四判据保持 4/4，A0/A′/A/B 未发现阻止一次 defect-only smoke 的新科学致命项；但 Sun/Xie/Qiu exact-action debt继续限制 novelty claim。历史 b3 因 truth-h、全局 RNG、offset/FSTS 未注入和 MRC 公式错误而不复用端到端；独立 sandbox 的 receiver/truth firewall、paired RNG、corrected MRC、Park/FSTS proxy、raw/receipt 与统计路径经 fresh review 后执行。

### 冻结合同与规模

- Commit 1：`cbb8a2d`；receipt=`test_started=false`。
- primary grid：3 GG×K{2,4}×H{0,1,2}=18 cells；dev seeds 0..19；test seeds 10000..10099。
- frozen B1=`-8 dB`；B2=`L=K`；strongest cheap=`B2`；bootstrap=2000 seed clusters。
- held-out raw：1800 paired frames，12600 normalized rows。

### G1–G4

| Gate | Frozen criterion | Held-out result | Verdict |
|---|---|---|---|
| G1 occurrence | rate≥10%，≥3 cells | 56/1800=`3.1111%`，CI `[2.3333%,3.9444%]`；14 cells | FAIL |
| G2 damage | regret≥10% or outage +5pp，CI low>0 | B0 regret=`0.1114%`，CI `[-0.3785%,0.4947%]`；outage +0 | FAIL |
| G3 cheap residual | regret≥5% or outage +2pp，CI low>0 | B2 regret=`0.1114%`，CI `[-0.3907%,0.5062%]`；outage +0 | diagnostic FAIL |
| G4 observability | multi AUC≥0.65、delta≥0.05、both CI gates | multi=.993209；power=.992744；delta=.000464，CI `[-.000675,.001692]` | diagnostic FAIL |

## 结论

唯一 first fail-stop terminal=`PROBLEM_ABSENT_OR_TOO_SMALL`。自然事件发生率远低于门，且加入此类支路相对 truth-aware O1 的 damage 接近零、CI 跨零；power-only 已吸收几乎全部 inclusion information。Q001 不恢复为 problem-bearing candidate。

formal science disposition=`PROBLEM_ABSENT_OR_TOO_SMALL`；mission_method_delta=`NONE`；thesis_method_disposition=`NO_METHOD / NO_CH4_CONTRIBUTION`。

## 对决策的影响

建立 D008 并关闭专题。不得实现 soft reliability/abstention、运行 fair comparison、进入 Contract、改参数重跑或把 negative result 包装成 novelty/collision/baseline failure。
