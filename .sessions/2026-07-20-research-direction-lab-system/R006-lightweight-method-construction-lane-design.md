# [R006] 轻量方法构造车道设计

> 2026-08-04 | 关联：2026-07-20-research-direction-lab-system / D023

## 调研问题

为什么现有 Research Direction Lab 能稳定纠错和闭合负面，却长期没有产生新的学位
论文方法？怎样在保留科学诚信门的同时，让 Ch4、Ch5 高效形成可命名、可运行、
可与传统方法比较的方法，并避免检索慢、对话压缩和治理膨胀再次拖垮主线？

## 发现

### 1. 根因不是单一的“领域太难”

- CCISP 的形成顺序是“先观察 DA/NDA 稳定互补，再把条件变成 receiver-visible
  信息源，构造窗口级分支动作，最后补完整证据”。
- 后续长程运行的默认单元逐渐变成“给既有 baseline 注入一个失效条件并可信裁决”。
  CP001–CP017 的 `mission_method_delta` 为 0/17；方法工厂出现 2 个 signal，但 formal
  转化为 0/2；P01–P07-R 七个有效包均为局部负面或边界。
- T004/T005 表明错误发生在重实验之前：2A 的 online calibration 在 dev 上比
  conventional regional retune 低 0.04096 dB；2B 的 single-branch scheduling 已写入
  CCISP `method.tex`，只能成为既有方法的工程实现证据。两者都不应先进入重型闭包。
- 当前 testbed 物理自由度窄、传统算法强、AMC baseline/testbed 缺位，客观难度真实；
  但“候选构造晚于审查、以可信终态代替新动作”为流程放大的主要部分。

### 2. 现有 Skill 的强项和缺口

应保留 executable semantic gates、caller→callee 信息边界、任务适配的传统
comparator、formal/method 双账、按 action lineage 分账和三层持久化。它们能阻止
scale artifact、truth leakage、虚假成本和非法晋级。

真正缺口是：Skill 主要优化“消除一个科学不确定性”，而不是“先塑造一个完整的新
deployable action”。现有回归主要验证不会误晋级和不会丢掉已给定的 adapter，没有
验证能从资产与同行 recipe 主动构造方法。pre-formal factory 又要求失效点、作用点、
传统 comparator 和源码证据先对齐，使候选出生前承担接近 Groundwork 的成本。

## 方案比较

| 方案 | 顺序 | 优点 | 主要问题 | 裁决 |
|---|---|---|---|---|
| A 严格 Stage-first | 每个想法先 GW Step 1–4a，再设计方法 | 最安全 | 弱想法也先付全文与科学成本，延续低产出 | 不选 |
| B 双车道 | 概念构造与筛选；胜者再回正式 GW | 先产完整动作，严审只给胜者 | 必须严守“不实验、不 claim”边界 | **采用** |
| C 章节倒推 | 先定章名、方法名、主图，再反推动作 | 最贴近毕业 | 容易先有标题后造机制 | 只作 B 的候选来源 |

## 推荐设计

### 1. 两条车道

**概念方法构造车道**只做设计，不跑新科学实验、不读 held-out、不产生 Go/claim。
它是既有 `PREFORMAL_METHOD_FACTORY` 的设计型前半段，只在目标章节槽位同时满足以下
条件时启用：mission 明确以方法产出为目标；该槽位没有正在正式推进的 active carrier；
inventory remap 对该槽位给出 `READY=0 / NEEDS_SMALL_ADAPTER=0`。若已有可直接闭合的
方法资产，优先闭合该资产，不另开概念构造。

每张方法原型卡必须包含：

1. 方法名与章节位置；
2. `M-C-A` 与 receiver-visible `input → action → output`；
3. 可执行算法步骤；
4. 与已有贡献的动作差异；
5. 一个充分传统 comparator 与最强廉价替代；
6. 主结果图、消融、最小实现路径、claim ceiling；
7. 失败后的降级包装。

候选来源包括算法互补、可见量校准、分阶段估计、鲁棒控制、计算流程和资源约束，
但 recipe 只是生成器，不能替代真实动作。

**正式科学车道**只接收概念车道选出的最多两个候选。winner 必须回到 GW
Step 1–3/3.5/4a；只有通过正式 gate 后才跑 bounded experiment 和 Deep Evidence。
概念构造不是 MVE，因此不绕过 FR-22。

### 2. 轻量碰撞与踩坑入口

不新建 registry。复用
`projects/thesis-fso/direction-lab/harvest/internal-method-kernel-inventory.yaml`，后续只在
需要时补 `action_signature / collision_scope / reopen_condition`。它统一索引：

- 已有方法及其动作边界；
- 可复用但不能单独声称的方法组件；
- invalidated/rejected 路线、失败范围与重开条件。

每张原型卡内嵌五行 `collision receipt`，不单独建文件：已有动作碰撞、历史 dead-end
碰撞、最强廉价替代、是否满足重开条件、`NEW_ACTION / EXTENSION /
ENGINEERING_COMPONENT / REJECT` 分类。只按命中 ID 追原始 decisions/worker-log，不全读
历史。`thesis-lessons.md` 继续只保存通用科学与仿真教训。

### 3. 检索后移与可中断执行

1. 本地资产建图和方法构造不做外部检索；使用代码、旧结果、inventory 和已精读的
   同行硕士论文 recipe。
2. 内部碰撞与廉价替代筛选后，只给排名前 1–2 的候选做定向查重；已有本地索引和
   全文优先，外部检索按候选独立落盘，某一篇获取失败不阻塞其他候选。
3. 只有 survived candidate 才进入正式 GW 的全文闭包；不再先搜大池再猜方法。
4. `topic-index` 保存当前入口，inventory 保存方法/组件/dead-end，T/worker-log/artifact
   保存单包细节。聊天只回状态、路径、commit、异常；任何对话中断均可从文件恢复。

### 4. 工作量熔断

- 概念构造包不得跑仿真、生成大 raw artifact、创建普通 S/D/V/H 全套或独立 verifier。
- 新候选先过动作重复和廉价替代两个便宜检查；失败立即合并、降级或退出。
- 科学包先执行核心方法比较；没有正向诊断信号时，不升级到大规模 held-out、receipt
  和 Deep Evidence。
- 具体时长、查询数和文件数是 task-local budget，不写成通用固定包数或 scheduler。
- 一个科学包经一次确定性修复仍未执行核心比较，则轮转，不继续治理闭包。

## Skill 最小修改与 RED→GREEN

设计通过后才修改 Skill。预期只改现有 `method-production.md` 的路由/原型卡合同和少量
主路由文字，不新增 controller。

RED/GREEN 至少覆盖：

1. CCISP：识别为不同于固定 DA/NDA 的新运行时动作，允许进入候选池；
2. 2B：实验前识别 single-branch scheduling 与既有 CCISP action 重复，降为工程组件；
3. 2A：实验前识别 regional retune 是强廉价替代，只允许极小决胜或降级；
4. 正向新动作样本：不得因碰撞门过严而被误杀；
5. 中断恢复样本：只靠 topic-index、inventory 和一个 worker-log 恢复正确下一步；
6. 工作量压力样本：不得在核心 construct 未运行前扩成 receipt/verifier 大包。

历史对照结果以 Git commit 固定：T004=`1140134e89e8b0571274944cb44471ab6403481f`
（`2a-calibration-aware-cpr-method-package.md`）；
T005=`67970307a051dd8149e1a750498a20674dfcfe6f`
（`2b-fixed-point-branch-routed-cpr-method-package.md`）。T004/T005 任务书只证明授权，不
作为结果证据。

## 成功与失败标准

Live test 不以包数或全部正收益为成功。成功要求至少形成一张：

- 不重复已有贡献；
- 有真实 deployable action、传统 comparator、完整章节形状；
- 能用一个 bounded experiment 决定去留；
- 没有在核心比较前投入重型治理。

连续两个构造周期仍无一张卡满足前三项时，判候选来源或 thesis target 需要调整；才
允许扩大检索、换系统层级或请求用户裁决，不回到“再注入一个失效条件并全套审判”。

## 结论

采用“轻量概念方法构造 → 小范围筛选 → survivor 回正式 GW → 正信号后重证据”的双
车道。该设计不能保证科学正收益，但能保证昂贵工作之前已经形成并筛过真实方法动作，
并把慢检索、上下文压缩和单候选阻塞限制在局部。

## 对决策的影响

支持 D023。下一合法动作是用户审阅本设计；通过后先写 Skill RED 测试，再做最小
GREEN patch。当前不修改 Skill、不派方法构造任务、不运行仿真。
