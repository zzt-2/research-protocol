# Verifications — 论文插图全局 Skill

## V001: design-paper-figures TDD 与最终独立验证

> 结论: PASS
> 日期: 2026-07-14
> 关联: S001 / D001 / R001

### 验证对象

- `C:\Users\zzt\.agents\skills\design-paper-figures\SKILL.md`
- `references/patterns.md`、`references/drawio-contract.md`、`references/test-records.md`
- `scripts/validate_drawio.py` 与 `scripts/test_validate_drawio.py`
- 真实样本 `projects/simulation/figures/fig2_adaptive_cpr.drawio`

### 新鲜证据

1. RED 语义压力复现无证据仪表盘、旋转器、样本云与内部短条；GREEN 新上下文明确拒绝这些默认图元，并回到源机制/同角色领域证据。
2. 参考就绪场景在四类图型中缺两类合格样本时返回 PARTIAL，阻断整体冻结。
3. draw.io 新上下文验证真实文件 43 cells、12 条 source/target 绑定正交边、三块等宽垂直背景带精确连续、crossing 使用 gap。
4. validator 经三轮 RED/GREEN/REFACTOR：首次 5 项失败后通过；两次独立 reviewer 分别发现 4 类和 3 类边界假阳性，均先补失败测试再修复；最终 12/12 单元测试 PASS。
5. `quick_validate.py` 输出 `Skill is valid!`。
6. 最终独立 verifier 额外探测伪 wrapper、scaffold-only、负尺寸、NaN、freeform 下缺 endpoint、多页、多 graph，全部按合同拒绝；结论 PASS，无 blocking finding。
7. 从 skill 根目录执行 `python -m unittest discover -s ... -p 'test_*.py' -v` 可发现并通过 12 项测试；真实 Fig.2 validator 返回 PASS、0 errors、0 warnings。

### PASS 判据

- 主 skill 可触发且未固化 DA/NDA、三泳道、具体配色、标签或 region 数量。
- 语义图元必须有源机制或至少两份同角色领域参考支持。
- 缺必需图型样本时不能进入设计冻结。
- draw.io validator 不对空壳、伪结构、无效端点、错误 edgeStyle 或非法背景几何给出假阳性。
- 文档、脚本、测试与真实样本行为一致。

以上判据全部满足，结论 PASS。
