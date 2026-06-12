# 仿真验证框架 — 检查点地图与集成指南

> 创建: 2026-06-12 | 配套文件: `tests/test_common.py`, `tests/red_flags.py`

## 1. 框架总览

```
                    ┌─────────────────────────────────┐
                    │  实验脚本 (experiments/*.py)      │
                    │  ┌─────────────────────────────┐ │
                    │  │ 1. 生成信道 (shared)         │ │
                    │  │    ↓ [CP-1] 信道验证         │ │
                    │  │ 2. 均衡 + 载波恢复           │ │
                    │  │    ↓ [CP-2] 方法输出验证      │ │
                    │  │ 3. BER 计算                   │ │
                    │  │    ↓ [CP-3] 结果红旗检测      │ │
                    │  │ 4. save_results()             │ │
                    │  │    ↓ [CP-4] JSON 元数据       │ │
                    │  └─────────────────────────────┘ │
                    └─────────────────────────────────┘

    持续验证:  ~/.venvs/torch/bin/python -m pytest tests/ -v
```

## 2. 检查点地图

### CP-1: 信道生成后 (generate_shared_realization 之后)

**验证内容:**
- h > 0 (Gamma-Gamma 物理约束)
- E[h] ≈ 1 (归一化约束)
- 同 seed → 同信道 (公平性基础)
- 信号模型 SNR ≈ gamma_bar * E[h]

**自动测试:** `TestT4ChannelFairness` (7 个测试)
**红旗规则:** RF-06 (h 正值), RF-09 (信道共享)

**手动检查 (实验脚本内):**
```python
shared = generate_shared_realization(...)
assert np.all(shared['h'] > 0), "h 含非正值"
assert abs(np.mean(shared['h']) - 1.0) < 0.1, "E[h] 偏离 1"
```

### CP-2: 载波恢复后 (各方法输出)

**验证内容:**
- 输出不含 NaN/Inf
- 输出长度 = 输入长度
- 星座图基本形状正确 (QPSK 四点 / 16-QAM 十六点)

**自动测试:** `TestT2CarrierRecovery` (8 个测试), `TestT3KalmanFilter` (7 个测试)
**红旗规则:** RF-07 (NaN/Inf)

**手动检查:**
```python
rx_comp = run_fixed(shared)
assert not np.any(np.isnan(rx_comp))
assert len(rx_comp) == len(shared['rx_raw'])
```

### CP-3: BER 计算后 (ber_eval / resolve_qpsk 之后)

**验证内容:**
- BER ∈ [0, 1]
- BER 不接近 0.5 (高 SNR 下)
- BER 在已知范围内 (SPEC §6.1)
- 增益在合理范围 [-10, +20] dB
- 强湍流 BER > 弱湍流 BER
- BER 随 SNR 单调下降

**自动测试:** `TestT5PhysicalInvariants` (9 个测试), `TestT6RegressionGuard` (5 个测试)
**红旗规则:** RF-01~RF-05

**集成到实验脚本:**
```python
from tests.red_flags import check_ber, format_flags

for seed in range(N_SEEDS):
    ber = run_single_seed(...)
    flags = check_ber(ber, method='DPLL', turbulence=turb, snr_db=snr_db)
    if any(f.severity == 'CRITICAL' for f in flags):
        print(format_flags(flags))
        raise RuntimeError(f"红旗检测失败: {flags[0].message}")
```

### CP-4: 保存结果时 (save_results 之前)

**验证内容:**
- JSON 元数据完整 (script, common_md5, git_commit, timestamp)
- 多种子统计量合理 (置信区间、失败率)
- 结果文件可被绘图脚本正确解析

**自动测试:** `TestT7ParameterConsistency` (13 个测试) — 验证参数未漂移
**红旗规则:** RF-08 (种子方差)

## 3. 测试套件分层

| 层次 | 类名 | 测试数 | 耗时 | 触发频率 |
|------|------|--------|------|----------|
| T1 信号原语 | TestT1SignalPrimitives | 11 | <1s | 每次改 common.py |
| T2 载波恢复 | TestT2CarrierRecovery | 8 | ~3s | 每次改 VV/DPLL/BPS/KF |
| T3 Kalman 滤波器 | TestT3KalmanFilter | 7 | ~2s | 每次改 kf_unified |
| T4 信道公平性 | TestT4ChannelFairness | 8 | ~2s | 每次改信道生成 |
| T5 物理不变量 | TestT5PhysicalInvariants | 9 | ~3s | 每次出结果 |
| T6 回归守卫 | TestT6RegressionGuard | 5 | ~5s | 每次 commit 前 |
| T7 参数一致性 | TestT7ParameterConsistency | 13 | <1s | 每次 common.py 改动 |
| T8 数值稳定性 | TestT8NumericalStability | 7 | ~2s | 新方法/新参数 |
| **总计** | | **69** | **~8s** | |

## 4. 红旗规则速查

| 规则 | 严重性 | 触发条件 | 根因 |
|------|--------|----------|------|
| RF-01 | CRITICAL | BER ∉ [0,1] | 数值溢出 |
| RF-02 | CRITICAL | BER ≈ 0.5 at high SNR | 载波恢复完全失败 |
| RF-03 | WARNING | BER > 10% at SNR≥20dB | 信号模型或方法 bug |
| RF-04 | WARNING | BER 远离已知范围 | 回归或参数漂移 |
| RF-05 | CRITICAL | 增益 > 20 dB | 基线有 bug (如旧 VV 公式) |
| RF-06 | CRITICAL | h ≤ 0 | 信道生成 bug |
| RF-07 | CRITICAL | NaN/Inf in rx | 除零/数值溢出 |
| RF-08 | WARNING | 种子间方差极小 | 种子未传递 |
| RF-09 | INFO | 未提供 channel_seed | 提醒用 shared 信道 |

## 5. 实施优先级 (最大影响 / 最小成本)

### Phase 1: 立即实施 (30 分钟)

1. **运行 `pytest tests/test_common.py -v`** — 69 个测试已覆盖核心函数
2. **在 multi_seed_sweep.py 中集成红旗检测** — 在 `run_single_seed` 后加 `check_ber`
3. **commit 前跑一次完整测试** — 确保改动不破坏已知结论

### Phase 2: 下次实验时 (每次新实验)

4. **新实验脚本开头 import red_flags** — 每个结果都过 RF-01~RF-07
5. **运行前跑 `pytest -k T7`** — 确认参数未漂移
6. **运行后跑 `pytest -k T5`** — 确认结果符合物理

### Phase 3: 长期维护

7. **新方法/新参数 → 加 T2/T3 测试** — 验证新组件
8. **新验证事实 → 加 T6 回归守卫** — 防止结论被推翻
9. **新红旗发现 → 加 RF 规则** — 每次抓到 bug 都加规则

## 6. 关键教训映射

| 教训 | 验证措施 | 测试 |
|------|----------|------|
| TL-01 信号模型错误全盘皆错 | CP-1 SNR 验证 | TestT4::test_signal_model_snr |
| TL-09 P 矩阵跨块重置 | CP-2 P 传递验证 | TestT3::test_kf_P_cross_block_propagation |
| TL-13 信道共享公平性 | CP-1 确定性验证 | TestT4::test_shared_realization_deterministic |
| TL-20 先建理论预期 | CP-3 与已知范围对比 | TestT5::test_dpll_strong_turbulence_known_range |
| TL-22 震撼发现先查物理 | 全套红旗检测 | RF-02, RF-03, RF-05 |
| TL-25 save_results 元数据 | CP-4 JSON 验证 | common.py save_results() |

## 7. 文件位置

```
projects/simulation/
├── common.py              # 仿真基础设施 (被测代码)
├── SPEC.md                # 已验证事实 (测试断言来源)
├── tests/
│   ├── test_common.py     # 69 个 pytest 测试 (T1-T8)
│   └── red_flags.py       # 红旗检测器 (RF-01~RF-09)
└── experiments/
    └── *.py               # 实验脚本 (集成检查点)
```
