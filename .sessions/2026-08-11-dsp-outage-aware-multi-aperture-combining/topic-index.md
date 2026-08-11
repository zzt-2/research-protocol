# DSP 失效感知的多孔径相干 FSO 可靠合并

> 状态：active | 当前阶段：Groundwork Step 1 verified，等待主控确认 Step 2

## 范围边界

### 原始目标

基于现有仓库、已下载一手材料和 reference baseline，判断 post-DSP multi-aperture MRC 在支路 DSP-outage/lock 异质条件下是否存在值得进入 Groundwork 的 reference-method extension 入口。

### 当前范围

仅执行 GW Step 1：最多 6 组 query、两轮结构化检索；形成问题证据、传统 comparator、潜在 soft/hysteretic extension 与 exact-collision 初筛。所有条目保持 `HYPOTHESIS_ONLY`。

### 明确不含

- 不下载或全文精读新论文；不进入 Step 2 及以后。
- 不实现、不仿真、不运行 smoke、不修 b3 代码。
- 不把固定 SNR 阈值 branch-drop、SC/GSC 或 Johst 2024 已给出的 discard rule 当新方法。
- 不重开 coded decoder-feedback C1；decoder/FEC flag 只可列为可选 receiver-visible feature。
- 不输出 Go/Kill、METHOD_SIGNAL、方法成立或论文贡献。

### 范围变更记录

- 2026-08-11，D001：主控验收 K1 后授权新专题仅执行 GW Step 1；原因是 coded C1 科学关闭后需寻找不同算法研究对象。

## 进展线索

- S001 / D001：注册表去重通过；冻结 M-C-A hypothesis、Step 1 检索合同与越界禁止项。
- T001–T002：两路摘要/元数据级语义初筛完成；27-entry matrix、24 formal、8 must-read。
- R001：hard route 已归 comparator；宽泛 soft weighting 有 RF 先例；2019 optical direct competitor collision 未闭合，provisional terminal=`STEP1_PASS_READY_FOR_STEP2_CONFIRMATION`。
- T003 首验：`FAIL 0/1/1`；计数/scope PASS，identity/provenance binding 与 26→27 残字需窄修。`step1-provenance-receipt.md` 已绑定既有全局索引的 2019/Geisler S2+OpenAlex 条目，等待第二次 fresh 终验。
- V001 / H001：第二个 fresh verifier `PASS 0/0/0`；terminal=`STEP1_PASS_READY_FOR_STEP2_CONFIRMATION`，Step 2=`NOT_AUTHORIZED`。

## 已确认结论

### 不变量

1. Johst 2024 的 outage-branch discard 只支持 defect 形状；固定阈值丢支路是 mandatory comparator，不是本专题方法。
2. 只有 receiver-visible multi-source DSP validity 驱动的 soft shrinkage/abstention，或有明确时序物理前提的 hysteretic admission，才可作为潜在 extension 检索对象。
3. Step 1 只能产生检索终态；没有 Step 2 授权，不得下载、精读、实现或仿真。

### 其他结论

1. 历史 b3 multi-aperture caller path 可作未来资产，但 truth-h 信息边界与 RNG/offset 是未来 Step 4a 债务，不在本轮修复。
2. 当前冻结问题只是候选，不等于问题或方法已成立。

## 未决项

1. 主控是否确认进入 Step 2；确认前不得下载或精读。

## 当前位置

`GROUNDWORK_STEP1_VERIFIED_READY_FOR_STEP2_CONFIRMATION`：V001=`PASS 0/0/0`；Step 2=`NOT_AUTHORIZED`。
