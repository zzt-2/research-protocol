# [S030] PROMPT-027 D 类 CMA+ML 混合解析门

> 2026-07-16 | GW Step 1 + Step 4a 维度 D | 修正 MVE 完成

## 目标

核对 D1/D2 是否越过 D031、是否真正不同于 D028 回滚，并决定是否进入 5-seed MVE。

## 记录

完成 hybrid CMA+ML、CMA neural switching、polarization swap ML recovery 三组 `tools/search` 并落盘。OpenAlex 限速后用 arXiv 补齐；无直接命中，但不据单源零结果宣称绝对空白。

D1/D2 在 test 段切换，故通过 D031。其相对 D028 的真实差异是 ML 独立状态不继承 CMA swap 权重，恢复能力优于回滚。但 D028 的永久 swap block 36698 早于 late 起点约 block 68359：早切时 hybrid late 完全等于 L0 ML，晚切更差。因此对预注册 strict `mean PI<L0` 存在解析不可能性，当前化身 KILL，不运行被支配网格。

创建并运行 `projects/simulation/explore/cma-fade-divergence/prompt027_d_class_hybrid_gate.py`，结果 `projects/simulation/results/cma-fade-divergence/prompt027_d_class_hybrid_gate.json`。JSON 固化 D031、四判据、D028 差异、信息访问三联卡、解析上界和复活条件。

## 决策引用

- D034：D 类解析 KILL（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是；仅 D 类，未修改 common/。

### 2026-07-16 独立审查 FAIL

D034 解析 Kill 撤回：永久 swap 仅 seed1000/1003，不能泛化 5/5；clean seeds 的 hybrid 可能保持 CMA；PI-BER 全段消歧非线性，晚切无单调更差定理。禁止进入 E，须先跑 L0/CMA/D1/D2 真实 5-seed MVE，结果由 D035 取代。

## 后续

### 修正 MVE 结果

`prompt027_d_class_hybrid_mve.py` 跑满 5 seeds。因果检测规定 block b 只控制 b+1；D1 永久切换、D2 1000-block hold；fixed/PI 在完整序列重算。当前代码 5 seeds 全 0 trigger，D1/D2 逐 seed等于 CMA-only，mean PI=2.2536e-4，对 L0 ML-only 6.944e-5 为 0/5 胜、p=1.0，KILL。forced-switch=ML-only 证明恢复输出路径可用。

旧 prompt021 的 2/5 永久 swap 与当前 0/5 不一致，标 baseline drift 债务；本轮结论只限当前源码元数据，不覆盖 D028。

## 后续

主控决定先冻结复现 D028 债务，或带着明确限制进入 E 类。

### 2026-07-16 baseline drift 系统诊断与历史域重跑

先复跑原 `prompt021.run_v0_swap_frequency`：当前工作树 5 seeds 全 0 swap，与 PROMPT-027 一致，排除检测器分叉。随后只把通道 strong Gamma-Gamma 参数从当前 `alpha=4.2,beta=1.4` 改回 D022 历史 `1.5,0.8`（不写文件），原 prompt021 精确恢复 `{1000,1003}` 2/5 swap，确认根因是输入参数漂移，不是 CMA、PI 评价或随机数接口。

PROMPT-027 隔离冻结 D022 参数并加入触发集合断言后跑满 5 seeds：触发 `[9765,0,0,9765,0]`；D1/D2 mean fixed=0.21215008、mean PI=0.01505264，相对 L0 mean PI=0.01043760 为 0/5 胜、p=1.0，KILL。forced-switch 逐 seed 等于 L0。结果：`projects/simulation/results/cma-fade-divergence/prompt027_d_class_hybrid_mve_d022frozen.json`。

证据指纹：prompt021 `24CF3870…E88`；prompt027 `7443B6F3…E79D`；当前 params `A1D5F051…72E1`；历史 prompt021 JSON `F6862F3A…0DD`；新结果 JSON `FBAD5B4C…C67`。D036 取代 D035 作为 H013 注册域结论，baseline drift 债务关闭。

## 决策引用（续）

- D036：D 类历史注册域 5-seed MVE KILL（新建）

## 后续（续）

D 类完成；baseline drift 不再阻塞主控决定 E 类。
