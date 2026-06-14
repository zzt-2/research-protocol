# 月度审计流程（skill 演进的证据来源）

每月初（或大规模使用后）跑一次。输出报告 → 改 skill → 写 CHANGELOG。

## 审计命令

```bash
LOG_DIR=.sessions/sim-preflight-log
MONTH=${1:-$(date +%Y-%m)}   # 默认本月，可传参审计历史月
LOG=$LOG_DIR/usage-$MONTH.md

# 0. 月度日志是否存在
test -f "$LOG" && echo "✓ $LOG 存在" || { echo "⚠️ $LOG 不存在（漏写）"; exit 1; }

# 1. 总使用次数
echo "=== 总使用次数 ==="
grep -c "^\[" "$LOG"

# 2. 场景分布（哪个场景最常用）
echo "=== 场景分布 ==="
grep -oP "场景=\K\S+" "$LOG" | sort | uniq -c | sort -rn

# 3. 路由判断分布
echo "=== 路由判断 ==="
grep -oP "routing=\K\w+" "$LOG" | sort | uniq -c
# 计算 ambiguous+wrong 比例，>20% 说明决策树分支不全

# 4. 中断类型分布（哪些规则真的在工作）
echo "=== 中断类型分布 ==="
grep -oP "interrupts=\[\K[^\]]+" "$LOG" | tr ',' '\n' | sort | uniq -c | sort -rn
# 从未出现的中断类型 → 疑似无效规则

# 5. 自检 agent 结果分布
echo "=== 自检结果 ==="
grep -oP "self-check=\K\w+" "$LOG" | sort | uniq -c

# 6. 反复出现的 issues（skill 缺陷候选）
echo "=== 反复 issues（缺陷候选）==="
grep -oP 'issues="\K[^"]+' "$LOG" | grep -v "^none$" | sort | uniq -c | sort -rn | head -10

# 7. stuck 比例（流程卡死频率）
echo "=== stuck 比例 ==="
TOTAL=$(grep -c "^\[" "$LOG")
STUCK=$(grep -c "duration=stuck" "$LOG")
echo "stuck: $STUCK / $TOTAL"

# 8. 约定变更数
echo "=== 约定变更数 ==="
grep -oP "changes=\[\K[^\]]+" "$LOG" | grep -v "^$" | wc -l

# 9. 与 handoff 数对比（漏写检测）
echo "=== 漏写检测 ==="
HANDOFF_COUNT=$(ls .sessions/*/H*.md 2>/dev/null | xargs -I{} basename {} | \
  awk -F'-' '{print substr($1,2)}' | sort -u | \
  awk -v m="$MONTH" '$1>=m' | wc -l)
LOG_COUNT=$(grep -c "^\[" "$LOG")
echo "本月 handoff 数: $HANDOFF_COUNT, 本月日志数: $LOG_COUNT"
# 比例 < 0.5 → 警告：可能漏写日志
```

## 审计报告模板

```markdown
# Skill 月度审计报告 — {YYYY-MM}

## 数据快照
- 总使用次数: N
- 场景分布: A=x, B=y, C=z, D=w
- 路由 ambiguous 比例: X%
- 中断触发次数（按类型）: ...
- stuck 比例: Y%
- 反复 issues（top 3）: ...
- 日志/handoff 比: ...

## 诊断

### 决策树分支
- [ ] ambiguous+wrong 比例 ≤ 20%
- [ ] 若 > 20%，列出最常 ambiguous 的场景 → 补决策树分支

### 失效规则
- [ ] 列出从未触发的中断类型
- [ ] 如某条规则 6 个月未触发 → 标记 TENTATIVE，下月再观察 1 个月仍 0 触发 → 删除

### skill 缺陷
- [ ] 列出反复 issues top 3
- [ ] 每条制定修复方案（改哪个文件、哪段）

### 流程卡死
- [ ] 若 stuck 比例 > 30% → 流程过重，需简化

### 漏写检测
- [ ] 日志/handoff 比 ≥ 0.5
- [ ] 若 < 0.5 → skill 强制力不足，考虑加 hook（但 B 方案默认不加）

## 行动清单

| 优先级 | 改动 | 文件 | 触发证据 |
|--------|------|------|---------|
| 高 | ... | ... | ... |
| 中 | ... | ... | ... |
| 低 | ... | ... | ... |

## CHANGELOG 写入

每条改动写入 `.claude/skills/sim-preflight/CHANGELOG.md`：

```
## [YYYY-MM-DD] vX.Y.Z
- 改动: ...
- 触发证据: 月度审计 {YYYY-MM} 报告 / usage-log 反复 issues
- 影响: 哪些规则、文件
```
