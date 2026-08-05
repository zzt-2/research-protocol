# Topic Index: Adaptive Intra-Window Segmented CPE Groundwork

> 状态: closed | 创建: 2026-08-06 | 最后更新: 2026-08-06（D002：PHYSICAL_PREMISE_UNSUPPORTED；Step 2 未执行）

## 专题信息

- **slug**: `2026-08-05-adaptive-segmented-cpe-groundwork`
- **title**: Adaptive Intra-Window Segmented CPE Groundwork
- **性质**: 承接 RDL system D025/CP006 的有界正式 Groundwork 专题；只执行 Step 1，条件满足时执行
  Step 2，并停在覆盖面确认门。

## 范围边界

### 原始目标（冻结）

判断“依据当前窗口 receiver-visible 统计量选择 NDA/blind CPE 分段长度或跟踪粒度”是否针对一个
有近期 task-matched baseline、有真实物理条件、且未被直接竞品或历史同动作证据吸收的研究问题。

### 当前范围

- 修复 P1 closed 后的控制面陈旧状态，不修改 P1 历史 D/V/R/H；
- GW Step 1：优先复用 `all-papers` 索引与 carrier-recovery 文献，最多 4 组新增定向 query；
- 优先关闭 2019+ 顶刊 task-matched 固定粒度 baseline、同信息同动作粒度 adaptive segmentation、
  以及主流 linewidth/SNR/turbulence 下的物理前提；
- 只有至少一个四判据 Q# 存活，才执行 Step 2；Step 2 至少获取 5 篇 CORE 全文并停在
  `STEP2_READY_FOR_USER_CONFIRMATION`。

### 明确不含

- 不进入 Step 3、Step 3.5、Step 4a、Contract、方法实现、MVE 或仿真；
- 不提高 linewidth 或采用无文献来源的不真实参数制造问题；
- 不把 metadata/abstract 当全文精读结论，不把“没人题名相同”当 novelty；
- 不撤销或改写 D-011、CP004、既有 A1/B1 负面证据；不通过改名重开历史同动作方向；
- 不修改 `common/`、`params.py`、既有算法、旧 raw/result 或四个 `p05_run*.log`；
- 不 push；本对话只做一次最终 commit。

### 范围变更记录

- 无。

## 已确认结论

### 不变量

- **M**：NDA/blind CPE 使用固定块内估计粒度，例如整窗 mean-angle 或固定 `segK`。
- **C**：Wiener phase noise 与不同 linewidth/SNR/turbulence 工况下，固定粒度可能存在“长窗降噪但
  跟踪不足”与“短窗跟踪快但估计方差高”的偏差—方差冲突；该物理前提必须由主流参数与文献支持。
- **A**：依据当前窗口 receiver-visible 统计量选择 CPE 分段长度/跟踪粒度；动作位于 NDA 分支内部
  CPE 估计几何，不是 selector 阈值重调。
- 历史 `D-011 adaptive K` 与 inventory `a1_adaptive_segmented_cpe` 是强制反证边界；本专题是用户
  授权的 bounded Step 1 复核，不预设 reopen condition 已满足。
- Step 1 terminal 为硬门；无四判据 Q# 时不得进入 Step 2。

### 其他结论

- 4/4 query：raw=187、query-dedup=179、final=151、跨组 unique=140；published=77、unknown=63。
- recent task-matched fixed baseline 存在：JLT 2020 `10.1109/JLT.2020.2976166`，JLT 2021 补强。
- 未发现外部同 receiver-visible 信息、同 K/segment 动作粒度的 adaptive segmentation。
- 历史 exact action 的 reopen condition 未满足；terminal=`PHYSICAL_PREMISE_UNSUPPORTED`。

## 进展线索

- **S001**：专题建立、范围冻结、历史碰撞前置核查与 Step 1 定向检索。
- **D001**：只授权 bounded Step 1；Step 2 条件式；不撤销历史 adaptive-K 否决。
- **R001**：四组 query、近期 baseline、direct competitor、物理前提与四判据综合。
- **D002**：物理前提不支持；无 Q#，Step 2 不执行，专题关闭。
- **H001**：closed-state handoff；下一轮回上游轮换机制不同的新候选。
- **项目 literature notes**：`projects/thesis-fso/literature_notes_adaptive_segmented_cpe.md` 同步 Step 1
  STOPPED 与 Step 2 NOT_RUN，和 master-state 的 C3 GW Progress 一致。
- **Step 1 receipt**：`projects/thesis-fso/adaptive-segmented-cpe-groundwork/step1-search-receipt.json` 固化
  query/source/count、四个 JSON SHA256 与 raw 计数的证据边界。
- **V001**：fresh-context verifier 8/8 PASS；terminal、控制面、检索统计、历史反证、Step 2 gate 与
  Git 边界均通过。

## 未决项

- 无。本专题已在 Step 1 硬停止；abstract 级边界仅供未来机制不同的候选复用，不触发本专题 Step 2。

## 当前位置

`PHYSICAL_PREMISE_UNSUPPORTED / CLOSED`。无四判据全 PASS Q#；Step 2 合格全文=0、失败项=0，
原因是 Step 1 gate stop，不是下载失败。不得改名重开或进入 Step 3/4a/实现/仿真。
