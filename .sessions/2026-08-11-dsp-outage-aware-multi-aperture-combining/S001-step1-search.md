# [S001] DSP-outage-aware multi-aperture combining Step 1

> 2026-08-11 | Groundwork Step 1 | COMPLETE_VERIFIED

## 目标

在两轮、最多六组 query 内，判断冻结 M-C-A hypothesis 是否有足够的一手候选与传统 action 覆盖，并排查 soft DSP-validity weighting / branch admission 的 exact-action collision。

## 记录

- 注册表查重：未发现同研究对象、同动作的 active/dormant 专题。历史 `2026-07-08-b3-joint-estimation` 已 closed，只复用资产形状；coded C1 保持科学关闭边界。
- 冻结 M：各支路完成 FS/CE/CPE 后按 estimated-channel weight 合并的 post-DSP multi-aperture MRC。
- 冻结 C：各支路接收功率与 DSP lock/recovery 状态异质，部分支路接近或越过 DSP-outage。
- 冻结 A：channel-amplitude weight 不等价于 DSP-validity，失效或错相支路仍获非零权重，可能使增加孔径反而恶化 BER/outage。
- 候选动作仅为 hypothesis：receiver-visible DSP confidence → reliability shrinkage/abstention → robust soft combining。
- 两条必备路线：A hard branch admission（传统 comparator）；B soft robust weighting/shrinkage（潜在 extension）；C temporal/hysteretic admission 只有文献提供时序物理前提才保留。
- 六组 query 分两轮执行；不下载、精读、实现、仿真或 smoke。
- 机械结果为 169 rows / 157 DOI-title unique；三贡献源。两路语义初筛形成 27-entry matrix，24/27 正式、8 篇 must-read。
- hard SC/GSC/threshold admission 已碰撞；ICCC 2022 使宽泛 pilot-reliability soft MRC 也只能作 neighbor/comparator。
- 2019 Optics Communications adaptive digital combining 是最近 direct competitor，摘要缺完整 trigger/weight，collision=`UNRESOLVED`。
- provisional terminal=`STEP1_PASS_READY_FOR_STEP2_CONFIRMATION`；仅待 fresh-context 独立终验。
- fresh verifier 第一次终验为 `FAIL 0/1/1`：计数/scope PASS，但专题未绑定既有全局索引中的 2019/Geisler S2+OpenAlex 条目，另有一处 26→27 残字。只做一次 provenance receipt 窄修，不新增 query。
- 第二个 fresh-context verifier 在最终字节上复核 2019/Geisler 行哈希、全部计数、collision 与 scope，结论 `PASS 0/0/0`；V001 接收 terminal。

## 决策引用

- D001：新专题仅授权 Groundwork Step 1（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

等待主控裁决是否进入 GW Step 2。确认前不下载、不精读、不实现、不仿真。
