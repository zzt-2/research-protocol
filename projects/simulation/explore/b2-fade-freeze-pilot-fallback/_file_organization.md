# 阶段 0.6：文件组织规约（目录结构 + 命名规则 + 下游引用同步清单）

> 专题: 2026-07-08-b2-fade-freeze-pilot-fallback | 阶段: 0.6
> 日期: 2026-07-08
> 守: NDA-ML D-007 教训 2（多 results 目录并存 + 下游引用没清理）+ INVARIANT（不污染 common，explore 探针不进 experiments）+ TL-13（共用信道）

## 0. 目标

定死 `explore/b2-fade-freeze-pilot-fallback/` 目录结构 + 命名规则，防 NDA-ML D-007 文件混乱重蹈（MVE 薄包装 + 双套参数共存 + 两 results 目录）。

## 1. 目录结构（B2-Q2 专属）

```
projects/simulation/explore/b2-fade-freeze-pilot-fallback/
├── _step4a_detail_extract.md        # 阶段 0.1 输入：子 agent 核查 step4a 实测细节（✅ 已存在）
├── _tension_validation_design.md    # 阶段 0.1 产出：张力验证设计 4 维度分解（✅ 已存在）
├── _db_sourcing_audit.md            # 阶段 0.2 产出：dB 溯源核查（✅ 已存在）
├── _architecture_decision.md        # 阶段 0.3 产出：架构定性（前馈化不撞 D006）（✅ 已存在）
├── _fair_comparison_framework.md    # 阶段 0.4 产出：公平对照框架（✅ 已存在）
├── _param_truth_source.md           # 阶段 0.5 产出：参数真相源（✅ 已存在）
├── _file_organization.md            # 阶段 0.6 产出：本文件（✅ 已存在）
├── _b2_params_draft.py              # 阶段 0.5 B2Params 草稿（待落盘，sandbox 前）
│
├── _sandbox_three_way.py            # 阶段 1 sandbox 三方对照脚本（待写）
├── _sandbox_results.json            # sandbox 结果（待写）
├── _gamma_th_sweep.json             # γ_th 敏感性扫描结果（待写）
├── _rho_fade_measure.json           # ρ_fade 实测结果（待写）
│
├── B2-Q2-MVE-SPEC.md                # 阶段 2 MVE 契约（sandbox 通过后写，正式文件无 _ 前缀）
├── b2q2_mve.py                      # 阶段 3 MVE 脚本（MVE SPEC 通过后写，正式文件无 _ 前缀）
└── _mve_results.json                # MVE 结果（待写）
```

## 2. 命名规则（强制）

### 2.1 私有文件 `_` 前缀（诊断/核查/草稿/探针）

| 文件类型 | 命名 | 例子 |
|---|---|---|
| 阶段 0 规约产出 | `_{阶段简名}.md` | `_tension_validation_design.md` / `_db_sourcing_audit.md` |
| 子 agent 核查产出 | `_{核查对象}_extract.md` | `_step4a_detail_extract.md` |
| sandbox 探针脚本 | `_{实验名}.py` | `_sandbox_three_way.py` |
| sandbox 探针结果 | `_{实验名}_results.json` | `_sandbox_results.json` |
| 参数草稿 | `_{参数类}_draft.py` | `_b2_params_draft.py` |

**私有文件含义**：MVE 通过前都是探针/草稿，不进 experiments/，不进 common/。MVE 通过后才转正。

### 2.2 正式文件无 `_` 前缀（SPEC / MVE 主脚本）

| 文件类型 | 命名 | 例子 |
|---|---|---|
| MVE 契约 | `{候选名}-MVE-SPEC.md` | `B2-Q2-MVE-SPEC.md`（待写，sandbox 通过后）|
| MVE 主脚本 | `{候选名小写}_mve.py` | `b2q2_mve.py`（待写，MVE SPEC 通过后）|

### 2.3 禁止的命名（NDA-ML D-007 教训）

- ❌ `sc_nda_ml_main_improved.py`（"improved" 后缀，D-007 教训：旧版新版并存混乱）
- ❌ `b2q2_mve_v2.py` / `b2q2_mve_v3.py`（版本号后缀，应直接改原文件）
- ❌ `results/` 子目录（所有结果 JSON 平铺在 explore 目录，不建子目录）
- ❌ `results_backup/` / `results_old/`（备份目录，D-007 教训：旧目录不清引下游误用）

## 3. 下游引用同步清单（D-007 教训 2）

### 3.1 参数变更触发下游清理（NDA-ML D-007 教训）

**NDA-ML D-007 发现**：参数真相源统一后（LASER_LW 500kHz→10kHz），下游引用没清理——`sc_nda_ml_main`（新）和 `sc_nda_ml_main_improved`（旧）两目录并存，`run_sdfec_eval.py` / `run_uplink_experiment.py` 仍引用旧目录 → 跑 SD-FEC 会用旧 +1.483 数据得出错结论。

**B2-Q2 防御**：每次参数变更（如 γ_th 从扫描值定到最优值），必须同步清理：
1. explore/ 目录内所有引用该参数的脚本
2. results JSON 的 meta 字段（记录参数值，方便核查）
3. decisions.md 记一笔"参数变更 + 下游清理完成"

### 3.2 B2-Q2 下游引用清单（sandbox 阶段 1 维护）

| 引用点 | 引用什么 | 同步时机 |
|---|---|---|
| `_sandbox_three_way.py` | B2Params（γ_th / ρ_fade / 估计器选择）| γ_th 变更时 |
| `_sandbox_results.json` meta | 参数值（γ_th / ρ_fade / OSNR / 湍流档）| 每次跑 sandbox |
| `_gamma_th_sweep.json` | γ_th 扫描值 + 对应 ρ_fade / fair gain | γ_th 扫描后 |
| `B2-Q2-MVE-SPEC.md` | sandbox 结论 + 定稿参数 | sandbox 通过后写 |

### 3.3 results JSON meta 字段强制（D-007 教训）

**所有 results JSON 必须含 meta 字段**（仿 step4a `_time_domain_crlb.py:592-597`）：
```json
{
  "meta": {
    "candidate": "B2-Q2",
    "stage": "sandbox",
    "timestamp": "2026-07-XX",
    "params": {
      "LASER_LW": 10000,
      "R_SYM": 2.5e9,
      "DA_PILOT_SPACING": 4,
      "N_DFT": 256,
      "CH_BLOCK": 100,
      "N_BLOCKS": 400,
      "GAMMA_TH": "<sweep values>",
      "BLIND_ESTIMATOR": "fft_foe",
      "PILOT_ESTIMATOR": "da_ml"
    },
    "source": "explore/b2-fade-freeze-pilot-fallback/_sandbox_three_way.py"
  },
  "results": { ... }
}
```

## 4. common 污染防御（INVARIANT）

### 4.1 explore 探针不进 common

- B2-Q2 sandbox 脚本（`_sandbox_three_way.py`）放 `explore/b2-fade-freeze-pilot-fallback/`
- **不修改** `common/_recovery.py`（4 估计器已具备，只需 import）
- **不修改** `common/_channel.py`（TL-13 共用信道，只 import）
- **不新增** `common/` 下任何 B2 专属文件

### 4.2 MVE 通过才转正

- MVE 通过（阶段 3 Go 判定）前，所有 B2-Q2 代码在 explore/
- MVE 通过后，才把 B2-Q2 双模切换逻辑转正到 `experiments/`（如果需要）
- **转正决策由主控对话定**（工作对话不擅自转正）

## 5. 阶段 0.6 结论

**文件组织规约完成**：
- 目录结构定死（私有 `_` 前缀 + 正式无前缀）
- 命名规则强制（禁 "improved"/版本号/备份目录）
- 下游引用同步清单建立（参数变更触发清理 + results JSON meta 强制）
- common 污染防御（explore 不进 common，MVE 通过才转正）

**阶段 0 六项规约全部完成**，可进阶段 1 sandbox 三方对照（下一对话）。

## 6. 阶段 0 六项规约完成度总览

| 阶段 | 产出文件 | 状态 | 核心结论 |
|---|---|---|---|
| 0.1 张力验证设计 | `_tension_validation_design.md` | ✅ | 张力可分解 4 维度，不直接 Kill，增量在动态恢复时间 |
| 0.2 dB 溯源核查 | `_db_sourcing_audit.md` | ✅ | sat.1553 +1dB 限定到 PE vs VV+diff，B2-Q2 不能搬 |
| 0.3 架构定性 | `_architecture_decision.md` | ✅ | 前馈化不撞 D006（INVARIANT 级）|
| 0.4 公平对照框架 | `_fair_comparison_framework.md` | ✅ | baseline=纯 blind freeze[79]，双测度+摊薄+多维够格 |
| 0.5 参数真相源 | `_param_truth_source.md` | ✅ | σ²_pN vs GG α/β 严格区分，ref[58]=Martins dual-stage 修正叙事 |
| 0.6 文件组织 | `_file_organization.md` | ✅ | 目录结构+命名+下游同步+common 防御 |

**守 profile 第 9 次"急于推进"防线**：阶段 0 六项规约全做完才进 sandbox，本轮全部完成（用户授权继续后一次做完）。
