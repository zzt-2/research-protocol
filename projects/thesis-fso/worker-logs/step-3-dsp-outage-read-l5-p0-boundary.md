# Step 3 精读证据：ICCC 2022 与 2019 P0 摘要边界

> 执行任务：T009 | 日期：2026-08-11 | fresh-context reader C
> 边界：ICCC 2022 为本日志唯一全文精读对象；2019 P0 仅使用既有 metadata/abstract/provenance receipt，不称 fulltext read，不推断 exact action，不裁决 Q# terminal。

## 0. ICCC 标题门

| brief 指定对象 | 全文实际标题 | 结果 | 证据 |
|---|---|---|---|
| ICCC 2022 reliability MRC；DOI `10.1109/ICCC56324.2022.10065885` | *Reliability Analysis of MRC Diversity Reception System Based on LS and MMSE Channel Estimation* | **PASS**：venue/year、MRC+LS/MMSE+reliability 主题和 DOI 对象实质一致 | 全文 L1-L11；§I L13-L27 |

## 1. L5 — Yang, Jiang & Luo, ICCC 2022

### 1.1 标准字段（15/15）

- **DOI**：`10.1109/ICCC56324.2022.10065885`（brief/资产目录绑定）。
- **source path**：`papers/doi/10.1109_iccc56324.2022.10065885/content.md`。
- **read status**：全文精读完成；system model、LS/MMSE estimation、proposed algorithm、simulation 与 conclusion 均覆盖。
- **发表状态**：正式发表。
- **venue**：2022 IEEE 8th International Conference on Computer and Communications (ICCC)。
- **year**：2022。
- **贡献**：论文先比较 LS/MMSE channel estimation 与 receive-antenna count 对传统 MRC BER 的影响，确认 imperfect channel estimate 会在 combined signal 中引入 error term（L29-L81、L83-L139）。随后它提出真正改变 combining action 的 pilot-attenuation soft weighting：由每根接收天线的 pilot attenuation 形成 `α`，计算 pilot weight、插值得到 information-symbol combining coefficient `γ`，再对 LS/MMSE estimated-channel MRC 施加额外权重（L141-L177）。
- **方法概览**：1×M、independent Rayleigh fading、AWGN 模型下，以 comb pilots 做 LS 或 MMSE channel estimation；标准 MRC 使用估计 channel coefficient 的 complex conjugate。proposed method 额外按 pilot attenuation 分配连续权重，严重衰落支路权重更小、较轻衰落支路权重更大，经 interpolation 扩展到 data symbols 后再合并（L31-L81、L145-L177）。
- **实验设置**：MATLAB Monte Carlo；OFDM、128 carriers、32 comb pilots、250 kb/s、QPSK、linear interpolation；比较 LS/MMSE、不同 receive-antenna counts 与 proposed-vs-standard MRC BER（§V-A/Table I，L179-L194）。
- **baseline**：标准 estimated-channel MRC + LS；标准 estimated-channel MRC + MMSE；antenna count 2/4/8（Fig.2）以及 proposed comparisons 4/8/16（Fig.3-4）。SC/EGC、threshold drop、oracle CSI 或其他 reliability weights 未进入实验。
- **结论**：在 SNR=6 dB、M=4/8/16 时，proposed weighting 相比对应 standard MRC，LS case BER 降 `15%/19%/25%`，MMSE case 降 `12%/17%/21%`；增益随 antenna count 增大，且 LS case 相对改善更大（L198-L224）。
- **与本专题关系**：它直接占据宽泛的“pilot reliability/attenuation 驱动连续 MRC weight”动作族；但系统是 RF-style Rayleigh OFDM receive diversity，不是 coherent multi-aperture FSO，也没有 post-DSP lock/outage、FS/CE/CPE 多源 validity 或 abstention/no-valid flag。
- **具体实现**：对每根天线与每个 pilot 计算 positive attenuation matrix `α ∈ R^(M×Np)`；`α` 越小代表 attenuation 越严重；由 `α` 得 pilot weight matrix，再 interpolation 得 signal combining coefficient `γ`；LS/MMSE 仍独立产生 `Hhat`，最终 weighted combining 后 decision detection（L161-L177）。PDF-to-text 未保留式(15)-(16)完整可读代数，故不臆造 normalization/closed-form。
- **fit**：适合作为 pilot-derived soft-weight collision neighbor 与 standard LS/MMSE-MRC comparator evidence；不适合作为本专题 receiver-visible DSP-validity action 的直接实现证据，也不能据它断言 optical outage-aware exact collision。
- **code**：无开源代码；论文只报告 MATLAB simulation，未给 repository/link。
- **validation**：title/author/venue 与指定本地全文一致；所有结论由上述 source path 的 method/results 行定位。执行合同禁止外部搜索，未做外部代码或引用验证。

### 1.2 七个结构段

1. **state**：N/A（非 DRL）。算法可见量为每支路 received pilot、pilot attenuation `α`、LS/MMSE estimated channel `Hhat`、插值得到的 `γ`；无 learning state。
2. **action**：非 DRL deterministic soft action。pilot attenuation 越严重→连续 combining weight 越小；pilot attenuation 越轻→权重越大；interpolation 将 pilot weights 扩展到 data-symbol weights，所有支路随后加权合并（§IV-B，L153-L177）。没有 hard branch drop/abstention。
3. **reward/objective**：reward=N/A。objective 为在不增加 antenna 或换更复杂 CE 的条件下降低 BER，同时维持较低 complexity；性能指标为 BER，复杂度只作定性声称（L21-L27、L179-L224）。
4. **model assumptions**：one transmit/M receive；branch fading independent；antennas mutually noninterfering；only AWGN；full diversity gain；pilot attenuation 能代表受 noise 影响程度；comb pilot+linear interpolation；Rayleigh multipath fading（L29-L31、L151-L183）。
5. **network/algorithm**：network=N/A。algorithm=`pilot attenuation matrix α -> pilot weight -> linear interpolation γ -> γ-modified LS/MMSE MRC -> decision`；没有 learned network/optimizer。
6. **fit**：真正驱动额外 weight 的是 pilot attenuation，不是 LS/MMSE residual、posterior covariance、sync margin 或 CPE coherence。LS/MMSE estimation quality 只决定 `Hhat` 基础 MRC 与相对 improvement 大小；论文没有把 estimator uncertainty 显式输入 `γ`。
7. **problem extraction**（论文自身问题，不是本专题 Q# 裁决）：
   - **M**：基于 LS/MMSE imperfect channel estimate 的 standard MRC。
   - **C**：1×M independent Rayleigh-fading OFDM receive diversity，系统不能继续加 antenna 或提高 CE complexity，且强衰落支路的 pilot estimate 被 noise 污染。
   - **A**：standard MRC 把有较大 estimation error 的 channel coefficient 直接当 combining weight；严重衰落支路因此把更强 noise/error 带入 combined signal（L145-L155）。
   - **四判据**：①具体技术矛盾 **✅**；②方法产出形态 **✅**（可复用 attenuation-weight/interpolation algorithm）；③近期 baseline **❌/未闭合**（LS/MMSE MRC 明确但主要是传统方法，全文未建立“近期顶刊 task-matched M”身份）；④量化对标 **✅**（proposed vs standard LS/MMSE-MRC 的 BER curves/percent reductions）。

### 1.3 精确 input → trigger/action → output

`M 路 independent Rayleigh-faded OFDM samples + 每路 comb pilots -> 每个 pilot 时刻计算 attenuation α；α 越小(衰落越严重)则分配越小连续 weight，经 linear interpolation 得 data-symbol γ；同时 LS/MMSE 产生 Hhat，执行 γ-modified estimated-channel MRC -> 输出 weighted MRC signal，送 decision detection/BER evaluation。`

**判别结论（论文事实）**：这不是“只分析 estimation error 下的传统 MRC”。pilot attenuation **确实驱动了新增权重动作**（L153-L177）。但它也不是“estimation-quality-aware”到可泛化为 LS residual/uncertainty：`γ` 的显式输入是 attenuation `α`，而 LS/MMSE 只生成基础 `Hhat`；全文未定义 residual、posterior variance、lock flag 或 DSP-outage confidence 输入。

### 1.4 通信参数表

| 链路/模块 | 模型 | 关键参数 | evidence pointer |
|---|---|---|---|
| diversity link | 1×M independent Rayleigh fading + AWGN | branches mutually noninterfering；full-diversity assumption | §II Fig.1 L29-L58；§IV-B L157-L163 |
| waveform | OFDM/QPSK | 128 carriers；32 pilots；symbol rate `250 kb/s` | §V-A Table I L179-L194 |
| pilots/interpolation | comb pilot + linear interpolation | per-antenna `α ∈ R^(M×Np)`；`α` smaller means stronger attenuation | §III L83-L85；§IV-B L161-L173 |
| channel estimation | LS / MMSE | LS ignores noise；MMSE needs channel/noise autocorrelation and matrix inverse | §III-A/B L87-L139 |
| antenna/SNR sweep | receive diversity | Fig.2 M=2/4/8 at SNR=10 dB comparison；Fig.3-4 M=4/8/16 at SNR=6 dB improvements | §V-B L196-L220 |
| metric | reliability=BER | LS reductions `15/19/25%`; MMSE `12/17/21%` for M=4/8/16 at 6 dB | abstract L9；Fig.3-4 L206-L220 |

### 1.5 实验完备性（≤20 行）

1. **claims/scope**：bounded MATLAB evidence for Rayleigh OFDM BER; conclusion's “practical application/large-scale array” is not backed by hardware test.
2. **statistics**：states Monte Carlo but gives no run count, seed count, CI/error bars or significance test.
3. **baseline matrix**：standard LS-MRC and MMSE-MRC only; no EGC/SC/GSC/oracle-CSI or alternative soft weighting.
4. **fairness**：proposed and standard methods appear under same estimator/antenna/SNR settings; tuning of attenuation weights is not documented.
5. **ablation**：antenna count and LS-vs-MMSE sweeps; no removal/replacement of attenuation weighting, no interpolation sensitivity, no pilot-count sweep (left as future work).
6. **channel realism**：independent Rayleigh + AWGN, no correlation/interference/mobility/time variation/hardware impairment; reality level idealized-to-basic.
7. **topology diversity**：single 1×M topology with M varied; no different correlation/topology families.
8. **complexity**：only qualitative “low complexity”; no O(), operation count, runtime, memory or hardware resource.
9. **VVUQ**：Verification `1/3`（single MATLAB model, unspecified MC volume）；Validation `1/3`（no empirical test）；Uncertainty `1/3`（no CI/model sensitivity）。

## 2. 2019 P0 — 仅 metadata/abstract/receipt 的三栏边界

> 身份：Sun, Huang, Yao & Guo, *Adaptive digital combining for coherent free space optical communications with spatial diversity reception*, Optics Communications, 2019, DOI `10.1016/j.optcom.2019.03.069`。
> read status：**ABSTRACT/METADATA ONLY；不是全文精读，也不计为第六篇全文。**

| 可由 title/abstract 断言 | 不可断言 | 若 Q# 存活，Step 3.5 必须补的债 |
|---|---|---|
| 正式身份：2019 / Optics Communications / DOI 上述；作者 Jing Sun、Puming Huang、Zhoushi Yao、Jingzhong Guo。 | exact per-branch input 是 instantaneous amplitude、pilot energy、SNR、channel estimate、error residual、DSP validity，或其组合。 | 取得合法 primary fulltext（或能覆盖完整方法式的一手等价来源），做 title/DOI/content identity gate。 |
| 研究对象是 coherent FSO spatial-diversity reception，目标是实时、快速 fading 下高效 adaptive combining 多路接收信号。 | trigger 是每 symbol/block/frame，是否有 threshold、lock/outage event、更新周期或 temporal memory。 | 提取完整 `input -> trigger -> action -> output`，含 weight formula、normalization、update law、时间粒度与初始化。 |
| 动机之一是避免 random/time-varying channel fading 的耗时、复杂 estimation process。 | weight 是 real/complex、normalized/unbounded、MRC shrinkage/EGC adaptation，是否能置零、drop 或 abstain。 | 闭合 receiver observability：所需量是否在 post-FS/CE/CPE receiver 可见，是否使用 truth/channel oracle。 |
| 提出“novel adaptive digital combining algorithm”；仿真对象为 BPSK/QPSK four-aperture receiver。 | DSP ordering：combining 位于 coherent detection/digitization、FS/CE/CPE/equalization 的哪一侧；是否属于 post-DSP MRC。 | 提取完整 DSP/combining ordering、支路相位对齐与 carrier-sharing 假设，明确是 estimator-changing 还是 weight-changing。 |
| baseline 是 traditional EGC；abstract 报告不同 turbulence 下同 BER 所需 transmit power 可降约 `3–10 dB`。 | 是否比较 MRC、hard discard/GSC、ICCC pilot attenuation 或 no-valid-branch behavior；也不能由未提及推断“没有”。 | 核验 baseline 实现、公平参数、turbulence/channel settings、branch count、modulation、BER sample volume 与统计报告。 |
| 这是 closest direct adaptive-combining competitor 的**风险证据**。 | exact collision=`YES/NO`、与本专题完整多源 DSP-validity signature 相同/不同、或方法新颖性已闭合。 | 在完整动作签名证据上再做 exact collision audit；此前状态只能保持 `UNRESOLVED`，不得用 abstract 缺词判 non-exact。 |
| S2/OpenAlex 既有索引与当前 Step2 OA/title receipt 在 title/year/venue/DOI/abstract 上一致。 | 开源 code、FPGA/hardware implementation、complexity formula、weight count、实测链路；abstract 均未披露。 | 核 code/implementation availability 与 complexity/hardware evidence；若不可得，显式记录 limitation。 |

### 2.1 2019 P0 证据指针

- `.sessions/2026-08-11-dsp-outage-aware-multi-aperture-combining/step1-provenance-receipt.md` §P01：identity、四条 abstract action facts、exact collision `UNRESOLVED` 及索引 SHA-256。
- `search-archive/2026-08-11/step2-p0-oa-title.json` → `results[0]`：authors/year/venue/DOI、完整 abstract、OA=false、pdf_url=null。
- `.sessions/2026-08-11-dsp-outage-aware-multi-aperture-combining/R001-step1-synthesis.md` §4：hypothesis-vs-abstract 动作签名表；trigger/weight semantics 未披露。
- `.sessions/2026-08-11-dsp-outage-aware-multi-aperture-combining/step1-candidate-collision-matrix.md` C04/Collision synthesis：`CLOSEST_DIRECT / COLLISION_RISK_UNRESOLVED` 是摘要级风险分类，不是全文 exact collision verdict。

## 3. 跨对象边界摘要（仅供主线综合）

| 维度 | ICCC 2022（全文） | Optics Communications 2019（摘要/metadata only） |
|---|---|---|
| 可见 input | pilot attenuation `α` + LS/MMSE `Hhat` | 仅知 multiple received signals；exact input 未披露 |
| action | `α -> interpolated continuous γ -> weighted MRC` | adaptive digital combining；weight/update semantics 未披露 |
| hard drop/abstain | 无 | 不可断言 |
| task/medium | Rayleigh OFDM receive antennas | coherent FSO four apertures |
| 当前能支持的边界 | 宽泛 pilot-derived soft-weight 先例 | closest direct collision risk；exact collision unresolved |

## 4. 证据路径

- ICCC 全文：`papers/doi/10.1109_iccc56324.2022.10065885/content.md`。
- 2019 provenance receipt：`.sessions/2026-08-11-dsp-outage-aware-multi-aperture-combining/step1-provenance-receipt.md`。
- 2019 metadata/abstract：`search-archive/2026-08-11/step2-p0-oa-title.json` 的 `results[0]`。
- Step 1 synthesis/collision：`.sessions/2026-08-11-dsp-outage-aware-multi-aperture-combining/R001-step1-synthesis.md`；`.sessions/2026-08-11-dsp-outage-aware-multi-aperture-combining/step1-candidate-collision-matrix.md`。
- 规范：`stages/gw-read.md`；`stages/glossary.md`；`domain-comms.md` §1.1。
