# Handoff: GW Step 1 verified，等待 Step 2 确认

> 来源: S001 | 交接目标: 主控裁决是否授权 Groundwork Step 2
> 文件名: H001-step1-ready-for-step2-confirmation.md

## 已完成边界

- 六组 query、两轮上限已用完：169 rows→157 DOI/title unique；S2/OA/Tavily 三贡献源。
- 27-entry semantic matrix：24 formal、3 unknown、8 must-read；两路初筛与 fresh verifier 分离。
- A hard admission 已归传统 comparator；B 仅保留 post-DSP multi-source validity 的窄 soft route。
- 最近 direct competitor 为 Optics Communications 2019，完整动作签名 exact collision=`UNRESOLVED`。
- V001=`PASS 0/0/0`；terminal=`STEP1_PASS_READY_FOR_STEP2_CONFIRMATION`。
- 当前门控：`Step 2=NOT_AUTHORIZED`；必须等待主控显式确认。

## 不要做什么

- 不把 Step 1 PASS 写成 Q#、Go、METHOD_SIGNAL、方法或论文贡献。
- 不把固定 SNR discard、SC/GSC/H-S-MRC、宽泛 pilot-reliability MRC 包装成 extension。
- 不在主控确认前下载或全文精读；不实现、不仿真、不修 b3 truth-h/RNG 债务。
- 不用 decoder/FEC flag 重开 coded C1。

## 必读

1. `topic-index.md`
2. `R001-step1-synthesis.md`
3. `step1-candidate-collision-matrix.md`
4. `step1-provenance-receipt.md`
5. `verifications.md` V001

## 接口变更（如有代码改动）

无。

## 失败数据附录（如涉及路线失败）

第一次 verifier=`FAIL 0/1/1`，原因是 provenance 未绑定和 26→27 残字；唯一窄修后第二个 fresh verifier=`PASS 0/0/0`。没有科学实验或方法失败数据。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| 2019 direct competitor trigger/weight 未知 | exact action 要比较完整签名 | `UNRESOLVED` | 仅在 Step 2 获授权后获取/绑定全文 |
| C26 NT-GSC/TV+NT-GSC identity 未闭合 | strongest comparator 要正式身份 | UNKNOWN | Step 2 前半段补 identity；不得用 unknown 冒充 formal |
| Wang content 未物化到本 worktree | 来源路径必须显式 | shared root success；worktree metadata failed | Step 2 source binding 时处理，不修平台 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|---|---|---|---|
| Step 1 corpus | unique≥20、contributing source≥3、formal≥50%、must-read≥5、route≥2 | gw-search + 本轮授权 | 本轮 157/3/88.89%/8/2 |
| terminal wording | 三个允许 terminal 之一；无 novelty/Go 越界 | D001 / 主控授权 | V001 PASS |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称（列出验证了哪些）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反“明确不含”

## 下一轮

等待主控确认。若授权 Step 2，先重读 Groundwork acquire 规范，按 must-read shortlist 获取并闭合 2019 direct competitor 的完整 input-trigger-action-output；否则保持 idle。
