# 场景 A：跑已有实验 / 改参数 / 复现结果

> ⚠️ **CRITICAL 参数真实路径**（必须从 params.py grep 验证，不是凭记忆）：
> - `cfg.kf.q_params_weak.sigma2_turb` = 1e-6
> - `cfg.kf.q_params_moderate.sigma2_turb` = 1e-4
> - `cfg.kf.q_params_strong.sigma2_turb` = 1e-3
> 全部 `source="NO VERIFIED SOURCE"`（CRITICAL 待推导）

## 读（开始前必读，按顺序）

1. **`projects/simulation/params.py`** — 跑 `audit_params()`，确认相关参数无未解决 CRITICAL
2. **`毕设/CONCLUSIONS.md`** — 找到相关结论，确认安全等级 ≥ ⚠️ 需限定
3. **`毕设/formulas-master.md`** — 取对应公式，不从 archive 或子文件取

**关键**：读完把条目抄到工作笔记（M1 管道断裂防护）。格式：

```
{文件:行号} | {指标}={值} {单位} | {安全等级} | {限定条件}
```

**用户口述值与真相源不符时**：先 grep 真相源（params.py / CONCLUSIONS.md），如发现不符 → **中断**（参见 `rules/interrupt.md` 第 8 条），向用户澄清。

## 守（执行时）

- 信道必须用 `generate_shared_realization()`，禁止各方法独立生成信道（TL-13 根因：P-05 假增益就是这么来的）
- 结果必须用 `common._experiment.save_results()`，禁止裸 `json.dump`（CP-4 元数据自动注入）
- 跑完过 `red_flags.py` 9 条规则（`SIM_CHECKPOINTS=1` 启用 CP-1~4）
- 执行开头先核对：工作笔记里的限定条件是否仍然适用
- **目标脚本必须存在**：用户引用脚本名时，先 `ls projects/simulation/experiments/{name}.py` 验证；不存在 → 反问用户"是否指 {最接近的脚本}"

## 改（结束后必更新）

1. **`results/{name}.json`** — `save_results` 自动生成
2. **`毕设/CONCLUSIONS.md`** — 如有新结论，先查代码来源标签（`[common.py]`/`[纯理论]`/`[旧代码]`），再定安全等级
3. **handoff"约定变更"段** — 如有约定变更（参数值/公式形式）必须记录（最高频丢失类型，详见 `rules/doc-discipline.md`）
4. **写使用日志**（见 `rules/usage-log.md`）：
   ```
   [YYYY-MM-DD HH:MM] 场景=A | 任务="..." | routing=correct | interrupts=[] | self-check=none | changes=[...] | issues="..." | duration=2min
   ```

## 特例：修改 CRITICAL 参数流程

CRITICAL 参数（`sigma2_turb`×3、`Q_fine_df`）修改前必须先写来源推导：

1. 在 `.sessions/{专题}/decisions.md` 写一条 D###：
   - 参数名 + **params.py 真实旧值**（grep 验证，不是用户口述）+ 新值
   - 来源推导（Rytov 相位结构函数 / GG 闪烁指数 / 文献引用）
   - 影响范围（哪些结论会变）
2. 推导经用户确认后，改 `params.py` 的 `default_factory`（不要新建 lambda，直接修改原 lambda 里的数值 + 同时把 `source_type` 改为 `derived` 或 `literature`，并写 `source`/`derivation`）
3. `audit_params()` 重新跑，CRITICAL → WARNING
4. handoff"约定变更"段强制记录

详见 `rules/constraints.md` 的 AuditFlag 四级行动。
