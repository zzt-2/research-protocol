# C5: 综合迁移方案

> 2026-06-12 | 方案设计 | 综合 C1/C2/C3/C4/C6/A4 所有迁移需求
> 约束: 增量迁移、27 脚本全程可运行、每个阶段可验证可回滚

---

## 0. 迁移全景

### 0.1 迁移范围汇总

| 方案 | 核心变更 | 新建文件 | 修改文件 | 预计行数 |
|------|---------|---------|---------|---------|
| C1 代码模块化 | common.py → common/ 包（7 模块 + __init__.py） | 8 | 1（删除 common.py） | ~970 |
| C2 参数溯源 | 新建 params.py（Pydantic 模型 + 审计 + SPEC 生成） | 1 + 1 测试 | 1（common.py 垫片） | ~420 |
| C3 验证集成 | conftest/checkpoints/分层验证 | 3 | 2（test_common.py 微调、save_results +3 行） | ~240 |
| C4 文档架构 | 注册表清理 + 公式去冗余 + 成熟度标签 + ROT 基线 | 0 | ~15 文档文件 | ~0 净增（去冗余为主） |
| C6 Handoff | 模板更新 + topic-index 分区 + 状态漂移检测 | 0 | 2（CLAUDE.md、session-governance） | ~50 |

### 0.2 关键依赖关系图

```
Phase 0: 安全网（git branch + 基线验证）
    │
    ├── Phase 1: C4 注册表清理（独立，5 分钟）
    │
    ├── Phase 2: C3 验证基础设施（独立于 C1/C2）
    │       ↓
    │   Phase 3: C2 参数溯源（params.py + common.py 垫片）
    │       ↓       （C2 依赖 C3 的测试验证参数改动不破坏功能）
    │   Phase 4: C1 代码模块化（common.py → common/ 包）
    │       ↓       （C1 在 C2 之后，因为 C2 的垫片策略需要先确认
    │                common.py 常量来源已迁移到 params.py）
    │   Phase 5: C3 分层验证测试 + checkpoints 集成
    │       ↓       （依赖 C1 完成后的模块结构）
    │
    ├── Phase 6: C4 文档去冗余 + 成熟度标签（可与 Phase 3-5 并行）
    │
    └── Phase 7: C6 Handoff 模板 + session-governance 更新
            ↓
        Phase 8: 全量验证 + 收尾
```

**并行机会**：
- Phase 1（C4 注册表清理）与 Phase 2（C3 基础设施）可完全并行
- Phase 6（C4 文档去冗余）与 Phase 3-5（代码侧）可完全并行
- Phase 7（C6 模板更新）可与任何阶段并行

---

## 1. Phase 0: 安全网（10 分钟）

### 1.1 创建工作分支

```bash
cd /mnt/d/code/study/research-protocol
git checkout -b feat/simulation-foundation-rebuild
```

### 1.2 基线验证

```bash
cd projects/simulation

# 1. 确认所有测试通过
~/.venvs/torch/bin/python -m pytest tests/test_common.py -v
# 预期: 69 passed, ~9.69s

# 2. 确认 common.py 导入正常
~/.venvs/torch/bin/python -c "from common import *; print('OK')"

# 3. 确认一个实验脚本能跑
~/.venvs/torch/bin/python -c "
from common import generate_shared_realization, run_fixed, resolve_qpsk
d = generate_shared_realization(1000, 100, 'strong', 150e6, seed=42)
rx = run_fixed(d)
ber = resolve_qpsk(rx, d['bits'])
print(f'Baseline BER = {ber:.6f}')
"
```

### 1.3 记录基线数字

将上面第 3 步的 BER 值和测试结果记录下来，作为后续每步验证的对照。

**验证标准**: 69 测试全通过 + 实验脚本输出正常 BER 值
**回退策略**: `git checkout main`（未做任何修改）

---

## 2. Phase 1: C4 注册表清理（5 分钟）

**依赖**: 无
**与什么并行**: 可与 Phase 2 完全并行

### 2.1 执行步骤

编辑 `.sessions/_registry.yaml`：

**P0 级修正（9 个状态错误）**：
- framework-evolution: active → closed
- direction-scouting: active → closed
- thesis-structure-research: active → closed
- chapter-quality-audit: active → closed
- thesis-chapter-fixes: active → closed
- 2026-05-13-mega-constellation-gnn-routing: dormant → closed
- 2026-05-13-hgat-satellite-dag-offloading: dormant → closed
- 2026-05-13-ris-phase-drl: dormant → closed
- 2026-05-17-leo-congestion-routing: dormant → closed

**P1 级修正**：
- thesis-direction-pivot: active → dormant
- thesis-sim-exploration: active → dormant
- thesis-simulation-consolidation: active → dormant
- 2026-05-30-ch3-direction-exploration: active → dormant
- 2026-06-04-advisor-review-revision: active → dormant

**其他修正**：
- 修复 thesis-chapter-fixes 重复 depends_on 键（合并为数组）
- 3 个未注册目录补注册（2026-05-31-thesis-writing-prep, 2026-05-31-thesis-writing, 2026-06-04-citation-verification）
- 为所有条目添加 `maturity` 字段

### 2.2 验证

```bash
# YAML 语法检查
python3 -c "import yaml; yaml.safe_load(open('.sessions/_registry.yaml')); print('YAML OK')"
```

**验证标准**: YAML 合法，所有 closed 专题的 status 为 closed
**回退策略**: `git checkout .sessions/_registry.yaml`

---

## 3. Phase 2: C3 验证基础设施（15 分钟）

**依赖**: Phase 0
**与什么并行**: 可与 Phase 1 并行

### 3.1 创建 conftest.py

文件: `projects/simulation/tests/conftest.py`

```python
"""测试共享配置"""
import sys, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SIM_DIR = os.path.dirname(SCRIPT_DIR)
if SIM_DIR not in sys.path:
    sys.path.insert(0, SIM_DIR)
```

### 3.2 修改 test_common.py

删除 test_common.py 头部的 sys.path 设置代码（约 4 行），改为依赖 conftest.py。

### 3.3 验证

```bash
cd projects/simulation
~/.venvs/torch/bin/python -m pytest tests/test_common.py -v
# 预期: 69 passed
```

**验证标准**: 测试结果与基线完全一致
**回退策略**: `git checkout projects/simulation/tests/test_common.py`

---

## 4. Phase 3: C2 参数溯源（30 分钟）

**依赖**: Phase 2（测试基础设施就绪）
**与什么并行**: 可与 Phase 6 并行

### 4.1 创建 params.py

文件: `projects/simulation/params.py`（~300 行）

包含：
- SourceType, AuditFlag 枚举
- 8 个 Pydantic BaseModel: SystemParams, TurbulenceParams, DopplerParams, KFParams (含 KFQParams), FixedCfgParams (对应 DPLLParams+FOEParams+VVParams), BPSParams, ExperimentParams
- SimulationConfig 聚合配置
- design_Q() 方法
- audit_params() 审计函数
- generate_spec_md() SPEC 生成函数

关键注意事项：
- Pydantic 需要安装: `~/.venvs/torch/bin/pip install pydantic -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple`
- 所有模型的 `Config.frozen = True`
- SimulationConfig 提供兼容方法: get_turb_dict(), get_fixed_cfg(), get_fixed_cfg_optimal(), get_q_turb_params()

### 4.2 修改 common.py 垫片

在 common.py 顶部添加（替换硬编码常量）：

```python
from params import SimulationConfig
_CFG = SimulationConfig()

R_SYM = _CFG.system.R_SYM
T_S = _CFG.system.T_S
# ... 其余常量同理 ...
TURB = _CFG.get_turb_dict()
FIXED_CFG = _CFG.get_fixed_cfg()
FIXED_CFG_OPTIMAL = _CFG.get_fixed_cfg_optimal()
Q_TURB_PARAMS = _CFG.get_q_turb_params()
```

**关键**: 所有函数实现不变。函数内部引用的模块级常量（如 T_S, BLOCK）已经从 _CFG 导出，行为完全一致。

### 4.3 添加 params 审计测试

文件: `projects/simulation/tests/test_params.py`（~80 行）

包含 TestParamAudit:
- test_no_critical_params（初期 @pytest.mark.xfail，sigma2_turb 仍为 CRITICAL）
- test_no_dead_params（初期 @pytest.mark.xfail，kappa 仍为 DEAD）
- test_all_params_have_source
- test_frozen_config

### 4.4 验证

```bash
cd projects/simulation

# 1. params.py 导入测试
~/.venvs/torch/bin/python -c "from params import SimulationConfig; c = SimulationConfig(); print(c.system.R_SYM)"

# 2. 常量值不变
~/.venvs/torch/bin/python -c "from common import R_SYM, T_S, TURB, BLOCK; print(R_SYM, T_S, BLOCK, TURB['strong'])"

# 3. 全部测试通过（参数值不变 = T7 测试应逐项通过）
~/.venvs/torch/bin/python -m pytest tests/ -v

# 4. 实验脚本 BER 不变
~/.venvs/torch/bin/python -c "
from common import generate_shared_realization, run_fixed, resolve_qpsk
d = generate_shared_realization(1000, 100, 'strong', 150e6, seed=42)
rx = run_fixed(d)
ber = resolve_qpsk(rx, d['bits'])
print(f'BER = {ber:.6f}')  # 应与基线完全一致
"
```

**验证标准**: 69 + 4(新增) 测试通过，BER 值与基线完全一致
**回退策略**: `git checkout projects/simulation/common.py`

### 4.5 快速见效项（5 分钟内）

如果时间紧张，Phase 3 可以只做 params.py 的骨架（不含完整 Pydantic 模型），common.py 垫片暂不改。params.py 作为"参数来源文档"先行存在，垫片改造后续再做。这样零风险。

---

## 5. Phase 4: C1 代码模块化（40 分钟）

**依赖**: Phase 3（common.py 已从 params.py 导入常量）
**与什么并行**: 无（这是核心重构，需串行）

### 5.1 执行步骤（C1 方案的 12 步）

**Step 0**: 备份 common.py
```bash
cp common.py common.py.bak
```

**Step 1**: 创建 common/ 目录
```bash
mkdir -p common
```

**Step 2**: 创建 `_config.py`（~90 行）
- 从 common.py L29-64 提取全部常量
- 从 common.py L302 提取 SIGMA2_LASER
- 从 common.py L304-308 提取 Q_TURB_PARAMS
- 从 common.py L367-372 提取 PILOT_PATTERN
- 添加 SystemConfig, ScenarioConfig, FixedRecoveryConfig 三个 frozen dataclass

验证: `python -c "from common._config import R_SYM, TURB; print(R_SYM, TURB)"`

**Step 3**: 创建 `_modulation.py`（~110 行）
- 提取 qpsk_mod/demod, ber_count, resolve_qpsk, qam16_*, ber_eval, hard_decision

验证: `python -c "from common._modulation import qpsk_mod; print('OK')"`

**Step 4**: 创建 `_channel.py`（~100 行）
- 提取 gg_block, doppler_phase, generate_shared_realization

验证: `python -c "from common._channel import generate_shared_realization; d = generate_shared_realization(1000, 100, 'strong', 150e6); print(d['Ns'])"`

**Step 5**: 创建 `_recovery.py`（~280 行）
- 提取 fft_foe, dpll_track, dpll_track_dd, vv_cpr, bps_cpr, carrier_recovery_fixed

验证: `python -c "from common._recovery import vv_cpr, bps_cpr; print('OK')"`

**Step 6**: 创建 `_equalizer.py`（~50 行）
- 提取 amp_limit, mmse_equalize, equalize_oracle, equalize_hmed

验证: `python -c "from common._equalizer import equalize_oracle; print('OK')"`

**Step 7**: 创建 `_kf.py`（~220 行）
- 提取 design_Q, kf_unified, get_pilots, kf_oracle_recovery, kf_frame_h_recovery, kf_pilot_recovery

验证: `python -c "from common._kf import kf_unified; print('OK')"`

**Step 8**: 创建 `_experiment.py`（~120 行）
- 提取 insert_pilots, run_*, run_trial_shared, save_results, db_ratio

验证: `python -c "from common._experiment import run_trial_shared; print('OK')"`

**Step 9**: 创建 `__init__.py`（~50 行）
- C1 方案 §6 的完整重导出内容
- **注意 OUT 常量**: 需要 `os.path.dirname(os.path.dirname(...))` 两层（见 C1 附录 C）
- **注意 matplotlib.use('Agg')**: 放在 __init__.py 中

**Step 10**: 删除旧 common.py + 验证全部导入
```bash
rm common.py  # common/ 目录成为 common 包

# 验证 from common import * 仍然工作
~/.venvs/torch/bin/python -c "from common import *; print('OK')"
```

**Step 11**: 数值一致性验证
```bash
~/.venvs/torch/bin/python -c "
from common import generate_shared_realization, run_fixed, resolve_qpsk
d = generate_shared_realization(10000, 100, 'strong', 150e6, seed=42)
rx = run_fixed(d)
ber = resolve_qpsk(rx, d['bits'])
print(f'BER = {ber:.6f}')  # 应与基线完全一致
"
```

**Step 12**: 清理备份
```bash
rm common.py.bak
```

### 5.2 与 C2 params.py 的集成

模块化后，common/__init__.py 的常量来源有两种选择：

**选择 A（推荐）**: _config.py 直接从 params.py 导入
```python
# common/_config.py
from params import SimulationConfig
_CFG = SimulationConfig()
R_SYM = _CFG.system.R_SYM
# ...
```
这样 params.py 是唯一真相源，_config.py 是重导出层。

**选择 B**: _config.py 独立定义常量，params.py 也独立定义
这会造成两处定义，违反单一真相源原则。不推荐。

**选择**: Phase 3 已在 common.py 中建立 params.py 垫片。Phase 4 模块化时，_config.py 直接从 params.py 导入，__init__.py 从 _config.py 重导出。链路：

```
params.py (唯一真相源)
    ↑ _config.py (从 params 导出常量 + 定义 dataclass)
    ↑ __init__.py (从 _config 重导出常量 + 从其他模块重导出函数)
    ↑ 27 个实验脚本 (from common import *)
```

### 5.3 验证

```bash
cd projects/simulation

# 1. 全部测试
~/.venvs/torch/bin/python -m pytest tests/ -v

# 2. 全部实验脚本导入检查
for f in experiments/*.py; do
    echo "=== $f ==="
    ~/.venvs/torch/bin/python -c "
import importlib.util, sys, os
spec = importlib.util.spec_from_file_location('test', '$f')
" 2>&1 | head -3
done

# 3. 数值一致性
# 同 Step 11
```

**验证标准**: 全部测试通过 + BER 与基线完全一致 + 27 脚本无 ImportError
**回退策略**: `git checkout .` 恢复 common.py

---

## 6. Phase 5: C3 分层验证 + Checkpoints 集成（25 分钟）

**依赖**: Phase 4（模块化完成后才能在正确位置插入检查点）

### 6.1 创建 checkpoints.py

文件: `projects/simulation/tests/checkpoints.py`（~80 行）

包含 CP-1 (信道), CP-2 (载波恢复), CP-3 (BER 红旗), CP-4 (结果保存前) + cp4_save_scan()。

环境变量 SIM_CHECKPOINTS=1 启用，默认关闭零开销。

### 6.2 save_results 内 CP-4 集成

在 common/_experiment.py 的 save_results() 中，`data['_meta'] = ...` 之后添加 3 行元数据完整性检查。

### 6.3 创建分层验证测试

文件: `projects/simulation/tests/test_layered_verification.py`（~150 行）

B5 六步验证:
1. AWGN QPSK BER 理论值
2. Gamma-Gamma 信道统计
3. AWGN + 衰落 BER
4. VV 相位方差
5. DPLL 相位方差
6. 完整系统端到端

### 6.4 一个实验脚本集成示范

修改 experiments/multi_seed_sweep.py，添加 CP-1/CP-2/CP-3 调用。

### 6.5 验证

```bash
cd projects/simulation

# 1. 全部测试
~/.venvs/torch/bin/python -m pytest tests/ -v
# 预期: 69 (原有) + 4 (params) + 6 (分层) = 79 passed

# 2. checkpoints 功能验证
SIM_CHECKPOINTS=1 ~/.venvs/torch/bin/python experiments/multi_seed_sweep.py \
    --n-seeds 3 --n-symbols 1000 --methods DPLL \
    --turbulence strong --snr-min 20 --snr-max 20
```

**验证标准**: 全部测试通过 + checkpoints 无 CRITICAL 报错
**回退策略**: `git checkout projects/simulation/experiments/multi_seed_sweep.py`

---

## 7. Phase 6: C4 文档去冗余 + 成熟度标签（30 分钟）

**依赖**: 无（纯文档操作）
**与什么并行**: 可与 Phase 3-5 完全并行

### 7.1 公式文档去冗余

1. 从 `毕设/写作材料/formulas-ch3ch4-sync.md` 提取 32 条独有公式 → 追加到 `毕设/formulas-master.md` Ch4
2. 从 `毕设/写作材料/formulas-ch4-kf.md` 提取 13 条独有公式 → 追加到 `毕设/formulas-master.md` Ch4
3. 4 个冗余文件移入 `毕设/写作材料/archive/`
4. 重命名 `formulas-ch5-fpga.md` → `fpga-reference.md`
5. 刷新 `毕设/formulas-index.md`

### 7.2 附录 G 修正

编辑 `毕设/CONCLUSIONS.md`：
- 升级 6 条结论安全等级
- 修正 3 处编号
- 补充 C4-13/C4-14/C4-15
- P-06 状态更新

### 7.3 成熟度标签

为 `毕设/` 下 ~15 个 md 文件头部添加 `<!-- maturity: XXX -->` 标签。

### 7.4 验证

```bash
# 公式编号连续性检查
grep -c "^## F" 毕设/formulas-master.md
# 确认无重复编号
```

**验证标准**: 无公式编号冲突，archive 文件已移入，成熟度标签正确
**回退策略**: `git checkout .` 恢复所有文档

---

## 8. Phase 7: C6 Handoff 模板更新（15 分钟）

**依赖**: 无
**与什么并行**: 可与 Phase 3-6 并行

### 8.1 更新全局 CLAUDE.md Handoff 模板

1. 添加"约定变更"段（在"已完成边界"和"不要做什么"之间）
2. "必读"段改为三级格式（恢复/执行/参考）
3. 添加大小指导注释
4. "接收方验证"精简为 3+3 格式

### 8.2 更新 topic-index 模板

添加"活跃区域/历史区域"分区设计。

### 8.3 session-governance skill 更新（如适用）

增加状态一致性检查和 YAML 结构校验。

### 8.4 验证

人工检查 CLAUDE.md 模板格式完整性。

**验证标准**: 模板包含所有新增段落，格式与 C6 附录一致
**回退策略**: `git checkout CLAUDE.md`

---

## 9. Phase 8: 全量验证 + 收尾（15 分钟）

**依赖**: Phase 1-7 全部完成

### 9.1 全量验证清单

```bash
cd /mnt/d/code/study/research-protocol/projects/simulation

# 1. 全部测试
~/.venvs/torch/bin/python -m pytest tests/ -v
# 预期: ~79 passed

# 2. 数值一致性（与 Phase 0 基线对照）
~/.venvs/torch/bin/python -c "
from common import generate_shared_realization, run_fixed, resolve_qpsk
d = generate_shared_realization(10000, 100, 'strong', 150e6, seed=42)
rx = run_fixed(d)
ber = resolve_qpsk(rx, d['bits'])
print(f'BER = {ber:.6f}')
"

# 3. params.py 审计
~/.venvs/torch/bin/python -c "
from params import SimulationConfig, audit_params
c = SimulationConfig()
report = audit_params(c)
print(f'Total: {report[\"summary\"][\"total\"]}')
print(f'OK: {report[\"summary\"][\"ok\"]}')
print(f'WARNING: {report[\"summary\"][\"warning\"]}')
print(f'CRITICAL: {report[\"summary\"][\"critical\"]}')
print(f'DEAD: {report[\"summary\"][\"dead\"]}')
"

# 4. YAML 合法性
python3 -c "import yaml; yaml.safe_load(open('.sessions/_registry.yaml')); print('YAML OK')"

# 5. 全部实验脚本导入检查
for f in experiments/*.py; do
    ~/.venvs/torch/bin/python -c "
import sys, os
sys.path.insert(0, '$(pwd)')
exec(open('$f').read().split('if __name__')[0])
" 2>&1 | head -1 && echo "OK: $f" || echo "FAIL: $f"
done
```

### 9.2 git 提交

```bash
git add -A
git status  # 确认变更清单
git commit -m "feat(simulation): infrastructure rebuild - C1-C6

C1: common.py modularized into 7 domain modules + __init__.py shim
C2: params.py parameter traceability with Pydantic models + audit
C3: verification integration (conftest, checkpoints, layered tests)
C4: registry cleanup (9 status fixes), formula dedup, maturity labels
C6: handoff template improvements (convention changes, tiered reading)"
```

---

## 10. 风险评估

### 10.1 27 脚本兼容性风险

| 风险 | 概率 | 影响 | 缓解 |
|------|------|------|------|
| __init__.py 遗漏某个名称 | 中 | 1-2 脚本 ImportError | C1 附录 A 已逐脚本审计，覆盖率 25/25 |
| OUT 常量指向错误路径 | 低 | 8 脚本输出路径错 | C1 附录 C 已明确两层 dirname |
| save_results 的 __file__ 变化 | 低 | 元数据中文件名变化 | __file__ 指向 __init__.py，行为一致 |
| qpsk_mod 跨模块调用断裂 | 极低 | generate_shared_realization 失败 | C1 唯一跨模块调用已明确标注 |

### 10.2 数据丢失风险

| 风险 | 概率 | 影响 | 缓解 |
|------|------|------|------|
| 公式迁移遗漏 | 低 | 丢失独有公式 | 提取前先 diff master vs 子文件 |
| 注册表误删条目 | 低 | 专题不可发现 | git 可恢复 |
| SPEC.md 参数值不一致 | 中 | 文档与代码矛盾 | C2 assert_spec_consistency 测试门控 |

### 10.3 时间估算

| 阶段 | 预计时间 | 累计 | 可中断点 |
|------|---------|------|---------|
| Phase 0: 安全网 | 10 min | 10 min | -- |
| Phase 1: C4 注册表清理 | 5 min | 15 min | Phase 1 后 |
| Phase 2: C3 conftest | 15 min | 30 min | Phase 2 后 |
| Phase 3: C2 参数溯源 | 30 min | 60 min | Step 1 后 |
| Phase 4: C1 代码模块化 | 40 min | 100 min | Step 1-8 每步后 |
| Phase 5: C3 分层验证 | 25 min | 125 min | 6.1/6.3 后 |
| Phase 6: C4 文档去冗余 | 30 min | 155 min | 7.1 后 |
| Phase 7: C6 模板更新 | 15 min | 170 min | 8.1 后 |
| Phase 8: 全量验证 | 15 min | 185 min | -- |
| **总计** | **~3 小时** | | |

**可拆分为 2-3 个对话**:
- 对话 1: Phase 0-3（1 小时 15 分钟）
- 对话 2: Phase 4-5（1 小时 5 分钟）
- 对话 3: Phase 6-8（1 小时）

---

## 11. 快速见效项（5 分钟内可完成）

以下项零风险、立即可做、对日常工作有直接改善：

| # | 项目 | 耗时 | 所属方案 | 收益 |
|---|------|------|---------|------|
| Q1 | _registry.yaml 9 个状态修正 | 3 min | C4 P0 | 消除恢复时读到过时信息 |
| Q2 | _registry.yaml maturity 字段添加 | 2 min | C4 | 为所有条目标记活跃度 |
| Q3 | common.py save_results +3 行元数据检查 | 1 min | C3 | 防止保存无元数据的结果 |
| Q4 | 创建 conftest.py | 2 min | C3 | 消除测试文件的重复路径设置 |
| Q5 | thesis-final-review 目录移入 _archive/ | 1 min | C4 | 清理活跃目录中的已归档专题 |

**建议**: 在开始正式迁移前，先完成 Q1-Q5。总耗时 <10 分钟，零风险。

---

## 12. 回滚方案

### 12.1 git 分支策略

```
main
  └── feat/simulation-foundation-rebuild  ← 所有改动在此分支
        ↓ 如果失败
      git checkout main  ← 立即回到安全状态
```

**不合并到 main 直到 Phase 8 全量验证通过。**

### 12.2 每阶段回滚命令

| 阶段 | 回滚命令 |
|------|---------|
| Phase 1 | `git checkout .sessions/_registry.yaml` |
| Phase 2 | `git checkout projects/simulation/tests/` |
| Phase 3 | `git checkout projects/simulation/common.py; git clean -f projects/simulation/params.py projects/simulation/tests/test_params.py` |
| Phase 4 | `git checkout projects/simulation/common.py; rm -rf projects/simulation/common/` |
| Phase 5 | `git checkout projects/simulation/tests/checkpoints.py projects/simulation/tests/test_layered_verification.py projects/simulation/experiments/multi_seed_sweep.py` |
| Phase 6 | `git checkout 毕设/` |
| Phase 7 | `git checkout CLAUDE.md` |
| 全部 | `git checkout main; git branch -D feat/simulation-foundation-rebuild` |

### 12.3 断点续接

如果迁移在某个 Phase 中断，从该 Phase 的验证步骤开始重新执行。验证通过则继续下一 Phase，失败则回滚本 Phase。

---

## 13. 执行顺序速查

```
Step 1:  git checkout -b feat/simulation-foundation-rebuild     [5 min]
Step 2:  跑基线测试 + 记录 BER                                   [5 min]
Step 3:  _registry.yaml P0/P1 修正 + maturity 字段              [5 min]
Step 4:  创建 conftest.py + 修改 test_common.py                 [10 min]
Step 5:  pip install pydantic + 创建 params.py                  [20 min]
Step 6:  修改 common.py 垫片（从 params.py 导出常量）            [10 min]
Step 7:  创建 test_params.py + 验证                              [10 min]
Step 8:  创建 common/ 包（7 模块 + __init__.py）                 [35 min]
Step 9:  删除 common.py + 全量导入验证                           [5 min]
Step 10: 创建 checkpoints.py + test_layered_verification.py     [15 min]
Step 11: multi_seed_sweep.py 集成示范                            [10 min]
Step 12: 公式去冗余 + 成熟度标签                                 [25 min]
Step 13: CLAUDE.md 模板更新                                      [15 min]
Step 14: 全量验证 + git commit                                   [15 min]
```

每步完成后运行对应验证命令，失败立即回滚本步。

---

## 设计决策记录

| 编号 | 决策 | 理由 | 替代方案 |
|------|------|------|---------|
| C5-D1 | params.py 先于 common/ 模块化 | 参数溯源先建立，模块化时直接从 params 导入 | 先模块化再溯源（垫片改两次） |
| C5-D2 | C4 注册表清理作为 Phase 1（最早执行） | 零风险、5 分钟、立即改善恢复体验 | 最后做（恢复成本持续到收尾） |
| C5-D3 | 文档去冗余与代码改动并行 | 纯文件操作，不依赖代码结构 | 串行（总时间更长） |
| C5-D4 | 快速见效项在正式迁移前做 | 建立信心、验证 git 流程 | 随各 Phase 分散做 |
| C5-D5 | 全部改动在 feat/ 分支 | 随时可回 main，不污染主线 | 直接在 main 上改（风险高） |
| C5-D6 | 分层验证测试放在模块化之后 | 依赖最终模块结构 | 放在模块化之前（需后续调整导入路径） |
