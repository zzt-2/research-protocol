# [S029] PROMPT-026 B 类架构准入门审计

> 2026-07-16 | GW Step 1 + Step 4a D031 前置门 | 完成

## 目标

按 H013 执行 B1/B2/B3 检索、D031 test 段过滤与四判据；只有架构有证据打破固定前馈时序正交才进入 MVE。

## 记录

### GW Step 1 检索

每个子方向执行两组 `bash tools/search` 查询并落盘至 `search-archive/2026-07-16/`：

- B1：complex-valued RF MIMO equalization；complex-valued coherent optical equalizer
- B2：rotation-equivariant optical equalization；SOP rotation-equivariant polarization network
- B3：dual-branch polarization demux；dual-polarization branch neural equalizer

默认源遭 S2/OpenAlex 限速，随后用项目工具 arXiv 降级补齐落盘；B1 的 OpenAlex 查询成功返回 20 篇。B1 命中 Optics Letters 2024 MIMO-CVNN/PDM 强邻近占点，B2/B3 无直接命中，但不把单源零结果解释为绝对空白。

### D031 与四判据

B1/B2/B3 都能写出技术矛盾、方法形态、L0 baseline 和公平比较，因此四判据形式成立。然而三者都保持 test 权重冻结：B1 复值只增强复表示；B2 attention 没有当前 SOP 角输入且无群等变证据；B3 固定 X/Y 分支依赖坐标基。均未通过 H013 明定的 D031 额外准入门。

### 产物

创建并运行 `projects/simulation/explore/cma-fade-divergence/prompt026_b_class_architecture_gate.py`，结果为 `projects/simulation/results/cma-fade-divergence/prompt026_b_class_architecture_gate.json`。JSON 明确 `performance_mve_run=false`、三个候选的四判据和 defer 理由、以及若复活时的参数域、双口径、参数量匹配和消融合同。

## 决策引用

- D033：B 类固定前馈架构整体 defer（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是；仅 B 类，未修改 common/ 或参数/信号模型。

## 后续

按 H013 进入 D 类。若提出严格 SOP 群等变架构或显式 test SOP 状态输入，须作为新化身重新走检索和 D031 门。
