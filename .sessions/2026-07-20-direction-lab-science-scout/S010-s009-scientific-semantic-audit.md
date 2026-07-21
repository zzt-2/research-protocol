# [S010] S009 科学语义审计与状态纠正

> 2026-07-21 | 外部审计收口 | 已记录，待方法体系重设计

## 目标

纠正 S009 对 C04/C09 失败的过度机制解释，保留可复现数字与来源闭合事实，并为后续方法体系、恢复入口和文件组织重设计提供可信起点。本轮不重跑实验、不修改旧 artifact、不修改 Skill。

## 记录

### 1. 审计发现

- `c04-c09-shared-corrector-v1/src/run_corrector_batch.py:231-265` 优化的是到 16QAM 各坐标电平的 soft expected squared distance，不是合同文字所说的 fixed hard pseudo-label MSE。
- 该目标存在与输入无关的常数最优解：令 `A=0`、每个实坐标输出约 `±0.6075`，一维最小损失约 `0.32710044`，四个实坐标合计约 `1.30840175`，与所有训练组合停在 `1.3084` 一致。
- 因此候选 PI-SER 约 `0.928`、相对 blind affine 退化约 `+0.624`、worst degradation 约 `+0.78` 是真实可复现的运行结果，但它首先证明训练目标诱发常数塌缩，不能证明 `z_calib` 没有信息、残差必为非仿射、或 receiver-visible affine 在机制上不可学习。
- runner 实际对每个函数类只训练一个硬编码配置（`hidden_dim=64, lr=3e-3, weight_decay=1e-4`）；合同和 synthesis 所写 8 组合 sweep 没有对应 raw artifact。增加超参数搜索不能修复常数塌缩，因此本轮不以“补 sweep”掩盖根因。

### 2. 仍然有效的科学事实

- D013 的 truth-assisted affine bound 与 blind comparator 数字仍有效，但语义收窄：`fixed - oracle` 的 signed macro 约 `0.05575`，95% CI `[0.00240, 0.12098]`；artifact 中 clipped `H_total=0.06172` 是另一聚合定义，二者不得混写。
- 5/7 cells 的 clipped truth-assisted headroom 不低于 MDE，说明特权 TX truth 下存在局部 affine 上界差距。
- blind affine 相对 fixed-μ CMA 的 macro gain 为 `-0.00837`，95% CI `[-0.01529, -0.00251]`，所以当前具体 blind comparator 在该 slice 上有害。
- `H_residual = blind - oracle` 同时包含 blind comparator 自己造成的损害，不能直接解释为合法、可学习的 ML target。
- D012 的 C11 局部结论不受本次审计影响。
- V004 仍证明 raw 数字、hash、seed split、protected-history 守护和可复现性；它不再承担上述科学机制解释的确认。

### 3. 状态纠正

- D013 改为 `TX_TRUTH_ASSISTED_AFFINE_GAP_PRESENT / LOCAL_SLICE / DIAGNOSTIC`，不再自动授权 learned corrector。
- D014 改为 `IMPLEMENTATION_CONFOUND_CONSTANT_COLLAPSE`；C04/C09 的科学状态恢复为 `UNRESOLVED`。
- D015 中“由 exact mechanism negative 强制轮转”的推理失效。是否轮转仍可作为资源选择，但不是被本批科学证据强制。
- H009 变成历史交接，不得作为当前恢复入口；H010 是新的唯一恢复入口。

### 4. 对方法论的反馈

这次失误不是缺少 hash、receipt 或独立重算，而是语义门晚于完整证据链：先把错误目标函数跑得高度可复现，再对坏结果做机制解释。以后小型 Probe 必须先过分钟级的语义对照（恒等/no-harm、常数输出、输出方差与星座占用、单样本过拟合、简单 comparator 可复现），通过后才允许扩成 cells × seeds 的 Scout 证据链。

本专题已有 10 个 S 文件，达到膨胀预警。下一阶段不继续在科学专题堆流程设计，而回到 `2026-07-20-research-direction-lab-system` 专题统一设计 Skill、恢复投影与目录结构。

## 决策引用

- D016：S009 的 corrector 机制级负面撤回，改记为实现混淆与候选未决（新建）
- V005：S009 科学语义复核 FAIL（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是。仅修订证据语义与恢复入口；没有运行实验、修改历史 artifact、改 Skill 或启动下一候选。

## 后续

暂停新的科学批次。下一阶段在体系设计专题中完成“轻量 Probe → Scout → Deep Evidence”的分层、单一恢复投影、当前结论索引、抗膨胀目录和恢复演练；经过推演并固定后，再修改 Skill 并启动大规模运行。
