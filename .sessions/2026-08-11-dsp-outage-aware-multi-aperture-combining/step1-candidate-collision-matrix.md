# Step 1 Candidate / Collision Matrix

> 仅标题、摘要、元数据与已核实本地锚点；`FORMAL` 要求可识别 venue/year/DOI 或等价正式身份。

| ID | 候选 / identity | 源 | 正式 | 语义分类 | Step 1 判读 |
|---|---|---|---|---|---|
| C01 | Johst et al., *Data-Aided Multi-Format DSP...*, WiSEE 2024, DOI `10.1109/WISEE61249.2024.10850117` | local primary | FORMAL | DEFECT_EVIDENCE + HARD_COMPARATOR | 低于约 −1 dB 的 DSP-outage 支路可恶化合并并应 discard；支持 defect/hard rule，不支持软方法新颖性。 |
| C02 | Wang et al., *Carrier FOE Scheme Based on FSTS...*, IEEE Photonics Journal 2023, DOI `10.1109/JPHOT.2023.3265847` | local primary | FORMAL | REFERENCE_M | FS/CE/CPE 后 MRC 链与支路形状；不是 validity-aware action。 |
| C03 | Geisler et al., *Multi-aperture digital coherent combining...*, Optics Express 2016, DOI `10.1364/OE.24.012661` | existing-index S2+OA；current Q2/Q6 Tavily | FORMAL | REFERENCE_M | 各孔径 coherent detection/digitization 后进入 DSP combining；四支路 lossless combining。摘要未给 DSP-outage admission。 |
| C04 | *Adaptive digital combining for coherent FSO with spatial diversity*, Optics Communications 2019, DOI `10.1016/j.optcom.2019.03.069` | existing-index S2+OA；current Q2 Tavily | FORMAL | CLOSEST_DIRECT / COLLISION_RISK_UNRESOLVED | 既有索引摘要明确四孔径 adaptive digital combining，并以避免耗时的时变衰落估计为动机；仍未披露 trigger/weight 公式，不能判 exact 或 non-exact。 |
| C05 | *Phase Alignment With Minimum Complexity...*, IEEE Photonics Journal 2020, DOI `10.1109/JPHOT.2020.2977955` | OA+S2 | FORMAL | STRONG_NEIGHBOR | 优化 PAA 复杂度与相位误差/combining loss，不做坏支路准入。 |
| C06 | *Toward Practical Digital Phase Alignment...*, IEEE Access 2020, DOI `10.1109/ACCESS.2020.3035748` | OA | FORMAL | STRONG_NEIGHBOR | 对 MRC/EGC phase alignment complexity 做 OSNR-aware 设计；动作不是 validity shrinkage。 |
| C07 | *FSO Communication Based on Mode Diversity...*, IEEE Photonics Journal 2023, DOI `10.1109/JPHOT.2022.3225337` | S2 | FORMAL | CHEAP_COMPARATOR_NEIGHBOR | EGC/MRC mode-diversity 比较；研究对象不是多孔径 post-DSP outage。 |
| C08 | *Two aperture pairs + multiple-mode receivers + MIMO DSP*, Optics Letters 2020, DOI `10.1364/OL.391120` | S2 | FORMAL | ESTIMATOR_CHANGING_NEIGHBOR | 多孔径/多模 MIMO 恢复，不是分支 validity admission。 |
| C09 | *Experimental demonstration...3.2-km free-space link*, SPIE 2017, DOI `10.1117/12.2256581` | OA | FORMAL | REFERENCE_M | 大气链路四支路近无损 MRC；无坏支路动作。 |
| C10 | *Real-time demonstration of two-aperture coherent digital combining*, Optics Letters 2024, DOI `10.1364/OL.511941` | Tavily+S2/OA identity | FORMAL | STRONG_NEIGHBOR | real-valued MIMO equalizer联合 equalization/combining；摘要未见 validity trigger。 |
| C11 | *Pilot-Assisted Phase Recovery...Robust Locally Weighted Interpolation* | Tavily | UNKNOWN | FEATURE_NEIGHBOR | 鲁棒 CPR 插值，但未驱动 branch combining。 |
| C12 | *Turbulence-resilient pilot-assisted self-coherent FSO...*, Nature Photonics 2021, DOI `10.1038/S41566-021-00877-W` | OA | FORMAL | ESTIMATOR_CHANGING_NEIGHBOR | 多模自相干接收；不是 post-DSP branch action。 |
| C13 | *Selection combining hybrid FSO/RF...*, 2019 | S2 | FORMAL | IRRELEVANT_TO_BRANCH | FSO/RF 链路选择，不是同一接收机的 aperture admission。 |
| C14 | *2-D PDA Based Spatial-Diversity Reception...*, MWP 2024, DOI `10.1109/MWP62612.2024.10736287` | S2 index | FORMAL | CHEAP_COMPARATOR_NEIGHBOR | 采用传统 MRC，未引入 DSP validity。 |
| C15 | *High-Speed FSO Using Mode Demultiplexers and Coherent Beam Combining*, JLT 2025, DOI `10.1109/JLT.2025.3577382` | S2 index | FORMAL | OPTICAL_CONTROL_NEIGHBOR | 光学/控制环 coherent beam combining，不是 post-DSP soft admission。 |
| C16 | *Reliability Analysis of MRC...LS/MMSE*, ICCC 2022, DOI `10.1109/ICCC56324.2022.10065885` | S2 | FORMAL | SOFT_ACTION_COLLISION_NEIGHBOR | pilot energy attenuation→interpolated weight matrix；碰撞“宽泛 reliability-weighted MRC”，但非 coherent FSO/DSP-outage。 |
| C17 | *Optimal Diversity Combining with Imperfect CSI...*, Electronics 2024, DOI `10.3390/ELECTRONICS13204026` | S2 | FORMAL | SOFT_STRONG_NEIGHBOR | 估计误差/残余干扰下重算最优权重；输入和目标任务不同。 |
| C18 | *RIS-Assisted SIMO with GSC*, MAPCON 2025, DOI `10.1109/MAPCON65020.2025.11426358` | S2 | FORMAL | HARD_COMPARATOR | top-L/limited-RF-chain GSC；固定选择动作。 |
| C19 | *TAS–MRC relay systems over non-identical channel estimation error*, IET Communications 2019, DOI `10.1049/IET-COM.2018.5742` | S2 | FORMAL | HARD_NEIGHBOR | max-SNR selection + MRC；传统 task-matched action family。 |
| C20 | *Generalized BER of MCIK-OFDM with imperfect CSI: SC GD vs ML*, 2022 | S2 | FORMAL | HARD_NEIGHBOR | imperfect-CSI 下 SC/GSC 性能，不是 DSP lock-aware。 |
| C21 | *Dual Selection With MRC Over Nonidentical Imperfect CE*, 2018 | S2 | FORMAL | HARD_NEIGHBOR | selection→MRC 传统动作。 |
| C22 | *Multipath Selection Method for MRC in Underwater Acoustic Channels*, 2018 | S2 | FORMAL | HARD_NEIGHBOR | 逐径选择后 MRC，跨域 comparator 先例。 |
| C23 | *GSC Scheme for OSTBC with M-QAM/M-PAM*, 2016 | S2 | FORMAL | HARD_COMPARATOR | 传统 GSC；固定动作无新颖性。 |
| C24 | *ODPM...Multiple MRC and New Reliability Test*, KSII TIIS 2021, DOI `10.3837/TIIS.2021.12.018` | S2 | FORMAL | VALIDITY_NEIGHBOR | reliability test 控制 selective TDA，不直接缩减 branch weight。 |
| C25 | *BER analysis of hybrid selection/MRC with channel estimation error* | Tavily | UNKNOWN | HARD_COMPARATOR | H-S/MRC；正式身份需 Step 2 前补齐。 |
| C26 | *Unified analysis of NT-GSC / TV+NT-GSC* | Tavily | UNKNOWN | STRONGEST_HARD_COMPARATOR | 归一化阈值准入、保底 N 支；正式身份需补齐。 |
| C27 | Johst et al., *Experimental demonstration of robust spatial-diversity combining*, OFC 2024, DOI `10.1364/OFC.2024.W2A.31` | local S2 identity | FORMAL | HARD_COMPARATOR | MRC/SDC/X-MRC 与低-SNR discard；固定 SNR 门控，不是多源 DSP-validity soft action。 |

## Collision synthesis

- **已碰撞**：固定 SC/top-L GSC/threshold GSC/hybrid S-MRC；它们只能做传统 comparator。宽泛的“pilot reliability-weighted MRC”也被 C16 的 pilot-energy attenuation→soft weight 明确占据。
- **exact collision 仍为 `UNRESOLVED`**：摘要中没有完整一致的 `多源 per-branch DSP validity（FS/CE/CPE）→ post-DSP MRC weight shrinkage/abstention → combined symbols + no-valid-branch flag`，但 C04 没披露 trigger/weight 细节，不能以缺词判 non-exact。C10 是 estimator-changing strong neighbor，C27 是 hard comparator。
- **未保留 temporal route**：当前证据只有快速时变、feedback delay 或 block-length 响应，没有 hysteresis 必需的时序物理前提。

## Must-read shortlist（Step 2 候选，当前未授权）

1. C01 Johst 2024：defect 与 hard discard rule。
2. C02 Wang 2023：reference post-DSP chain。
3. C03 Geisler 2016：foundational MRC/phase-alignment action。
4. C04 Optics Communications 2019：最近 direct adaptive-combining competitor，必须闭合完整动作签名。
5. C05 IEEE Photonics Journal 2020：phase-error/complexity boundary。
6. C06 IEEE Access 2020：MRC/EGC practical PAA competitor。
7. C16 ICCC 2022：pilot-derived soft-weight collision neighbor。
8. C27 Johst OFC 2024：hard discard/X-MRC comparator；C26 作为 identity 待补的最强传统形态并列。
