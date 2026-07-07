# Handoff: 对话 5 — sandbox 前 4 步完成，进对话 6 三方对照 + MVE（剩 2 步）

> 来源: S005 | 交接目标: 新对话执行 sandbox 后半 2 步（三方对照 + MVE）
> 文件名: H005-conversation5-sandbox-back-half-mve.md
> 日期: 2026-07-08
> 续接：用户授权"往下"，追加步骤 4 CRB 下界（独立轻量，本轮做完）。剩步骤 5/6。

## 到哪了（状态）

**sandbox 前 4 步完成**（S005，D006 新建），profile 第 9 次防线解除后本轮开始写代码，守 sim-preflight v1.3.0 + INVARIANT 6 解除。剩 2 步（三方对照 + MVE）。

- **步骤 1 B7Params 回写 params.py**（主线程直接做）：`params.py` L606-680 B7Params 整体替换，旧 6 字段 → 新 15 字段。审计 14 OK + 1 WARNING（GARDNER_GAIN 典型值），**0 DEAD/CRITICAL**，全局 SimulationConfig total 55→64（DEAD/CRITICAL 数不变 6/4，未引入新问题）。下游 grep 无断链。
- **步骤 2 PSA FOE baseline 重写**（子 agent）：4 产出 in `explore/b7-gardner-ted-foe/`（`_psa_foe_asymmetry.py` + `_results.json` + `_curve.png` + `_summary.md`）。Vieira 2023 content.md L343-347 Δf̂=α·ln(P+/P−)/2，α_calib=0.953GHz。**诚实反常发现**：coarse-only 线性区仅 ~1GHz（远低于 poster 半 baud 12.5GHz），主线 V5 核查确认非 bug（β=0.1 谱边缘物理结果），登记为已知限制。
- **步骤 3 TED_gain 解析推导 + Leven 对比**（子 agent）：4 产出。**G(f_D) = K_max·|cos(πf_D/B)|** 解析成立（f_D 依赖性解耦为余弦因子，跟脉冲形状无关），K_max=0.132142 bit-exact 复现 0.2a 锚点。Leven 2007 对比判**弱同族 (B) 不降级 (C)**（三层运算不等价），**D002 残留风险闭合**。
- **步骤 4 CRB 下界**（子 agent，续接追加）：4 产出。`var(f_D) ≥ 12/[(2π)²·(E_s/N_0)·T_s²·N·(N²−1)]`（Rife-Boorstijn/Kay/Mengali 溯源）。主测点 N=1024 OSNR=17dB CRB std = **59.42 kHz**，比扫频间隔 1GHz 小 **16830 倍**。结论：**B7 精度瓶颈是 1GHz 扫频量化网格，不是理论 CRB 极限**；CRB 完全不卡 B7，FR-21 不触发 Kill（D005 降级合理）。

**D006 三个登记项**：① PSA coarse-only 弱（fair gain BER gain 标为上界）② Leven DOI 修正 891597→891893 ③ D002 残留风险闭合。

**关键产出**（对话 6 会用到）：
- `explore/b7-gardner-ted-foe/_psa_foe_asymmetry.py`（PSA FOE baseline，谱不对称法）
- `explore/b7-gardner-ted-foe/_ted_gain_analytic.py` + `_results.json`（G(f_D) 解析式 + Leven 对比数据）
- `explore/b7-gardner-ted-foe/_crb_lower_bound.py` + `_results.json`（CRB 数据，N scaling −3/2 验证）
- `params.py` B7Params 15 字段（对话 6 三方对照主脚本可直接 import）
- 0.2a `_b7_map_reconstruction.py`（B7 proposed FOE 数值重建，sandbox 三方对照的候选方实现基础）

## 下一步干什么（对话 6 = 三方对照 + MVE，剩 2 步）

> **守 sim-preflight v1.3.0**：C7 三方对照 / V2 三方归因 / V3 祖师爷红线（B7 vs Gardner 1986 BER gap <0.1dB）/ V5 子 agent 归因主线独立重算 / TL-20 偏离即查。

### sandbox 后半 2 步

5. **三方对照主脚本**（C7+V2）：`b7_gardner_ted_mve.py`，三方 = B7 proposed FOE / Gardner 1986 TR（用户代码祖师爷方）/ PSA FOE（步骤 2 重写的 `_psa_foe_asymmetry.py`），按 `_fair_comparison_framework.md` §4 架构执行。fair gain 二维报告（BER gain @ 双工作点 + 范围比 1.9×）。**注意 PSA coarse-only 弱（D006）**：BER gain 标为上界，范围/鲁棒性优势独立报告。
6. **MVE + consistency**：`B7-MVE-SPEC.md` 契约（仿 N1/NDA-ML SPEC，TL-20 预期表已在 `_fair_comparison_framework.md` §5 落盘）+ 跑 MVE + consistency 检查。**MVE 结果需用户做 Go/Conditional Go/Kill 判断**（profile 画像：不宜在长上下文一口气塞完）。

### 红线警报（sandbox 发现立刻停）

- **V3 祖师爷警报**（C8）：B7 vs Gardner 1986 TR BER gap <0.1dB（持平）→ 红线警报。0.2 已确认任务正交（FOE vs STR），步骤 3 解析推导 G(f_D)=K_max·|cos(πf_D/B)| 进一步验证机制独立，持平可能性低。若真持平查实现 bug（B7 前馈扫频是否被错实现成反馈跟踪）。
- **TL-20 偏离**：BER gain @ BER 2e-2 偏离 0.6dB >0.2dB → 查 LPF2 实现 + PSA FOE baseline 是否真是谱不对称法（步骤 2 已验证是谱不对称法，所以重点查 LPF2）。
- **D006 边界**：sandbox 实现时若发现写了"把湍流相位进载波同步环路"→ 立即停，这不是 B7-Q1 范围。
- **D006 PSA 弱发现**：若三方对照发现 B7 vs PSA BER gain 异常高（如 >2dB），先查是不是 PSA coarse-only 弱（D006）导致的虚高，不是 B7 真有那么强。fair-comparison 框架记录此限制。

## 纪律（和下一步直接相关的约束）

1. **sim-preflight v1.3.0 C7+V2 三方对照**：B7 proposed / Gardner 1986 TR / PSA FOE 三方归因可信。守 V5 子 agent 归因主线独立重算（D-009 教训 6：只信原始数字不信归因）。
2. **V3 祖师爷红线**（C8）：B7 vs Gardner 1986 TR BER gap <0.1dB → 立即停。0.2 + 步骤 3 解析推导已双重确认任务正交 + 机制独立，持平可能性低。
3. **TL-13 共用 common/_channel.py**：B7 三方都用相同信道实现（25GBaud DP-QPSK + Doppler），禁自建信道。
4. **B7Params 跟 SystemParams 物理隔离**：B7 脚本 import B7Params（25GBaud/1.8kHz），NDA-ML 脚本 import SystemParams（2.5GBaud/10kHz），不混用。
5. **PSA FOE baseline 已就绪**（步骤 2）：`_psa_foe_asymmetry.py`，对话 6 三方对照直接 import。注意它自包含（不依赖 params.py/common），如要跟 B7 三方共用信道需适配（或三方都用各自自包含信号生成 + 相同 seed）。
6. **环境**：本机无 `~/.venvs/torch/`，用 `python`（scoop python311，numpy 2.4.3/scipy 1.17.1/mpl 3.10.8）。
7. **D006 PSA 弱限制**：三方对照 BER gain 是上界（PSA coarse-only 弱），论文叙事分两维报告（BER gain 上界 + 范围 1.9×/OSNR 10dB 结构性优势）。

## 接口变更（如有代码改动）

本轮 sandbox 前半代码改动：
- `projects/simulation/params.py` B7Params 类（L606-680）：15 字段重写（D005 草稿落地）
- `projects/simulation/explore/b7-gardner-ted-foe/`：新增 8 文件（PSA FOE baseline 4 + TED_gain 解析 4）
- `projects/simulation/common/_recovery.py`：**未改**（psa_foe_recovery pilot-aided 实现保留，加 deprecation 注释留到对话 6 或不做，旧函数不删防 explore 历史探针断）

预期对话 6 代码改动：
- `explore/b7-gardner-ted-foe/`：新增 4 文件（`_crb_lower_bound.py` + `_crb_results.json` + `b7_gardner_ted_mve.py` + `B7-MVE-SPEC.md` + `_mve_results.json`）

## 失败数据附录（如涉及路线失败）

无新增路线失败。sandbox 前半 3 步全通过。

**D006 登记的已知限制（非失败）**：PSA FOE coarse-only baseline 线性区 ~1GHz（25GBaud/β=0.1 物理结果），f_D≥2GHz 全 failA。三方对照时 B7 vs PSA BER gain 是上界。

**潜在失败模式**（未触发但对话 6 要警惕）：
- B7 0.6dB @ BER 2e-2 在 HD-FEC 处增量明显变小（HD-FEC 是外推非实测）→ 对话 6 需测并论证，若 HD-FEC 处 gain <0.3dB 触发 Conditional Go（TL-05 薄增益转分析叙事）
- 三方对照发现 B7 vs Gardner 1986 持平 → V3 红线警报（0.2 + 步骤 3 双重确认任务正交，可能性低，若真持平查实现 bug）

## 已知债务（原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| ~~B7 poster 落盘~~ | FR-26 | 已解决（S002）| - |
| ~~Gardner 1986 数学同族性~~ | INVARIANT 11 | 已解决（S003/D002）| - |
| ~~架构定性~~ | INVARIANT 12 | 已解决（S003/D003）| - |
| ~~公平对照框架~~ | D005 | 已解决（S004/D004）| - |
| ~~符号率/线宽场景差异~~ | TL-26 | 已解决（S004/D005 + 用户决策）| - |
| ~~B7Params 旧字段问题~~ | TL-26 + FR-26 V6 | **已解决（S005）**：15 字段回写 params.py，0 DEAD/CRITICAL | - |
| ~~B7 TED_gain(f_D) 解析式缺失~~ | INVARIANT 13 / V1 | **已解决（S005/D006）**：G(f_D)=K_max·\|cos(πf_D/B)\| 解析成立 | - |
| ~~common psa_foe_recovery 概念错~~ | 公式忠实原文 | **已解决（S005）**：PSA FOE 谱不对称法 baseline 重写 in explore（旧 pilot-aided 函数保留不删）| - |
| ~~Leven 2007 论文落盘 + DOI~~ | FR-26 | **已解决（S005/D006）**：DOI 891893 已落盘 | - |
| B7 算法框图 Fig.1b omitted | C6 | 按文字描述 + 用户代码定时环对接 | 对话 6 MVE 实现 |
| **PSA FOE coarse-only 线性区 ~1GHz** | fair gain 真实性 | **新登记（D006）**：非 bug 是物理限制，BER gain 标为上界 | 对话 6 三方对照记录 + 可选补 fine CFE stage 作双方对称增强 |
| NDA-ML 线宽/方向未定 | step4a-mve-execution | dormant | 不阻塞 B7 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| ~~0.1 公式完整性~~ | ~~核心公式完整可实现~~ | ~~V1~~ | **PASS（S002/D001）** |
| ~~0.2 数学同族性 + 映射数值重建~~ | ~~非同族 + 周期相关可复现~~ | ~~V3+C8~~ | **PASS（S003/D002）** |
| ~~0.3 架构定性~~ | ~~前馈化不撞 D006~~ | ~~INVARIANT 12~~ | **PASS（S003/D003）** |
| ~~0.4 公平对照框架~~ | ~~fair gain 定义明确 + 工作点论证~~ | ~~D005 + SPEC~~ | **PASS（S004/D004）** |
| ~~0.5 参数真相源~~ | ~~每个参数标 source_type+source+audit_flag~~ | ~~TL-26 + V6~~ | **PASS（S004/D005）** |
| ~~0.6 文件组织~~ | ~~explore 目录结构 + 命名规约~~ | ~~防 E 类混乱~~ | **PASS（S004/D005）** |
| ~~sandbox 1 B7Params 回写~~ | ~~15 字段 + 0 DEAD/CRITICAL~~ | ~~D005 + TL-26~~ | **PASS（S005）** |
| ~~sandbox 2 PSA FOE baseline 重写~~ | ~~谱不对称法（非 pilot-aided）~~ | ~~D004 + V6~~ | **PASS（S005，coarse-only 弱限制登记 D006）** |
| ~~sandbox 3 TED_gain 解析 + Leven 对比~~ | ~~解析式成立 + 弱同族 B 确认~~ | ~~V1 + V3~~ | **PASS（S005/D006）**：G(f_D)=K_max·\|cos(πf_D/B)\|，D002 残留风险闭合 |
| ~~sandbox 4 CRB 下界~~ | ~~FR-21 参考值（不当 Kill 门）~~ | ~~D005 降级~~ | **PASS（S005）**：CRB std=59.42kHz << 扫频间隔 1GHz（小 16830 倍），精度瓶颈是量化非 CRB，FR-21 不卡 |
| sandbox 5 三方对照 | 改进版/1986 原版/PSA FOE 三方归因可信 | V2+C7 | 未跑 |
| MVE BER gain @ BER 2e-2 | ≈0.6dB（锚论文一致性）| content.md L21/65/69 | 未跑 |
| MVE BER gain @ HD-FEC | ≥0.3dB（跨候选主判据）| D004 + SPEC §5 | 未跑 |
| MVE Doppler 范围比 | ≈1.9×（23/12）| content.md L21/49/69 | 未跑 |
| MVE B7 vs Gardner 1986 gap | >0.1dB（V3 祖师爷警报）| D002 任务正交 + D006 解析闭合 | 未跑 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（13 条，重点 11/12/13 B7 特殊风险）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] S005 B7Params 回写 = 15 字段 0 DEAD/CRITICAL（核查 `params.py` L606-680 + 跑 `python -c "from params import B7Params; ..."` 审计）
  - [ ] S005 PSA FOE baseline = 谱不对称法（核查 `explore/b7-gardner-ted-foe/_psa_foe_asymmetry.py` docstring 含 Δf̂=α·ln(P+/P−)/2，非 pilot-aided）
  - [ ] S005 D002 残留风险闭合 = G(f_D)=K_max·|cos(πf_D/B)|（核查 `_ted_gain_analytic_results.json` + 主线 V5 核查记录 in S005）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on（4 个依赖）
- [ ] 已确认当前范围未违反"明确不含"

## 下一轮

**对话 6**（三方对照 + MVE，剩 2 步）：
- 三方对照主脚本 + MVE + consistency
- 守 sim-preflight v1.3.0 C7+V2+V3（三方归因 + 祖师爷警报）
- sandbox 发现 B7 vs Gardner 1986 持平 → V3 红线警报（但 0.2 + 步骤 3 解析推导双重确认任务正交，持平可能性低）
- 注意 D006 PSA coarse-only 弱限制：三方对照 BER gain 标为上界
- CRB 已完成（步骤 4）：不卡 B7，MVE Go 判据仍按 D005 务实路线（赢传统 baseline 几 dB）
