# Handoff: 对话 4 — 阶段 0 全部收尾，进 sandbox 三方对照

> 来源: S004（阶段 0.4-0.6 收尾 D004+D005）| 交接目标: 新对话执行 sandbox 三方对照（阶段 1）
> 文件名: H004-conversation4-sandbox-three-way.md
> 日期: 2026-07-08

## 到哪了（状态）

**阶段 0 六项规约全部通过**（0.1-0.6，D001-D005），profile 第 9 次防线**解除**——可进 sandbox。

- **0.1**（D001）：Gardner TED 1986 公式源 = 用户本地 Matlab 代码，B7 映射靠数值重建
- **0.2**（D002）：B7 数学同族性 = 弱同族 (B)，机制数值验证成立（G(0)=0.132142 bit-exact）
- **0.3**（D003）：B7-Q1 架构 = FOE 前馈扫频 + Gardner TR 保留反馈环，不撞 D006
- **0.4**（D004）：fair gain = 二维报告（BER gain @ 双工作点 HD-FEC 主+BER 2e-2 锚 + Doppler 范围比 1.9×）+ PSA FOE baseline 必须 sandbox 重写（谱不对称法）
- **0.5**（D005）：B7Params 修正版 15 字段全溯源 content.md 行号 + B7 锚论文原参数 25GBaud/1.8kHz 不跟 NDA-ML 统一（用户决策）
- **0.6**（D005）：explore 目录结构落盘 + 下游引用同步清单

**关键产出**（下对话 sandbox 会用到）：
- `explore/b7-gardner-ted-foe/_fair_comparison_framework.md`（0.4 fair gain 框架 + TL-20 预期表）
- `explore/b7-gardner-ted-foe/_stage0_5_6_params_files.md`（0.5 B7Params 草稿 §1.2 + 0.6 文件组织 §2）
- 已有 0.2a 数值重建（`_b7_map_reconstruction.py` + `_b7_map_results.json`，sandbox 扩展复用）

## 下一步干什么（对话 5 = sandbox 三方对照，开始写代码）

> **profile 第 9 次防线已解除**：阶段 0 六项全做完，sandbox 合法。本对话开始写代码（但仍守 3 步上限 + sim-preflight v1.3.0）。
> **守 sim-preflight v1.3.0**：C6 公式核对 / C7 三方对照 / C8 祖师爷警报 / V1 公式逐项 / V2 三方归因 / V3 祖师爷 / V5 子 agent 归因独立核查 / V6 FR-26 读原文数值。

### sandbox 六步（建议拆 2 对话，每对话 ≤3 步）

**对话 5（sandbox 前半，3 步）**：
1. **B7Params 回写 params.py**（`_stage0_5_6_params_files.md` §1.2 草稿）：15 字段，修正 LEO_DOPPLER_RATE，删 PSA_PILOT_SPACING，补 7 新字段。回写后跑 `python params.py` 审计报告确认无 DEAD/CRITICAL
2. **PSA FOE baseline 重写**（谱不对称法 Vieira 2023 [5]）：新写 `_psa_foe_asymmetry.py`，不用旧 `psa_foe_recovery`。机制 = FFT 估功率谱 → 检测谱不对称方向/幅度 → 反演频偏。验证估准范围 ≤ 半 baud rate（25GBaud → ≤12.5GHz，跟 poster `content.md:19/49` 一致）
3. **B7 TED_gain(f_D) 解析推导 + Leven 对比**（残留风险闭合，V3）：`_ted_gain_analytic.py`，推导 B7 TED 增益随 f_D 的解析关系，显式对比 Leven M-th-power FOE [7]（content.md L87 ref [7]）。排除强同族 (C) 残留风险（D002 弱同族 B 结论的补强）

**对话 6（sandbox 后半 + MVE，3 步）**：
4. **CRB 下界**（FR-21 参考）：`_crb_lower_bound.py`，B7 FOE 的 CRB。FR-21 在 D005 下降级为参考不当 Kill 门，但 sandbox 仍算作对照
5. **三方对照主脚本**（C7+V2）：`b7_gardner_ted_mve.py`，B7 proposed FOE / Gardner 1986 TR（用户代码祖师爷方）/ PSA FOE 三方，按 `_fair_comparison_framework.md` §4 架构执行。fair gain 二维报告（BER gain @ 双工作点 + 范围比）
6. **MVE + consistency**：`B7-MVE-SPEC.md` 契约（仿 N1/NDA-ML SPEC，TL-20 预期表已在 0.4 落盘）+ 跑 MVE + consistency 检查

### 红线警报（sandbox 发现立刻停）

- **V3 祖师爷警报**（C8）：B7 vs Gardner 1986 TR BER gap <0.1dB（持平）→ 红线警报。0.2 已确认任务正交（FOE vs STR），持平可能性低。若真持平查实现 bug
- **D006 边界**：sandbox 实现时若发现写了"把湍流相位进载波同步环路"→ 立即停，这不是 B7-Q1 范围
- **TL-20 偏离**：BER gain @ BER 2e-2 偏离 0.6dB >0.2dB → 查 LPF2 实现 + PSA FOE baseline 是否真是谱不对称法

## 纪律（和下一步直接相关的约束）

1. **sim-preflight v1.3.0 C7+V2 三方对照**：B7 proposed / Gardner 1986 TR / PSA FOE 三方归因可信。守 V5 子 agent 归因主线独立重算
2. **V6 FR-26 读原文数值**：PSA FOE baseline 重写需查 Vieira 2023 IEEE Access 原文（`papers/doi/10.1109_access.2023.xxx` 需先确认是否已落盘，若未落盘走 `tools/download`）
3. **TL-13 共用 common/_channel.py**：B7 三方都用相同信道实现（25GBaud DP-QPSK + Doppler），禁自建信道
4. **B7Params 跟 SystemParams 物理隔离**：B7 脚本 import B7Params（25GBaud/1.8kHz），NDA-ML 脚本 import SystemParams（2.5GBaud/10kHz），不混用
5. **环境**：本机无 `~/.venvs/torch/`（AGENTS.md 路径过时），用 `python`（scoop python311，numpy 2.4.3/scipy 1.17.1/mpl 3.10.8）
6. **psa_foe_recovery 概念错债务**：common `_recovery.py:435` 是 pilot-aided 非谱不对称法，B7 baseline 不用这个，新写 `_psa_foe_asymmetry.py`。旧函数保留不删（explore/ 历史探针可能 import）
7. **5 个口径警示**：B7 0.6dB @ BER 2e-2 + 1.9× 范围 + OSNR 10dB（会议级别，范围+鲁棒性维度够格）

## 接口变更（如有代码改动）

**预期 sandbox 代码改动**（本轮阶段 0 无代码改动）：
- `projects/simulation/params.py` B7Params 类（L606-680）：15 字段重写（sandbox 第一步）
- `projects/simulation/explore/b7-gardner-ted-foe/`：新增 6 文件（`_b7params_draft.py` / `_psa_foe_asymmetry.py` / `_ted_gain_analytic.py` / `_crb_lower_bound.py` / `b7_gardner_ted_mve.py` / `B7-MVE-SPEC.md`）
- `projects/simulation/common/_recovery.py`：`psa_foe_recovery` 加 deprecation 注释（不改实现，标"非 B7 真 baseline"）

## 失败数据附录（如涉及路线失败）

无新增路线失败。阶段 0.4-0.6 全通过。

**潜在失败模式**（未触发但 sandbox 要警惕）：
- B7 0.6dB @ BER 2e-2 在 HD-FEC 处增量明显变小（HD-FEC 是外推非实测）→ sandbox 需测并论证，若 HD-FEC 处 gain <0.3dB 触发 Conditional Go（TL-05 薄增益转分析叙事）
- PSA FOE baseline 重写后估准范围 ≠ 12GHz（谱不对称法实现差异）→ 查 Vieira 2023 原文具体算法
- B7 TED_gain 解析推导发现跟 Leven M-th-power FOE 等价 → 触发 D002 残留风险条件 1，降级 (B)→(C) 强同族，需重新定位贡献（可能性低，0.2 数值重建已验证机制独立）

## 已知债务（原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| ~~B7 poster 落盘~~ | FR-26 | 已解决（S002）| - |
| ~~Gardner 1986 数学同族性~~ | INVARIANT 11 | 已解决（S003/D002）| - |
| ~~架构定性~~ | INVARIANT 12 | 已解决（S003/D003）| - |
| ~~公平对照框架~~ | D005 | 已解决（S004/D004）| - |
| ~~符号率/线宽场景差异~~ | TL-26 | 已解决（S004/D005 + 用户决策）| - |
| B7 TED_gain(f_D) 解析式缺失 | INVARIANT 13 / V1 | sandbox 前补解析推导 + Leven 对比 | sandbox（对话 5 第 3 步）|
| B7 算法框图 Fig.1b omitted | C6 | 按文字描述 + 用户代码定时环对接 | sandbox |
| **common `psa_foe_recovery` 概念错** | 公式忠实原文 | pilot-aided 非谱不对称法，sandbox 重写 | sandbox（对话 5 第 2 步）|
| **B7Params 旧字段问题** | TL-26 + FR-26 V6 | LEO_DOPPLER_RATE 错 + 缺 5 字段 + PSA_PILOT_SPACING 概念错 | sandbox（对话 5 第 1 步）|
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
| sandbox 三方对照 | 改进版/1986 原版/PSA FOE 三方归因可信 | V2+C7 | 未跑 |
| MVE BER gain @ BER 2e-2 | ≈0.6dB（锚论文一致性）| content.md L21/65/69 | 未跑 |
| MVE BER gain @ HD-FEC | ≥0.3dB（跨候选主判据）| D004 + SPEC §5 | 未跑 |
| MVE Doppler 范围比 | ≈1.9×（23/12）| content.md L21/49/69 | 未跑 |
| MVE B7 vs Gardner 1986 gap | >0.1dB（V3 祖师爷警报）| D002 任务正交 | 未跑 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（13 条，重点 11/12/13 B7 特殊风险）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] S004 D004 = fair gain 二维报告（核查 `decisions.md` D004 + `_fair_comparison_framework.md` §2）
  - [ ] S004 D005 = B7Params 修正版 15 字段（核查 `decisions.md` D005 + `_stage0_5_6_params_files.md` §1.2）
  - [ ] psa_foe_recovery 概念错（核查 `common/_recovery.py` L435-453 实现是 pilot-aided 非谱不对称法，L437 注释自承）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on（4 个依赖）
- [ ] 已确认当前范围未违反"明确不含"

## 下一轮

**对话 5**（sandbox 前半，3 步）：
- B7Params 回写 params.py + PSA FOE baseline 重写（谱不对称法）+ B7 TED_gain 解析推导 Leven 对比
- 守 sim-preflight v1.3.0 V6（PSA FOE 需查 Vieira 2023 原文，若未落盘走 `tools/download`）

**对话 6**（sandbox 后半 + MVE，3 步）：
- CRB 下界 + 三方对照主脚本 + MVE + consistency
- 守 sim-preflight v1.3.0 C7+V2+V3（三方归因 + 祖师爷警报）
- sandbox 发现 B7 vs Gardner 1986 持平 → V3 红线警报（但 0.2 已确认任务正交，持平可能性低）
