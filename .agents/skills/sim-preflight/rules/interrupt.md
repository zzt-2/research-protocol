# 遗漏中断 + 自检机制

## 中断清单（12 条）

执行任何仿真任务时，发现以下情况**立即中断**。每条配可执行检测命令。

> v1.3.0 新增 10-12 条（算法正确性防线，源自 NDA-ML D-007~D-009 教训：consistency PASS 但算法是错的 / vs 祖师爷持平当合理结果接受 / 参数变更后没重审算法）。

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

### 9. 参数真相源分裂（v1.2.0 新增）

发现以下任一 → 中断（详见 `rules/param-source.md`）：

**(a) 函数默认参数固化模块常量**：
```bash
grep -rn "def [a-z_]*([^)]*=[A-Z_]" projects/simulation/ --include="*.py"
# 例如 def doppler_phase(N, f_res=F_RESIDUAL, lw=LASER_LW) —— import 时冻结，patch 模块属性无效
```

**(b) 同一物理量跨模块多个数值源**：
```bash
# 检查线宽/符号率/噪声等高频混淆项是否多处定义
grep -rn "LASER_LW\|CLW\b\|R_SYM\|BAUD\b" projects/simulation/ --include="*.py" | grep -v "import\|#"
# 若同一物理量名（如 LASER_LW vs CLW_B11）在不同模块有不同数值 → 中断
```

**(c) sweep/ablation 脚本用 monkey-patch `__defaults__` 注入参数**：
```bash
grep -rn "__defaults__" projects/simulation/ --include="*.py"
# __defaults__ 是函数默认参数固化的症状——正路是传参或重新初始化 SimulationConfig
```

匹配 → 中断，向用户澄清"这个物理量的真相源字段是哪个、为何有多个"。修复方向：默认参数留 None + 函数体读 params.py 单一字段（见 `param-source.md` 失败模式 A/B 正确做法）。

### 10. "vs 祖师爷方法持平"警报（v1.3.0 新增）

**触发条件**：实验结果显示"我们的方法"与领域祖师爷经典方法（如 VV 1983 升幂 mean-angle / Gardner TED 1986 / Decision-aided ML 1980s）在 BER/RMSE/gain 上**持平或差异 <5%**。

**立即查数学同族性，不当"合理结果"接受**。两种可能：
- (a) **数学同族**（如 NDA-ML 升幂 mean-angle vs VV 升幂 mean-angle，只差 ML 加权）→ 持平是必然，**创新性受质疑**，必须找到拉开差距的条件（换参数/换场景）或重新定位贡献
- (b) **对照不公平**（实现 bug / 参数掩盖差异）→ 修 bug 后重跑

**自检命令**：
```bash
# 查最近 results JSON 是否有 vs 经典方法对照
grep -rln "vv_cpr\|bps_cpr\|gardner\|decision_aided\|da_ml" projects/simulation/results/ projects/simulation/explore/*/  2>/dev/null
# 如有，grep gain 字段看是否 |gain|<0.05dB 或 BER ratio 在 [0.95,1.05]
```

**来源**：NDA-ML D-008——vs VV 持平被当合理结果接受长达 2 个 session，实际是漏 ML 加权 bug（两者数学同族都是等权 mean-angle）。用户原话"这和 VV 持平真没问题吗？"戳穿。

**匹配 → 中断**，向用户报告"方法 X 跟祖师爷方法 Y 持平，数学同族性检查结果={a/b}，建议={换条件重跑/修 bug/重新定位贡献}"。**禁当合理结果默默接受**。

### 11. 参数变更后未触发算法重审（v1.3.0 新增）

**触发条件**：CRITICAL 参数值变更后（如线宽 500kHz→10kHz、符号率 25GBaud→2.5GBaud、噪声方差改量级），未重新审视算法实现是否在新区间仍正确 + 是否仍有增量。

**参数选择和算法验证是耦合的**——改参数可能掩盖或暴露算法 bug / 算法创新。

**必做清单**（参数变更后、重跑前）：
1. 该参数影响哪些算法路径？（如线宽影响 ML 加权收益、segmented 跟踪收益、CRB 下界）
2. 原参数下的算法增量结论，在新参数下还成立吗？
3. 是否需要补 sandbox 验证新参数下的算法对错（不只 consistency）？

**自检命令**：
```bash
# 查最近 git diff 是否改了 params.py 的 CRITICAL 参数
git diff HEAD~3 -- projects/simulation/params.py | grep -E "^\-.*[0-9]|^\+.*[0-9]" | grep -iE "lw|linewidth|baud|r_sym|sigma2|kappa"
# 如有改动，检查同 commit 是否同时改了算法实现或跑了 sandbox 验证
```

**来源**：NDA-ML D-008 教训 4 + D-009 教训 7——D-007 选 10kHz 低线宽后，ML 加权收益退化（低线宽下样本 SNR 均匀，加权≈等权），掩盖了 D-008 双 bug（漏 ML 加权 + 升幂未归一化）。consistency 0.0000% PASS 是因为 MVE 和 Formal 都漏同一加权，"两者一致"不证明符合原论文。

**匹配 → 中断**，向用户报告"参数 X 从 A 改到 B，影响算法路径 {list}，原增量结论 {成立/待重验}，建议 {补 sandbox / 重跑全量 / 仅记录}"。

### 12. MVE/sandbox 缺三方对照（v1.3.0 新增）

**触发条件**：MVE 或 sandbox 验证只跑了"我们的方法 vs baseline"两方对照，**没含"祖师爷方法/原论文方法"第三方**。

**MVE/sandbox 必须含三方对照**：
1. 我们的方法（加权版 / segmented 版 / 增强版）
2. 等权 / naive 版（消融，证明增强有效）
3. 祖师爷方法（VV / Gardner 1986 / BPS 等领域经典，证明非数学同族）

**缺第 2 方**（消融）→ 增量归因不可信（可能增量来自其他改动非核心算法）。
**缺第 3 方**（祖师爷）→ 数学同族性不可查（可能跟祖师爷持平被当合理接受，见中断 10）。

**自检命令**：
```bash
# 查 MVE/sandbox 脚本是否 import 了至少 3 个对照方法
grep -rE "from common import|from common._recovery import" projects/simulation/explore/*/  --include="*.py" | grep -oE "(vv_cpr|bps_cpr|nda_ml|da_ml|gardner|dpll|kf_)" | sort -u
# 如不足 3 个 → 中断
```

**来源**：NDA-ML D-008 教训 1——之前 sandbox（`explore/nda-awgn-tracking-sandbox`）只验证 segK8 vs none（都是等权 mean-angle 变体），没验证 vs B11 真 ML（加权版）。结果 bug 没被抓，直到 vs VV ablation 才暴露。

**匹配 → 中断**，向用户报告"sandbox/MVE 只含 {N} 方对照，缺 {消融/祖师爷}，建议补 {X} 再下结论"。

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
