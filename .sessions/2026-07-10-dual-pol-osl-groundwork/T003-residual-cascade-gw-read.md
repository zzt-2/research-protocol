# T003 — residual cascade GW Step 3 全文精读

## 任务边界

你是执行 worker。只做 Groundwork Step 3（gw-read），不得做 Step 4a Go/No-Go、不得跑 MVE、不得改代码。逐篇读取以下 5 个 `content.md`，确认标题/来源后按模板抽取证据；输出写入同专题 `S038-residual-cascade-read.md`。

## 输入全文

1. `papers/doi/10.1109_jsac.2022.3191346/content.md` — VAE neural equalizer（直接/邻近待自检）
2. `papers/doi/10.1109_jlt.2021.3056869/content.md` — DNN vs Volterra soft demapping（邻近）
3. `papers/arxiv/2109.14942/content.md` — Neural Networks Equalizers: Caveats and Pitfalls（方法学/邻近）
4. `papers/doi/10.1109_jlt.2022.3146839/9695357.md` — CNN-aided DP-64QAM coherent optical systems（直接/邻近待自检）
5. `papers/doi/10.1109_jlt.2023.3276637/content.md` — CMA-based complex-valued MIMO adaptive equalizer for FSO（强邻近）

## 必须输出（每篇）

- 标题、作者、年份、期刊/来源、文件路径、标题与正文自洽检查
- 问题 M、条件 C、机制/失效 A、方法、输入输出、训练/测试协议、数据/信道、指标、baseline、主要数字结果（含页/节/表/图或 markdown 行号）
- 是否真的涉及“standard CMA always-online + additive NN residual”；若不是，明确标记 direct / adjacent / reject，不得把邻近证据写成直接先例
- 训练标签与信息泄漏风险；复杂度/延迟；是否依赖 pilot/CSI/历史
- 7 个横向子表：M-C-A 映射、baseline 对照、输入输出/动作空间、训练测试公平性、信道/扰动、指标口径、可复现实验条件
- 用 stages/glossary.md 的问题四判据审查 residual-cascade 候选：每条 PASS/FAIL/UNKNOWN，并指出证据路径

## 纪律

- 只读本地全文，不调用 web reader；不要凭摘要补全文中没有的数字。
- 低于证据强度的结论写 UNKNOWN；不要替主控做 Step 4a 判定。
- 完成后只返回结构化摘要，并说明精读覆盖是否达到 5/5。
