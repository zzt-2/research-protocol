# Task Brief: Step 3.5 新直接竞品 acquire→read

> 来源: S001 | 产出位置: `projects/thesis-fso/worker-logs/step-3-5-new-competitor-read.md`
> 日期: 2026-08-06
> 唯一文档: 执行方可读取本 worktree、T006 worker log 与项目 acquisition/read 工具

---

## 0. TL;DR（执行方先读）

**你的任务**：对引用链新发现的三篇高相关论文按 `gw-acquire→gw-read` 处理，重点裁决其是否为真正同信息、同动作的 joint `(frame, τ, CFO)` estimator。
**产出**：获取 receipt + 全文 action-contract 精读报告；成功全文还需按既有规范写全局 read note 与项目 read-log。

**最高纪律（违反一条就废了）**：
1. 只用 `tools/download`/`tools/blit`/`tools/convert` 合法通道，先 dry-run，每篇最多三条适用路径，不突破访问控制。
2. 必须读全文才能裁 exact jointness；摘要只能作 blocker/筛查。获取失败就记录 coverage gap，不脑补。
3. 严格区分 generic shared-preamble/resource reuse、sequential timing/frame/CFO、真正 joint estimator。
4. 不修改 canonical decisions/topic/master/literature notes；不进入 Step 4a、不实现、不仿真、不提交。

## 1. 背景

Sun 2025 双向引用链发现：

- P1 `10.1109/JLT.2025.3528909`, *Burst-Mode Digital Signal Processing for Coherent Optical Time-Division Multiple Access*：摘要同时列 sampling-phase offset、sync position、FO、SOP、equalizer，是新增最直接候选；jointness 未决。
- P2 `10.1364/OE.566136`, *Polarization-independent preamble design in Alamouti code-based simplified coherent system for PON downstream*：摘要为 FS/FOE/CE，需核是否含未写入摘要的 timing action。
- P3 `10.1364/JOCN.402591`, *Efficient preamble design and digital signal processing in upstream burst-mode detection of 100G TDM coherent-PON*：早期多动作 preamble baseline，需核动作时序与 timing 边界。

JOCN 2026 `10.1364/JOCN.587273` 已在 T006 三路径止损，不得重复获取。

## 2. 任务详情

### 2.1 要回答的问题

- 每篇是否取得合法 source/content，identity/title、SHA256、行数是否通过？
- receiver-visible information、各同步 action/output、处理时序、共享/分区 preamble 结构是什么？
- 是否单一联合 objective/metric 同时估计 frame index、fractional timing/phase、CFO，还是顺序模块/资源复用？
- 与 Q1 及 polyphase/Farrow + sequential chain 的 collision/delta 是什么？

### 2.2 执行方式

1. 先读 `stages/gw-acquire.md`、`stages/gw-read.md`、`tools-guide.md` 与 T006 worker log。
2. 按 DOI dry-run→合法获取；成功后执行 title 自检、SHA、≥50 行与非拦截页门。
3. 对成功全文写 14+ 标准字段、七子表中与本文最相关的 information/action/assumption/适配/问题提取，以及实验完备性；全局 read note 路径按现有命名规则，read-log 追加。
4. 未获取全文的条目只写 blocker receipt，不用摘要裁 exact action。

### 2.3 产出格式（强制）

```markdown
# Step 3.5 new competitor acquire→read
## Acquisition receipts
| DOI | attempts | source/content | title | SHA | lines | verdict |
## Paper 1/2/3 action contracts
| information | action/output | timing/order | joint objective? | Q1 collision | evidence lines |
## Generic reuse vs sequential vs true joint
## Global read notes / read-log updates
## Coverage gaps
## Conclusion and claim ceiling
```

## 3. 已知陷阱

- 论文标题里的 `joint` 可能只指 FS+FOE+CE 或同 preamble 复用。
- sampling-phase offset 可由一个独立 correlator 得到，不自动等于 joint `(frame,τ,CFO)` objective。
- 同一 system/block diagram 里有多个模块不等于动作耦合。

## 4. 验收

- [ ] 三篇均有 acquisition receipt，失败遵守止损。
- [ ] 成功全文有 identity/SHA/行数与具体 evidence lines。
- [ ] exact-action verdict 不依赖摘要。
- [ ] 成功精读已写全局 read note 与 read-log。
- [ ] 未修改 canonical 状态、代码、实验或 protected paths。

## 附：产出回传位置

`projects/thesis-fso/worker-logs/step-3-5-new-competitor-read.md`
