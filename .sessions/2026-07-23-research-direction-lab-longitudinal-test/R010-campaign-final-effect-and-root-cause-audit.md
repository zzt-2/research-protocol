# [R010] Method-production campaign 最终效果与根因审计

> 2026-08-02 | 关联：2026-07-23-research-direction-lab-longitudinal-test / D058

## 调研问题

这次长程运行是否实现了“低用户负担、稳定推进真实研究并积累方法材料”；7/10 应如何解释；哪些资产可进入论文；流程为什么反复出现 verifier 接收后被推翻；Skill 最小补丁是什么。

## 发现

### 1. 最终效果

- 原始 mission 是“用户只中转任务路径和极短回执，稳定推进真实研究并积累可用方法材料”（`mission-log.md:3`）。
- CP001–CP017 方法增量为 0/17；T019–T026 出现 2 个 signal，但 formal 转化为 0/2；D039 campaign 最终接收 7 个局部负面/边界包，`METHOD_SIGNAL=0`、`active_carrier=0`。
- 7 个有效包是 P01–P06 加替代原 P07 的 P07-R。P08/R/R2、P09、P10、P11、G1 均不计数。7/10 不是失败，也不是继续补三包的自动授权；它只说明固定数量合同在可用机制入口耗尽前未达到。
- 终态是 `SATURATED_NO_ACTIVE_CARRIER / DORMANT`：当前模型、证据与授权下没有 active carrier；不宣称数学上穷尽所有可能方向。

### 2. P11 新纠偏

P11 的 cell 字典只声明了 9/11/13/15 dB 标签（`p11_run.py:118-128`），但 caller 调用 `MLF.gen_channel()` 时只传 `N, alpha, beta, f_g, sop_rate, seed`（`:271-274`）。generator 没有 gamma 参数，直接使用 `GAMMA_BAR_DEFAULT=100`（`ml_long_seq_failure.py:60-61,154-169`；`params.py:502-504`）。因此四个 cell 实际都是 20 dB；旧 `PARTIAL_LOCAL_9to15DB_BASELINE_ASSET` 被纠正为 `PARTIAL_LOCAL_20DB_BASELINE_ASSET`。raw 仍可作 20 dB、不同湍流/fG/SOP 的局部 baseline，不能作跨 SNR 证据。

### 3. 客观困难与流程不足

客观困难：当前星地 coherent dual-pol testbed 的物理自由度窄，多条候选被 region retune、uniform precision、standard CMA、last-value persistence、gain calibration 等强传统方法直接吸收；合法 problem-bearing M-C-A 稀缺。

流程不足：semantic correctness 长期晚于 hash/receipt/复算一致性；固定包数被误当终局代理；入口作用面常依赖名字或标签而非 caller→callee；普通包持续写 D/V/checklist，导致控制面过重。专题累计 10 个 S、32 个 T，决策与验证文件均超过 3500 行，D057 还出现重复且首份截断。

### 4. `consistency != correctness` 撤回链

1. V071 后由 V072 推翻 P07：漏 `q/g`、AGC 递推和 trajectory lifecycle。
2. V073 后由 V074 推翻 P08：漏 GG 真相源、receiver-visible σ²、oracle 粒度、metric、interleaver、统计单位。
3. V074 后由 V075 推翻 P08-R：漏间接 gamma 泄漏、非递归 AST、post-hoc MDE/CI。
4. V075 后由 V077 推翻 P08-R2：缺独立 pre-test freeze chronology。
5. V078 后由 V079 推翻 P09：对称冗余、真实成本少报、TX-bit resolve、MDE 与 paired CI 错误。
6. V080 后由 V081 推翻 P10：只有 2 cell×6 dev，未跑 held-out/Phase B。
7. V082 后由 V083 推翻 P11：pooled 掩盖 per-cell 反转，LS 并非唯一强 comparator。
8. V083 后由本次 V084 纠正 P11：9/11/13/15 dB 只是未生效标签，实际全为 20 dB。

共同根因是 verifier 主要验证合同自洽与 artifact 忠实，没有执行足以推翻结论的端到端语义反例。

### 5. 用户负担与恢复

- 任务运输负担较低，但科学纠偏负担没有降到目标水平：P07、P08、P08-R、P08-R2、P09、P10、P11、G1 的承重纠正主要由用户长指令触发。
- 唯一 recovery receipt 的 elapsed/files-read 是 `UNMEASURED`，所以“五分钟恢复”仍未被真实测量证明。
- 有效机制：foreground control、防 lane 丢失、完整 supersession 血缘、formal/method 双账、raw 独立复算、problem→conventional→factory 门。
- 纯治理成本：持续扩张的 prose、每包 D/V、固定包计数，以及在没有语义门时的 N/N PASS。

### 6. Skill 最小 patch brief（只做三类）

1. **Executable semantic gates**：进入 held-out 或 ACCEPT 前，必须执行 caller→callee 作用面/物理自由度、参数注入 sentinel、隐藏真值 metamorphic、state/action trace、metric 独立换算、真实调用/成本计数、逐 cell 非 pooled 判读；任一承重门 FAIL 即 fail-closed。
2. **Contribution tiers**：固定 T0 integrity/diagnostic、T1 bounded negative/engineering/writing asset、T2 pre-formal method signal、T3 formal thesis method。每包预声明 ceiling；只有 promotion preflight+GW 闭合才能升层，negative/packaging 不折算 method progress。
3. **Lightweight persistence**：普通包只留 T、worker-log、artifact、commit、mission-log 一行；D/V 只用于方向决策、撤回或跨 owner 合同；topic-index 只保 current snapshot；recovery receipt 仅在真实压缩/fork 时记录 elapsed/files/lane-match。

不增加第四、第五类 patch；下一对话只改 Skill 并对历史 case 做回归，不启动 AMC。

## 结论

campaign 在运行连续性与资产保全上有效，在正式方法生产上没有产出：0 个新主方法、0 active carrier。它留下 7 个可信局部边界包、若干 B 级工程资产和一条高价值的语义审计撤回链。继续追逐“10 个有效包”只会制造范围偏离，因此应 dormant；恢复只能由新物理自由度、新系统层级或用户明确 scope change 触发。

## 对决策的影响

建立 D058：固定 10 包从执行目标退役；P11 改为 20 dB partial；campaign 置 `SATURATED_NO_ACTIVE_CARRIER / DORMANT`。论文资产分级写入独立 harvest map；H003 只交接三类 Skill patch 与历史回归。
