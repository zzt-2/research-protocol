# 遗漏中断 + 自检机制

## 中断清单（8 条）

执行任何仿真任务时，发现以下情况**立即中断**。每条配可执行检测命令。

### 1. 试图从 archive/ 或已删除的子文件取公式

```bash
grep -rn "_archive/\|formulas-ch[0-9]" 毕设/*.md projects/simulation/ --include="*.py" --include="*.md"
```

### 2. 试图硬编码参数值

**注意**：不白名单 params.py——`params.py` 内部 `default_factory=lambda: X(sigma2_turb=1e-6)` 也是硬编码（CRITICAL 参数尤其严重）。

```bash
# 检查 lambda default_factory 里硬编码 CRITICAL 参数
grep -rn "lambda.*sigma2_turb\s*=\s*[0-9]\|lambda.*kappa\s*=\s*[0-9]" projects/simulation/ --include="*.py"

# 检查 experiments/ 直接写数字（排除 params 导入）
grep -rn "R_SYM\s*=\s*[0-9]\|sigma2_turb\s*=\s*[0-9]" projects/simulation/experiments/ --include="*.py"
```

匹配 → 中断。CRITICAL 参数硬编码（包括 params.py 内部 lambda）必须先走"来源推导"流程（见 `scenarios/run.md` 特例段）。

### 3. 试图独立生成信道

```bash
grep -rn "np.random" projects/simulation/experiments/ --include="*.py"
```

如非诊断脚本且未调 `generate_shared_realization` → 中断

### 4. 试图裸 `json.dump` 保存结果

```bash
grep -rn "json.dump" projects/simulation/experiments/ --include="*.py" | grep -v "save_results"
```

### 5. 文档改动导致超限且未归档

```bash
wc -l 毕设/CONCLUSIONS.md 毕设/formulas-master.md 毕设/TERMS.md
# 任一超 limits（见 doc-discipline.md）→ 中断
```

### 6. 引用了 ❌ 不可写 或 🔄 待重验 的结论

```bash
grep -E "❌|🔄" 毕设/CONCLUSIONS.md | head -5
# 引用前核对该条目状态
```

### 7. 重复定义已有内容

```bash
# 改内容前 grep 是否已有定义
grep -rn "{要加的内容}" 毕设/*.md
```

如已存在于拥有者文件 → 中断

### 8. 指令模糊（无具体目标）

用户指令缺以下任一 → 中断反问：
- 算法名（VV/DPLL/BPS/KF/均衡器/无）
- 参数集（SNR/湍流强度/调制）
- 操作类型（跑/读/改/写）

无 grep，纯 agent 判断。中断后**显式反问用户**，不允许默认选择。

## 中断状态持久化（强制，F1/F2 压缩防护）

每次中断 → 双写：

**1. 在 `.sessions/{专题}/` 当前 session note（S###）追加一条**：

```
[中断] YYYY-MM-DD HH:MM | 类型={1-8} | 触发文件={path} | 修复尝试 N
```

**2. 在 `.sessions/sim-preflight-log/usage-{YYYY-MM}.md` 追加一行**（格式见 `usage-log.md`）：

```
[YYYY-MM-DD HH:MM] 场景=X | 任务="..." | routing=interrupted | interrupts=[类型 N] | self-check=pending | changes=[] | issues="中断原因简述" | duration=stuck
```

**截断规则**（P2 失败截断）：
- 同类型中断连续触发 **2 次** → 怀疑理解偏差，重读场景文件
- 同类型中断连续触发 **3 次** → 升级到 D### 决策，怀疑架构问题

**跨对话恢复**：新 agent 必须先 `grep "\[中断\]"` 读取最近 5 条（见 `scenarios/recover.md` Step 3）。

## 中断后流程

1. 停止当前任务
2. 在 session note + usage-log 双写中断记录（见上）
3. 派**外部 agent** 自检（不能自己修，不能派同源 agent）：
   - **主选**：`subagent_type: critic`（设计挑战型，独立审查视角）
   - **备选**：`subagent_type: verifier`（验证专家，独立证据收集）
   - **禁用**：`explore`（只读不能修）、`code-reviewer`、`executor`（三者都与主对话同源/同认知，复现 M5 自审自验失效）
4. 自检 agent 的 prompt 必须包含**反向假设**："假设这份产出有 3 个违规，找出最可能的 3 个"
5. 自检 agent 必须**独立跑更宽的 grep**（不信 skill 给的 grep——skill 的 grep 可能漏报）：
   ```bash
   # 自检 agent 必跑（比 skill 第 2 条更宽）
   grep -rn "sigma2_turb\s*=\s*[0-9]" projects/simulation/ --include="*.py"
   grep -rn "np\.random" projects/simulation/experiments/ --include="*.py"
   grep -rn "json\.dump" projects/simulation/experiments/ --include="*.py"
   ```
6. 主对话用 grep 抽查修复点（不重审全部）
7. 修复完成才继续原任务

## 自检 agent prompt 模板（用 critic）

```
任务：审查 [文件路径] 是否违反 sim-preflight skill。

反向假设：假设这份产出有 3 个违规，找出最可能的 3 个。

**重要**：不要只读 skill 文件按 skill 的 grep 跑——skill 的 grep 可能漏报。
你必须独立跑以下更宽的检测：
- sigma2_turb 硬编码（不白名单 params.py）：grep -rn "sigma2_turb\s*=\s*[0-9]" projects/simulation/ --include="*.py"
- np.random 在 experiments/：grep -rn "np\.random" projects/simulation/experiments/ --include="*.py"
- json.dump 在 experiments/：grep -rn "json\.dump" projects/simulation/experiments/ --include="*.py"

参考清单（从 .claude/skills/sim-preflight/rules/ 读）：
- tech.md 的 6 条规则
- doc-discipline.md 的拥有者机制
- interrupt.md 的 8 条中断条件

输出：
- 违规清单（按严重程度排序）
- 每条附具体修复建议（可执行）
- 如可修复，直接修（你是 critic，可读写）
```
