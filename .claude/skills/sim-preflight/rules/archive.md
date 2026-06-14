# 文档超限归档流程

`formulas-master.md` 是最高频接近上限的文件（当前 2487/2500 行）。

## 预警线

- **2400 行**：预警线，留 100 行 buffer。下次加新公式前必须先归档
- **2500 行**：硬上限，必须立即归档

```bash
wc -l 毕设/formulas-master.md
# >2400 → 进入归档流程
```

## 归档流程（6 步）

### Step 1：找出可归档候选（基于代码引用，**不是索引引用**）

⚠️ **常见错误**：用 `formulas-index.md` 的引用次数判——但索引文件每个公式天然引用 1 次，会误判全公式为候选。

**正确判据**：基于"代码 + 论文正文"的引用次数。

```bash
# 1. 提取 formulas-master.md 中所有公式编号（兼容 F1 / F3.1 / F4.15 等格式）
grep -oE "F[0-9]+(\.[0-9]+)?" 毕设/formulas-master.md | sort -u > /tmp/all_formulas.txt

# 2. 找代码注释/文档里引用的公式（projects/simulation/）
grep -rhoE "F[0-9]+(\.[0-9]+)?" projects/simulation/ --include="*.py" --include="*.md" | sort -u > /tmp/code_formulas.txt

# 3. 找论文正文引用的公式（毕设/下除 formulas-master/index/archive 外的 .md）
find 毕设/ -name "*.md" ! -name "formulas-master.md" ! -name "formulas-index.md" \
  ! -path "*/_archive/*" -exec grep -hoE "F[0-9]+(\.[0-9]+)?" {} \; | \
  sort -u > /tmp/thesis_formulas.txt

# 4. 合并被引用的公式
cat /tmp/code_formulas.txt /tmp/thesis_formulas.txt | sort -u > /tmp/used_formulas.txt

# 5. 候选 = all - used
comm -23 /tmp/all_formulas.txt /tmp/used_formulas.txt
```

候选 = 全部公式 - 被代码/论文引用的公式。

**安全阀**：候选列表必须人工核对——某些公式即使没被直接引用，可能是当前章节推导链的中间步骤，归档会破坏推导完整性。

### Step 2：移到归档文件

把候选公式整段（含标题、LaTeX、说明、推导链路）移到：

```
毕设/_archive/formulas-superseded-{YYYY-MM-DD}.md
```

归档文件头部加：

```markdown
# 归档公式（{日期}）

> 来源：formulas-master.md 超限归档
> 触发：行数 {N} > 预警线 2400
> 归档判据：代码 + 论文正文均无引用（comm -23 all_formulas used_formulas）

## F0XX: [公式名]
[原内容]
```

### Step 3：原位置加占位

在 `formulas-master.md` 原位置加一行：

```markdown
> 已归档：见 `_archive/formulas-superseded-{日期}.md` F0XX-F0YY
```

### Step 4：更新索引

`毕设/formulas-index.md` 把归档公式标记为 `[archived]`：

```markdown
- F0XX: [公式名] [archived: _archive/formulas-superseded-{日期}.md]
```

### Step 5：handoff 记录

在最新 handoff 的"约定变更"段加：

```
- 公式归档：F0XX-F0YY 移到 _archive/formulas-superseded-{日期}.md（原因：formulas-master 超限；判据：comm -23 all_formulas used_formulas）
```

### Step 6：写使用日志

```
[YYYY-MM-DD HH:MM] 场景=archive | 任务="归档 formulas-master 超限" | routing=correct | interrupts=[] | changes=[F0XX-F0YY 归档] | issues=none | duration=15min
```

## 找归档公式（论文需要引用历史版本时）

```bash
# 在 _archive/ 下找某公式
grep -rn "F0XX" 毕设/_archive/

# 注意：核心 5 条第 4 条"禁止从 archive 取公式"指的是"取公式定义"。
# 论文写作时如需引用旧版本作为对比，必须在 handoff 记录"为何引用 archived 版本"
```

## 其他文件归档

`CONCLUSIONS.md`（500 行）超限时类似流程：
- 旧结论（已被新结论取代）→ 移到 `毕设/_archive/conclusions-superseded-{日期}.md`
- 在 CONCLUSIONS.md 原位置加 `> 已归档：见 ...`

`TERMS.md`（500 行）超限时：
- 极少触发（术语稳定）
- 如触发：废弃术语移到 archive
