# 仿真体系统一化

> 状态: active | 创建: 2026-05-31 | 最后更新: 2026-05-31 (S003)

## 背景

两段对话各自产出 SIM-SYSTEM.md 和 SIMULATION_SPEC.md，内容重叠且互相矛盾。23 个 .py 文件中 resolve_qpsk 重复定义 10+ 次。需要合并规范、建立统一项目目录、升级公共模块。

## 进展线索

### S003: Ch3→Ch4 衔接实验
> 2026-05-31 | 衔接实验 | 完成

- 用 noisy h 替代 oracle h 注入 MMSE 均衡，量化估计误差对载波同步 BER 的影响
- 3 方法 × 3 湍流 × 5 NMSE × 10 种子，6.6 秒完成
- **核心结论**：载波同步对信道估计误差极度鲁棒，NMSE ≥ -5 dB 退化 < 1 dB
- **附带发现**：VV 在强湍流反而有害（Fixed=8.7% vs FOE+DPLL=1.9%），DPLL 独用最优
- 论证了 Ch4 oracle h 假设的合理性，衔接 Ch3→Ch4 叙事

### S002: Ch4 代码+参数审计 + D1/D2 重验
> 2026-05-31 | 审计+重验 | 完成
> 2026-05-31 续接 — D1/D2 重验发现 VV 公式 bug 致命影响

- 3 个 explore agent 并行审计 16 个文件（15 旧 + 1 新 common.py）
- **参数一致性**：全部通过，无实质性不一致
- **函数一致性**：1 处严重（VV unwrap 公式 5 文件不一致）、1 处命名（ber vs ber_count）
- **Bug 确认**：4/5 项确认（P-matrix bug 仅在已废弃文件，Agent 3 误判已手动纠正）
- **D1/D2 重验**：用新 common.py 跑 30 种子，发现 VV 公式修正导致结果巨变
- **3 个子 agent 交叉验证**：head-to-head 测试 + 旧 systematic_analysis 检查 + 数学分析
- **核心发现**：旧 stress_common 的 VV 公式 bug 膨胀了 Fixed 基线 BER，KF 增益全部消失
- SPEC.md §6 已按修正后结论全面重写

### S001: 项目初始化 + 规范合并
> 2026-05-31 | 收 H024 handoff | 完成

- 收 H024 handoff，Trigger 5 验证发现 handoff 关键声称有误（见不变量 §2）
- 4 个 explore agent 并行摸底：代码 23 文件、结果 17 JSON + 54 图表、2 份规范重叠
- 新项目目录 `projects/simulation/` 创建
- SPEC.md 合并完成（唯一真相源）
- common.py 升级完成（ber_eval + FIXED_CFG_OPTIMAL + VV 公式修正）
- archive/README.md 旧文件索引完成
- _registry.yaml 注册完成
- 旧 SIM-SYSTEM.md / SIMULATION_SPEC.md 标记废弃

## 已确认结论

### 不变量

1. **信号模型锁定**：r=√h·s·exp(jφ)+n, γ=γ̄·h（TL-01）
2. **H024 "D1/D2 评估方法不一致"声称有误**：
   - H024 称"KF pilot 用 ber_count，Fixed 用 resolve_qpsk"
   - 代码验证：`sim_kf_stress_D1_D2.py` L95 `resolve_qpsk(rx_fixed, sh['bits'])` + L98 `resolve_qpsk(corrected[data_idx], data_bits)` — **两者都用 resolve_qpsk**
   - D1/D2 评估方法**实际一致**
3. **旧目录 projects/thesis-figures/simulation/ 不再新增代码**
4. **载波同步对信道估计误差鲁棒**（S003 衔接实验）：NMSE ≥ -5 dB 退化 < 1 dB，Ch4 oracle h 假设合理
5. **VV 公式 bug 影响**（S002 重验发现）：
   - 旧 stress_common.py L144 `unwrap(angle*M)/M` 导致 VV BER 虚高 2-1800 倍
   - 正确公式 `unwrap(angle)/M`（common.py L170）
   - 修正后 KF 增益从 +11/+5/-1.4 dB → 0/-0.7/-2.5 dB
   - 旧 D1/D2 压力测试中涉及 Fixed 基线和 VV 的结论需修订

### 其他结论

- VV 在强湍流反而有害（Fixed=8.7% vs FOE+DPLL=1.9%），DPLL 在强湍流是最优方法
- resolve_qpsk 对 VV/DPLL **同时也是必要配套**（4 次方鉴相器引入 π/4+π/2 模糊，resolve_qpsk 通过试旋转解决）
- ber_count 仅适用于 KF pilot（不做 4 次方无模糊）；VV/DPLL 用 ber_count BER≈25%（clean signal 测试确认）
- π/4 修正不可行：简单减 π/4 无法解决 π/2 模糊（测试确认 VV 减 π/4 后 ber_count 仍=1.0）
- VV 公式从 `unwrap(angle*M)/M` 修正为 `unwrap(angle)/M`（SIM-SYSTEM.md 已标记的已知问题）

## 范围边界

### 原始目标

合并两份仿真规范、统一评估方法、建立可维护的项目结构

### 当前范围

1. ~~新项目目录 `projects/simulation/` 已建~~ ✅
2. ~~SPEC.md 已合并~~ ✅
3. ~~common.py 已升级并验证~~ ✅
4. ~~旧文件归档索引已完成~~ ✅
5. ~~Ch3→Ch4 衔接实验已完成~~ ✅

### 明确不含

- 不重跑 D1/D2 实验（下一轮任务）
- 不删除旧目录文件
- 不修改 thesis-lessons.md
- 不开发新方法
- 不对 D1/D2 结论做可靠性判定（超出范围，待下一轮重验）

### 范围变更记录

无

## 未决项

- [x] D1/D2 重验 — 已完成，发现 VV 公式 bug 致命影响
- [x] Ch3→Ch4 衔接实验 — 载波同步对估计误差鲁棒，oracle h 假设合理
- [ ] Ch4 论文叙事重新规划：从"KF 算法创新"转为"系统性分析"
- [ ] SNR 扫描曲线（BER vs SNR）— 论文必需
- [ ] C5 深衰落改善用修正 Fixed 重验
- [ ] 评估 resolve_qpsk 对绝对 BER 值的影响量级

## 当前位置

**S003 完成。载波同步对信道估计误差极度鲁棒（NMSE ≥ -5 dB 退化 < 1 dB），Ch4 oracle h 假设合理。VV 在强湍流有害，DPLL 独用最优。**

待用户返回决定 Ch4 叙事方向。
