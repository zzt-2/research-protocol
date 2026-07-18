# Task Brief: Fig.5 common-payload 全九点 CI 重画

> 来源: S001 / D012 | 产出位置: `projects/simulation/figures/plot_fig3_gain.py`、`ccisp_fig3_gain.pdf/.png`
> 日期: 2026-07-15
> 唯一文档: 执行方可读取 T011 产出的权威 JSON 和当前论文图样式；不得修改论文文字

---

## 0. TL;DR（执行方先读）

**你的任务**：在 T011 明确回传 `READY_FOR_FIGURE_AND_TEXT` 后，把 Fig.5 重画为 common-payload paired-seed mean gain 的全九点曲线，并显示 95% t-CI。

**产出**：更新绘图脚本、矢量 PDF、300-dpi PNG，以及九点数值和最终单栏视觉 QA 报告。

**最高纪律（违反一条即 FAIL）**：

1. T011 未 PASS 或权威 JSON 没有 `paper_summary.mean_gain_db/ci95_low_db/ci95_high_db` 时立即 BLOCK，不从旧 JSON 或正文抄数。
2. 只读取 paired-seed `paper_summary`；不得画 pooled-count `common768.gain_db`。
3. 必须全 9 点、必须有 95% CI、必须有零基准线；不得隐藏 strong、断轴或做 strong inset。
4. 这是 BER ratio 的对数减少量，不是 equal-BER SNR gain、goodput gain、total-energy gain 或 selector accuracy。
5. 只改绘图脚本和 Fig.5 PDF/PNG；不改任何 `.tex`、仿真、JSON、治理文件；不提交 git。

---

## 1. 图的唯一论点

在相同 average data-symbol SNR 下，selector 相对 fixed NDA 在共同 768-bit data population 上产生状态依赖的 BER-ratio reduction：weak/moderate 点较大，strong 点为 0.08--0.14 dB 的小幅正改善。图完整展示数据，不承担 deep-fade 因果证明。

## 2. 图规格

- 数据：weak/moderate/strong × 5/10/15 dB，共 9 点。
- 横轴：`Average data-symbol SNR, $\bar{\gamma}_d$ (dB)`。
- 纵轴：`Common-payload BER-ratio reduction (dB)`。
- 三条曲线：Weak、Moderate、Strong；颜色和 marker 均不同，灰度打印仍可区分。
- 每点：mean marker + 95% t-CI error bar。
- 零线：细灰色水平虚线。
- 不加图内标题、数值标签、显著性星号、第二坐标轴、断轴、inset 或面积填充。
- 输出尺寸与当前单栏 Fig.5 一致；PDF 保持矢量文字，PNG 为 300 dpi 预览。
- legend 不遮挡数据和 CI；字体、线宽、marker、error-bar cap 在最终单栏尺寸可读。

正式改样式前，检查当前 Fig.3/Fig.4 的绘图脚本和至少 3 个本地可用的同类通信论文数据图，只提取字体、线宽、marker 和 legend 密度规则，不复制其数据或结论。

## 3. 实施与数值测试

1. 检查当前 `plot_fig3_gain.py` diff；保留无冲突的既有样式，不覆盖无关用户改动。
2. loader 一次读取 JSON，逐 scene 严格验证 SNR 集合等于 `{5,10,15}`、每点 `n_seeds=30`、CI 有序且中心位于 CI 内。
3. plot 使用 `paper_summary.mean_gain_db`，误差长度分别为 `mean-low` 和 `high-mean`。
4. 写/运行确定性数值检查，证明传给 Matplotlib 的 9 个中心和 18 个 CI 端点与 JSON 差值小于 `1e-12`。
5. 生成 PDF/PNG，检查两者修改时间晚于权威 JSON。
6. 将 PDF 按论文实际尺寸渲染为图像，检查文字截断、legend 遮挡、error bar 可见性、strong 点与零线可区分、黑白可辨性。

## 4. caption 接口

本任务不改 LaTeX，只把以下短 caption 作为文字线程接口回传：

`Common-payload BER-ratio reduction relative to fixed NDA. Error bars show 95% confidence intervals over 30 paired seeds.`

## 5. 回传格式（强制）

```markdown
## 状态
PASS / FAIL

## 数据绑定
JSON 路径/hash、读取字段、九点中心与 CI 核验

## 图规格
尺寸、轴名、曲线/marker/CI/零线

## 视觉 QA
单栏、灰度、遮挡、截断、字体

## 产物
脚本/PDF/PNG 路径与 hash

## 未修改项
论文、仿真、治理文件、git commit
```

## 6. 验收

- [ ] 全九点来自权威 paired-seed summary。
- [ ] 95% CI 和零线均存在且可读。
- [ ] axis/caption 使用 BER-ratio reduction，不写 SNR gain。
- [ ] strong 三点完整显示，无视觉隐藏。
- [ ] PDF/PNG 通过最终单栏视觉检查。
- [ ] 未修改正文或提交 git。

