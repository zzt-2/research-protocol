# [R001] ML/LSTM 自适应调制切换在光通信的现状调研

> 2026-07-10 | 关联：专题 2026-07-10-dual-pol-osl-groundwork（并行开放调研，不阻塞 Step 4a 主线）
> 来源 PROMPT：`.sessions/2026-07-10-dual-pol-osl-groundwork/PROMPT-002-ml-modulation-switching-survey.md`

## 调研问题

1. **有多少人在做？** ML 做光通信调制切换/自适应调制，是成熟大方向还是小众？
2. **别人具体做了什么？** 切什么 / 用什么 ML / 什么场景 / 增量指标 / 对手是谁
3. **学位论文多不多？** 用户印象里"别人写了学位论文"——确认这个印象
4. **跟我们场景的关系**：有没有人在双偏振星地湍流 FSO 下做 ML 调制切换？

## 检索执行记录

两轮检索（先广后窄），全部用 `tools/search`（英文学术聚合）+ `tools/blit --source cnki`（中文学位论文），结果存 `search-archive/2026-07-10/`。

| 轮次 | 查询 | 工具 | 命中(归档) | 存档文件 |
|---|---|---|---|---|
| 1 | `adaptive modulation optical machine learning`（最广） | search | S2 命中 **2472** 篇，归档 20 | `ml-amc-survey-q1-broad.md` |
| 1 | `modulation format selection optical communication` | search | 归档 20（偏光纤核心网） | `ml-amc-survey-q2-format-selection.md` |
| 1 | `LSTM deep learning adaptive modulation free space optical` | search | 归档 20 | `ml-amc-survey-q3-lstm-fso.md` |
| 1 | `自适应调制 光通信 深度学习` | blit/cnki | 10 | `cnki-amc-optical-dl.md` |
| 1 | `调制格式 自适应 光纤 深度学习` | blit/cnki | 13 | `cnki-modformat-fiber-dl.md` |
| 1 | `自由空间光 自适应调制` | blit/cnki | 12 | `cnki-fso-adaptive-mod.md` |
| 1 | `FSO 调制切换 自适应` | blit/cnki | 2 | `cnki-fso-mod-switch.md` |
| 1 | `卫星光通信 自适应调制` | blit/cnki | 2 | `cnki-sat-opt-adaptive-mod.md` |
| 2 | `LEO satellite optical communication adaptive modulation coding` | search | 归档 20 | `ml-amc-survey-r2-q1-leo-acm.md` |
| 2 | `reinforcement learning modulation selection optical wireless` | search | 归档 20 | `ml-amc-survey-r2-q2-rl-mod.md` |
| 2 | `modulation format adaptation satellite downlink deep learning` | search | 归档 20 | `ml-amc-survey-r2-q3-sat-dl.md` |
| 2 | `链路自适应 光通信` | blit/cnki | 2 | `cnki-r2-link-adaptation.md` |
| 2 | `AMC 自适应调制编码 激光` | blit/cnki | 1 | `cnki-r2-amc-laser.md` |

中文 CNKI 学位论文跨 5 个去重后约 34 篇（第一轮）+ 3 篇（第二轮，多为不相关）。

## 发现

### 调研问题 1：有多少人在做？

**结论：广义"ML for 光通信"是成熟大方向，但精确"ML 驱动光通信调制切换"是小众新兴。**

- **广义**：`adaptive modulation + optical + machine learning` 在 S2 命中 **2472 篇**——领域庞大，但里面混了大量光纤核心网 modulation format recognition（识别）、认知无线电 spatial modulation MIMO、power allocation、adaptive optics（自适应光学，跟调制无关）。
- **精确子题**：真正"ML 做光通信**调制切换/ACM**"的工作几乎全是 **2022–2026 年**、引用 **<40** 的近期工作。高引论文（>50）集中在 2010–2022，且多为综述/边缘主题（绿色光通信 Tucker 2010=287引、adaptive optics 综述 Guo 2022=200引、spatial modulation MIMO Yang 2019=119引）——**这些不是"ML 调制切换"**。
- **中文 CNKI**：跨 7 个查询去重约 34 篇学位论文，但**没有一篇在标题层匹配"LSTM/ML 做调制切换"**，大半是 ML/DSP 通用方向（自适应光学、均衡、捕获跟踪、OAM、极化码）。
- **形态判断**：按 TL-12"不少人做至少说明形态可发表"——广义"ML+光通信"形态可发表无疑；但"ML+光通信调制切换"这个精确子题，**发表形态稀薄**，谈不上成熟大方向。

### 调研问题 2：别人具体做了什么？

跨两轮去重后的代表性论文（按场景相关度排序）：

| 标题 | 年/引 | 切什么 | 用什么 ML | 场景 | 增量指标(标题层) | 对手 |
|---|---|---|---|---|---|---|
| Leveraging DL for ACM for LEO satellite-terrestrial (Xia) | 2024/10 | AMC（编码+调制） | DL | LEO 星地 | ACM | 未明 |
| Adaptive Coding and Modulation for Sun Outage Alleviation in Ultradense LEO (Xia) | 2025/3 | AMC | DL | LEO 星地 | 日凌缓解 | 未明 |
| Deep-Learning-Based ModCod Predictor for Satellite Channels (AL MAKARA) | 2024/7 | ModCod 预测 | DL | 卫星(疑似 RF) | ModCod 预测 | 未明 |
| Hybrid Deep Learning-Based Adaptive Modulation for FSO (Sahrab) | 2026/1 | 调制切换 | 混合 DL | FSO | 自适应调制 | 未明 |
| Adaptive Modulation Scheme for Soft-Switching Hybrid FSO/RF (Shao) | 2024/22 | 软切换 | ML | FSO/RF 混合 | 软切换 | 未明 |
| Adaptive Modulation Techniques in FSO Using ML (Arunachalam) | 2024/0 | 调制切换 | ML | FSO | 自适应 | 未明 |
| Deep RL for QoT-Aware RMSA (Asiri) | 2025/20 | 调制+频谱**分配** | DRL | 光纤 EON | RMSA | 未明 |
| ANN-based adaptive modulation for EON (Reihani) | 2022/2 | 调制切换 | ANN | 光纤 EON | EON | 未明 |
| Link handling atmospheric turbulence using LSTM in FSO (Lapsiwala) | 2025/8 | 链路处理(**非切换**) | LSTM | FSO | 链路处理 | 未明 |
| Modulation Format Recognition RL Coherent (Yang) | 2024/1 | 格式**识别**(非切换) | RL | 光纤相干 | 识别 | 未明 |

**几个结构性观察**：

1. **"切换"和"识别"常被混在一起**：大量工作做的是 **modulation format recognition**（识别接收信号的调制格式，是分类问题），不是 **modulation switching/adaptation**（根据信道主动切换发送端调制）。这两个是不同的技术问题。
2. **场景分布**：英文工作大半是**光纤核心网 EON**（routing + modulation + spectrum assignment, RMSA），其次是**FSO**（含大气湍流），再次是 VLC/水下光/认知无线电。
3. **方法分布**：CNN/分类（识别）> 泛"深度学习" > DRL（多用于 EON-RMSA 资源分配）> ANN > LSTM。**LSTM 在调制切换方向极少**——唯一 2 篇 LSTM+FSO 做的是"信号检测/链路处理"非调制切换。
4. **增量指标/对手**：标题层普遍看不出具体 dB/throughput 增量和明确对手（多写"自适应调制"这种自指）——需精读全文才能判断增量形态，但本调研是开放调研不下精读。
5. **DRL 第一轮可能低估**：第二轮补了 DRL 查询，但新增多为 EON-RMSA（资源分配）或 OWC 资源分配，**不是"调制切换"动作本身**——DRL 在"光通信调制切换"这个精确动作上确实少。

### 调研问题 3：学位论文多不多？

**结论：用户"见过别人用 LSTM 做调制切换学位论文"的印象，在本次中文检索（7 个查询）中未得到标题层佐证。**

- 中文 CNKI 跨 7 个查询（自适应调制光通信深度学习 / 调制格式自适应光纤深度学习 / 自由空间光自适应调制 / FSO 调制切换 / 卫星光通信自适应调制 / 链路自适应光通信 / AMC 激光）去重约 34 篇学位论文。
- **标题含 LSTM + 调制切换的学位论文：0 篇**。
- **标题含任意 ML + 调制切换的学位论文：0 篇**。
- 中文论文大半主题：自适应光学（跟"调制"无关）/ DSP 均衡 / 捕获跟踪 / OAM 模分复用 / 极化码 / 大气湍流补偿——是"光通信 + ML/DSP"的广义相邻方向，不是"ML 做调制切换"。

**对用户印象的可能解释**（推测，非结论）：
- 用户记忆的"学位论文"可能是**RF 卫星通信 ACM**（DVB-S2 自适应调制编码）方向——这个在 RF 领域是成熟大方向，学位论文很多，但不是"光通信"。本调研限定光通信，未覆盖 RF-ACM 学位论文。
- 或用户记忆的是**LSTM 做信道预测**（用于辅助 AMC 决策），这类工作存在但不是"调制切换"本身。
- **不排除检索词仍偏**。但换了 7 个中文说法（含"链路自适应""AMC""调制切换""自适应调制"）都搜不出，说明至少在 CNKI 标题层这个精确组合很稀。

**形态判断**：按 TL-12，"别人能写学位论文 ≠ 增量够（换皮风险）"——但这里的情况是**连"别人写了"都没在光通信里找到**，谈不上换皮。RF-ACM 学位论文多，但那是另一个领域。

### 调研问题 4：跟我们场景的关系

**结论：双偏振星地湍流 FSO + ML 调制切换 = 空白。**

跨两轮确认：
- **"双偏振 + 调制切换"**：英文 0 篇，中文 0 篇——**完全缺失**。
- **"星地/LEO + ML + 调制切换/ACM"**：英文约 4–5 篇（Xia 2024/2025 LEO 星地 ACM、AL MAKARA 2024 卫星 ModCod 预测、He Yu 2026 LEO 链路优化），但**除 Ni 2025 外都是 RF/全电卫星链路**，不是激光/FSO 星地。
- **"激光/FSO 星地 + ML + 调制切换"**：唯一弱候选 Ni 2025 *Laser communication base on channel-based autonomous learning and control*（0 引，标题层看不出是否真做调制切换）。
- **"FSO + ML + 调制切换"（不限星地）**：约 3–4 篇（Sahrab 2026 混合 DL、Shao 2024 FSO/RF 软切换、Arunachalam 2024），但都不涉及星地过境/双偏振。

**我们场景在这个领域的位置**：处于明显欠覆盖的角落。"ML 做光通信调制切换"本身小众，"星地 FSO"再切一刀所剩无几，"双偏振"完全没有。

## 结论

### 对 4 个调研问题的回答

1. **规模**：广义"ML for 光通信"成熟大方向（S2 命中 2472）；精确"ML 驱动光通信调制切换"小众新兴（2022–2026，引用<40），谈不上成熟大方向。
2. **别人做了什么**：大半是光纤 EON 的调制格式**识别**（非切换）和 RMSA 资源**分配**（非切换）；真做"切换"的多在 FSO（Sahrab/Shao/Arunachalam）和 LEO 卫星 ACM（Xia，但多为 RF）。LSTM 在切换方向极少。增量指标和对手标题层看不出，需精读。
3. **学位论文**：用户"见过 LSTM 调制切换学位论文"的印象在光通信 CNKI（7 个查询）中**未获标题层佐证**（0 篇）。可能印象来自 RF-ACM 领域或 LSTM 信道预测。
4. **场景关系**：双偏振星地湍流 FSO + ML 调制切换 = **空白**。星地 FSO + ML 调制切换极稀疏（1 弱候选），双偏振完全缺失。

## 对决策的影响

### 本调研是开放调研，不立 Q#，不判 Go/Kill（守 FR-22）

以下是**留待 Step 4a 评估的观察**，不是结论：

1. **空白 ≠ 可做方向**（FR-23）。"双偏振星地 ML 调制切换没人做"只是新颖性证据，须转译成"M 在 C 下因 A 失效"才是问题。
2. **③ 的 oracle 上界（D009）仍是硬约束**。③ 算的是单偏振 LEO 过境 DVB-S2 8 阶 MCS，oracle max 0.09dB（12/12 <0.5dB）。调研发现的"空白"不能无视这个物理事实。若有人想重新提议调制切换方向，仍须回答"为什么这次不同"（③ 的 F3 否决条件）。
3. **③ 未覆盖的角度（PROMPT-002 列出的 4 个），调研有部分信号**：
   - *双偏振下调制切换*：领域空白（新颖性最强，但空白本身不证可做）
   - *ML 预测的其他价值（减少 CSI 反馈/降低切换延迟/鲁棒性）*：调研中看到的 FSO LSTM 工作（Lapsiwala 2025）做的是"链路处理"非吞吐增益，暗示 ML 的价值可能在非 dB 维度——但这要 Step 4a 维度 A/B/D 具体验
   - *连续速率自适应/概率整形连续阶梯*：调研未专门覆盖（N1 已 Kill PS on 16-QAM gain≈0）
4. **用户印象与证据的张力**：用户记得"见过 LSTM 调制切换学位论文"，但 7 个中文查询搜不出。这个张力**不影响**调研结论（结论以证据为准），但记录在此供用户核实记忆来源（是否 RF 领域、是否信道预测非切换）。

### 不需要新建 D###

本调研是 R### research note，结论是"领域现状描述 + 空白确认"，不涉及推翻现有决策或确立新方向。不动 decisions.md。
