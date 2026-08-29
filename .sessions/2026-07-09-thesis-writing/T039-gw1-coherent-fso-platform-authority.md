# Task Brief: coherent FSO 共同平台物理 authority

> 来源: S028 | 产出位置: `projects/thesis-fso/direction-lab/harvest/coherent-fso-platform-authority.md`
> 日期: 2026-08-30
> 唯一文档: 本 T + 当前仓库既有证据；允许用项目 `tools/search` 做外部学术检索

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 1
  action_class: EXTERNAL_EVIDENCE
  mission_checkpoint: CP001
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

为 DP-(8,8)-16APSK+BICM/LDPC 星地相干 FSO 共同平台完成 Groundwork Step 1 authority 检索，回答 SOP、PDL、PMD/ISI、滤波记忆、CFO/相噪中哪些真实存在、可取什么量级，以及有限 2×2 FIR 是否可作为 Ch4 合法自由度。

最高纪律：只做 Step 1，不跑实验、不改仿真代码、不发明新损伤；参数没有论文/标准依据就标 UNKNOWN。使用 `tools/search`，不得用网页全文抓取代替论文。

## 1. 背景

共同平台已冻结为 coherent DP-(8,8)-16APSK+BICM/LDPC。Ch3 研究 per-tributary CPR；Ch4 需要 2×2 均衡方法；Ch5 消费均衡后符号做软解调/LDPC。第一轮建议暂不主动加入 PDL/PMD/CFO，有限 FIR/ISI 尚缺物理来源。

## 2. 任务详情

1. 至少用三组不同查询，覆盖 coherent FSO polarization tracking/Jones channel、space-ground optical receiver impairments、DP coherent optical FIR equalization/PMD/filters。
2. 去重后审查不少于 20 条元数据；优先正式 JLT/JOCN/OFC/Optics Express/IEEE 文献和权威标准/综述。
3. 为每项损伤给出：物理来源、星地 FSO 是否相关、典型量级/时间尺度、可否在论文中主动扫描、直接证据（题目、作者、年份、DOI/URL）。
4. 明确区分“光纤 PMD”与“自由空间偏振/SOP/光学前端滤波造成的等效记忆”，不得借光纤文献为 FSO 杜撰频率选择性。
5. 输出 5–8 篇 Step 2 必读候选，标可获取全文状态与为什么会改变 testbed 决策。

产出结构：一句话结论；损伤 authority 表；有限 2×2 FIR 判决；候选文献表；仍 UNKNOWN；对 Ch4/Ch5 的最小影响。保存产出并只提交该 harvest 文件及本任务生成的唯一 search JSON；最终回报 commit、路径和一句结论。

## 3. 已知陷阱

- 不为了让算法有收益叠加 PDL+PMD+CFO+人工 residual。
- 不把双偏振系统中的 Jones mixing 自动等同有 tap memory。
- 不以摘要中的泛称“coherent optical”推断作者研究的是星地 FSO。

## 4. 验收

- [ ] 每个允许进入 testbed 的损伤都有至少两个独立权威指针
- [ ] 有明确的 FIR YES/NO/CONDITIONAL 结论和边界
- [ ] 5–8 篇 Step 2 候选身份可核
- [ ] 无实验、代码或论文正文修改

