# Verifications — 论文写作全局 Skill

## V001: paper-writing Skill 结构、行为与独立审查

> date: 2026-07-14
> 关联：S001 / D001

### 验证项

- [x] RED/GREEN 行为测试：3 个相同组合压力场景分别由无 skill 与有 skill 的独立 agent 执行 → RED 3/3 FAIL，GREEN 3/3 PASS。
- [x] 边界复测：8 个未在首轮覆盖的绕门/过约束场景由 fresh agent 执行 → 8/8 PASS，Overall PASS。
- [x] 结构校验：以 UTF-8 模式运行 `quick_validate.py` → `Skill is valid!`。
- [x] 历史规则与分层审查：独立 agent 对照批准设计、R013、R016 和 external-output；首次 PARTIAL 后完成两轮 delta 修复 → 最终 PASS。
- [x] 文件完整性：主 `SKILL.md` 174 行，小于 500 行；5 个 reference 与 `agents/openai.yaml` 均存在，无模板 TODO。

### 证据

```text
RED:
P1 FAIL — 无 benchmark/事实矩阵时直接提出通用扩写项。
P2 FAIL — 未判核心影响便默认要求主动披露弱场景。
P3 FAIL — 以“预览稿”为名在 TBD/占位表/数字冲突未解时进入润色。

GREEN:
P1 PASS — 停在 INTAKE/G0，要求 artifact identity、有效正文、benchmark、fact matrix 和 contract。
P2 PASS — 固定 13 dB=实现事实，crossover=事后观察；不默认披露非核心弱场景。
P3 PASS — 拒绝预览绕门，BLOCKED 项未解前不进入 WRITE。

Boundary retest:
A-H: PASS
Overall: PASS

Validator:
Skill is valid!

Independent final delta audit:
PASS — venue=N/A 已贯穿 diagnosis/verification；L0 明确仍走六状态且不得冒充整篇完成；benchmark PARTIAL 已传播至诊断与交付门。
```

### 结论

PASS
