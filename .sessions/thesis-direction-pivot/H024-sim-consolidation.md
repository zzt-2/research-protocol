# Handoff: 仿真体系整理 + 评估方法统一 + 关键实验重验

> 来源: S023+S024 | 交接目标: 整理混乱的仿真代码，统一评估，重验关键结论
> 文件名: H024-sim-consolidation.md

## 已完成边界

1. S022: KF 方向完整链条（定位→搜索→推导→仿真→公平审查）→ 原 STRONG PASS
2. S023: VV/BPS/DPLL 系统性分析仿真 + Track A 100种子验证
3. S024: KF 20维度压力测试 → CONDITIONAL PASS（多个 FAIL）
4. 代码验证：发现 VV/DPLL π/4 偏移 + resolve_qpsk 不一致

## 不要做什么

1. **不要开发新方法**——当前任务是整理和验证，不是创新
2. **不要信任 D1/D2 的原始结论**——评估方法不一致
3. **不要修改 thesis-lessons.md 或 thesis-status.md 的决策部分**——等验证完成后再更新
4. **不要用 resolve_qpsk 作为主 BER 指标**——它用 oracle（TX bits）信息
5. **不要从旧文件（sim_direction_a.py, sim_ch4_kf_carrier_sync.py）复制代码**——它们有已知 bug

## 必读（按优先级）

1. **`projects/thesis-figures/simulation/SIM-SYSTEM.md`** — 本对话创建的仿真体系文档（含 π/4 问题、评估方法不一致、结论置信度分级）
2. **`projects/thesis-figures/simulation/SIMULATION_SPEC.md`** — Track B 对话创建的仿真规范（含 D1 最优参数、压力测试索引、13 条验证事实）
3. **`thesis-lessons.md`** — 13 条教训（TL-01 到 TL-13）
4. **`.sessions/thesis-direction-pivot/S024-kf-stress-test.md`** — Track B 完整压力测试报告
5. **`.sessions/thesis-direction-pivot/topic-index.md`** — 专题索引（刚更新，含 S023/S024）

## 核心任务

### 任务 1：合并两份仿真规范

将 SIM-SYSTEM.md 和 SIMULATION_SPEC.md 合并为**一个**唯一真相源：
- 保留 SIMULATION_SPEC.md 的结构（更完善）
- 补入 SIM-SYSTEM.md 的独有内容（π/4 偏移、resolve_qpsk 不一致、结论置信度分级）
- 标记每个结论为 ✅已验证 / ⚠️需重验 / ❌已证伪
- 写入 `SIMULATION_SPEC.md`（覆盖），删除 `SIM-SYSTEM.md`

### 任务 2：统一评估方法

所有方法统一用 `ber_count`（直接解调）：
- VV/DPLL 输出需先减去 π/4 恒定偏移：`rx_corrected = rx * exp(-j*pi/4)`
- 或实现差分解调（differential decoding）
- KF pilot 不需要修正（没有 π/4 问题）
- BPS 不需要修正（公式已正确处理）

### 任务 3：重验 D1（KF vs 最优 Fixed）

用统一评估方法重跑：
- Fixed 最优参数：M_vv=256, omega_n=20MHz（来自 SIMULATION_SPEC.md）
- KF pilot：5% 导频，标准参数
- 3 档湍流 × 30 seeds × Ns=10000
- **关键问题**：统一后 KF 是否仍然输给 DPLL？

### 任务 4：重验 D2 消融

用统一评估方法重跑消融实验：
- FOE only / FOE+VV / FOE+BPS / FOE+DPLL / KF pilot
- VV 是否真的有害？还是 resolve_qpsk 的假象？

### 任务 5：更新结论

根据重验结果：
- 更新 SIMULATION_SPEC.md 的结论置信度
- 更新 S024 的判定（如果结论变化）
- 列出最终"可靠结论"清单

## 接口变更

无代码接口变更。所有工作在现有代码基础上修改评估逻辑。

## 失败数据附录

### π/4 偏移验证数据（来自代码验证 agent）

| 条件 | VV BER (直接解调) | VV BER (resolve_qpsk) |
|------|-----------------|---------------------|
| AWGN 20dB, 无湍流 | 25.06% | ≈0 |
| 已知相位, 无噪声 | 49.8% | 0% |
| 弱湍流 20dB | 25.00% | 0.018% |
| 强湍流 20dB | 35.50% | 12.9% |

resolve_qpsk 在弱湍流下放大约 862×，在强湍流下仅 2.4×。说明弱湍流的"VV 有效"部分是 resolve_qpsk 的贡献，强湍流的"VV 有害"是真实跟踪失败。

### D1 原始数据（评估方法不一致）

| 湍流 | Default Fixed | Best Fixed | KF pilot | KF vs Best |
|------|-------------|-----------|----------|-----------|
| weak | 1.47% | 0.32% | 0.016% | +13.0 dB |
| moderate | 3.56% | 0.58% | 0.17% | +5.3 dB |
| strong | 19.8% | 2.22% | 3.08% | **-1.4 dB** |

**注意**：Best Fixed 用 resolve_qpsk（oracle），KF pilot 用 ber_count（公平）。统一后 KF vs Best 的差距可能缩小甚至逆转。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| SIM-SYSTEM.md 与 SIMULATION_SPEC.md 重复 | 唯一真相源 | 两个文件并存 | 本对话合并 |
| resolve_qpsk 掩盖 CPR 失效 | 公平评估 | 已确认未修 | 本对话统一 |
| VV/DPLL π/4 偏移未补偿 | 正确实现 | 已确认未修 | 本对话修复 |
| sim_ch4_kf_carrier_sync.py P-matrix bug | TL-09 | 未修，文件已废弃 | 不需要修（已废弃） |
| thesis-status.md Ch4 状态过时 | 状态准确 | 还停在 KF STRONG PASS | 验证完成后更新 |

## 验证阈值

| 验证项 | PASS 标准 | 来源 |
|--------|----------|------|
| 评估方法统一 | 所有方法用相同 BER 计算 | 本 handoff |
| D1 重验 | 统一后 KF 弱/中增益 >3 dB | S024 A1 基线 |
| D1 重验（强湍流） | KF 不输给 FOE+DPLL >2 dB | 或诚实报告差异 |
| D2 重验 | VV 有害/无害结论有明确条件 | 代码验证 |
| 规范合并 | 只有一个 SIMULATION_SPEC.md | 唯一真相源 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 SIM-SYSTEM.md 和 SIMULATION_SPEC.md
- [ ] 已理解 π/4 偏移的物理原因（QPSK 星座在 π/4+kπ/2）
- [ ] 已理解 resolve_qpsk 为什么是 oracle（用 TX bits 选旋转）
- [ ] 已检查 sim_kf_stress_common.py 的 VV 公式（unwrap(angle*M)/M，比 systemic 更差）
- [ ] 已确认 thesis-lessons.md 中的 TL-09/TL-11/TL-12/TL-13

## 下一轮

1. 读 SIM-SYSTEM.md + SIMULATION_SPEC.md
2. 写统一评估的公共函数（VV/DPLL 减 π/4 + 全部用 ber_count）
3. 重跑 D1 + D2
4. 合并规范文档
5. 输出最终可靠结论清单
