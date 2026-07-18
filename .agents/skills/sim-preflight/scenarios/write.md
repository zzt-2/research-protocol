# 场景 C：写论文 / 引用仿真数字

> ⚠️ **本文件所有示例均为格式占位（`{...}`），非真实数字**。引用前必须从 `CONCLUSIONS.md` grep 真实条目，禁止照抄占位。

## 读（引用前必读，只从真相源取）

1. **`毕设/CONCLUSIONS.md`** — 数字只从这里取。安全等级 ≥ ⚠️ 才能写入论文；❌ 不可写 / 🔄 待重验 禁止引用
2. **`毕设/TERMS.md`** — 术语统一（如"归一化辐照度 h"不是"信道增益"）
3. **`毕设/formulas-master.md`** — 公式编号和 LaTeX 从这里取，不从论文草稿或记忆取
4. **`毕设/symbol-conventions.md`** — 符号用法

**关键**：每个引用的数字/公式，抄到工作笔记（M1 管道断裂防护）。同时沿真实调用链填写实现真相三联卡，不能只抄结论文件或 JSON 元数据。格式：

```
{文件名:行号 或 结论编号} | {指标}={值} {单位} | {安全等级} | {限定条件}
code_path={paper line -> caller -> callee -> metric/state}
information_access={online known, genie/oracle, post-hoc}
metric_signature={error population, numerator, denominator, excluded positions, aggregation, dataset/figure}
state_lifecycle={initialization scope, reset scope, generator-call scope, continuity span}
```

举例（**真实格式，数字必须 grep 验证**）：

```
CONCLUSIONS.md:128 | VV(Nw=64) 弱湍流 BER=2.33e-4 [1.1e-4, 3.6e-4] | ⚠️ 需限定（Nw=64 非最优）| 代码来源 [common.py]
formulas-master.md:F3.5 | VV 相位估计方差 | σ² ≈ 1/(2·Nw·γ)
```

三联卡任一字段为空、调用链未追到实际 callee/外层循环，或论文表述强于实现 → `BLOCKED`，不得进入写作。`CONCLUSIONS.md` 与 JSON/meta 只能定位证据，不能单独证明信息流、指标分母或重置范围。

强制回归锚点：

- `blind-genie-information`：论文称 blind，但 `resolve(rx, tx_bits)` 等运行/评估路径读取发送标签或 ground truth → `BLOCKED`，除非明确标为 genie/post-hoc 评估或移除该输入；
- `metric-signature-mismatch`：不同结果的 error population、分子、分母、排除位置或聚合不同，却共用同一 BER/增益名称 → `BLOCKED`；
- `reset-scope-mismatch`：外层循环逐窗口 `generate(..., new_seed)`，却声称跨窗口连续 → `BLOCKED`。

## 守（写作时）

- 每个数字必须能在 CONCLUSIONS.md 找到对应条目，找不到 → 不写入论文
- 每个算法声称和 headline/figure 必须有完整实现真相三联卡；同名指标逐项比对 `metric_signature`
- 安全等级 ⚠️ 需限定的结论，引用时必须加边界条件（见下方模板）
- 公式编号连续，不自创编号
- **符号一致性检查**（强制）：h 在 Ch3/Ch4 含义不同（信道估计误差 vs 辐照度），引用前 grep TERMS.md 确认

## ⚠️ 结论引用模板

⚠️ 结论引用必须加边界条件。**完整占位**（不只是调制）：

- **正文句式**："在 {SNR} {湍流强度} 下，{方法}（{参数版本}）的 BER 为 {值}（仅 {调制}，{统计显著性}）。"
  - 占位说明：
    - {参数版本}：如 Nw=64 / Nw=256（区分最优 vs 非最优）
    - {统计显著性}：如"10 seeds, 95% CI [{lower}, {upper}]"或"CI 与 {对比方法} 重叠"
  - 真实示例（**写论文时 grep 验证**）：`在 20dB 弱湍流下，VV 算法（Nw=64）的 BER 为 2.33×10⁻⁴（仅 QPSK，10 seeds, 95% CI [1.1×10⁻⁴, 3.6×10⁻⁴]）`
- **表格脚注**："该值仅在 {调制} + {湍流} + {方法}({参数版本}) 下验证。"
- **图题**：名词短语 + 无括号条件 + ≤15 字（GB/T 7713.1）

❌ 禁止句式：
- "BER 为 X%"（无边界条件）
- "性能提升 X%"（无对比基线）
- 任何不带 {参数版本} 和 {统计显著性} 的 ⚠️ 结论引用

## 改（写作后）

1. **`毕设/thesis-status.md`** — 更新章节完成状态
2. 如发现 CONCLUSIONS.md 数字有误 → **先改 CONCLUSIONS.md**（拥有者文件），再改论文
3. **写使用日志**（见 `rules/usage-log.md`）：场景=C | 任务=... | issues=...
