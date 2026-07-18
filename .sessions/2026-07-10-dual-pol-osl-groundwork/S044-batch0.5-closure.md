# [S044] Batch 0.5 参数与事件指标闭合审计

> 2026-07-16 | 批量探索基础设施 | 状态：BLOCKED（现有三脚本均不得原样进入 Batch 1）

## 目标

只审计 Batch 1 候选脚本的参数真相源、paired shared realization、fade/swap/divergence/recovery 事件与指标口径；不改源码、参数或旧结果，不运行 Batch 1。

## 记录

### 1. 总判定

**BLOCKED。** 三个候选脚本均有可复用部件，但没有任何一个满足“原样作为 Batch 1 统一入口”的最小闭合条件：

- `r7_freeze_quantification.py`：参数、信道入口、标准 CMA、双偏振双口径、事件 schema 和结果保存均未闭合。
- `prompt030_domain_swap_audit.py`：同 realization 的方法内比较成立，但参数与信道入口不合规，使用的是缺 Godard `z` 因子的 current-CMA，BER 只计 `zX` 单流，且无时序事件。
- `prompt015_unified_baseline.py`：standard/current CMA 区分、双流 fixed/PI 评估和同一 realization 复用可作为主要基建；但关键参数仍从历史脚本模块常量导入，且只有 late-slice 终态指标，没有 fade/first-swap/recovery 事件，因此只能“拆函数复用”，不能原样跑 Batch 1。

S043 所列 4 个全局 CRITICAL 是路径外债务：`Q_fine_df` 位于 KF 参数（`projects/simulation/params.py:308-316`），三档 `sigma2_turb` 来自同一 CRITICAL 字段的三个 KFQ 实例（字段定义见 `projects/simulation/params.py:270-277`，实例见 `:351-357`）。本批 CMA/fade 信道和均衡调用链不读取这些字段；它们不阻断本候选族，但也不能宣称全局参数审计通过。

### 2. 参数真相源审计

| 项目 | 真相源现状 | 判定与证据 |
|---|---|---|
| GG `alpha/beta` | `params.py` 已有 current strong `(4.2,1.4)`，均为 OK；`as_dict()` 暴露统一入口 | **PASS（current 域）**：`projects/simulation/params.py:149-170,220-228`。`prompt015` 在每个 seed 运行时从 `SimulationConfig` 读取（`prompt015_unified_baseline.py:496-501`）。`prompt030` 把 current/old 两域都写死（`:99-107`），其中 old `(1.5,0.8)` 明标无溯源，故该脚本 FAIL。 |
| 信道 block | `ExperimentParams.BLOCK=100`，WARNING | **有单一源但来源未验证**：`projects/simulation/params.py:490-500`；`common/_config.py:15-16` 只是重导出。三脚本读到该值，但 CMA 内部 block size `64` 是另一物理/算法量，均为脚本硬编码。 |
| `f_G` | `GREENWOOD_FREQ_SWEEP=(30,100,300,1000)`；WARNING，要求扫描 | **prompt015/prompt030 FAIL**：真相源见 `projects/simulation/params.py:1147-1169`，历史依赖却写死 `F_G=30`（`ml_long_seq_failure.py:64-70`）。`r7` 的 full 列表 `[100,300,1000]` 也写在入口（`r7_freeze_quantification.py:627-631`），未从 sweep 字段读。 |
| SOP rate | `params.py` 无该字段 | **FAIL**：`r7` 写死 `1e-4`（`:54-58`），`prompt030` 写死 `4e-7` 和扫描表（`:90-107`），`prompt015` 从 `ml_long_seq_failure.py:64-70` 的模块常量导入。进入 Batch 1 前必须新增/指定唯一实验配置来源；本审计不代替用户拍值。 |
| fade threshold | `params.py` 无该字段 | **FAIL**：`r7` 写死默认 `0.1` 与扫描 `[0.05,0.1,0.3,0.5]`（`:57-58`）。阈值针对的是 `h`（信号中使用 `sqrt(h)`），不是场幅 `sqrt(h)`；进入 Batch 1 前必须冻结名称、单位/语义和来源。 |
| CMA `mu/taps/R2/block_size` | `params.py` 无 CMA 参数族 | **FAIL**：`r7` 的 `mu/taps` 扫描和 `CMA_BLOCK_SIZE=64` 位于脚本（`:54,627-632`）；`prompt030` 写死 `N_TAP=11, MU_SAFE=1e-3, R2=1` 且调用时再写死 block 64（`:90-96,178-182`）；`prompt015` 从历史脚本常量导入，签名仅把值记录下来（`:440-458`），没有变成真相源。 |
| symbol count / evaluation slice | `params.py` 无候选族实验长度字段 | **FAIL**：`r7` 写死 2M 并允许 CLI 覆盖（`:48,594-603`）；`prompt030` 写死 5M/扫描 2M、5M、8M（`:91,105-107`）；`prompt015` 从 `prompt013` 的 `N_SYMBOLS=5M` 与固定 late slice 导入（`prompt013_swap_mechanism_q2.py:49-53`）。CLI 值或跨脚本 import 不是统一实验配置。 |

### 3. Shared realization 与算法公平性

规范的双偏振共享入口已经存在：`generate_shared_realization_dp()` 在调用时从 `SimulationConfig` 解析 gamma/block/`T_S`/生成方法，并返回同一组 `rX/rY/sX/sY/h/theta/bitsX/bitsY`（`projects/simulation/common/_dual_pol_channel.py:10-33,35-81`）。

| 脚本 | 同 seed/同信道比较 | 统一入口 | 判定 |
|---|---|---|---|
| `r7_freeze_quantification.py` | baseline 与 freeze 在一个 trial 中复用同一 `rX/rY/h/theta`（`:284-326`） | 自建 `gg_time_envelope + gen_signals`（`:220-264,284-300`），未调用 `generate_shared_realization_dp` | **PARTIAL**：paired 公平性成立；共享生成器契约不成立。 |
| `prompt030_domain_swap_audit.py` | 每个 domain/seed 只生成一次，再传给 CMA/ML/oracle（`:275-286`；SOP/N sweep 同理 `:312-340`） | 自建 `gen_channel`（`:159-175`） | **PARTIAL**：paired 公平性成立；统一入口不成立。 |
| `prompt015_unified_baseline.py` | 每 seed 只生成一次 tuple，current/standard/ML/oracle 全复用；结果还写 `shared_realization_seed`（`:496-515,518-544`） | 实际 `gen_channel` 来自 `ml_long_seq_failure.py`，该函数仍自建信道（`ml_long_seq_failure.py:151-170`） | **PARTIAL（最接近可复用）**：方法内 paired 成立；必须迁移到 canonical DP shared generator，并保存 realization/config 签名。 |

### 4. 现有事件能力

- **fade start/end**：`r7` 能从 `h_block < threshold` 形成连续 `freeze_segments`（`r7_freeze_quantification.py:119-145,167-173,189-217`），但输出 trial 摘要丢掉了具体 segments，只保留计数和漂移（`:331-341`）；另外 freeze segment 是“CMA block 均值低于阈值”，尚未冻结为全批次 fade 事件定义。其余两脚本只保留 `h` 在内存，无 fade 事件。
- **first swap**：三个脚本都没有。`prompt030`/`prompt015` 只在整个 late slice 结束后给一次 classification（`prompt030_domain_swap_audit.py:185-228`；`prompt015_unified_baseline.py:471-472,496-535`），不能定位首次 swap。仓库里已有按 block 计算 post-hoc correlation 的历史实现提示，但 T006 禁止把 TX 真值 detector 冒充部署方法；本批只能把它作为离线诊断上界。
- **divergence**：`r7` 定义为权重范数超过初值 10 倍、输出幅度超过 `1e3` 或非有限，并给 `diverge_idx`（`:111-116,175-187,202-217`）。`prompt030` 只保留 current-CMA 的布尔值并在发散时把两种 BER 都置 0.5（`prompt030_domain_swap_audit.py:178-204`），未保存 index；`prompt015` 对 CMA 方法硬传 `False`（`prompt015_unified_baseline.py:519-524`），因此现状不能统一统计 divergence。
- **recovery point/delay**：三个脚本均没有。`r7` 注释声称评估“恢复后 BER”，实际 `compute_ber_X` 是整段单流 BER（`:267-279,308-335`），没有按 fade end 切片，也没有 recovery point。

### 5. Batch 1 最小事件与指标 schema（不改代码版合同）

以下是下一步实现必须满足的合同；本轮只定义，不把它冒充已实现功能。

#### 5.1 事件记录

每个 `seed × condition × method` 至少输出：

```yaml
realization:
  seed: int
  config_signature: sha256
  shared_realization_id: string
events:
  fades:
    - start_symbol: int
      end_symbol: int
      threshold_h: float
      eligible_for_recovery: bool
      recovery_symbol: int|null
      recovery_delay_symbols: int|null
      censored_at_symbol: int|null
  first_swap_symbol: int|null
  first_swap_persistence_windows: int
  diverged: bool
  divergence_symbol: int|null
```

统一定义：

1. `h_block` 是每个 CMA block 覆盖的 **irradiance `h` 均值**；`fade_start` 为首次 `h_block < threshold_h`，`fade_end` 为随后首次连续 `K_fade` 个 block 均满足 `h_block >= threshold_h` 的第一个 block 起点。`threshold_h`、`K_fade` 必须来自显式 Batch 配置并写结果元数据。
2. `first_swap_symbol` 仅作为**离线诊断**：在不重叠或固定步长的双流窗口中，用 fixed/PI assignment + 相关优势判 swap，并要求连续 `K_swap` 个窗口成立；位置记第一窗口起点。使用 `sX/sY` 的版本必须标 `information_access=post-hoc`，不得命名为 online detector。
3. `recovery_symbol` 为 fade end 后第一个满足以下条件且连续 `K_rec` 窗保持的窗口起点：双流 fixed-label BER 回到预注册阈值，同时不处于 swap/diverged。`recovery_delay_symbols = recovery_symbol - fade_end_symbol`。直到观测结束都未恢复则记 `null`，并用 `censored_at_symbol` 保存右删失位置，禁止填 0 或整段长度冒充恢复。
4. caller 必须持有 canonical shared realization、逐符号 `h/theta/sX/sY/bitsX/bitsY`；callee 必须返回逐窗口输出或事件 trace。现有 `prompt015::_run_single_seed` 是合适 caller 骨架，但 `run_cma_diagnostic`、ML 分支和事件 evaluator 都要暴露/消费同一窗口边界。

#### 5.2 Metric signature

| 指标 | numerator / denominator | 排除位置 | seed 内与跨 seed 聚合 |
|---|---|---|---|
| fixed-label BER | 两流固定 X/Y 映射下、每流仅消除 QPSK 载波象限模糊后的总 bit errors / `2 streams × 2 bits/symbol × N_eval`；“fixed”冻结的是流映射，不是禁止每流载波相位校正（沿用 `prompt012::evaluate_outputs`） | FIR 未覆盖首尾；预注册 warm-up；被判无效/发散后的未生成样本不能悄悄当 0 | seed 内按总误码计；跨 seed 报 paired 值、均值/中位数与区间。不得只报 `zX`。 |
| PI-BER | 在 2 个流排列与每流 4 个 QPSK 相位旋转上，最小总 bit errors / 同一 denominator | 与 fixed 完全同一 eval mask | 同时保存获胜 assignment；只作第二口径/离线下界，不替代 fixed。现有双流实现证据：`prompt012_longseq_audit.py:98-138`。 |
| swap rate | 主口径：发生 persistent first-swap 的 trial 数 / 全部 paired trials；另报 nondiverged 条件口径 | first-swap 搜索只从 warm-up 后开始；右删失 trial 仍留在全体分母 | 先每 seed 一个布尔，再跨 seed 比率；不把一个 seed 的多个窗口当独立样本。 |
| divergence rate | `diverged=True` trial 数 / 全部 paired trials | 不排除 swap/fade trial | 每 seed 一个布尔，跨 seed 比率；必须保存统一 divergence symbol。 |
| recovery success | `recovery_symbol != null` 的 eligible fade 事件数 / eligible fade 事件总数 | 排除序列尾部不足一个 recovery window 的 fade；排除 warm-up 前已开始且 start 不可观测的左截断事件 | seed 内先给事件计数；跨 seed 按 seed 汇总并另报 pooled 描述，避免长序列 seed 支配。 |
| recovery delay | `recovery_symbol - fade_end_symbol`；无单一 BER 分子/分母 | 仅已恢复 eligible events；未恢复单列右删失，不能从 delay 分布删除后仍不报 success | 每 seed 报 median/IQR；跨 seed 对 seed-level 统计做 paired 比较。另同时报 symbols 与 `delay_s = symbols × T_S`。 |

### 6. Batch 1 脚本准入清单

**允许直接进入 Batch 1 的现有完整脚本：无。**

**允许拆用的部件：**

- `prompt015_unified_baseline.py::_run_single_seed` 的“单 realization 喂所有方法”结构（`:496-544`）。
- `prompt013_swap_mechanism_q2.py::run_cma_diagnostic(mode="standard")` 的含 `z` 标准 CMA 梯度（`:300-316,377-382`），但其参数默认值与 block size 必须由显式配置传入。
- `prompt012_longseq_audit.py::evaluate_outputs` 的双流 fixed/PI/correlation 终态评估（`:98-138`），但 Batch 1 还需窗口级 wrapper 和统一 eval mask。
- `common/_dual_pol_channel.py::generate_shared_realization_dp` 作为唯一 shared channel 入口（`:10-81`）。
- `r7` 的连续低阈值 segment 提取思路（`r7_freeze_quantification.py:119-173`），但必须抽成与方法无关的 event evaluator，保留原始 segment。

**必须先修、不得原样运行：** `r7_freeze_quantification.py`、`prompt030_domain_swap_audit.py`、`prompt015_unified_baseline.py`。其中前两者不应继续充当 Batch 1 主入口；最小工作是以 `prompt015` caller 骨架新建/改造统一 Batch runner，而不是在三个历史脚本上分别补丁。

### 7. 进入 Batch 1 的最小闭合条件

- [ ] Batch 配置中有且只有一个来源定义：GG 域、`f_G`、SOP rate、信道 block、CMA block、fade threshold、CMA `mu/taps/R2`、symbol count、evaluation window/persistence。
- [ ] 所有方法从一次 `generate_shared_realization_dp()` 返回对象读取输入；结果保存 shared realization ID + seed + config/source SHA。
- [ ] standard-CMA 明确使用含 `z` 梯度；current-CMA 只能作为 historical-bug 对照，不得改名 standard。
- [ ] 所有方法输出同一窗口网格上的双流 fixed/PI、assignment、swap event、divergence index、fade events、recovery/censoring。
- [ ] 固定并保存上述 metric signature；PI 不遮盖 fixed，post-hoc TX detector 清楚标注信息访问。
- [ ] 结果使用 `common._experiment.save_results()`；`r7` 的裸 `json.dump`（`:538-545`）和 `prompt030` 的裸 `_save/json.dump`（`:232-242`）不得用于正式 Batch 结果。
- [ ] 先用同一 seed 的 baseline 重算验证“旧 runner 与统一 runner 在共同终态口径一致”，再启动任何新机制。

## 决策引用

- D045：候选族先地图，再批量排跑。
- 无新 D###；本轮是执行准入审计，未改变候选族方向或范围。

## 范围确认

- 本轮是否在 scope boundary 内：是。只完成 S043/T006 指定的 Batch 0.5 审计，没有改代码、参数、旧结果，没有跑 Batch 1。
- Inflation：写入本文件后专题有 45 个 `S*.md`（含重复编号 `S033` 债务）。本轮是 D045 批量工作流内的闭合步骤，不扩大软件 DSP/ML 范围，F1/G2 仍明确不含。

## 后续

主线先按“最小闭合条件”派一个独立实现任务，生成统一 Batch runner 与事件 evaluator；实现验证通过前，Batch 1 保持阻断。不要分别继续修补三个历史脚本，也不要先跑任一新方法。
