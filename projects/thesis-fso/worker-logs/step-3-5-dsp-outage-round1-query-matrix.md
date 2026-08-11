# Step 3.5 Round 1 query matrix

> 任务：T011 | 日期：2026-08-11 | 证据边界：title / abstract / metadata only

## 1. Command / query receipt

8 个 query 均使用同一合同执行：

```text
bash tools/search "<query>" --sources s2 openalex --mode academic \
  --max-per-source 20 --top 40 --year-from 2000 \
  --output search-archive/2026-08-11/step3-5-dsp-r1-qNN.json
```

| Query | Provider raw（S2 / OpenAlex） | 单 query 去重 | JSON 保留 | JSON 实际贡献（S2 / OpenAlex） | 输出 |
|---|---:|---:|---:|---:|---|
| q01 post-DSP reliability / lock-aware optical combining | 20（0 / 20） | 19 | 6 | 0 / 6 | `step3-5-dsp-r1-q01.json` |
| q02 frame-sync confidence / branch admission | 3（0 / 3） | 3 | 1 | 0 / 1 | `step3-5-dsp-r1-q02.json` |
| q03 phase-validity / cycle-slip-aware diversity | 21（1 / 20） | 21 | 4 | 0 / 4 | `step3-5-dsp-r1-q03.json` |
| q04 bounded abstention / invalid-branch robust MRC | 0（0 / 0） | 0 | 0 | 0 / 0 | `step3-5-dsp-r1-q04.json` |
| q05 DSP-outage-aware multi-aperture coherent FSO | 20（2 / 18） | 20 | 8 | 2 / 6 | `step3-5-dsp-r1-q05.json` |
| q06 reliability-weighted MRC under sync / phase error | 34（14 / 20） | 33 | 20 | 10 / 10 | `step3-5-dsp-r1-q06.json` |
| q07 robust MRC / CE outlier / branch rejection | 12（0 / 12） | 12 | 3 | 0 / 3 | `step3-5-dsp-r1-q07.json` |
| q08 confidence-weighted coherent FSO aperture combining | 5（5 / 0） | 5 | 4 | 4 / 0 | `step3-5-dsp-r1-q08.json` |
| **合计** | **115（22 / 93）** | **113** | **46** | **17 / 29** | **8/8** |

说明：q08 的 OpenAlex 调用经历 5 次限流重试后未返回结果，故该 query 的 OpenAlex 贡献记 0；这不影响全矩阵双源实际贡献。跨 query 按 DOI 优先、否则 normalized title 去重，仅发现 1 个重复组（自动驾驶传感器综述，q02/q07），因此 46 行变为 **45 unique**。其中 `published=37`、`preprint=2`、`unknown=6`。归一化后的 unique source contribution 为 **S2=17、OpenAlex=28**；两源均有实际贡献。

原始 JSON：`search-archive/2026-08-11/step3-5-dsp-r1-q01.json` 至 `q08.json`。

## 2. Method × scenario coverage

| 方法 / 动作强调 | optical / direct 覆盖 | robust-diversity / problem 覆盖 | new MUST / SHOULD |
|---|---|---|---:|
| reliability / lock-aware soft weighting | q01、q08 | q06 | 0 / 0 |
| frame-sync confidence / branch admission | q02 | q06 | 0 / 0 |
| phase validity / cycle-slip-aware action | q08（直接光学 phase alignment 邻居） | q03 | 0 / 0 |
| invalid / outlier branch abstention or rejection | q05 | q04、q07 | 0 / 0 |

矩阵覆盖了 4 类动作强调及 optical/direct、robust/problem 两类场景。命中集中在宽泛 MRC/SC/EGC、信道幅度或 CSI 权重、同步/相位误差性能分析、以及 estimator/equalizer-changing 方法；没有 abstract 显示 receiver-visible branch-local DSP validity 实际驱动 bounded weight、admission 或 abstention。

## 3. Candidate table

### 3.1 MUST / SHOULD

无。**Round 1 new MUST=0，new SHOULD=0。**

### 3.2 MAY 邻居（不升级）

| Title | Year / venue / DOI / source | Abstract-supported facts | Provisional signature | Class |
|---|---|---|---|---|
| Combining techniques for the reception of signals from satellite constellations with path diversity at the User Terminals | 2026 / University of Luxembourg repository / DOI UNKNOWN / OpenAlex | 估计 symbol-time misalignment，并称把 misalignment information 纳入 UT diversity combining；同时含 coarse frame sync、fine tracking 与 distributed compensation | input=estimated time misalignment；position=UT pre-combining；trigger=misalignment estimate；action=compensation/combiner modification；no-valid=UNKNOWN；stateful=tracking loop；output=combined STBC sequence；Q001=sync/estimator-changing neighbor | MAY |
| Enhanced GNSS Signal Tracking in Fading Environments Using Diversity Reception | 2016 / University of Calgary / 10.11575/prism/25900 / OpenAlex | spatial/frequency diversity combined signal 用于闭环 carrier/code tracking，并报告 cycle-slip 减少 | input=diversity branch correlator outputs；position=tracking loop；trigger=UNKNOWN；action=combine then track；no-valid=UNKNOWN；stateful=yes；output=tracking/navigation solution；Q001=因果方向相反（combining→tracking） | MAY |
| ODPM Channel Estimation Method using Multiple MRC and New Reliability Test in IEEE 802.11p Systems with Receive Diversity | 2021 / KSII TIIS / 10.3837/tiis.2021.12.018 / OpenAlex | MRC 生成 one-data-pilot；new reliability test 使 selective TDA 生效 | input=MRC-derived data pilot/reliability test；position=CE update；trigger=reliability criterion；action=selective temporal averaging；no-valid=UNKNOWN；stateful=TDA；output=updated CE；Q001=CE-internal action，不是 branch weight/admission | MAY |
| APPLYING DIVERSITY TO MITIGATE INTERFERENCE IN UNDERWATER ACOUSTIC COMMUNICATION NETWORKS | 2015 / dissertation / 10.23860/diss-mcgee-james-2015 / OpenAlex | 识别各接收器受干扰的 signal portions，删除后再合并 clean portions | input=interference-contaminated portions；position=pre-combining；trigger=interference identification；action=hard blank/removal；no-valid=UNKNOWN；stateful=UNKNOWN；output=combined clean portions；Q001=hard discard comparator neighbor，且非 DSP validity | MAY |
| Blind Gradient-Ascent Phase Alignment for Multi-Aperture Coherent Digital Combining Under Aperture-Dependent Phase Disturbance | 2026 / venue UNKNOWN / DOI UNKNOWN / S2 | 直接从各 aperture field 最大化 combined power，迭代更新 per-aperture phase correction | input=received aperture fields/combined power；position=pre-combining phase alignment；trigger=gradient update；action=phase correction；no-valid=none stated；stateful=iterative；output=phase-aligned combined signal；Q001=phase-estimator-changing，不是 validity-driven weight/admission | MAY |

这些条目均缺少 brief 所要求的完整耦合：`receiver-visible reliability/confidence/lock/phase-validity -> branch weight/admission/abstention`。因此不能升为 MUST/SHOULD；未由 abstract 支持的字段均标为 UNKNOWN。

## 4. Reject taxonomy

对 45 个 unique 条目逐一读取 title + abstract 后：`MUST=0 / SHOULD=0 / MAY=5 / REJECT=40`。

| Reject reason（互斥主因） | Count |
|---|---:|
| 跨领域或系统/网络级假阳性，无相关接收机 branch combining action | 10 |
| 综述、容量/BER/outage 分析或 impairment 描述，未提出 validity-driven action | 9 |
| conventional MRC/EGC/SC、channel-amplitude/CSI/decision-boundary weighting；可靠性仅为性能目标 | 12 |
| estimator/equalizer/synchronizer/phase-alignment changing，但未让 validity 驱动 branch weight/admission/abstention | 7 |
| hard selection/blanking/discard、GSC 泛论，落入已排除 comparator 类 | 2 |
| **合计** | **40** |

特别未升级：`adaptive combining` 仅按信道/CSI/功率适配；`phase/timing synchronization error` 多为 BER/SER 分析；`cycle slip` 条目未连接 branch-local admission/weight；两篇 coherent multi-aperture 直接条目分别是 joint MIMO equalizer 或 phase-alignment estimator，不是 Q001 action collision。

## 5. Round 1 result and minimum Round 2 query

- Round 1：**new MUST=0，new SHOULD=0**。
- 只建议、不执行的最小 Round 2 query：

```text
("frame synchronization confidence" OR "carrier lock indicator" OR "cycle slip detector")
("branch weighting" OR "branch admission" OR abstention)
(MRC OR "coherent combining") receiver
```

该 query 刻意绑定“receiver-visible validity feature”和“实际 branch action”，避免再次召回仅 BER 分析、channel-amplitude weighting、SC/GSC 泛论或 estimator-changing 文献。本日志不作 terminal、Go/Kill、新颖性或方法成立判断。
