# PROMPT-002: ML/LSTM 自适应调制切换在光通信的现状调研

> 粘贴此文档开新对话。这是开放调研，不是试方向（守 FR-22）。
> 动机：用户记得见过别人用 LSTM 等 ML 方法做调制切换的学位论文，想搞清楚这个领域到底什么现状。

## 你要做什么

**开放调研**：ML/LSTM 做自适应调制切换（AMC / modulation scheduling / adaptive modulation）在光通信（尤其 FSO/星地光通信）里的领域现状。先看全貌，再判断。

## 第一步（必须按顺序）

1. **session-governance 报到**：读 `.sessions/2026-07-10-dual-pol-osl-groundwork/topic-index.md`
2. **读背景**：本文件下方的"调研背景"
3. **开始检索**：先广搜看全貌，看到结果后再收敛关键词（不要预设太窄）

## 调研问题（要回答的）

1. **有多少人在做？** ML 做光通信调制切换/自适应调制，是成熟大方向还是小众？
2. **别人具体做了什么？** 切什么（调制格式/编码率/符号率/PS）、用什么 ML（LSTM/DRL/CNN/传统）、什么场景（光纤/FSO/星地）、增量是什么指标（throughput/outage/dB/鲁棒性）、对手是谁
3. **学位论文多不多？** 用户印象里"别人写了学位论文"——确认这个印象，找中文学位论文
4. **跟我们场景的关系**：有没有人在双偏振星地湍流 FSO 下做 ML 调制切换的？

## 检索策略（先广后窄，用户要求"先看看有啥再想咋搜"）

### 第一轮：广搜看全貌（tools/search，不要预设太窄）
先用宽泛关键词看领域规模和形态分布。建议起点（可根据结果调整）：
- `"adaptive modulation" + "optical" + "machine learning"` — 最广
- `"modulation format selection" + "optical communication"` — 换个说法
- `"LSTM" / "deep learning" + "adaptive modulation" + "free space optical"` — 带具体 ML 方法

中文检索（tools/blit --source cnki --doc-type phd/master）：
- `自适应调制 光通信 深度学习`
- `调制格式 切换 LSTM 自由空间光`

### 第二轮：看第一轮结果后收敛
看到全貌后，根据结果里密集的子方向/方法，构造更精准的检索词。这一轮的目标是"找到跟我们场景最接近的工作"。

## 纪律

1. **这是调研不是试方向**（FR-22）——不立 Q#、不判 Go/Kill、不预设结论
2. **先广后窄**——用户明确要求"先看看有啥，再想咋搜"。不要一开始就用太窄的词限死范围
3. **主对话禁 WebSearch**——用 tools/search + tools/blit
4. **子 agent 强制委托**——检索结果消化在子 agent 做
5. **中性**——不预设"这个方向烂"也不预设"这个方向好"，看证据说话
6. **对照 ③ 的 Kill（见调研背景）但不锁死**——③ Kill 的是"DVB-S2 8阶MCS在单偏振LEO过境"的具体化身。调研目的是看有没有③没覆盖的角度，不是确认③ Kill对了

## 产出

一个 R### research note（放 `.sessions/2026-07-10-dual-pol-osl-groundwork/R001-ml-modulation-switching-survey.md`），回答上面的 4 个调研问题，含：
- 领域全貌统计（论文数量/年份分布/方法分布/场景分布）
- 代表性论文清单（标题/venue/年份/做了什么/增量指标）
- 与我们场景的关系判断
- 是否存在 ③ Kill 未覆盖的角度（如有的话列出，不立 Q#，留 Step 4a 评估）

---

## 调研背景（必读）

### 这个想法怎么来的

用户在 GW Step 3 双偏振精读完成后，想到"之前见过别人用 LSTM 等 ML 方法做调制切换的学位论文"。想搞清楚这个方向到底什么现状，值不值得重新考虑。

### 之前 Kill 过的相关方向（③，D009）

2026-06-10 专题里，候选 ③「过境仰角感知 MCS/调制阶数排程」被 Kill。Kill 证据：

- **oracle 上界**（完美 CSI + 零开销切换 + N=200000）：12 个 (σ²_R_zenith, γ̄) 组合 max **0.09 dB**，8/12 case = 0.00 dB，12/12 <0.5dB 阈值
- **指标**：算的是 **outage 容量**（不是只算 throughput——这个维度已覆盖）
- **场景**：**单偏振** LEO 过境，DVB-S2 标准 8 阶 MCS（QPSK-1/4 ~ 32APSK-9/10）
- **根因**：① oracle 下整个过境只切 2-3 次（调制阶梯太粗）② 全程最优固定 MCS 已"聪明"（argmax 加权平均）③ 与 N1（16-QAM PS gain≈0）同家族
- **详细数据**：见 `.sessions/2026-06-10-research-direction-exploration/decisions.md` D009（L522-601）
- **oracle 脚本**：`projects/simulation/explore/mcs-gain-upperbound/mcs_gain_upperbound.py`

**③ 的否决条件（F3）**：若重新提议"LEO 过境 MCS 排程"，要求显式论证"为什么这次不同"。

**但注意**：D009 砍的是"DVB-S2 8阶MCS在单偏振LEO过境"的**具体化身**。以下角度**未被 ③ 覆盖**（调研要留意的）：
- 更细粒度调制集（连续速率自适应 / 概率整形连续阶梯）——但 N1 Kill 了 PS on 16-QAM gain≈0
- 非增益维度的贡献（切换的复杂度/延迟/开销优化）
- 双偏振空间下的调制切换（③ 是单偏振算的）
- ML 预测的价值不在"逼近 oracle 增益"而在其他维度（如：减少 CSI 反馈开销/降低切换延迟/鲁棒性）

### 当前位置

- GW Step 1-3 双偏振 OSL 完成（3 个 Q#：Q-DP1 动态SOP跟踪 / Q-DP2 CMA fade发散 / Q-DP3 跨帧恢复）
- 即将进 Step 4a（H002 已交接）
- 这个调研是**并行的开放调研**，不阻塞 Step 4a 主线

### 不变量提醒

- 不变量1：9 次 Kill 是物理事实——③ 的 oracle 上界是硬证据，调研结论不能无视它
- 不变量7：找方向方法论是用户过程决策不问导师；具体选定方向才跟导师谈
- TL-12：别人能写学位论文 ≠ 增量够（换皮风险）。但"不少人做"至少说明形态可发表
