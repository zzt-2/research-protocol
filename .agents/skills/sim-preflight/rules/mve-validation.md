# MVE 算法正确性验证（区别于 consistency）

> v1.3.0 新增。源自 NDA-ML D-007~D-009 教训：consistency bit-exact 0.0000% PASS 但算法是错的。
> 适用阶段：MVE 设计/执行 + sandbox 验证 + Formal 仿真器一致性检查。

## 核心区分：consistency ≠ 算法正确性

| 验证类型 | 查什么 | 能查 | 查不了 |
|---|---|---|---|
| **consistency bit-exact**（MVE vs Formal）| 两套实现输出是否逐 bit 一致 | 实现同步（MVE 和 Formal 跑同一套代码路径）| **算法对错**（两套都漏同一 bug 时会假 PASS）|
| **算法正确性验证**（本规则）| 实现是否符合原论文公式 + 是否有真增量 | 公式逐项核对 + 三方对照 + 祖师爷警报 | — |

**关键教训**（NDA-ML D-008）：MVE `_time_domain_crlb.py` 和 Formal `sc_nda_ml_sim.py` 都漏了 ML 加权（都用等权 mean-angle），consistency 0.0000% PASS 是因为两者错误一致。**consistency 锚点只能查实现同步，查不了算法对错**。

## MVE 算法正确性验证清单（跑 MVE 前必过）

### V1. 公式来源逐项核对（禁靠文字描述重建）

每个核心公式必须：
- **标注原论文页码 + 公式编号**（如"B11 Eq.16 p.561"）
- **从原 PDF/源 LaTeX 核对**，不从 PDF→md 转换后的文字描述重建（LMMSE 复现失败教训：PDF→md 把 eq(5)(6)(7) 转成 `picture intentionally omitted`，靠文字重建缺关键项）
- **公式不全直接标红**，不硬磕复现（如 LMMSE #15 JPhoto，S008 复现失败后切 VV/BPS）

**自检**：
```bash
# 查 MVE/SPEC 或代码注释里是否每个公式都标了页码+公式号
grep -rE "Eq\.|equation|p\.[0-9]|公式" projects/simulation/explore/*/  --include="*.py" --include="*.md" | grep -E "[0-9]" | head
# 如核心公式无页码标注 → 补核对
```

### V2. 三方对照（消融 + 祖师爷，见 interrupt.md 第 12 条）

MVE/sandbox 必须含三方：
1. 我们的方法（完整版 / 增强版）
2. naive / 等权版（消融，证明增强有效）
3. 祖师爷方法（VV / Gardner 1986 / BPS 等领域经典，证明非数学同族）

**缺任一方 → MVE 不算闭合**（见 interrupt.md 第 12 条中断）。

### V3. 祖师爷持平警报（见 interrupt.md 第 10 条）

实验结果显示"我们的方法 vs 祖师爷方法"持平（BER/RMSE 差 <5%）→ **立即查数学同族性**，不当合理结果接受。

两种可能：
- (a) 数学同族 → 创新性受质疑，找拉开差距的条件（换参数/换场景）或重新定位贡献
- (b) 对照不公平（bug / 参数掩盖）→ 修 bug 重跑

### V4. 参数变更触发算法重审（见 interrupt.md 第 11 条）

CRITICAL 参数变更后（线宽/符号率/噪声量级），必做：
1. 该参数影响哪些算法路径？
2. 原参数下的增量结论在新参数下还成立吗？
3. 是否需要补 sandbox 验证新参数下算法对错？

**参数选择和算法验证耦合**——改参数可能掩盖 bug（如低线宽下 ML 加权≈等权，bug 不易暴露）。

### V5. 子 agent 归因独立核查

**子 agent 报告的原始数字可信，归因不可信**——主线必须独立从原始 JSON 重算归因。

NDA-ML D-009 教训：子 agent 报"加权拉开 VV"，主线独立从 JSON 原 BER 重算发现"等权也拉开 VV"，真因是 segmented 跟踪非加权。**子 agent 的因果归因必须主线独立验证，不能直接信**。

**核查方法**：
```bash
# 子 agent 报告归因后，主线独立 grep 原 JSON 重算
# 如子 agent 说"加权 vs VV -19.4%"，主线独立算"等权 vs VV"对照
# 若等权也拉开 → 真因不是加权，子 agent 归因错
```

### V6. FR-26 读原文数值（不只引位置）

**"已查证文献 X"必须读原文数值，不能只引页码/章节**。

NDA-ML D-009 教训：D-007 引"Valjus sat.1553 §4.2 L438"但没读 L438 原文"0.1-1MHz typical"，锁定 10kHz。证据链断在"引位置"而非"读数值"。

**核查方法**：
```bash
# 引用文献参数时，必须附原文具体数值 + 行号
grep -rE "sat\.1553|valjus|paillier|fernandes" projects/simulation/ --include="*.py" --include="*.md" | grep -E "[0-9]+.*[mk]Hz|[0-9]+.*GBaud"
# 如只有文献名无数值 → 补读原文
```

## 与 consistency 的协作

**consistency 仍要做**（MVE vs Formal bit-exact 一致），但它的角色是"实现同步检查"，不是"算法正确性证明"。

**正确顺序**：
1. V1-V6 算法正确性验证（本规则）→ 证明算法对
2. consistency bit-exact（MVE vs Formal）→ 证明两套实现同步
3. 两者都过 → MVE 结论有效

**只过 consistency 不过 V1-V6** = 算法可能错（两套实现错得一致）。
**只过 V1-V6 不过 consistency** = 实现不同步（MVE 和 Formal 跑不同代码路径）。

## 触发时机

- 设计 MVE-SPEC 时（V1/V2 前置）
- 跑 sandbox 时（V2/V3/V5）
- 参数变更后重跑前（V4）
- 引用文献参数时（V6）
- 任何"我们的方法 vs 经典方法"对照（V3）

**强制触发**：MVE PASS 判 Go 前，V1-V6 必须全过。缺任一项 → Go 判定无效，补验证。
