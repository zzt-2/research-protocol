# Voice — B2-Q2 Fade-Freeze + Pilot-Aided Fallback 第三候选

> 用户/导师原话档案，按日期。除零信息推进/应答外都收，不去重。
> 仅标 →产出(可选) 和 ⟶冲突(仅对立时)。用户说的不标来源。

## 2026-07-08

- "再开另一个方向" → 触发第三候选选择（B7 active + NDA-ML dormant 之外）
- 选"B2-Q2 pilot 在 fade"（选项标签）→ 第三候选锁定 B2-Q2（饱和池 §A，pilot 主题跟 NDA-ML 去 pilot 对偶）
- 选"开，但首验证张力"（选项标签）→ **D001 拍板**：开 B2-Q2 专题，但首验证 step4a 实测反证张力（DA pilot 在 fade 崩溃 vs NDA 鲁棒 vs sat.1553 +1dB 口径错位），不直接搬 sat.1553 +1dB

## 2026-07-08（主控对话 sandbox 核查 + 方向定夺）

- "啥情况？会不会是代码哪里不对？还是确定物理上不可行?" → 对 Kill 判断的质疑，要求主线区分代码 bug vs 物理必然（主线答：Kill2 动态恢复是前馈架构物理必然，Kill3 稳态 BER 有 da_ml 实现可疑点）
- "那别人咋弄的？" → 对文献路线的追问（主线答：别人用闭环 freeze [79] + power-boosted pilot，B2-Q2 sandbox 两个都没做对；精读 D006 后修正：[79] 式闭环 hold 不撞 D006，阶段 0.3 前馈化 INVARIANT 过度保守）
- "为啥撞 D006？" → 对 D006 边界的追问（主线精读 D006 + 阶段 0.3 后修正：[79] 式闭环 hold 功率阈值 gate 不碰 φ_T 建模，严格说不撞 D006）
- 选"放松前馈化 + power-boost（救 B2-Q2）"（选项标签）→ **D003 拍板**：不 Kill B2-Q2，转救援路线（放松前馈化到 [79] 式闭环 hold + 加 power-boosted pilot），重新走阶段 1.5 重设计。用户不愿轻易放弃，要求试文献已验证的路线
