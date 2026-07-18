# Task Brief: common-payload selector 全文论证闭环

> 来源: S001 / D012 | 产出位置: CCISP `abstract.tex`、`introduction.tex`、`results.tex`、`conclusion.tex`
> 日期: 2026-07-15
> 唯一文档: 执行方可读取 T011 权威 JSON、D008/D009/D012、R004/R005 和现有 LaTeX；不得修改图或仿真

---

## 0. TL;DR（执行方先读）

**你的任务**：在 T011 回传 `READY_FOR_FIGURE_AND_TEXT` 后，用 common-payload paired-seed mean+t-CI 契约修订论文四处论证链，同时彻底消除 Results 中把 26/29 称为 recovery/accuracy 的旧措辞。

**产出**：只修改 `abstract.tex`、`introduction.tex`、`results.tex`、`conclusion.tex`，返回逐项 evidence map 和 scoped stale-claim 检查。

**最高纪律（违反一条即 FAIL）**：

1. 开始前读取 `paper-writing`、`external-output`、D008、D009、D012、R004、R005 和 T011 权威 JSON；T011 未 PASS 则 BLOCK。
2. 只使用 `paper_summary.mean_gain_db` 和对应 CI；正文可四舍五入，但不得抄 pooled diagnostic。
3. strong 只能写“小幅正改善/benefit narrows to 0.08--0.14 dB”，不得写 zero、near zero、insignificant 或 deep fade causes。
4. 26/29 只称 aggregate selected-output alignment；不得出现 selector recovery、branch recovery、accuracy、correct estimator、locally optimal。
5. 不改 `system_model.tex`、`method.tex`、标题、Fig.1/Fig.2、参考文献、绘图脚本、图资产、仿真或 JSON；不提交 git。

---

## 1. 指标与措辞合同

论文指标名统一为 **common-payload BER-ratio reduction**。共同集合 \(\mathcal C\) 为每个 DSP window 中 192 个非 pilot symbols，即 768 bit。正文统计定义为：

\[
G_{\mathcal C}^{(s)}=10\log_{10}\!\left( P_{b,\mathcal C,\mathrm{NDA}}^{(s)} / P_{b,\mathcal C,\mathrm{SW}}^{(s)} \right),
\]

并报告 30 个 paired seeds 的均值；Fig.5 error bars 给出双侧 95% t-CI。不要把它叫 SNR gain、goodput、throughput、total-energy gain、全 payload BER 或 selection accuracy。

门面段只使用受限 headline：`up to about 1.3 dB common-payload BER-ratio reduction relative to fixed NDA over the evaluated downlink points`。该结果必须与 fixed-estimator 的最高 3.1 dB total-energy-equivalent advantage 分开，不能相加或互证。

## 2. 修改范围

### 2.1 Abstract

在保留 fixed NDA 最高 3.1 dB 及其组成解释的基础上，增加一句 selector 的 bounded 结果：最高约 1.3 dB、common-payload BER-ratio、相对 fixed NDA、仅限 evaluated downlink points。避免同时堆叠 9 点和 CI。

### 2.2 Introduction

在第三项贡献中补入规范 selector 性能证据，使“提出 selector”与“验证 selector 输出”闭环。保持 1.3/1.2/1.9 和 2.5/2.4/3.1 fixed-estimator 结果原义不变。

### 2.3 Results 的实验设置

明确区分三层数据：

1. fixed-estimator benchmark/extension；
2. common-payload Fig.5 performance layer：weak/moderate/strong × 5/10/15 dB，30 paired seeds，每 seed 400 windows；
3. 独立 29-point aggregate alignment diagnostic。

删除 `selector-recovery count/layer` 命名。

### 2.4 Results §IV-C

- 删除 `R_FB/G_FB`、1024 full-block normalization、旧 mixed 数字 2.3/2.0/1.3。
- 用 \(\mathcal C\)、per-seed BER 和 \(G_{\mathcal C}^{(s)}\) 定义 paired estimand，并说明 Fig.5 报告 30-seed mean 和 95% CI。
- 代表结果用：weak@10 about 1.3 dB，moderate@10 about 0.9 dB；strong 统一概括为 0.08--0.14 dB 的小幅正改善。不要逐点列九个数。
- 可写“benefit is concentrated in the evaluated weak and moderate conditions and narrows under strong turbulence”。不得写 deep fades 已证明导致该现象。
- 26/29 段按 D008 重写为 aggregate selected-output alignment；清楚说明它采用 branch-specific data-BER/既有接近规则，是辅助诊断，与 common-payload Fig.5 不是同一指标。不要把 26/29 和 Fig.5 合并成“共同证明正确选择”。
- caption 使用 T012 给出的短句；若 T012 尚未完成，可先使用同一冻结文本，最终由主控核对。

### 2.5 Conclusion

在 fixed NDA 最高 3.1 dB 后增加 selector 的 bounded 结果，并限定 evaluated downlink points。结论不主动逐点放大 strong，也不声称普遍适用于 AWGN、uplink 或所有 SNR。

## 3. 格式和专业性

- 保持 IEEE 双栏会议文风，段落首句先承担论点，公式只承担指标定义。
- 数字主文按已有 R016 习惯使用 `about` + 一位小数；strong 范围因本身小，可写 `0.08--0.14 dB` 防止四舍五入成零。
- 不出现 mixed、审计、机械白送、证据债务等内部过程语言。
- 不新增引用，不改 section/subsection 标题，不增加新的 displayed equation group；优先用现有 §IV-C 公式位置替换。
- 保持纯正文不少于 3500 词；若删改导致低于 3500，先压缩冗余改写而非添加 filler，并在回传中报告实际词数。

## 4. 验证

1. 逐文件给出 claim → JSON/D008/D009/D012 的 evidence map。
2. scoped grep §IV-C，确保没有 `full-block-normalized`、`G_FB/R_FB`、旧 mixed 锚点、`selector recovery`、`branch recovery`。
3. 不得全局禁止 `1.3`：§IV-B 的 fixed-estimator 1.3 dB 合法且必须保留。
4. 检查 Abstract/Introduction/Results/Conclusion 的 common-payload 名称和最高约 1.3 dB 一致。
5. 对比 diff，证明 §IV-A、§IV-B、system model、method、参考文献均未改。
6. 只做局部 LaTeX 语法检查；fresh build 和视觉 QA 由主控在 T012/T013 汇合后统一执行。

## 5. 回传格式（强制）

```markdown
## 状态
PASS / FAIL

## 修改摘要
四个 section 各自改了什么

## Evidence map
claim | source field/decision | paper location

## 术语与数字审计
common-payload、paired mean、CI、26/29、3.1 dB 分离

## Scoped stale-claim grep
命令和结果

## 范围审计
明确列出未修改文件

## 待主控整合项
caption/图引用/fresh build/词数/视觉 QA
```

## 6. 验收

- [ ] 四个 section 形成 selector 方法—结果—结论闭环。
- [ ] common-payload 定义、paired estimand 和 Fig.5 CI 语义一致。
- [ ] 26/29 不再称 recovery/accuracy。
- [ ] strong 没有被写成零或未经验证的因果。
- [ ] §IV-B 的 fixed-estimator 1.9/3.1 dB 原样保留。
- [ ] 未修改图、仿真、参考文献或提交 git。

