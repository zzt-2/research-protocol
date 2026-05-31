# 对话提示词：Ch2/Ch3 证据缺口定向补充检索

> 产出文件: `.sessions/thesis-direction-pivot/S010-ch2-ch3-evidence-gap.md`
> 优先级: 高
> 依赖: S008(A0检查v5), S006(Ch2+Ch3精读)
> 预计耗时: 30-40分钟

## 背景

硕士论文"星地激光通信信号处理关键技术研究"。S008 A0 检查发现 Ch2/Ch3 虽然比 Ch4 证据充分，但都存在**场景外推**问题——核心实证数据不是在目标场景（LEO 星地 SP-QPSK）下获得的。

## 核心问题

**Ch2 和 Ch3 的现有证据，是否遗漏了更匹配目标场景的文献？**

## Ch2 证据缺口

### 当前证据

| 论文 | 场景 | 调制 | 缺口 |
|------|------|------|------|
| Amirabadi 2019 | FSO GG 湍流（通用） | **16-QAM** | 不是 SP-QPSK |
| Rustum 2026 | FSO+LEO OFDM | 64-QAM/QPSK | OFDM 非单载波 |
| Mohammed 2026 | FSO GG 湍流 | BPSK/QPSK | 无数值对比 |

**关键缺口**：
1. 16-QAM → SP-QPSK：星座点数减少（16→4），DL 估计可能更容易。但 SP（单极化）vs DP（双极化）有区别吗？
2. Amirabadi 的 DL 是 MLP 结构，是否有更新的架构（CNN/Transformer/ResNet）用于 FSO CE？
3. 是否有论文专门做过 QPSK 下的 DL 信道估计 vs 传统方法对比？

### 搜索策略

1. **SP-QPSK / QPSK FSO 信道估计**：
   - "QPSK channel estimation free space optical"
   - "SP-QPSK coherent FSO receiver"
   - "QPSK pilot-free channel estimation optical"

2. **DL 信道估计 架构进展**（2023-2026）：
   - "deep learning channel estimation optical communication 2024 2025"
   - "CNN ResNet transformer channel estimation FSO"
   - "neural network channel estimation coherent optical 2024"

3. **无导频/盲信道估计 FSO**：
   - "pilot-free channel estimation FSO coherent"
   - "blind channel estimation free space optical QPSK"
   - "无导频 信道估计 自由空间光 相干检测"

### 判断标准

- 如果找到 **SP-QPSK 下的 DL CE 论文** → Ch2 场景匹配度大幅提升
- 如果找到 **DL CE vs LS/MMSE 在 QPSK 下的直接对比** → A0-1 从 [外推] 升级为 [实证]
- 如果找到 **pilot-free CE 在 QPSK 下不work 的证据** → 致命信号

## Ch3 证据缺口

### 当前证据

| 论文 | 场景 | 调制 | 缺口 |
|------|------|------|------|
| Brandao 2024 | 地面 1.8km | **DP-QPSK** | 不是 LEO 星地 |
| Safi 2019 | 理论 | 通用 | 无 FSO 验证 |
| Ahmad 2026 | 仿真 FSO | QPSK | 用 DNN，非传统自适应 |

**关键缺口**：
1. 地面 → LEO：链路距离（1.8km → 500km+）、几何、Doppler 完全不同
2. DP-QPSK → SP-QPSK：双极化 vs 单极化对功率预补偿的影响
3. 是否有**卫星/LEO FSO 功率控制**的文献？

### 搜索策略

1. **LEO/卫星 FSO 功率控制**：
   - "LEO satellite FSO power control"
   - "satellite optical communication power allocation"
   - "星地激光通信 功率控制"
   - "LEO optical downlink power adaptation"

2. **FSO 功率预补偿/预加重**：
   - "FSO power pre-compensation turbulence"
   - "optical link power pre-emphasis fading"
   - "free space optical transmit power adaptation"

3. **LEO FSO 链路预算与自适应**：
   - "LEO FSO link budget adaptive"
   - "satellite-ground optical link margin"
   - "星地激光通信 链路预算 自适应"

### 判断标准

- 如果找到 **LEO FSO 功率自适应/预补偿论文** → Ch3 从 [外推] 升级为 [实证]
- 如果找到 **卫星 FSO 功率控制的工程限制**（如 EIRP 限制）→ Ch3 可行性确认
- 如果找到 **LEO 反馈延迟致命的证据** → Ch3 致命信号

## 输出格式

```markdown
# [S010] Ch2/Ch3 证据缺口补充检索

## Ch2 补充检索

### 新发现文献

| 论文 | 场景 | 调制 | 与 Ch2 关系 | 匹配度提升？ |
|------|------|------|-----------|------------|

### A0-1 状态更新
- 检索前：[外推]（16-QAM → SP-QPSK）
- 检索后：[实证] / [外推] / 无变化

### 新风险（如有）

## Ch3 补充检索

### 新发现文献

| 论文 | 场景 | 调制 | 与 Ch3 关系 | 匹配度提升？ |
|------|------|------|-----------|------------|

### A0-1 状态更新
- 检索前：[外推]（地面 → LEO）
- 检索后：[实证] / [外推] / 无变化

### 新风险（如有）

## 总结

### Ch2 证据强度变化
### Ch3 证据强度变化
### 是否需要更新 S008
```

## 约束

- 每个搜索方向 3-5 组关键词，每组读前 5 条结果摘要
- 不下载全文、不精读，仅从标题/摘要判断
- 重点关注 2022-2026 年的论文（老论文 S006 已覆盖）
- 中文输出
- 30 分钟内完成
- 搜索工具：用 `tools/search` 脚本，不用 WebSearch
- 如果需要 WebSearch，必须在子 agent 中执行
- **实事求是**：没找到就是没找到，不要为了"找到好消息"而放宽匹配标准
