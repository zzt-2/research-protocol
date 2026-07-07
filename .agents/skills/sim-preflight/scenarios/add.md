# 场景 B：加新算法 / 新模块 / 新参数

> ⚠️ 本文件模板字段名（`audit_flag`）必须与 `params.py` 真实写法一致。任何修改后必须跑校验命令。

## 读（设计前必读）

1. **`projects/simulation/DESIGN-modular-split.md`** — 模块结构，确认新算法该放哪个 `_xxx.py`
2. **`projects/simulation/tests/INTEGRATION_PLAN.md`** — 分层验证 6 步协议
3. **`毕设/formulas-master.md`** 对应章 — 取算法公式，确认编号
4. **`projects/simulation/params.py`** — 新参数必须加 Pydantic 字段 + `json_schema_extra` 溯源

## 加新算法前先 grep 确认是否已存在

```bash
# 检查算法是否已部分实现
grep -rn "{算法名}\|{Params类名}" projects/simulation/ 毕设/CONCLUSIONS.md 毕设/formulas-master.md
```

按结果选流程：

| grep 结果 | 流程 |
|----------|------|
| params.py 有 XParams + CONCLUSIONS.md 有 X 数据 + common/_x.py 存在 | **算法已完整实现**——不重做，按场景 A 跑实验 |
| params.py 有 XParams + CONCLUSIONS.md 有 X 数据 + common/_x.py 不存在 | **算法部分实现**——走"模块化合并"子流程（把散落在 experiments/ 的 X 代码合并进 common/_x.py，0 改动现有逻辑） |
| params.py 有 XParams + 其他全无 | **算法未实现但参数已占位**——走"实现模块化"子流程（新建 common/_x.py + 新测试 + 写 CONCLUSIONS） |
| 全无 | 走"新算法"主流程（下方） |

## 守（实现时）

- **新算法 = 1 个新文件**（加到 `common/_xxx.py` 或 `experiments/`）+ **0 改动现有代码**
- 新算法必须跑**分层验证相关步骤**（见下方算法适配矩阵）
- 新参数必须标 `AuditFlag`（OK/WARNING/CRITICAL/DEAD），CRITICAL 需写来源推导
- `sigma2_turb` 相关：若用到湍流方差，必须从 Rytov 相位结构函数或 GG 闪烁指数反推（双推导路径，见 S002）

## 改（实现后必更新）

1. **`毕设/formulas-master.md`** — 新公式追加到对应章末尾（注意 2500 行上限，超限先看 `rules/archive.md`）
2. **`毕设/CONCLUSIONS.md`** — 新结论带代码来源标签 + 安全等级
3. **`projects/simulation/params.py`** — 新参数 + 审计标记
4. **`projects/simulation/tests/`** — 新测试加到 `test_common.py` 或 `test_layered_verification.py`
5. **handoff"约定变更"段** — 如有约定变更必须记录
6. **写使用日志**（见 `rules/usage-log.md`）：场景=B | 任务=... | routing=... | issues=...

## 分层验证算法适配矩阵

6 步协议（`tests/test_layered_verification.py`）是为 VV/DPLL 设计的。新算法按矩阵选必跑步骤：

| 算法类型 | 1.AWGN BER | 2.GG 统计 | 3.衰落 BER | 4.VV 方差 | 5.DPLL 方差 | 6.端到端 |
|---------|-----------|----------|-----------|----------|------------|---------|
| VV | ✓ | ✓ | ✓ | ✓ | - | ✓ |
| DPLL | ✓ | ✓ | ✓ | - | ✓ | ✓ |
| BPS | ✓ | ✓ | ✓ | 替换为 BPS 方差 | - | ✓ |
| KF | ✓ | ✓ | ✓ | 替换为 KF 方差 | - | ✓ |
| 均衡器 | ✓ | ✓ | ✓ | - | - | ✓ |

"替换为 X 方差"：参照 `tests/test_layered_verification.py` 的 `test_step4_vv_phase_variance` 写法，理论值改为该算法的 CRLB 或文献参考。

新算法不在表内 → 必须先在本文档加一行（标明步骤适配理由），再实现。

## 新参数添加模板（嵌套子模型，字段名以 params.py 为准）

```python
# params.py 中添加
# 字段名约定：json_schema_extra 内必须是 "audit_flag"（不是 "audit"）
# 子模型示例：在 SystemParams（或对应子模型）内加字段

class SystemParams(BaseModel):
    new_param: float = Field(
        default=1.0,
        json_schema_extra={
            "audit_flag": AuditFlag.WARNING,   # 必须：OK/WARNING/CRITICAL/DEAD
            "source_type": SourceType.literature,  # assumption/literature/derived/measured
            "source": "文献 X 公式 Y",          # 来源引用
            "symbol": "NF",                    # 符号（可选）
            "unit": "dB",                      # 单位（dB/Hz/线性/无单位）
            "derivation": "...",               # CRITICAL 必填：推导步骤
        }
    )
```

### dB vs 线性单位决策

| 参数类别 | 存储单位 | 例 |
|---------|---------|-----|
| SNR / 信号功率类 | 线性（用于计算） | `gamma_bar=100.0`（=20dB） |
| 噪声系数 / 损耗（输入是 dB） | 存 dB + 加 `unit="dB"` + 代码用前转线性 | `noise_figure=3.0` |
| 频率 / 角频率 | Hz 或 rad/s，明确 `unit` 字段 | `omega_n=8e6` (rad/s) |

规则：**计算时用线性，存储可存 dB 但必须 `unit="dB"`**。代码读取后立即 `10**(x/10)` 转线性。

### 孤儿参数 AuditFlag 默认值

加了字段但暂无代码使用 → 标 `AuditFlag.DEAD`（不是 WARNING）。代码接入后改回 WARNING/OK。

## 校验命令（写完新字段必跑）

```bash
cd projects/simulation && ~/.venvs/torch/bin/python -c "
from params import SimulationConfig, audit_params
r = audit_params(SimulationConfig())
# 验证新字段被识别：WARNING/CRITICAL 计数应 +1（或 DEAD 计数 +1）
print(r['summary'])
"
# 如新字段未在对应级别计数 +1 → 字段名错（audit_flag 不是 audit）
```
