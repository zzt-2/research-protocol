# [R011] Selected-output 实现真实性追踪

> 2026-07-15 | 关联：R009 / R010 / D014

## 调研问题

当前论文与 Fig.2 所称“控制器选择 DA/NDA 相位估计并产生统一 carrier-corrected sequence”，是否由 Fig.5 权威实现实际支持？

## 发现

### 1. 可确认事实

- DA/NDA recovery 函数分别返回复数恢复序列：`common/_recovery.py:136-168,171-237`。
- 权威脚本 `_a4_switch_common768_30seed.py:120-139` 同时计算两路恢复序列；NDA 随后使用真实 `tx_bits` 做八重旋转消歧。
- `per_block()` 随即把两路序列解调为错误数，只返回三个整数；两路 `phi_est` 被 `_` 丢弃，没有 `selected_phi`。
- 主循环 `:325-342` 先完成两路均衡、恢复和错误统计，之后才调用 `decide()`；选择结果只累加 `ne_d` 或 `ne_n_common768`。
- 持久 JSON 只有错误数、BER、分支次数和 gain，没有 selected complex samples、phase 或 downstream output。
- 旧 A4 脚本同样使用 error-count mux；未找到另一个在线 selector runtime。

### 2. 论文/图与实现的关系

| 声称 | 结论 | 证据 |
|---|---|---|
| DA/NDA 两路各自产生 carrier-corrected complex sequence | PASS | recovery 返回值 |
| selector 判据只依赖 raw-window power 与 nominal SNR | PASS | `decide():97-107` |
| decision 在数据依赖上可先于两路恢复 | PARTIAL | 判据独立，但实际程序在两路处理后调用 |
| selector 实际 mux 两路相位估计或复数序列 | BLOCKED | `phi_est` 丢弃；只 mux error counts |
| Fig.2 的 `Selected \hat\theta -> Phase compensation -> Common downstream DSP` | BLOCKED | draw.io `:117-140` 强于 caller |
| common-768 selected BER 可视为先 mux 输出再硬判的数值等价 | PARTIAL | 仅在严格、后验 BER 条件下成立 |

### 3. 窄等价边界

error-count mux 只在以下条件下等价于“先按窗选择分支解调输出，再统计 common-768 BER”：selector 与错误/tx bits/branch output 无关；整窗二选一；两路使用相同 common-768 mask；downstream 仅是同一确定性硬判；指标只对逐窗错误数求和；无 EVM、LLR、FEC、突发结构或跨窗状态。

该等价仍依赖 NDA 用真实 `tx_bits` 做后验旋转消歧，因此只支持 post-hoc ambiguity-resolved BER evaluation，不支持可部署在线 NDA 输出、通用 downstream interface 或计算节省声称。

### 4. 路线后果

- 路线 A：只改标题/措辞为 adaptive CPR，同时保留 Fig.2 selected-phase/统一输出语义——FAIL，属于换名掩盖实现缺口。
- 路线 B：将论文和图收窄为“两阶段 branch decision + post-hoc selected-BER evaluation”——事实可支持，但是否仍满足导师所说“估计算法”需重新评估，且图结构必须重做语义 brief，不是局部挪字。
- 路线 C：实现真实 phase/complex-sequence mux，并验证与现有 metric、ambiguity protocol 和 downstream 等价——需要改代码/可能重跑，超出当前只读与不改仿真范围。

## 结论

整体 `BLOCKED`。当前权威实现属于 error-count mux；不能声称实际实现了 selected phase、统一 carrier-corrected complex sequence 或可复用 downstream receiver interface。R010 的局部图修路线失效；R009 定位 Batch 在路线 B/C 拍板前不得进入 WRITE。

## 对决策的影响

- 新建 D015，否决“只换定位文字 + Fig.2 局部挪字”的路线；D014 保留为目标定位，但进入 WRITE 的前提尚未满足。
