# [R003] P08-R2 / Sionna coded-burst testbed 静态 BOM

> 2026-08-07 | 关联：2026-08-07-strong-turbulence-coded-burst-groundwork / T003

## 调研问题

只按现有文件事实回答：P08-R2 的 5G NR LDPC / Gray-16QAM BICM / prefix-LS / trajectory 资产能否支撑 coded-burst 新 testbed；需要哪些最小 adapter；完整 testbed 的工期是多少。P08-R2 历史 verdict 不作为本记录的科学依据。

## 发现

### 1. 四项门控结果

| 门控 | 结论 | 静态依据 | 对 coded-burst 的含义 |
|---|---|---|---|
| channel lifecycle | **PARTIAL** | `p08r2_chain.py:195-220` 用 `n_cw_per_pol * (cw_n // 4)` 构造整条 data window，prefix 后只调用一次 `generate_shared_realization_dp(N=n_sym_total, ...)`；`p08r2_chain.py:221-233` 将返回的整段 `h/theta` 用于 16 个 codeword。 | caller 层没有在 codeword boundary 重置信道，因而具备跨 codeword 连续轨迹的结构。但 generator 内部的随机过程、相关函数与初始状态未在 T003 允许的 `p08r2_*` 文件内定义，所以不能把“跨 codeword 保持所需物理相关性”判为 YES。 |
| interleaver controllability | **NO** | `p08r2_chain.py:56-67` 只从 `p08r_chain` 导入 `CodecAdapterR`；`p08r2_chain.py:207-215` 调 `codec.encode()` 后立即 flatten 并 QAM 映射，无 placement/permutation 参数。`p08r2_verify.py:184-191` 只把 `codec.out_int` 当作可读身份证据。上游记录 `step-037-p08r-coded-chain-science-repair.md:33-38` 说明 inverse interleave 也由 decoder 内部处理。 | 现有 3GPP 位交织已启用，但是 encoder/decoder 内部固定配对；现有 runner 没有可传入的 permutation、parity placement 或 channel-slot mapping 接口。`out_int` 可读不等于可研究的 placement adapter。 |
| raw/result schema | **PARTIAL** | `p08r2_phaseA.py:219-232` 计算了 `cw_err` 向量，但只返回 per-pol 的 FER、错误 codeword 总数和 BER；`p08r2_phaseA.py:235-250` 只保存整条 trajectory 的 h mean/min/max 及 prefix 噪声估计；`p08r2_run.py:248-274` 按 method/seed 写一行 raw。 | 有 trajectory 边界（seed）和每极化 codeword 计数，但没有 per-codeword error vector、start/end boundary、per-codeword fade summary、bit/LLR 或 placement manifest。因而不能直接重建 burst 位置与 FER/outage 分类的关系。 |
| delay / overhead metric | **NO** | `p08r2_phaseA.py:219-232` 的得分仅包含 FER/BER 与 codeword 计数；`p08r2_run.py:369-386` 最终结果只额外保存脚本 `elapsed_sec`，不是通信 delay。`p08r2_chain.py:204-215` 实际在 6144 data symbols/pol 前加 32-symbol prefix，但 `p08r2_verify.py:297-301` 明确将 prefix 排除在 scored window 之外。 | 实物 overhead 存在但未进入 metric：32/6144 = 0.521%（相对 data），或 32/6176 = 0.518%（相对总符号）。无 interleaver latency、decoder latency、burst recovery delay 或 effective-throughput 字段。 |

### 2. 资产 BOM

| 资产 | 文件:行号 / 接口 | 当前能力 | 可复用性 |
|---|---|---|---|
| codec identity | `step-036-p08-coded-chain.md:17-18,20-37` | Sionna 2.0.1 `LDPC5GEncoder(k=1024,n=1536)`，BG2，Z=104，rate 2/3，20 次 normalized-min-sum，Gray-16QAM BICM。Sionna API 在 P08-R2 中由 `p08r_chain.CodecAdapterR` 隔离（`p08r2_chain.py:56-67`）；上游日志给出 base-graph CSV 位置 `sionna/phy/fec/ldpc/codes/5G_bg2.csv`。 | **YES（作为固定 codec）**；不应改 Sionna 内部码链。 |
| codeword/frame shape | `p08r2_phaseA.py:58-63`；`p08r2_chain.py:195-215` | 16 codewords/polarization/trajectory；1536 coded bits/cw = 384 16QAM symbols/cw；6144 data symbols + 32 prefix symbols/pol。 | **YES**，可作为最小 testbed 的固定 shape。 |
| inner bit interleaver | `step-037-p08r-coded-chain-science-repair.md:35-38`；`p08r2_verify.py:184-191` | 3GPP TS 38.212 §5.4.2.2，1536 位中 1534 位移动，`out_int` 可读，decoder 内部做 inverse。 | **YES（固定 baseline）/ NO（研究控件）**。建议保留 inner interleaver，在 encode 后/demap 前加外层可逆 placement adapter。 |
| TX mapping | `p08r2_chain.py:207-215` | 每个 codeword encode 后按数组顺序 flatten，直接 `qam16_mod`；prefix 前置。 | **PARTIAL**：连续映射骨架可用，但无 codeword/bit-role→channel-slot 显式契约。 |
| GG/SOP/AWGN trajectory | `p08r2_chain.py:216-233` | 整条 frame 一次生成 `h/theta`，再对双偏振加 AWGN；GG 参数通过 `get_gg_scenes` 导入（`p08r2_chain.py:56-59`），runner 调用（`p08r2_run.py:99-105`）。 | **PARTIAL**：caller 生命周期可用；必须另做 generator-level 相关性和跨 cw 无重置验收。 |
| prefix-LS receiver boundary | `p08r2_chain.py:77-145,236-277` | 32-symbol 已知 prefix 解 2x2 effective-channel LS，以残差生成 receiver-visible `sigma2_pre/gamma_vis`；equalizer 不读 true SNR。 | **YES**，可作为固定 receiver-visible baseline；不证明新 action/metric 合法。 |
| demap/decode | `p08r2_phaseA.py:128-147,150-194` | max-log soft demap，按 `contract.n` reshape 成 codeword LLR，再调 codec decode。 | **YES（基线）**；需在 demap 后、reshape/decode 前添加 placement inverse。 |
| runner/comparator | `p08r2_run.py:53-74,248-274` | 只支持 B0/B1/B2/O0/O1/O2，所有方法共用一条 realization。 | **PARTIAL**：配对比较骨架可用；无 fixed-deep comparator、continuous mapping、parity placement 或 segmentation 配置。 |
| failure decomposition | `p08r2_run.py:309-328` | 只以每 trajectory 的 all-cw-fail / full-success / oracle partial-rescue 计数分类。 | **PARTIAL**：有粗粒度分类骨架，但无 outage threshold 契约、burst start/length 与 per-cw fade 对齐。 |
| raw/result writer | `p08r2_phaseA.py:219-250`；`p08r2_run.py:270-274,369-386` | 可写 method/seed 级 raw 和 aggregate JSON。 | **PARTIAL**：写入机制可用，schema 需扩展。 |

### 3. 缺失接口表

| 缺失接口 | 最小契约 | 接入点 | 不补的后果 |
|---|---|---|---|
| `PlacementPlan` | 输入 `coded_bits[cw,bit] + bit_role + seed`，输出可逆 `channel_slot -> (cw,bit)` permutation 及 hash | `p08r2_chain.py:209-215` encode 后/QAM 前；`p08r2_phaseA.py:128-147` demap 后/decode 前 | 无法实现 continuous/random/parity-aware/segmented placement，也无法证明方法只差 placement。 |
| `BitRoleMap` | 每个 rate-matched 输出位标记 systematic/parity/filler/puncture lineage，明确 inner `out_int` 前后索引域 | `CodecAdapterR` 边界（P08-R2 只在 `p08r2_chain.py:56-67` 导入） | 仅凭编码后 bit index 不能安全声称“parity placement”。 |
| `ChannelLifecycleReceipt` | trajectory id、symbol index、cw boundary、generator initial/final state 或至少 h 的 lag correlation 验收值 | `p08r2_chain.py:204-220` generator 调用周围 | 一次长向量调用仍不足以证明所需时间相关性。 |
| per-codeword raw schema | `cw_id,start_symbol,end_symbol,fer,post_ber,h_mean,h_min,outage_class,placement_id`；LLR 建议存统计量/可选抽样而非默认全量 | `p08r2_phaseA.py:219-250` | 无法对齐 fade/burst boundary/codeword failure；全量 LLR 盲存会使 raw 体积膨胀。 |
| comparator config | `mapping_mode={fixed_deep,continuous,parity,segmented}` + 全部参数 + frozen hash | `p08r2_run.py:65-74,248-274` | runner 只能比 LLR 校准方法，不能比 coded-burst 映射。 |
| overhead/delay metric | prefix/interleaver/segmentation overhead，effective info bits/symbol，placement buffer depth，decoder latency，burst recovery span | `p08r2_phaseA.py:219-232`；`p08r2_run.py:369-386` | FER 改善可能是以额外延迟/缓冲/带宽换来，无法做公平比较。 |

### 4. 最小 adapter 工序与工期

**范围定义**：保留现有 Sionna codec、Gray-16QAM、一次整 trajectory channel 调用、prefix-LS 和 paired runner；只新增外层可逆 placement、四类 comparator 配置、per-cw schema 和 overhead/delay 计量。

| 工序 | 人日 |
|---|---:|
| 冻结 `PlacementPlan/BitRoleMap` 契约，确认 inner `out_int` 前后索引域 | 0.5-0.75 |
| 实现 encode 后外层 placement + demap 后 inverse，保持 codec 不变 | 0.75-1.0 |
| 加 fixed-deep / continuous / parity / segmented runner 配置与 paired dispatch | 0.75-1.0 |
| 扩展 per-cw boundary/fade/error/placement raw schema，补 outage 分类 | 0.5-0.75 |
| 加 prefix + placement buffer + segmentation 的 overhead/delay/effective-rate metric | 0.25-0.5 |
| 确定性验收：可逆性、noiseless round-trip、跨 cw lifecycle receipt、raw→aggregate | 1.0 |
| **合计** | **3.75-5.0 人日** |

这是“adapter”而非科学包工期；不包括方法调参、powered experiment、独立科学 verifier 或论文数字。

### 5. 完整 testbed 工序与工期

**范围定义**：不依赖 P08-R2 历史科学包，重建可审计 coded-chain + 时间相关信道 lifecycle + placement/interleaver runner + schema/metric + correctness gates。

| 工序 | 人日 |
|---|---:|
| codec/BICM 身份、bit-role lineage、可逆性与 noiseless 基础门 | 1.5-2.0 |
| 时间相关 GG/SOP/AWGN generator wrapper，lifecycle receipt，跨 symbol/block/cw/trajectory 检查 | 1.5-2.0 |
| placement/interleaver 策略层 + fixed-deep/continuous/parity/segmentation 实现 | 2.0-3.0 |
| prefix-LS receiver、demap/decode 管线整合与 receiver-information 边界审计 | 1.0-1.5 |
| per-cw/burst raw schema，outage 分类，overhead/delay/effective-rate metric | 1.0-1.5 |
| deterministic correctness/metamorphic/raw-recompute gates 与独立工程验收 | 1.5-2.0 |
| **合计** | **8.5-12.0 人日** |

### 6. `>5 天` 风险判定

- **最小 adapter：中风险，基准 3.75-5.0 人日，存在超过 5 天的尾部。** 两个主要不确定项是：① P08-R2 许可边界内看不到 generator 内部，跨 codeword 相关性可能需要补 wrapper 甚至更换 generator；② Sionna rate-matching + inner interleaver 后的 parity/systematic lineage 若无法稳定暴露，`BitRoleMap` 将从适配变成 codec 深度审计。任一项不闭合，最小方案预计增加 1-2 人日。
- **完整 testbed：高风险/几乎确定 >5 人日。** 下界 8.5 人日已同时包含 coded-chain、时间相关信道、可控 interleaver runner、schema/metric 和工程验收；任一块不能复用都会继续抬高工期。

### 7. 静态 semantic gaps

1. **连续调用 != 相关性已证明。** 代码能证明 16 cw 共享一次 N-symbol generator call，不能证明 generator 内部实现了预期的 GG 相关过程。
2. **`out_int` 可读 != interleaver 可控。** 现有代码用它验身份，没有把它变成可配置 action。
3. **per-cw FER 可计算 != per-cw evidence 已保存。** `cw_err` 向量在函数内被压缩成计数和均值，raw 无法回放错误位置。
4. **trajectory h mean/min/max != burst boundary。** 缺 per-cw 或至少固定 block 的 fade 序列、outage threshold 和 boundary label。
5. **16 个 codeword 直接 flatten != continuous interleaver baseline。** 它只是顺序串接，没有跨 cw 可逆重排或缓冲深度契约。
6. **prefix 被排除评分 != overhead 为零。** 其 32 个符号已进入物理 frame，必须进 effective-rate 分母。
7. **工程 verifier PASS != 新 coded-burst 合同 PASS。** `p08r2_verify.py:314-324` 的 lifecycle/schema 检查只验 per-traj h 字段与 per-pol FER/BER，并未验跨 cw 相关性、boundary 或 placement。

## 结论

P08-R2 可作为**最小 adapter 起点**：codec/BICM、固定 16-cw trajectory shape、一次长序列 channel caller、prefix-LS receiver 和 paired runner 都有现成骨架。它不是已完成的 coded-burst testbed：关键的可控 placement/interleaver、跨 cw lifecycle receipt、per-cw burst schema 与 overhead/delay metric 均缺失。

工程判断：优先做 **3.75-5.0 人日的最小外层 adapter**，前置闭合 generator correlation 与 bit-role lineage 两个风险；若两者任一不能在现有边界内闭合，应直接按 **8.5-12.0 人日的完整 testbed** 计划，其 `>5 天` 风险为高。

## 对决策的影响

本记录只提供工程 BOM 与工期边界，不继承 P08-R2 verdict，不新建或修改 D###。若后续决定实施，首个门控应是“generator 跨 cw 相关性 + `BitRoleMap` 可闭合”，未通过前不应展开完整 runner。

## 执行声明

- 本记录全程仅用 `rg` / `Get-Content` / `git status` 做静态检查。
- **未运行 Python、未 import 任何模块、未运行测试或仿真、未生成新结果。**
- **未修改源码、`common/`、`params.py`、旧 raw/result、Skill 或 `p05_run*.log`。** 本任务唯一写入为本 R003。
