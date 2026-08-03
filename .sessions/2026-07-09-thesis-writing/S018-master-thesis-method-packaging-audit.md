# [S018] 硕士论文方法包装逆向工程与本项目方法内核重审

> 2026-08-03 | paper-writing INTAKE/DIAGNOSE/PROPOSE | 完成（V013 PASS）

## 目标

诊断旧“看别人怎么包装”为何未产生可执行方法，盘点全项目可包装 method kernel，精读 8–12 篇真实硕士论文的核心方法章，并据此形成至少两套“每个核心技术章都有方法”的 thesis spine 与唯一推荐；若资产不足，只定义下一轮 method-shaped search target，不执行实验。

## 记录

- 当前 owner：`2026-07-09-thesis-writing`；专题已有 16 个 S 文件，D025 已登记强制 scope change。
- paper-writing phase：只允许 INTAKE/DIAGNOSE/PROPOSE；禁止 WRITE。
- 研究边界：不写正式论文、不跑仿真、不修改 Skill、不启动新方法实验、不复活 invalidated claim。
- D023/D024 已暂停；旧 dossier 保留并加 supersession banner。
- 本轮将以 T002–T00N 分批委托历史复盘、内部资产审计和硕士论文全文方法章精读；每个子 agent 单次不超过 15 分钟，主线程只接收结构化结果。

### 委托回执

| task | 结果 | 关键结论 |
|---|---|---|
| T002 | PASS | 旧 34/32 篇口径混合目录、摘要与少量全文；只有交织 4b#1 形成可执行 delta，后被 0 dB 上界 Kill |
| T003 | PASS | CCISP 唯一 8/8 chapter-capable；P01 与 route B 各 7/8；P02/Q(8,6)/prefix-LS 是组件；P05/P06/P07-R/G1/P09 不可晋级 |
| T004 | PASS | 建立 10 篇硕士候选池并精读 A1–A3；纠正张岱、王锋为博士、不得计入硕士样本 |
| T005 | PASS | 精读 A4–A6（闫佳欣、夏煜、管路阳），覆盖 calibration/low-complexity/fixed-point/hardware 方法粒度 |
| T006 | PASS | 精读 A7–A8（丁爽、王敏艳），确认 0.15–0.16 dB 固定点收益也可凭完整流程成章；纯解析模型不等于方法 |
| T007 | PASS | 精读 A9–A10（宁沛明、吴志航），确认 PMF/interface redesign 与 receiver architecture/calibration 可成硕士方法 |
| T008 | PASS / R6 FAIL | 精读 A11 许雅歆；同一 2 ms 时隙内顺序分解不构成双时标 |
| T009 | PASS / R6 FAIL | 精读 A12 韩旭林；集中训练/离线部署不构成运行期远端慢控制 |
| T010 | PARTIAL | 独立交叉映射确认唯一条件式 Spine S1；2A/2B 均为 NEEDS_ONE_BOUNDED_PACKAGE，2C SUPPORTING_ONLY，2D NEEDS_NEW_GW |
| T011 | PASS | fresh-context 独立 verifier：13/13 门 PASS，Critical/Important/Minor 均为 0，READY_TO_COMMIT |

### 事实结论

1. **旧包装失败根因**：证据深度不均、旧任务目标是结构/选方向而非方法 delta、没有统一“全文方法章→baseline delta→内部资产→最小验证”记录单元，并在唯一交织候选上先定方法后找问题。
2. **同行硕士粒度**：12 篇、每篇至少两个核心技术/方法章。R1–R5 各有至少两篇真实实例；常见 delta 包括 estimator/visible variable、threshold/weight、branch/compute graph、module reuse、word length/RTL 和 interface redesign。R6 在 12 篇中 0 例，两个定向样本均 FAIL。
3. **内部内核**：CCISP THESIS_METHOD_READY；2A/2B 各差一个 bounded package；2C 只是 correctness infrastructure；2D 必须新 GW；invalidated/unauthorized 结果未作正证据。
4. **唯一 spine**：Ch3 CCISP → Ch4 2A calibration-aware robustness → Ch5 2B low-complexity branch-route+fixed-point，grade B−/CONDITIONAL。Alternative Ch3/2B/2C 因 coded 章无新 action 排除。
5. **Phase G**：不触发。缺口不是泛泛“缺方向”，而是 2A cross-grid 与 2B formal cost/latency+float-Q 两个有界验证包；本轮均不执行。

### 产物

- `projects/thesis-fso/direction-lab/harvest/peer-thesis-method-packaging-audit.md`
- `projects/thesis-fso/direction-lab/harvest/internal-method-kernel-inventory.yaml`
- `projects/thesis-fso/direction-lab/harvest/packaging-recipe-library.md`
- `projects/thesis-fso/direction-lab/harvest/thesis-method-spines.md`
- 未创建 `missing-method-search-target.md`：Phase G 未触发。

## 决策引用

- D025：暂停旧 thesis blueprint，启动每个核心技术章的方法包装审计（已由 D026 取代）。
- D026：唯一推荐 thesis spine = CCISP 主方法 + 校准鲁棒方法 + 低复杂度部署方法（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是（见 topic-index 2026-08-03 D025 scope change）。

## 后续

V013 已按用户 13 项门独立终验 PASS。下一执行对话先走 sim-preflight/所属 GW gate，只做 2A calibration-aware cross-grid bounded package；本轮统一提交、不 push。
