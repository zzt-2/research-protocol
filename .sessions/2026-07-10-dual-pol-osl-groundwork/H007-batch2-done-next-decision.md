# Handoff: 批次2方法层加固完成 — 机制细化 + CMMA baseline，下一步定批次3/写作

> 来源: S011 | 交接目标: 决定进批次3（新方法）还是直接进写作准备
> 文件名: H007-batch2-method-reinforcement-done.md
> 日期: 2026-07-12

## 到哪了（状态）

批次 2 方法层加固**主控独立 P6 验证 PASS**（S011/D013）。R004 三批次规划中批次 1（数据补完）+ 批次 2（方法层加固）完成，方法层 + 分析层数据齐备，可支撑论文写作。剩批次 3（可选新方法：盲 VQ-VAE / 自适应步长 / 发散恢复）。

**核心进展**（本轮新增）：
1. **D013 机制修正**：CMA BER 损耗主因**不是** f_G 驱动的跟踪滞后，是 **2×2 蝶形 CMA 长序列次优锁定不稳定/相位漂移**（几乎不依赖 f_G）。D011 结论方向不变（ML 价值成立），但机制描述更精确且更强。
2. **CMMA baseline 全测**：QPSK CMMA=CMA（实现验证），16QAM CMMA 仅优 CMA 0.4-0.9%（modulus mismatch 非主因，CMMA 非强 baseline）。

## 不要做什么

- ❌ **不要在论文里卖"CMA f_G 越大跟踪滞后越严重"**——批次 2 数据否证（稳态 BER 几乎不依赖 f_G）。改卖"2×2 蝶形 CMA 长序列锁定不稳定（CMMA 修不好），ML 固定权重免疫"
- ❌ **不要把 r_lcr/批次1 的 N=2M 整段 BER 当作"CMA 稳态性能"**——它掩盖了 early/late 分化（前段良好稀释后段退化）。论文需说明 N=5M 暴露的长序列退化
- ❌ **不要用收敛判定方法 2（权重范数稳定）**——范数稳定 ≠ BER 收敛（CMA 相位漂移时 |w| 稳定但输出相位跑偏）。只用方法 1（窗口 BER 单调停止）
- ❌ **不要把 2×2 CMA 的相位漂移当实现 bug**——|w| 稳定证明非发散，是 CMA 类算法的旋转模糊结构性特性（论文需说明）
- ❌ **不要把 task1 的 0.32 稳态 BER 当"绝对真值"写论文**——它依赖 N=5M 长序列 + 强湍流 + 2×2 蝶形设定，且受 seed-bias 影响。报比率（CMA/oracle）+ per-seed 分布更稳

## 必读（下一轮按优先级）

1. `.sessions/2026-07-10-dual-pol-osl-groundwork/topic-index.md`（当前位置 + 不变量）
2. `decisions.md` D013（本轮机制修正）+ D011（原定位，被 D013 细化不取代）+ D012（批次1）
3. `S011-batch2-method-reinforcement.md`（本轮验证细节，含 4 步独立复现）
4. `R004-direction-full-plan.md`（批次3 候选：盲 VQ-VAE / 自适应步长 / 发散恢复）
5. `voice.md`（导师约束：必须出东西 / 不能只分析得有方法 / BER 到 1e-3）

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| seed-bias（h_mean CV≈1.0） | 绝对 BER 精度 | 批次2 关键点已加到 20 seeds；ML 仍 3 seeds | 论文写 limitations + 关键 16QAM ML 点补 seed |
| 监督 vs 盲不公平（D011 债务1） | 公平对比 | 连续传输 overhead<<1% 部分缓解；审稿人 attack 防御仍需 | 批次3 盲 VQ-VAE 或论文标 future work |
| ML 方法创新性（D011 债务3） | 非换皮 | 网络结构标 Qin 来源，损失用 MSE；批次2 未涉及 | 批次3 fade-aware loss 或论文强调"机制解释贡献" |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| QPSK CMMA=CMA（实现正确性） | 逐 seed BER diff < 1e-6 | 数学等价性（单环 CMMA 退化 CMA） | 20/20 seeds diff=0.00 |
| CMA 长序列锁定不稳定（任务1） | late BER > early BER（同 seed） | 主控独立复现 N=2M/5M | 5/5 seeds late>>early |
| CMMA 16QAM 优于 CMA（多模收益） | CMMA/CMA < 1 | TL-20 预期 | 6/6 f_G（幅度 0.4-0.9%）|

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] 任务1 稳态 BER ~0.32 不依赖 f_G（查 `results/cma-fade-divergence/cma_transient_steady_results.json`）
  - [ ] QPSK CMMA=CMA 逐 seed diff=0.00（查 `cmma_ber_vs_fg_results.json` per-seed）
  - [ ] N=2M late BER ~0.14 vs N=5M late BER ~0.5（主控 S011 复现，可重跑 `python -c` 验证）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反"明确不含"

## 下一轮

**决策点（交用户）**：进批次 3 还是直接写作？
- **批次 3（可选新方法）**：盲 VQ-VAE（解决监督 vs 盲不公平，D011 债务1）/ 自适应步长 CMA（新方法贡献）/ 发散检测+恢复（跟 Q-DP3 交集）。风险中，工作量 2-3 对话
- **直接写作**：方法层 + 分析层数据已齐备（D006/D007/D008/D011/D012/D013），导师"必须出东西"+"会议论文不给修改机会"。批次3 的债务（公平性/创新性）可在论文标 future work 或 limitations

**若进写作准备**：
1. D013 机制修正反映到论文叙事（"长序列锁定不稳定"非"跟踪滞后"）
2. 图表清单（R004 D-1）：系统框图 / BER vs SNR 主图（批次1）/ 发散概率图（批次1）/ ML vs CMA BER vs f_G（S009）+ 新增 CMA 瞬态/稳态分解图（批次2）+ CMMA 对比图（批次2）
3. r_lcr/批次1 BER 数据补 early/late 分化说明
4. seed-bias + ML seeds=3 写 limitations

**若进批次 3**：先读 R004 批次3 段 + D011 债务表，定优先级（盲 VQ-VAE 解决公平性最关键）。
