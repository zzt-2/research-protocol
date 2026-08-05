# Handoff: C3 Step 1 物理前提门停止

> 来源: S001 | 交接目标: 回到上游 RDL 轮换机制不同的新候选
> 文件名: H001-step1-physical-premise-stop.md
> 日期: 2026-08-06

## 已完成边界

完成 4/4 组 C3 Step 1 定向 query 与逐条 AI 标注。近期 fixed-window baseline 存在，外部同信息同动作
adaptive segmentation 未发现；但 C3 与历史 D-011 exact action 相同，且新增文献未满足 reopen
condition。terminal=`PHYSICAL_PREMISE_UNSUPPORTED`，无 Q#，Step 2 未执行，专题 closed。

## 不要做什么

- 不把“一般 window tradeoff 存在”改写成 C3 在主流 10–80 kHz 条件下可行；
- 不提高 linewidth、换同类 proxy、改名或复用旧 MVE 重开 C3；
- 不进入 Step 2/3/3.5/4a、实现或仿真；
- 不修改 P1 或 C3 的历史 D/V/R/H。

## 必读

1. `.sessions/2026-08-05-adaptive-segmented-cpe-groundwork/topic-index.md`
2. `.sessions/2026-08-05-adaptive-segmented-cpe-groundwork/R001-step1-directed-search.md`
3. `.sessions/2026-08-05-adaptive-segmented-cpe-groundwork/decisions.md`（D001–D002）
4. `projects/thesis-fso/direction-lab/harvest/internal-method-kernel-inventory.yaml`（`a1_adaptive_segmented_cpe`）

## 接口变更（如有代码改动）

无。

## 失败数据附录（如涉及路线失败）

### C3 adaptive segmentation

- 核心失败机制：主流物理区间内固定 K16 已吸收，proxy 不可部署地预测 best K，tuned VV 吸收高线宽表面增益；
- 具体数据：gain=0.000 dB、0/8 显著胜、K16 71% 持平 oracle、`|rho|max=0.361`、
  tuned VV 在 200/500 kHz 反超 14%/68%；本轮 4 query / 140 unique 未带来 reopen evidence；
- 已排除方向：CV/SNR/linewidth proxy → adaptive K；极端 linewidth 制造问题；同轴换名重开；
- 可复用部分：近期 fixed-window baseline、一般 tradeoff 文献、annotated search JSON。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| 部分功能断言仅 abstract 级 | Step 3 才能作全文数据流裁决 | 本专题在 Step 1 已硬停，不下载 | 仅机制不同的新候选明确依赖某篇论文时，按其独立 Step 2 获取 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称
  - 声称1：4/4 query、raw=187/final=151/unique=140 → 待续接者填写
  - 声称2：JLT 2020 fixed-window recent baseline 存在 → 待续接者填写
  - 声称3：历史 exact action 数据未满足 reopen condition → 待续接者填写
- [ ] 已检查 `_registry.yaml` 中本专题的 `depends_on` 和 `conflicts_with`
- [ ] 已确认当前范围未违反“明确不含”

## 下一轮

回到上游 RDL 候选池，选择机制不同、已有 2019+ 合法 baseline、且不复用 adaptive-K action
signature 的候选；先做 inventory/dead-end collision，再建立新的 Groundwork owner。
