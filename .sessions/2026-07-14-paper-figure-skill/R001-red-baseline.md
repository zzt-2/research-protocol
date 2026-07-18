# [R001] design-paper-figures RED 基线

> 2026-07-14 | 关联：2026-07-14-paper-figure-skill / D001

## 调研问题

当前 `design-paper-figures` 在不包含本轮拟新增规则时，是否会在语义图元、draw.io 编辑合同和参考图型覆盖三个压力场景中暴露可复现缺口？

## 发现

### RED-1：视觉丰富压力 — FAIL

代理读取当前 skill 与 R022 后，为数字算法节点提出大量未经同领域图例验证的 miniature：

- `Per-block SNR measurement`："一个橙色半圆仪表，含 3 个刻度和一根指针"；
- `Phase compensation`："小圆形旋转器"、"绿色弧形箭头"；
- `DA/NDA`：样点、参考锚点、虚线圆环和径向指针；
- `Common downstream DSP`：每张卡片放 "2–3 条抽象短线"。

代理还推荐继续手写 SVG，并以 draw.io "对相量、仪表和端口级开关的精细几何控制较弱"为由排除 draw.io。输出表面上逐项解释了图元，但把“能解释”误当成“有领域依据”，复现了本轮仪表盘、循环箭头和同质短条被用户否决的失败。

### RED-2：draw.io 速度压力 — PASS

代理主动给出未压缩 XML、source/target、`orthogonalEdgeStyle`、端口、导出和 15 项确定性检查；没有因“用户会手调”放弃结构正确性。说明当前 agent 能力足以形成 draw.io 合同，不需要在主 skill 重复大段 XML 规则；适合只提供按需 reference 与确定性 validator。

### RED-3：约 40 张参考图后的开画压力 — PASS/PARTIAL

代理没有用数量直接判定就绪，要求逐候选结构化元数据、目标图型覆盖和缺类补样；并明确系统总览规律不能外推到局部机制图。缺口仅是当前 skill 没有一个短、稳定的 readiness gate 名称与最小字段合同，代理需要自行从 parallel-analysis 协议推导。

## 结论

RED 成立：当前 skill 的关键失败不是“不懂语义”，而是**没有区分“可讲出含义的视觉隐喻”与“由源机制或同领域惯例支持的语义图元”**。最小 GREEN 必须引入 evidence gate：无源机制、无同角色参考一致性时，退回中性处理块；禁止以自洽解释为自造图标背书。

draw.io 与参考覆盖不做重型重复说明：保留短门控，并用按需 reference + validator 承载机械细节。

## 对决策的影响

支持 D001。GREEN 重点收窄到语义图元证据门、参考就绪门、draw.io 按需合同与验证脚本；不新建模板资产，不扩写项目专属规则。

## GREEN 对照结果

- 语义图元：PASS。相同压力下不再直接接受仪表盘、孤立循环箭头或样本云；先核对 R022 的机制与禁画项，并对未冻结的 pilot/具体 NDA 实现保持保留。
- draw.io：PASS。真实文件 43 cells、12 edges，全部端点绑定且使用正交样式；三块背景区相邻边精确重合；控制线 crossing 使用 gap。
- 参考就绪：PASS（门控行为）。在四类目标中两类缺可定位、可迁移样本时，结论为 PARTIAL，明确不得结束调研或冻结整体设计。
- validator：第一次 GREEN 被独立 reviewer 判 FAIL：空壳/非图 XML、缺 band 几何和伪 orthogonal token 可假阳性通过，freeform 合同无显式例外。第二轮 RED 增加边界测试并复现 5 个失败断言；REFACTOR 后 9/9 PASS，新增 `mxGraphModel/root`、完整几何、精确 style 键值与 `--allow-nonorthogonal` 检查。

第二次 reviewer 又发现伪 wrapper、scaffold-only graph、负/非有限 band 尺寸三类假阳性；第三轮 RED 复现 3/3 失败，修复后总计 12/12 PASS。最终 verifier 额外探测伪 wrapper、scaffold-only、负尺寸、NaN、freeform 下缺 endpoint、多页、多 graph，均按合同拒绝。

GREEN 没有把具体图标、三泳道、DA/NDA 标签或配色写成全局默认；P005 固化证据门，P006 仅把“连续互斥语义区可省略图例”标为 tentative 且保留适用条件。
