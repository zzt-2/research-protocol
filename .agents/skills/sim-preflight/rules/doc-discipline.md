# 通用文档纪律

所有场景必守。每条内容只有一个拥有者文件。

## 三层分档大小限制

| 层 | 文件 | 硬限制 | 超限处理 |
|----|------|--------|---------|
| 锚点 anchor | `CONCLUSIONS.md`, `TERMS.md`, `symbol-conventions.md`, `thesis-framework.md`, `innovation-points.md` | 500 行 | 不允许超，必须精简 |
| 积累 accumulation | `formulas-master.md`, `design-decisions.md`, `master-state.md`, `thesis-status.md`, `文献综述.md`, `写作质量规范.md` | 1000 行（formulas-master 2500） | 超限归档最旧条目到 `_archive/`（见 `rules/archive.md`） |
| 快照 snapshot | `formulas-index.md`, `thesis-preparation-checklist.md` | 300 行 | 整体重写，旧版本由 git 管 |

**行动**：改文档前先 `wc -l` 确认还有空间，超限就先归档。

## 每条内容只有一个拥有者文件

- `CONCLUSIONS.md` 拥有"结论 + 安全等级 + 数字"
- `TERMS.md` 拥有"术语定义"
- `formulas-master.md` 拥有"公式编号 + LaTeX"
- `params.py` 拥有"参数值 + 来源"
- 其他文件只引用，不重复定义

**判定流程**（改内容前必走）：

1. `grep -rn "{要改的内容}" 毕设/ projects/simulation/` 找出所有出现位置
2. 判断"拥有者文件"——内容完整定义所在文件
3. **只改拥有者文件**
4. 其他文件如果是索引（如 `formulas-index.md`），只更新引用行

**新文件加入时**：
- 文件头部声明 front matter（如有）：`owner_of: [术语/公式编号]`
- `grep "owner_of:"` 确认无冲突

## 更新顺序：拥有者 → 索引

新增/修改内容时：
1. 先改拥有者文件（完整定义）
2. 再改索引文件（一行引用，不解释内容）
3. handoff 的"约定变更"段记录关键变更

## 约定变更记录（最高频丢失类型）

参数/公式约定变更占 handoff 丢失案例的最高比例。**任何**以下变更必须在 handoff 显式记录：
- 参数值变更（旧值 → 新值 + 原因 + 影响范围）
- 公式定义变更（旧形式 → 新形式 + 原因）
- 信号模型变更（如 h 的物理含义）
- 评估方法变更（如 `resolve_qpsk` vs `ber_count`）

**无变更写"无关键变更"，不能省略段落。**

## 约定变更审计命令（每对话结束前必跑）

```bash
# 1. 找本对话改了哪些"约定源"
git diff --name-only | grep -E "params.py|formulas-master.md|CONCLUSIONS.md"

# 2. 如有匹配，最新 handoff 必须含"约定变更"段
LATEST_H=$(ls -t .sessions/{专题}/H*.md 2>/dev/null | head -1)
grep -c "约定变更" "$LATEST_H"
# 0 = 警告：改了约定源但没记录

# 3. 验证关键数字一致（举例）
grep "sigma2_turb" projects/simulation/params.py
grep "sigma2_turb" 毕设/formulas-master.md
grep "sigma2_turb" 毕设/CONCLUSIONS.md
# 三处值必须一致
```
