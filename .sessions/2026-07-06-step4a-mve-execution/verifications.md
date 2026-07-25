# Verifications — Step 4a 维度 D MVE 执行

## V001: T006 高阶 CPR 组合方法主控接收审查

> 日期：2026-07-25
> 关联：T006 / S015 / D012 / D013
> 结论：FAIL（科学裁决）/ PARTIAL（工程与完整性）

### 新鲜验证

- commit `21bfbda353e1779a26d498b43f6353fe458f494f` 位于预期分支，工作树
  clean；提交只新增 T006 explore/results/test/worker-log 16 个文件。
- `PYTHONUTF8=1`：T006 定向测试 `32 passed`；Pilot-Jones 回归 `65 passed`。
- Windows 默认 locale：T006 为 `30 passed, 2 failed`，两个失败均为 YAML
  默认编码触发 `UnicodeDecodeError`；worker-log 的“双 locale PASS”不成立。
- T006 文件缺少 `RDL-TASK-CONTROL` 标记，故 epoch 8 所称 control guard 实际
  不可验证。这是治理完整性缺口，不单独决定科学结论。

### 科学攻击结果

1. **B10 身份 FAIL**：论文要求连续 `N_p=128` pilot training 后才切 DD；实现把
   第一个 sparse pilot 当训练完成，并在首次非零 `h1` 后冻结 `F`。纯 CFO、20 dB
   AWGN 探针在 0.1/1/10 MHz 下，连续 128 pilots 的 BER 分别约
   `0.193/0.404/0.158`，估计斜率偏离真值多个数量级。
2. **B12 身份 FAIL**：关键 Eq.5/Eq.6 image-only，代码自行采用
   `angle(Sigma_phi @ z_unit)`；source closure 已承认公式缺失，却仍把结果归因为
   “MAP over-smoothing”。该实现不能代表已发表 joint ML/MAP。
3. **channel semantics FAIL**：data symbol 走 canonical
   `sqrt(h)(cos(theta)sX+sin(theta)sY)+n`，pilot 被重建为
   `sqrt(h)exp(j phi_total)pilot+n`。seed 7700/7708 的 pilot-channel relative
   RMSE 分别约 `0.171/0.646`，pilot 与 data 不在同一物理通道。
4. **oracle/eval PARTIAL**：`phi_true` 把 SOP real mixing angle 当 scalar carrier
   phase；`eval_resolve` 文档声明 4 个 pi/2 rotations，实际试 8 个 pi/4 rotations。
5. **headroom gate FAIL**：adversarial|14 dB 的 `0.6059 dB` mean 中，单个
   5.5545 dB collapse seed 占 `91.7%`；median=`0.0447 dB`，drop-max
   mean=`0.0560 dB`。operational|14 dB 同样由单 seed 占 `93.6%`。near-random
   BER 经非线性 Q² 变换制造 survivor，不能授权方法结论。

### 裁决

- `PROBLEM_SURVIVES_METHODS_FAIL`：FAIL，不接收。
- “9–20 dB 为真实机制失败而非 bug”：FAIL，被 source-native probe 反驳。
- T006 工程资产：PARTIAL，可作为错误实现、测试与失败模式素材。
- B10/B12 family：`UNRESOLVED_IMPLEMENTATION_INVALID`，不作 Kill。
