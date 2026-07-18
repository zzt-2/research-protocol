# 验证进度索引

> 最后更新: 2026-06-01 | Phase: 1a | 已完成: 24/24 ✅ + 3 交叉验证

## Phase 1: 调研

### Ch3 BER 闭合解
| 编号 | 主题 | 状态 | 文件 |
|------|------|------|------|
| V-01 | GG衰落QPSK BER文献基线 | ✅ 完成 | ch3-ber-closed-form/V-01-gg-fading-baseline.md |
| V-02 | BER floor理论位置 | ✅ 完成⚠️ | ch3-ber-closed-form/V-02-ber-floor-theory.md |
| V-03 | 解析解文献对照 | ✅ 完成 | ch3-ber-closed-form/V-03-analytical-comparison.md |
| V-04 | MC验证方法正确性 | ✅ 完成 | ch3-ber-closed-form/V-04-mc-validation-method.md |

### Ch3 BER 界
| 编号 | 主题 | 状态 | 文件 |
|------|------|------|------|
| V-05 | 上界理论 | ✅ 完成 | ch3-ber-bounds/V-05-upper-bound-theory.md |
| V-06 | 下界理论 | ✅ 完成 | ch3-ber-bounds/V-06-lower-bound-theory.md |
| V-07 | 界紧致性文献 | ✅ 完成 | ch3-ber-bounds/V-07-bound-tightness-literature.md |

### Ch3 设计准则+鲁棒性
| 编号 | 主题 | 状态 | 文件 |
|------|------|------|------|
| V-08 | 估计误差与BER关系 | ✅ 完成 | ch3-strengthening/V-08-estimation-error-ber-relationship.md |
| V-09 | DPLL对h不敏感验证 | ✅ 完成 | ch3-strengthening/V-09-dpll-sensitivity-theory.md |
| V-10 | VV对h敏感验证 | ✅ 完成 | ch3-strengthening/V-10-vv-sensitivity-theory.md |

### Ch3 级联灵敏度
| 编号 | 主题 | 状态 | 文件 |
|------|------|------|------|
| V-11 | 级联灵敏度理论框架 | ✅ 完成 | ch3-cascade/V-11-cascade-sensitivity-theory.md |
| V-12 | VV公式正确性证明 | ✅ 完成 | ch3-cascade/V-12-vv-formula-correctness.md |
| V-13 | PASS标准合理性 | ✅ 完成⚠️ | ch3-cascade/V-13-pass-criteria-rationality.md |

### Ch4 系统性分析
| 编号 | 主题 | 状态 | 文件 |
|------|------|------|------|
| V-14 | VV性能预期 | ✅ 完成 | ch4-systematic/V-14-vv-performance-expectations.md |
| V-15 | BPS性能预期 | ✅ 完成 | ch4-systematic/V-15-bps-performance-expectations.md |
| V-16 | DPLL性能预期 | ✅ 完成 | ch4-systematic/V-16-dpll-performance-expectations.md |
| V-17 | FOE理论与精度 | ✅ 完成 | ch4-systematic/V-17-foe-theory-and-accuracy.md |
| V-18 | 相对排名理论预期 | ✅ 完成⚠️ | ch4-systematic/V-18-relative-ranking-expectations.md |

### Ch4 KF
| 编号 | 主题 | 状态 | 文件 |
|------|------|------|------|
| V-19 | KF载波跟踪理论性能 | ✅ 完成 | ch4-kf/V-19-kf-tracking-theory.md |
| V-20 | KF vs DPLL理论差异 | ✅ 完成 | ch4-kf/V-20-kf-vs-dpll-theory.md |
| V-21 | KF参数敏感性理论 | ✅ 完成 | ch4-kf/V-21-kf-parameter-sensitivity.md |

### 缺口分析
| 编号 | 主题 | 状态 | 文件 |
|------|------|------|------|
| V-22 | thesis-status数字映射 | ✅ 完成⚠️ | gap-analysis/V-22-thesis-claims-vs-simulations.md |
| V-23 | 论文声称vs仿真覆盖 | ✅ 完成⚠️ | gap-analysis/V-23-missing-simulations.md |
| V-24 | 优先级缺口清单 | ✅ 完成 | gap-analysis/V-24-priority-gaps.md |

## Phase 2: 仿真（Phase 1 完成后启动）
| 仿真 | 状态 | 偏离数 |
|------|------|--------|
| ch3-ber-closed-form | ✅ 19/22通过 | 0 🔴 |
| ch3-ber-bounds | ✅ 6/6通过⚠️ | 0 🔴 (floor收敛晚10-15dB) |
| ch3-strengthening | ✅ 16/16通过 | 0 🔴 |
| ch3-cascade | ✅ 6/6通过⚠️ | VV公式bug致弱湍流增益虚高14dB |
| ch4-systematic | ✅ 核心结论验证⚠️ | DPLL优势4.2x✅; VV强湍流BER偏低待复验 |
| ch4-kf | ✅ 通过 | KF弱/中优7.6-7.9dB; 强湍流3.32% |

## 已发现问题: 1 🔴 / 3 🟡 / 2 🟢

## 异常区
- 🔴 V-18: "弱湍流VV>DPLL"是仿真伪影（DPLL零初始捕获瞬态），稳态应持平。见 V-18-cross-validation.md
- ⚠️ R-cascade: VV公式bug致弱湍流增益虚高14dB（理论0.5-1.5dB vs 仿真15.47dB）
- ⚠️ R-systematic: VV强湍流BER 1.86%低于Phase1预期7.9%（需100种子复验）
- ⚠️ V-13: VV公式错误导致弱湍流gain虚高1-6dB
- ⚠️ R-bounds: BER floor收敛SNR比预期晚10-15dB
- 🟢 R-ch3-ber-closed-form: 19/22通过（3项已知局限非bug）
- 🟢 R-ch3-strengthening: 16/16全部通过
- 交叉验证: V-01通过✅, V-12确证✅, V-18发现伪影🔴
