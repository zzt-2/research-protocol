# [S001] K2 Groundwork Step 1 检索

> 2026-08-12 | GW Step 1 | 完成，等待 Step 2 确认

## 目标

在不下载、不全文精读、不实现、不仿真的边界内，建立 Wang TSP 2022 suffix-pollution defect 的三路线候选池，裁入口级 exact collision，并冻结两个仅供后续审查的设计形态与复杂度合同字段。

## 记录

接收上游 D007 前，核验 Q001 terminal=`PROBLEM_ABSENT_OR_TOO_SMALL`、旧 R003/D006/V004 的 K2 `UNRESOLVED_HIGH_RISK / STRONG_NEIGHBOR` 边界，以及 registry 中 reference-extension/thesis-writing 依赖。registry 没有同名或同方向 active/dormant 专题，故建立本唯一 owner。

Step 1 分两个 fresh-context search worker 完成两轮共 11 组 query：路线 1/2 六组，路线 3 五组。全部结果逐条做 title/abstract/year/venue/status 语义初筛；`relevance_score` 未代替 AI 判断。合并当前 11 个 JSON 得 278 raw records、242 title-dedup，按 R002 的确定性 title/priority/status 规则保留 138 candidates；98/138 formal=`71.01%`，must-read=12。Semantic Scholar、OpenAlex、SerpAPI Scholar 三源实际贡献；arXiv 0 贡献，Exa 因额度无贡献，均不计来源门。

路线 1 聚焦 unwrap error propagation、cycle slip 与 multi-hypothesis unwrap；路线 2 聚焦 Tikhonov mixture、bounded order、sequence/fixed-lag tracker；路线 3 聚焦 coherent optical/FSO residual CFO + laser PN、cycle-slip robustness 与低复杂度 carrier recovery。最新 task-matched baseline 包括 2025 inter-satellite noise-tolerant CPR；2019 CSSC-CPE、2020 space-ground DPLL、2021 reduced-rate Kalman、2023 satellite DOPLL 与 2024 optical CPR 构成 cheap/direct neighbors。

动作碰撞初筛没有 confirmed exact action。TCOM 2016 已占宽泛 multi-trajectory mixture capability，必须比较 full mixture 与 fixed order 2/3；D1/D2 只能保留 task-specific bounded complexity/latency delta，不能声称 action atoms 新颖。

## 决策引用

- D001：创建唯一 K2 Groundwork owner，当前只授权 Step 1（新建）。
- D002：Step 1 通过，等待 Step 2 确认（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是；只执行检索、语义初筛与文档治理，无下载、全文精读、实现或仿真。

## 后续

下一合法动作仅为主控确认后执行 Step 2 acquisition，优先绑定 must-read 中的 direct/full-general/cheap comparators；未确认前保持 idle。
