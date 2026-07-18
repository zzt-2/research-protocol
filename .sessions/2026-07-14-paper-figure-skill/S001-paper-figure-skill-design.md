# [S001] 论文插图 Skill 设计与 TDD 启动

> 2026-07-14 | 设计 / RED → GREEN → REFACTOR | 已完成

## 目标

把 thesis-writing 专题中 Fig.1/Fig.2 的参考图调研、用户纠偏、renderer 选择与 draw.io 验证经验，提炼为全局 `design-paper-figures` 的可测试升级。

## 记录

现有 skill 已包含 semantic brief、layout spec、renderer choice、visual QA 和基础 motif reference，但没有形成以下强门：图型覆盖审查、逐候选可迁移/不适用元数据、语义图元的同领域证据、draw.io source/target 与正交边合同、交叉线伪 junction 审查，以及低改善迭代的截断规则。

用户确认不创建近义新 skill，而是升级现有 `design-paper-figures`。主文件只保留门控与流程；详细规则拆到 references；新增确定性 draw.io validator。禁止把 Fig.2 的三泳道、具体颜色或项目标签提升为全局模板。

TDD 设计：

1. RED-1：在“视觉丰富”压力下，检查当前 skill 是否允许无论文依据的仪表盘、循环箭头或内部短条。
2. RED-2：在“用户会手调、速度优先”压力下，检查当前 skill 是否遗漏 draw.io source/target、正交边、泳道接缝和真实导出验证。
3. RED-3：在“已有约 40 张参考图、想立即开画”压力下，检查当前 skill 是否要求图型覆盖、候选元数据和缺样本阻断。
4. GREEN：只针对 RED 暴露的缺口更新 skill 与脚本，并使用相同场景复测。
5. REFACTOR：运行真实 Fig.2 validator、quick_validate 和独立最终审查。

RED 结果见 R001：RED-1 FAIL，复现仪表盘、相量旋转器和内部短条等无领域证据图元；RED-2 PASS；RED-3 PASS/PARTIAL。最小 GREEN 因此聚焦“语义图元证据门”，并把 draw.io 机械合同放入按需 reference/validator，不重复堆入主流程。

GREEN 实施保持边界：主 skill 新增 Reference Readiness Gate、Semantic Primitive Evidence Gate、draw.io 按需 reference 路由，以及语义/视觉分离审查；`references/drawio-contract.md` 承载未压缩 XML、source/target、正交边、连续背景区与 crossing gap 合同；`validate_drawio.py` 只做可确定验证，不代替出版尺寸视觉检查。

脚本 TDD 证据：在实现 validator 前新增 5 项测试，首次运行因 `validate_drawio.py` 不存在而 5 项失败；最小实现后 5/5 PASS。真实 `fig2_adaptive_cpr.drawio` 通过：43 cells、12 edges、三块背景区精确连续。

三个全新上下文复跑同构场景：语义 agent 拒绝仪表盘、孤立旋转箭头和 DA/NDA 样本云；参考 agent 因自适应控制与多尺度拆图缺合格样本而返回 PARTIAL 并阻断冻结；draw.io agent 验证 12 条边均绑定且正交、交叉控制线使用 gap。详见全局 skill 的 `references/test-records.md` T002。

第一次独立审查结论为 FAIL，发现 validator 对空壳/非图 XML、缺失 band 几何和伪 orthogonal 字符串存在假阳性，且 freeform 文档无脚本例外。按 TDD 新增 4 项边界测试，首次出现 5 个失败断言；随后要求 `mxGraphModel/root`、完整 band 几何、精确解析 `edgeStyle`，并增加显式 `--allow-nonorthogonal`。REFACTOR 后共 9/9 PASS。

第二次独立审查仍为 FAIL：任意 wrapper 包含 graph tag、仅 0/1 scaffold、负数/非有限 band 尺寸可假阳性通过。再次先补 3 项失败测试，再限制合法 draw.io root/单 graph、要求至少一个 vertex/edge、要求 band 宽高为正且所有几何有限。最终 verifier 结论 PASS：12/12 单测、quick_validate、真实 Fig.2 和 7 类独立边界探针全部符合预期；未发现 Fig.2 专属结构固化。

## 决策引用

- D001：升级现有 `design-paper-figures`，采用精简主流程 + 按需 reference + draw.io validator，并执行 RED/GREEN 测试（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是。只升级全局论文插图 skill，不修改 Fig.1/Fig.2 图文件。

## 后续

- 返回 thesis-writing 专题，继续讨论 Fig.1 粗稿；后续绘图任务按升级后的 skill 执行。
