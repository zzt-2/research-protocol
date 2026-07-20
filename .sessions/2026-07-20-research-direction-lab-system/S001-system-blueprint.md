# [S001] Research Direction Lab 体系蓝图

> 2026-07-20 | 体系设计 | 已完成，待用户审阅

## 目标

基于用户原话和 Direction Lab 三代方案的真实运行结果，一次性规划完整目标体系；先锁职责、信息流、文件体系和验收，再决定 Skill 与代码如何实现。

## 记录

既有资产形成了三代演化：

1. `method-family-batch-exploration` 已正确规定“冻结基点 → 候选族全景 → 分批 → winner 晋级”，但没有长期恢复、自动换路、域扩展和论文收获；
2. DL-Process v0.3 增加 Scout/Sandbox/Promotion、Core/Profile/Adapter 和证据门，但把 Queue/Registry/状态转换扩展成较重运行规范；
3. Portfolio Autopilot 试图解决长期续跑，却让通用代码承担固定批次数、机制覆盖、resource slots、work-conservation 和停止证明，V035/V037 连续出现开放世界反例。

根因不是再少两个 preflight，而是开放式研究判断和确定性安全检查混在同一控制核。用户本轮明确纠正：代码只做轻量控制与碎片步骤，流程尽可能由 Skill 承担；并要求先一次规划完整体系，避免设计反复落成普通文档。

目标方案采用 `Skill-first, code-guarded`：Skill 是研究驾驶员，通用脚本是安全内核和办事工具，Domain Profile 是领域规则，Project Adapter 是项目事实。代码报告事实和阻断不可逆错误，不选择科学方向、不证明研究充分、不求解候选资源匹配。

完整目标设计见：

- `docs/superpowers/specs/2026-07-20-research-direction-lab-system-blueprint.md`
- `docs/superpowers/plans/2026-07-20-research-direction-lab-system-implementation.md`

自查确认：U01–U15 均出现在蓝图与实施验收中；目标态只有主 Skill 拥有开放式流程；旧 `process.md` 在激活前仍是当前项目规范，未被本轮静默改写；本轮没有修改控制器、仿真器或历史科学产物。

## 决策引用

- D001：目标体系采用 Skill-first、code-guarded（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是；只做体系规划，不改控制器、不运行实验。

## 后续

交用户审阅；审定前不进入 Skill 或代码实施。
