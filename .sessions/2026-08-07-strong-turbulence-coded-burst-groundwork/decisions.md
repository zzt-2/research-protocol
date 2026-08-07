# Decisions — 低仰角强湍流 coded-burst reliability Groundwork

## D001: 授权物理条件 scope change 并冻结旧方向 reopen gate

> status: active
> date: 2026-08-07
> 取代：无（新专题；不改写旧 4b#1 D001/D002）
> 被取代：无
> 依据: 用户原话 `voice.md` 2026-08-07 + 旧 4b#1 D001/D002 + P08-R/P08-R2 worker logs

### 决策

允许新专题把条件 C 从旧 4b#1 的 LEO 中弱湍流改为有一手物理依据的低仰角强湍流/outage 切片；但仅在六项 reopen gate 和 outage-vs-burst 语义门全部通过时继续，不恢复旧 B=27 depth switching、P08 coded-LLR calibration 或 AMC/MCS，也不授权仿真。

### 理由

旧 4b#1 的 0 dB 结论严格绑定中弱湍流、`Lburst=60–428` 与 B=27 容量约 810 的条件；用户显式授权改变该物理条件，足以合法检查新切片。但 P08-R2 已显示整 trajectory/codeword 的深衰落可能在 finest oracle 下仍不可恢复，因此必须先分离“错误聚集可被 placement 改写”和“信息量已丢失的 outage”。

### 排除的替代方案

- 不用任意极端 `α/β` 或 stress 参数制造强湍流 occurrence。
- 不把 action 写成旧 B=27 深度切换或“更深交织”。
- 不以 GG-aware LLR、coded-LLR calibration 或 AMC/MCS 作为新候选。
- 不先跑 coded-chain 再反推问题；Step 1–3/3.5/4a 门控保持有效。
- 不把 oracle 仍失败的整块 outage 改名为 burst/interleaving 问题。

### 影响范围

- 新建独立专题与 GW Step 1 进度表。
- `projects/thesis-fso/master-state.md` 当前控制面须转到本专题 Step 1。
- 旧 4b#1 与 P08/P08-R2 文件保持历史原样，仅作依赖证据。

### 来源

S001 + 用户 2026-08-07 显式 scope change 授权。

---

## D002: Step 1 证据不足，禁止进入 Step 2

> status: active
> date: 2026-08-07
> 取代：无
> 被取代：无
> 依据: 调研 R001/R002/R003/R004 + 用户原话 `voice.md` 2026-08-07（“任一承重条件不成立，不进入 Step 2”）

### 决策

以 `STEP1_EVIDENCE_INSUFFICIENT` 停止本轮 Groundwork；不进入 Step 2，不下载/获取 CORE，不运行 coded-chain，不形成 Go、METHOD_SIGNAL、方法卡或论文 claim。

### 核心失败机制

Step 1 没有闭合一条从“真实低仰角强湍流 occurrence”到“threshold-conditioned recoverable burst span”再到“placement 可改变译码输入分布”的证据链：

1. 大天顶角强起伏/GG 有一手物理推导支持，但目标站点/仰角的强条件数值与 AFD 没有同源闭合；现有 strong 参数主要是 simulation/stress。
2. ms 级相关时间在高速链路中远大于 810 symbols，反而提高整个 span 处于同一 fade/outage 的风险；没有证据证明 codeword 跨多个独立/弱相关 block。
3. 2019+ 严格 task-matched baseline 只有 1 篇，不满足 Step 2 的至少 2 篇要求；检索 API 也只有 S2+OpenAlex，未过 `gw-search.md` 三源门。
4. P08-R2 静态 BOM 无可控 placement、per-codeword burst schema 或 delay/overhead metric，不能靠现有 runner补足语义证据。

### 否决了什么

- 否决本轮直接进入 Step 2、下载 CORE 或做全文裁决。
- 否决用 53.42 km terrestrial surrogate、`Cn²(0)=10^-13`、PSI=10 或任意 `α/β` stress 参数冒充真实低仰角 occurrence。
- 否决把 ms coherence 直接换成 recoverable burst duration。
- 否决把 generic RF mapping、capacity-only work、工程 bundle、P08、AMC/HARQ 文献凑成 task-matched baseline。
- 否决用 coded-chain 实验倒推 Step 1 物理前提。

### 可复用部分

- R001 的物理来源分级和 CORE 获取缺口。
- R002 的 2025 CCSDS O3K baseline、2012 adaptive-depth collision 与 generic placement prior art。
- R003 的 P08-R2 工程 BOM、缺失接口和 3.75–5.0 / 8.5–12.0 人日估算。
- R004 的三张 HYPOTHESIS_ONLY 预卡与 outage-vs-burst 六问表。

### 影响范围

- 新专题 GW Progress：Step 1=`STOPPED`，Step 2=`NOT_RUN`，Step 3/3.5/4a=`FORBIDDEN`。
- `projects/thesis-fso/master-state.md` 当前入口更新为本 terminal；旧专题与历史结果不改写。
- 重开条件：新一手 target evidence 补齐 occurrence+AFD/相关尺度，且新增至少一篇 2019+ strict task-matched baseline；只能重开 Step 1 缺口补证。

### 来源

S001 + R001–R004。
