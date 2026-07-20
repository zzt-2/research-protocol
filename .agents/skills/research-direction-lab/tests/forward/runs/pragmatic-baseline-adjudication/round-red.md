# RED baseline — pragmatic baseline adjudication

> agent: fresh subagent `baseline_red_forward`
> skill state: before baseline-adjudication revision

## Blind prompt

请把自己当作接手正式研究推进的新智能体，必须先读取并使用 `.agents/skills/research-direction-lab/SKILL.md` 及它认为必要的 references。不要修改任何文件、不要运行实验，只根据以下原始事实给出当前证据级别、是否授权进入 ML、下一批怎么规划，以及为什么。事实：一个双偏振 16QAM 接收链使用实现正确的单模 Godard-with-z CMA；11 cells×10 paired seeds 中 10/11 对 nearest-decision 显示 oracle affine headroom≥MDE，最大 0.333；oracle affine 使用一段真实发送符号拟合，只作 scoring-only；blind affine 收益很小且有长窗变差；运行长度 N=512/8192，文献材料提示 CMA 可能需要约 1e5 symbols 收敛；多模 MMA/RDE 是 16QAM 常见传统方法但本轮未实现、未比较；用户明确偏好务实毕业，不要求追逐当前 SOTA，希望一次批量推进而不是每一步询问。请写一页式行动判断，不引用任何预期答案。

## Raw response

## 一页式行动判断

### 当前事实与证据级别

- 现有结果覆盖 11 个条件、每个条件 10 个配对种子；其中 10/11 个条件显示 nearest-decision 相对当前 CMA 输出仍有 oracle affine headroom，最大值 0.333。这不是孤立单次波动，而是当前执行切片上的稳定诊断信号。
- oracle affine 使用真实发送符号拟合，只能作为 scoring-only 上界诊断，不能作为可部署方法或合法性能对手。
- blind affine 收益很小，长窗甚至变差，说明“存在可恢复上界”尚未转化为“盲接收机可利用的增益”。
- 当前 CMA 是实现正确的单模 Godard-with-z，但 16QAM 的常见传统方法还包括 MMA、RDE；它们尚未实现和比较。
- 当前长度仅为 512/8192 symbols，而材料提示 CMA 可能需要约 \(10^5\) symbols 收敛。因此现象至少同时兼容三种解释：

  1. CMA 尚未收敛；
  2. 单模目标对 16QAM 存在结构性失配，MMA/RDE 可消除差距；
  3. 合法传统均衡后仍存在盲 affine 恢复困难。

**证据分类：**

- 对“当前短长度、单模 CMA 切片存在 scoring-only affine 可恢复余量”的主张：`VALID`，claim ceiling 为 `SLICE`。
- 对“blind affine 已被否定”的主张：证据不足；只能说当前实现/窗口配置未有效利用该余量。
- 对“传统方法仍有系统性缺口”或“需要 ML”的主张：`UNKNOWN`。
- 当前 CMA 可作为 no-change anchor，但不能作为 16QAM 场景下唯一或最强合法传统 comparator。

### 是否授权进入 ML

**现在不授权。**

原因不是 ML 不值得尝试，而是当前信号的因果来源尚未辨清。直接进入 ML，很可能得到以下任一伪贡献：

- ML 仅补偿短序列下尚未收敛的 CMA；
- ML 重新学到 MMA/RDE 已知的多模结构；
- ML 相对弱 comparator 获胜，但换成合法强传统 baseline 后优势消失。

对“务实毕业”目标而言，先补齐低成本传统基线，比现在投入训练、调参和泛化验证更有信息价值，也更容易形成可信论文叙事。

### 下一批：传统基线红队批次

**批次问题：** oracle headroom 究竟来自收敛长度、单模目标失配，还是合法传统接收链后的剩余盲恢复缺口？

**共享条件：** 保持同一信道、初始化、paired seeds、指标和评估切片；oracle 仅作诊断，并将拟合段与评分段分离。

**一次性准备：**

- 验证长序列运行与收敛曲线记录能力；
- 实现并验证标准 MMA、RDE；
- 保留当前 Godard-with-z CMA 作为 no-change baseline；
- 保留 blind affine 作为最强简单后处理器；
- 禁止把 oracle 结果混入运行时选择或调参。

**比较矩阵：**

| 轴 | 设置 |
|---|---|
| 方法 | CMA、MMA、RDE |
| 长度 | 8192、约 \(10^5\)，必要时增加一个中间点形成收敛曲线 |
| 后处理 | 无、blind affine |
| 诊断 | held-out oracle affine headroom |
| 范围 | 第一阶段覆盖有代表性的高/中/低 headroom cells；出现结构后再扩至 11 cells×10 paired seeds |

除最终 ML 门控外，准备、验证、代表性扫描和定向扩展可按批次契约自动连续推进，无须每一步询问用户。

### 预注册判据

- **长 CMA 消除 headroom：** 当前发现归因于未收敛；不进入 ML。
- **MMA/RDE 消除 headroom：** 当前发现归因于 baseline 目标失配；以最强传统方法作为后续 anchor，不进入 ML affine。
- **合法强 baseline 后仍稳定存在 headroom，但 blind affine 无法利用：** 才授权一个窄范围 ML 候选，目标明确限定为“利用传统盲处理后的剩余 affine 可恢复空间”。
- **oracle headroom 存在但对最终主指标无实质影响：** 终止该方向，避免为了诊断量改善而造方法。
- **结果仅在少数 cells 出现：** 保持 `CELL/SLICE` 结论，转为条件化方法，不包装成普遍接收机改进。

这批的价值在于用一个共享实验契约同时排除两个最便宜、最危险的替代解释；只有它们都不能解释现象时，ML 才具有清晰问题定义和合法比较基础。

## Pre-registered scorer output

`FAIL`：缺少务实 baseline 停止条件、`PROBLEM_SURVIVES_CONVENTIONAL_BASELINE` 显式状态和 Portfolio 并行继续要求。
