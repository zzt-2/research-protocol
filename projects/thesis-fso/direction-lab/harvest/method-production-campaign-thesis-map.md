# Method-production campaign 论文资产地图

> 2026-08-02 | 权威状态：D058 / V084 | 只做论文资产分级，不升级科学有效性

## A 级：可作主贡献

| 资产 | 有效性与上限 | 论文位置 | 可直接复用 | 仍缺闭环 |
|---|---|---|---|---|
| 基于接收功率 CV 与有效 SNR 的逐窗 DA/NDA 自适应 CPR | 已有论文材料有效；9 dB 下相对固定 NDA 改善约 0.8–1.5 dB；限于已测 16APSK、AWGN+三档 GG slice；**不是本 campaign 新产出** | Ch4 主贡献，Ch5 实现 | CCISP 方法、结果和图 | 毕业论文级系统整合、章节统一、边界陈述 |

SC-NDA-ML 是既有估计器/实验基础，不单独计作主贡献。

## B 级：工程或支撑资产

| 资产 | 有效性与上限 | 论文位置 | 可直接复用 | 仍缺闭环 |
|---|---|---|---|---|
| 5G NR BG2 rate-matched LDPC、3GPP bit interleaver、Gray-16QAM BICM、轨迹级 FER/oracle ladder | PARTIAL / reusable engineering；不得引用 P08/P08-R 旧科学结论 | Ch5 接收链/FEC 或附录 | coded-chain 组件与轨迹统计 | 独立 pre-test freeze 后的确认性重跑 |
| 32-symbol prefix-LS 噪声估计、隐藏 gamma metamorphic、递归 AST 信息边界检查 | 工程机制有效，科学 verdict 因 chronology 仅 PARTIAL | Ch5 实现纪律/附录 | estimator、metamorphic gate、AST verifier | 不可变冻结闭环 |
| bit-true Q-format 与 resource proxy | 局部工程结论有效；uniform Q(8,6) 已到性能地板，mixed 最多 +0.0166 dB；不得声称真实 FPGA 资源/功耗/吞吐 | Ch5 定点实现 | bit-true 模型、resource proxy | HDL 综合、时序或板级证据 |
| 强传统 comparator 边界 | region retune、standard CMA、last-value persistence、gain calibration 均为有效 local boundary；P11 仅 20 dB partial | Ch3/Ch4 对比边界 | 可组成“强基线先行”小节 | 统一 testbed、共同指标、跨切片验证 |

## C 级：负面、限制与方法论资产

| 资产 | 有效性与上限 | 论文位置 | 使用边界 |
|---|---|---|---|
| P01–P07-R 边界集 | 7 个有效局部负面包，ceiling=`LOCAL_SLICE` | limitations/鲁棒性 | 合并为一张表，不能拆成七项创新 |
| G1 与 P09 | INVALID scientific result；只作方法论反例 | threats-to-validity/附录 | G1 图必须降格或重标，不能作方法图 |
| metric/swap/oracle/lifecycle 撤回链 | 有效实验方法材料，非科学贡献 | 实验方法/附录 | 可形成审计 checklist |
| P03/P06/P07-R/P08-R2 代码 | 按各自 validity 复用 | 工程附录 | 不得超出局部/partial ceiling |

## 两条现实 thesis spine

### 方案 A：AMC 成功

- 主贡献 1：既有 DA/NDA 自适应 CPR。
- 主贡献 2：AMC；必须从独立 Groundwork 专题开始，形成真实 deployable action、合法 conventional comparator、独立 pre-test freeze、跨 cell held-out、paired CI 与真实复杂度核算。
- 次贡献：定点实现、coded receiver、鲁棒性边界。
- 最低交付：两主方法 + 一工程验证章。
- 禁止把 campaign negatives、G1、P09 或 P11 partial 当作 AMC 证据。

### 方案 B：AMC 失败

- 唯一方法主贡献：DA/NDA 自适应 CPR。
- 第二条改为“实现与评价扩展”，由 bit-true 定点、receiver-visible coded-chain 与强传统基线边界组成，明确不是第二个新算法。
- 最低交付：完成 Ch4 主方法整合，并至少闭合 coded-chain chronology 重跑或真实 FPGA 综合之一。
- 禁止声称“7 包负面=第二贡献”“全域鲁棒”“coded loss 已正式定论”或“G1/P09 是方法”。

## 当前使用规则

历史 harvest 血缘保留，但本文件与 `harvest/current.yaml` 的 `method_production_campaign_closeout` 是 campaign 资产的当前投影。任何论文使用必须同时读取对应 D/V/worker-log，且服从这里的最低 claim ceiling。
