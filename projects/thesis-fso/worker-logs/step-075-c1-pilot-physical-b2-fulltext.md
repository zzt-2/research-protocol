# Step 075 — C1 pilot B2 + coherent-FSO physical fulltext pair

> 2026-08-09 | T029 / CP009 / Groundwork Step 3.5 | `PAIR_FULLTEXT_READ`

## 1. Control 与范围

- Fresh validator：`python .agents/skills/research-direction-lab/scripts/validate_task_control.py .sessions/2026-08-09-coded-decoder-feedback-groundwork/T029-c1-pilot-physical-b2-fulltext.md` → `PASS`。
- 已按 task 复核 control packet、Step 3/3.5 规范和两篇全文；只执行 `FULLTEXT_ACQUIRE/READ`。
- 未改中央 owner/治理/代码，未运行实验，未 stage/commit/push，未触碰 `p05`。

## 2. Paper statuses

| Paper | status | identity / corpus |
|---|---|---|
| Li et al. 2019, DOI `10.3390/app9132749` | `FULLTEXT_READ_WITH_ALGORITHM_DEBT` | Crossref identity PASS；PDF 3,549,514 bytes / SHA256 `BD7267...892F`；正文 214 行 / 30,012 bytes / SHA256 `8A5146...8A7`；Figure 2 已核图 |
| Paillier et al. 2020, DOI `10.1109/JLT.2020.3003561` | `FULLTEXT_READ_PHYSICAL_ANCHOR` | DOI/TeX identity PASS；正文 244 行 / 46,321 bytes / SHA256 `52C184...E5F` |

## 3. PAPU evidence（9 条）

1. 28-Gbaud SP-QPSK、56 Gbit/s、1550 nm、300-kHz DFB；实验室 EDFA+VOA ASE/OSNR 链，不是 FSO turbulence。
2. RS(255,239)+DVB-S2 SD-LDPC，11.1% overhead、50 iterations、10 M-bit BER。
3. known pilot overhead=0.78%，作者原句 cadence=`per 127 symbols`。
4. GSOP→Gardner→M-power FOE→VVPE(+PAPU)→LDPC→RS；PAPU 完全前馈。
5. Figure 2 核图确认 pilot CPE→unwrap→interpolation→PAPU；decoder 不反馈。
6. filter sweep `{4,8,16,20,32,48}`；10.5/12.1 dB 且 filter<20 有连续 ±90° slip。
7. OSNR>17.5 dB 时 CS probability<1e-7；PAPU 不纠正离散 AWGN slip，交给 FEC。
8. filter 8/16/20 的 PRE gain≈3.1/1.3/0.6 dB，POST gain≈3/1/0.5 dB；FEC limits详见 read note。
9. 本文未给 PAPU 整数式/插值核/阈值/索引；exact arithmetic 仍欠 Cheng et al. 2013 [24]。

## 4. JLT physical evidence（10 条）

1. HV+Bufton+TURANDOT 35-layer split-step，代表性合成 2-s trace，非外场分布。
2. 1550 nm、`C0=1e-13`、winds=20/10/20 m/s、`r0=.039 m,L0=5 m,SI=.684,elev=20°,vSat=6.5 km/s,D=50 cm`。
3. AO mode91/12 orders、5 kHz、2-frame delay；flux penalty -23→-4.5 dB；WFS noise neglected。
4. `rho=|C|²` 与 `phi=arg C` 必须使用成对 correlated 2-s semantics。
5. turbulence phase coherence≈1 ms；本文结果中 turbulent phase noise 对 carrier synchronization negligible。
6. onboard laser phase noise 未讨论、linewidth 未给，不能从此文冻结。
7. 外部 coarse CFO assumed；residual CFO=100 MHz；symbol-rate 10-Gbaud BPSK、ideal timing、shot-noise AWGN。
8. AGC `Pref=1,G0=.1`；DPLL `T=.1ns,xi=1/sqrt2,BL=5MHz,K1=1.3e-3,K2=6.7e-4`。
9. 100-MHz CFO lock≈1.4 ms；constant-amplitude critical SNR≈-9 dB，fading 使稳定门槛上移≈5 dB。
10. fading penalty=2.3 dB at BER=1e-4；无 slip detector/count、reacquire、FEC 或 local repair。

## 5. 八字段裁决

| field | PAPU | JLT physical/DPLL |
|---|---|---|
| input | complex samples + known pilots + VVPE/pilot phase | ADC complex + power/loop state + coarse-CFO prior + paired `rho/phi` |
| trigger | periodic pilot, always-on feed-forward | continuous loop/start acquisition |
| localization | interpolation-constrained unwrap；无 boundary | per-symbol continuous phase/frequency；无 boundary |
| candidate/correction action | unwrap correction + symbol rotation；内部整数式欠债 | AGC gain + DPLL NCO；无 candidate reevaluation |
| decoder interaction | LDPC/RS downstream only | BPSK differential decoder only |
| fallback | isolated AWGN slips→FEC | coarse CFO + differential π ambiguity；无 reacquire branch |
| complexity/latency budget | 0.78% pilots + extra modules；数字未报告 | 10-GHz loop/5-MHz BL/约1.4-ms acquisition；op/memory 未报告 |
| output | corrected stream + CS/PRE-/POST-BER；无 boundary | corrected BPSK + BER/phase variance；无 local repair |

结论：两者都没有目标链的 decoder-evidence local repair 接口。

## 6. B2 / physical freeze 与碰撞

- **B2**：`topology-matched PAPU`；冻结 0.78%、作者 cadence `per 127 symbols`、filter sweep `{4,8,16,20,32,48}`；指标 CS/PRE-/POST-BER/pilot overhead/filter/decoder calls/latency。算法内部式未闭债前不得称 exact PAPU reproduction。
- **physical**：冻结 JLT turbulence/AO 参数、paired 2-s `rho/phi`、100-MHz residual CFO、AGC/DPLL 参数、5-dB stability shift、2.3-dB BER penalty。缺 TURANDOT trace 时只称 parameter-anchored synthetic approximation。
- **collision**：PAPU=`STRONG_NEIGHBOR / B2_TASK_MATCHED`；JLT=`NOT_COMPARABLE_COMPLETE_CHAIN`。两文都不含 decoder-evidence trigger + boundary + bounded segment/suffix candidate reevaluation + selective re-decode。
- **组合边界**：300-kHz PAPU linewidth + JLT turbulence 是 composite sweep，不是共同验证参数集；JLT 不证明 turbulence causes slips。

## 7. Protection

- `p05` 4 个冻结 SHA256 终验需 `4/4 MATCH`；git staging 需为空。
- 指定产物：`papers/_read_notes/10.3390_app9132749.md`、`papers/_read_notes/10.1109_jlt.2020.3003561.md`、本文件。

`PAIR_FULLTEXT_READ`
