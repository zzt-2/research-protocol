# [S076] P03 推理范围纠错与结论层级门

> 2026-07-19 | Direction Lab 流程纠错 | completed

## 目标

保留 P03 10-cell probe 的运行事实与复现证据，纠正“单一 QPSK/20 dB/短序列 slice → 停止整个 P03 候选”的范围越级，并为后续 Scout/Sandbox 增加机器可执行的结论范围门。

## 记录

P03 v1 的 source closure、10-cell 运行、零 BER/SER 和 residual 统计仍然有效；错误发生在解释层：合同把 zero headroom 记为 coverage=1.0，随后把一个 exact-slice 出口投影成候选级停止。该 slice 只有 QPSK、CSI_NONE、20 dB、单一湍流/动态条件、N=512，且历史已经存在调制、SNR、动态性和序列长度改变方法排序的反例，不能支撑 domain/candidate/family 结论。

本轮采用五级结论层级 `CELL → SLICE → DOMAIN → CANDIDATE → FAMILY`。P03 当前纠正投影为：cell=`NO_VISIBLE_HEADROOM`，slice=`LOCAL_NEGATIVE`，domain=`UNRESOLVED`，candidate=`P03_DOMAIN_ADEQUACY_UNRESOLVED`，family=`OPEN`。当前 slice 继续禁止训练 ML；下一科学动作是 baseline-only multi-domain Headroom Atlas，不是直接训练模型或启动 B004。

旧 P03 raw artifact、probe contract、D057/V030、B001–B003 和 canonical state 不删除、不重写。新增 adjudication overlay 与通用 claim-scope validator；future v4 Queue/controller 再绑定该门，不修改已被 B003 fingerprint 冻结的 legacy v3 controller/validator。

迭代计数器：第 1 轮独立审查在 V031 发现三项实际绕过并判 FAIL；第 2 轮改为结构化 decision class、真实证据/独立验证/统计灵敏度证书与内容寻址 receipt，V032 判 PASS。否决条件保持不变：如果新门允许 zero-headroom 单 slice 在无有效证书时把 domain/candidate/family 标为 ADVANCE/RETIRE，则不得进入 Headroom Atlas。

## 决策引用

- D058：P03 局部负面不得升级为候选级停止，并建立五级结论门（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是。属于 D045 批量探索流程的 P0 纠错；不改变 formal GW/Contract/Execute 授权，不启动新研究方向。

## 后续

流程修复已由 V032 验收。下一对话先实现并测试 Headroom Atlas 的唯一 preflight/assessment receipt consumer；只有该硬前置通过，才运行 baseline-only multi-domain Headroom Atlas。
