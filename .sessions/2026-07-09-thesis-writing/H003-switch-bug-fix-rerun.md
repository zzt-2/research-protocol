# Handoff: 切换方法三 bug 修复 + 30seed 重跑结果

> 来源: step4a-mve-execution S013 续（实验跑在 step4a）/ thesis-writing D001（结论回传写作专题）
> 交接目标: 用修复后切换数字更新简报 v3 + 重定切换方法的叙事定位
> 文件名: H003-switch-bug-fix-rerun.md
> 日期: 2026-07-09

## 已完成边界

修完切换代码三 bug + 30seed 重跑 + 诚实判定。**切换增益数字全部更新**。

**代码**：`projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_switch_30seed_fixed.py`（新；原 buggy `_a4_switch_30seed.py` 留作证据不改）
**数据**：`_a4_switch_30seed_fixed.json`（30 seed，net 口径）
**报告**：`_a4_switch_bugfix_report.md`（完整 bug 确认 + 修复 + 30seed 全表 + 结论）

**Bug 确认（独立核查，不盲信用户诊断）**：
- Bug 1 混合分母：✅ 成立（原 L110 NDA 分母=全块1024，DA 分母=data768，SWITCH 混用两套）
- Bug 2 判据脱钩：⚠️ **部分成立但非假增益驱动源**。脱钩属实，但脱钩只 *损* SWITCH 不 *帮* SWITCH，且 decide 必须在 raw 上做（接收端选估计器前没法均衡，鸡生蛋）。**判 raw 是合理的，Bug 2 不是 bug，保留原设计 + 文档说明**。这是对用户诊断的修正——用户把 Bug 2 也判为 bug，实际它不是假增益 +0.27-0.48dB 的成因。
- Bug 3 事后对照：✅ 成立（假增益主因，L152 min(n,d)=oracle）

**修复**：
- Bug1：统一全块 bit 口径（net）。NDA/DA/SWITCH BER 全除以全块 bit（=N_BLOCKS×N_DFT×BITS_PER_SYM）。DA 错误数仍在 data 位算（对齐主实验 ber_da_awgn is_data），但分母用全块 bit。**全块口径本质 = 已扣 pilot overhead(1.249dB) 的 net BER**，与论文 net-gain 框架（R003）一致。同时存 gross 口径（DA/768）作透明参考。
- Bug2：不修，保留 raw + 文档说明（见上）。
- Bug3：删 max(DA,NDA)，改报 switch_vs_DA_net + switch_vs_NDA 两个真实 baseline。额外加 per-block oracle 上界（Σ_b min(ne_n,ne_d_b)）= 可实现上界。

**TL-23 守门通过**：SW 必须 ≥ 逐 seed per-block-oracle。30seed 违例数=0。曾误用 frame-min 当边界（4 个"违例"实为合法 per-block 收益），已纠正为 per-block-oracle。

## 不要做什么

- ❌ **不要复用旧切换数字**：旧 +0.27~+0.48dB（switch_vs_max）是 Bug3 oracle 产物，禁用。简报 v3 / H002 里这个数字作废。
- ❌ **不要把 Bug 2 当 bug 修**：用户原诊断把 Bug 2（判据脱钩）列为三 bug 之一，但独立核查发现它不是假增益源（脱钩只损不帮，且 raw 判据合理）。decide() 维持 raw 信号。若主线/写作要再质疑，先读 report §1 + decide docstring。
- ❌ **不要用 gross 口径报 vs DA 增益**：gross 口径（SW 全块 vs DA_data）分母不同不公平。论文报 vs DA 必须用 net 口径（两边全块），脚注说明 pilot overhead 已在 BER 口径内扣。
- ❌ **不要把切换当核心卖点**：修复后切换无全场景增益（原 +1.2dB net gain 是主实验标准 BER 算的，不受切换 bug 影响，仍是主卖点）。切换真实价值是低 SNR 避 NDA 崩溃 + 强湍流高 SNR 微赢 DA，是"鲁棒性补丁"不是"增益引擎"。
- ❌ 不动 common/ / simulator/（守 sandbox 隔离）。

## 必读（按优先级）

1. `projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_switch_bugfix_report.md`（本任务完整报告，§3 30seed 全表 + §4 结论）
2. `_a4_switch_30seed_fixed.json`（修复后数据，字段：switch_vs_da_net_db_*, switch_vs_nda_db_*, oracle_vs_switch_db_mean）
3. 本专题 `topic-index.md` 不变量 7/8（切换数字禁用 + 叙事诚信边界）
4. D001（thesis-writing/decisions.md，三 bug 发现记录）

## 接口变更（代码改动）

```yaml
# 新文件，sandbox 内，不影响 common/simulator
script: projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_switch_30seed_fixed.py
output_json_fields:
  per_snr:
    nda: float              # NDA BER (full-block 口径)
    da_full: float          # DA BER (full-block net 口径，公平对比用)
    da_data: float          # DA BER (data 口径 gross，透明参考)
    sw: float               # SWITCH BER (full-block 口径)
    oracle: float           # per-block oracle 上界 (full-block 口径)
  summary_point:
    switch_vs_da_net_db_mean/ci95:   # SW vs 固定 DA (net, 公平) — 正=SW 赢
    switch_vs_nda_db_mean/ci95:      # SW vs 固定 NDA — 正=SW 赢
    oracle_vs_switch_db_mean:        # oracle vs SW — 正=oracle 更好 (SW 离上界多远)
    switch_vs_da_gross_db_mean:      # 透明参考，不作结论
ber_convention: full-block-bit (1024); DA errors on data positions, divided by full-block bits
selfcheck: selfcheck_min_violations=0 (SW>=per-block-oracle, 30seed)
```

## 核心数字（30seed，net 口径）

| 关系 | 范围 | 显著性 | 含义 |
|---|---|---|---|
| **SW vs 固定NDA**（低SNR 5-15dB, 全湍流） | **+1.3~+2.3 dB** | CI下界全正 | 切换避险真实价值：低 SNR 避 NDA 升幂崩溃 |
| SW vs 固定NDA（高SNR） | ≈0 | tie | 高 SNR 切换选 NDA，与固定 NDA 同 |
| **SW vs 固定DA**（AWGN/weak/mod 全 SNR） | **−0.1~−1.2 dB** | CI上界多为负 | 切换显著输给固定 DA（DA pilot 在这些场景稳赢） |
| SW vs 固定DA（strong 高 SNR 15-26dB） | +0.02~+0.20 dB | 多数 CI 跨 0 | 唯一可能微赢区，仅 strong@24 CI 显著(+0.20[+0.1,+0.3]) |
| oracle vs SW（全部） | +0.15~+1.75 dB | — | SWITCH 兑现 oracle 的部分空间（strong 高 SNR 兑现最好） |

**一句话**：切换不是全面赢两个固定方法。真实价值 = 低 SNR 避 NDA 崩溃（+1.3~+2.3dB vs NDA）+ 强湍流高 SNR 微赢 DA（+0.02~+0.20dB）。**净增益 +1.2dB（主实验）不依赖切换，仍成立。**

## 失败数据附录

无（非路线失败，是 bug 修复。原 +0.27-0.48dB 假增益数据在 `_a4_switch_30seed.json` 留存作 bug 证据）。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| 切换判据 CV 在 AWGN 低 SNR 误判（原 report §3.3） | 判据可改进 | 保留现状（net 口径下 AWGN 切换输 DA 是 DA 本就更强，非判据唯一锅） | 若要切换在 AWGN 也赢 DA，需归一化 CV 或 SNR 修正（但物理上 AWGN 无 fade，固定 DA 本就该赢，改进意义存疑） |
| strong@24 是唯一显著两边赢点 | 统计稳健 | 单点，样本依赖 | 论文若用切换卖点需更多 seed 或更多 strong 高 SNR 点确认 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| TL-23 SW≥per-block-oracle | 0 违例（30seed） | 盲判据不可能赢 oracle | 30/30 (100%) |
| TL-29 口径校准 | DA_full = DA_data×0.75 | pilot overhead 1.249dB | ✓ strong@24: 3.55e-2/4.73e-2=0.751 |
| TL-22 无"全面赢"震撼结果 | 修复后无全场景增益 | 盲判据不可能全面赢固定方法 | ✓ 符合预期（用户预判命中） |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 不变量 7/8（切换数字禁用 + 叙事诚信边界）
- [ ] 已验证报告 §3 表中至少 3 个关键数字（读 `_a4_switch_30seed_fixed.json` 核查：strong@24 vs DA net=+0.20[+0.1,+0.3] / weak@10 vs NDA=+2.30[+2.3,+2.3] / selfcheck_min_violations=0）
- [ ] 已确认 Bug 2 处理（不修，保留 raw）的理由（report §1 + decide docstring）
- [ ] 已确认当前范围未违反"明确不含"（sandbox 内，不动 common/simulator）

## 下一轮

1. **用新数字重写简报 v3 切换段**：删旧 +0.27-0.48dB，写真实价值（低 SNR 避 NDA 崩溃 +0.13~+2.3dB；强湍流高 SNR 微赢 DA）。守不变量 6 黑话禁令 + 不变量 8 数字禁用。
2. **切换叙事降级**：从"+1.2dB net gain 的兑现机制"降为"NDA-ML 低 SNR 鲁棒性补丁"。主卖点维持强湍流/上行 net gain +1.2-1.8dB（主实验标准 BER，不受 bug 影响）。
3. **若简报要保留切换**：必须脚注 net 口径（pilot overhead 在 BER 口径内扣），并诚实标注 strong@24 是唯一显著两边赢点。
4. **强湍流 BER 领域调研**（另一新对话）结果回来后一并整合进简报。
