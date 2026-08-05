# [S015] 论文方法包装门纠偏

> 2026-08-03 | Skill 最小修订 | V015 PASS，待派发 T002/T003
> 2026-08-03 续接 | 2A/2B bounded closure 授权 | V016 PASS，待创建两个执行任务
> 2026-08-04 续接 | 首个概念构造批次验收与候选源轮换
> 2026-08-05 续接 | T007 P1 工程候选纠偏与正式 GW 入口准备

## 目标

记录长程运行“科学纠错有效、方法包装失效”的根因，并以 RED→GREEN 方式给 Research Direction Lab 增加最小的论文方法章保留门；随后派出 2A/2B 两个只读包装任务。

## 记录

长程审计与手工 CCISP 对照给出一致结论：现有 Skill 擅长判断结论能否相信，却把方法生产主要绑定到 `METHOD_SIGNAL → active carrier → formal promotion`。因此，未达到论文科学主方法门的 estimator、校准链、条件分支、单分支计算图和字长设计，常在形成方法章之前就被降为 supporting material。

这不是取消科学门。artifact、privileged truth、执行无效、伪造授权和错误成本记账仍不得贡献正向数字。需要修的是另一层：对语义有效的中粒度技术内核，在 formal science disposition 之外单独做章节能力判定，允许诚实进入 `NEEDS_ONE_BOUNDED_PACKAGE`，而不是等待 `METHOD_SIGNAL` 后才谈包装。

本轮采用双门设计：

1. 科学主方法门继续决定 `METHOD_SIGNAL`、active carrier 与 formal promotion；
2. 论文方法章门检查可命名方法、M-C-A、deployable input→action→output、充分传统 comparator、算法步骤/框图、消融、主结果图和 claim ceiling。

论文方法章门只产生 `THESIS_METHOD_READY`、`NEEDS_ONE_BOUNDED_PACKAGE`、`SUPPORTING_ONLY`、`REJECT` 四种状态。它不自动创建 active carrier，也不把 invalidated evidence 升级。当前 RED 对象为 2A 校准鲁棒 CPR 与 2B 单分支低复杂度/定点 CPR；G1/P09 等 invalidated 反例必须继续拒绝。

T002/T003 两个独立只读诊断随后均返回 `NEEDS_ONE_BOUNDED_PACKAGE`：2A 的承重问题是在线 pilot-SNR calibration 是否超过静态 region retune；2B 的承重问题是完整 caller path 的真实成本下降与 Q(8,6) 端到端非劣。用户进一步授权两个单独对话持续运行到完成。D022 因此只解锁 T004/T005，各自一个包、最多一次确定性修复，正负结果均须形成可复现终态；未授权新方向、旧 campaign 或 formal stage。

T007 构造 5 张 Ch5 原型卡。P2–P5 的 collision 裁决成立，但 P1 被“编译器 CSE / 一行代码”
误判为已实现廉价替代。主控沿实际 caller 复核：当前 CPython/NumPy 在
`fft_foe_m0_omega` 与 `nda_ml_recovery` 两个独立调用中真实执行两次升幂，无自动 CSE；
输出等价是计算图工程组件的目标，不等于没有成本动作。D024 因此恢复 P1 为唯一
`ENGINEERING_COMPONENT` survivor，并将候选动作校正为升幂域
`raised*exp(-j*M0*omega*k)` 的 FOE/CPE 共享。其余四卡不恢复。

## 决策引用

- D021：增加独立的论文方法章保留门，并用 2A/2B 与 invalidated 反例做 RED→GREEN 回归（新建）
- D022：授权 T004/T005 各执行一个 bounded closure，持续到明确终态（新建）
- D024：恢复 P1 计算图工程候选，并要求廉价吸收以实际工具链 trace 为准（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是；D023 已授权 design-only 构造与 survivor 回正式 GW，D024
  只纠正 T007 的工程组件判据并准备合法 GW 入口。

## 后续

T004/T005 已写成自包含执行任务并由 V016 独立终验 PASS。统一提交后创建两个新 worktree 对话。主控只接收每个任务的终态、关键数字、证据路径和 commit SHA；执行细节全部留在各分支文件中。

T006 随后构造 4 张 Ch4 原型卡，但原报唯一 survivor C3 与历史 D-011 的 NDA 分段数
adaptive-K 完全同轴。D-011 已实测可实现判据退化为 always-K16、gain=0.000 dB，D-009
又证明 tuned VV Nw=16 在 200/500 kHz 反超 segmented 14%/68%。因此主控将 T006 验收为
`NO_CONSTRUCT_SURVIVES`。根因是 inventory 漏记该旧 dead end，属于碰撞信息管道断裂；
最小修复是补 inventory，并要求下一批按 action signature 定向 grep 历史，不增加新 registry
或 Skill 规则。下一批切到 Ch5 部署/计算流程候选源，不修 C3。

本次 Skill 只修一个语义歧义：廉价替代必须在实际 measured toolchain 中存在。结构回归先 RED
后 GREEN；历史 T007 输出作为真实失败 receipt。下一动作不是第三批构造或实验，而是 T008
新专题 GW Step 1–2 定向检索和获取。Step 2 覆盖面达到门槛后仍须用户确认，再进入 Step 3。
