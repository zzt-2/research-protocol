# [S004] 阶段 0.4-0.6 收尾（fair gain 框架 + B7Params 真相源 + 文件组织）

> 2026-07-08 | 阶段：B7 阶段 0.4+0.5+0.6 收尾 | 状态：阶段 0 六项规约全通过（D004+D005），可进 sandbox

## 目标

执行 H003 阶段 0.4-0.6 收尾，完成阶段 0 全部六项规约。不写代码（INVARIANT 6），不进 sandbox（profile 第 9 次防线——阶段 0 全做完才解除）。

## 记录

### 报到 + Handoff 验证（Trigger 1+5）

读 topic-index / _registry / profile / decisions / S003 + 0.2/0.3 报告 + B7 锚论文 content.md + B7 精读笔记 + N1/NDA-ML SPEC + params.py + common `_recovery.py`。

**H003 3 条事实核查全 PASS**：
- D002 弱同族 (B)：decisions.md D002 L62-107 + `_lineage_check.md` L102「标签: (B) 弱同族」
- D003 FOE 前馈化：decisions.md D003 L109-153 + `_architecture_decision.md` L80-89
- G(0)=0.132142：`_b7_map_results.json` L17 `0.13214186192586033` bit-exact

**本轮新发现 3 个关键事实**（影响 0.4-0.6 设计）：
1. `psa_foe_recovery` 概念错债务确认（`_recovery.py:435`，注释 L437 自承 pilot-aided 非谱不对称法）—— H003 债务描述精确
2. params.py `B7Params` 类（L606-680）有 4 问题：LEO_DOPPLER_RATE=30e3 错（B7 原文 ±100MHz@1GHz/s）/ 缺 5 个 poster 参数 / PSA_PILOT_SPACING 概念错遗留 / source 没引行号
3. 符号率/线宽场景差异需用户拍板（B7 25GBaud/1.8kHz vs NDA-ML 2.5GBaud/10kHz）

### 阶段 0.4 公平对照框架（用户决策后落盘）

用户拍板两个关键决策（AskUserQuestion）：
- 工作点：**BER 2e-2 + HD-FEC 双工作点**（HD-FEC 主判据跨候选可比 + BER 2e-2 锚论文一致性校验）
- 场景参数：**B7 锚论文原参数 25GBaud/1.8kHz**（不跟 NDA-ML 统一，防 D-007 覆辙）

**fair gain 定义**（跟 NDA-ML 不同维度，不照搬）：
- NDA-ML fair gain = BER gain @ HD-FEC（pilot overhead 1.25dB 代价维度）
- B7 fair gain = **二维报告**：BER gain @ 双工作点（HD-FEC 主 + BER 2e-2 锚）+ Doppler 范围比（1.9×）
- 理由：B7 vs PSA FOE 无 pilot overhead 差异（都盲前馈 FOE），增量半在 BER gain（0.6dB）半在范围（1.9×），单一指标丢信息

**PSA FOE baseline 债务登记**：sandbox 必须重写谱不对称法（Vieira 2023），不用旧 pilot-aided `psa_foe_recovery`。

**TL-20 理论预期表**落盘（`_fair_comparison_framework.md` §5）：BER gain @ BER 2e-2 预期 +0.4~0.8dB，@ HD-FEC 预期 +0.3~0.7dB，range_ratio 预期 ≈1.9×。

输出：`_fair_comparison_framework.md`（8 节）。

### 阶段 0.5 参数真相源（V6 读原文数值）

**B7Params 修正版草稿**（15 字段，在 explore 草拟不回写 params.py，守 INVARIANT 6）：
- 14 OK + 1 WARNING（GARDNER_GAIN 典型值）
- 所有 literature 字段 source 精确到 content.md 行号（L21/L25/L47/L49/L65/L69）
- 修正 LEO_DOPPLER_RATE（30e3 错 → 1e9 Hz/s）
- 删 PSA_PILOT_SPACING（概念错）
- 补 7 新字段：R_SYM_B7 / LASER_LW_B7 / ROLL_OFF / RX_BW_GHZ / SPS_RX / DOPPLER_INTERVAL / LEO_DOPPLER_EXCURSION

**符号率/线宽场景不统一**（用户决策 + D-007 教训）：B7 用锚论文原参数，复现 0.6dB 增量必须用 B7 场景。跨候选可比走 fair gain 维度（都报 HD-FEC）不走场景参数统一。

**下游引用同步清单**（D-007 教训 2）：5 文件核查，4 无需改 + 1 sandbox 重写（psa_foe_recovery）。

### 阶段 0.6 文件组织

explore 目录结构落盘：阶段 0 产出 8 文件（含本轮 2 新建 `_fair_comparison_framework.md` + `_stage0_5_6_params_files.md`）+ sandbox/MVE 待建 6 文件命名规约（`_crb_lower_bound.py` / `_ted_gain_analytic.py` / `_psa_foe_asymmetry.py` / `b7_gardner_ted_mve.py` / `B7-MVE-SPEC.md` / `_mve_results.json`）。

跟 NDA-ML 文件组织对照（防 E 类混乱）：单 explore/b7-gardner-ted-foe/ 目录 + 单 B7Params 真相源 + 单 _mve_results.json。

输出：`_stage0_5_6_params_files.md`（5 节）。

### 阶段 0.4-0.6 判定（D004+D005）

通过。**阶段 0 六项规约全部完成**（0.1 公式完整性 D001 / 0.2 数学同族性 D002 / 0.3 架构定性 D003 / 0.4 公平对照框架 D004 / 0.5 参数真相源 D005 / 0.6 文件组织 D005）。profile 第 9 次防线解除，可进 sandbox。

## 决策引用

- **D004**（新建）：B7 fair gain = 二维报告（BER gain @ 双工作点 + 范围比）+ PSA FOE baseline 必须重写
- **D005**（新建）：B7Params 修正版 15 字段全溯源 + B7 锚论文原参数不统一 + explore 目录结构落盘
- 无其他新建

## 范围确认

- 本轮是否在 scope boundary 内：**是**（0.4-0.6 是 H003 阶段 0 的项目）
- 未修改 params.py（阶段 0 不写代码，B7Params 草稿在 explore，守 INVARIANT 6）
- 未修改 common/_recovery.py（PSA FOE 概念错只登记债务，sandbox 重写）
- 未进 sandbox（守 profile 第 9 次防线——本轮做完才解除）

## 后续

1. **sandbox 阶段（下对话，profile 第 9 次防线已解除）**：
   - 第一步：B7Params 回写 params.py（`_stage0_5_6_params_files.md` §1.2 草稿）
   - 第二步：PSA FOE baseline 重写（谱不对称法 Vieira 2023，新写 `_psa_foe_asymmetry.py`）
   - 第三步：B7 TED_gain(f_D) 解析推导 + Leven 对比（残留风险闭合，`_ted_gain_analytic.py`）
   - 第四步：CRB 下界（FR-21 参考，`_crb_lower_bound.py`）
   - 第五步：三方对照（B7 proposed / Gardner 1986 TR / PSA FOE）
   - 第六步：MVE + consistency（B7-MVE-SPEC.md 契约 + b7_gardner_ted_mve.py + TL-20 理论预期表）
2. **残留风险带进 sandbox**：B7 TED_gain(f_D) 解析式缺失（V3 残留风险），sandbox 前补解析推导 + Leven 对比
3. **守 sim-preflight v1.3.0**：C6 公式核对 / C7 三方对照 / C8 祖师爷警报 / V1-V6
4. **环境注意**：本机无 `~/.venvs/torch/`，用 `python`（scoop python311，numpy/scipy/mpl 齐全）

### 已知风险

- B7 0.6dB @ BER 2e-2 在 HD-FEC 处的增量是外推（poster 未测 HD-FEC），sandbox 需测并论证
- PSA FOE baseline 重写需 Vieira 2023 [5] 谱不对称法具体实现（poster 只描述机制未给公式，需查 Vieira 2023 IEEE Access 原文）
- B7Params 回写 params.py 后需同步检查 explore/b7-gardner-ted-foe/_b7_map_reconstruction.py（0.2a 硬编码 25GBaud，sandbox 改成 import B7Params）
