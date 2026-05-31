# 对话提示词：Ch2+Ch3 关键基线论文验证

> 产出文件: R009-ch2-ch3-baseline-verify.md
> 优先级: 高

## 背景

硕士论文"星地激光通信信号处理关键技术研究"。

上一轮检索（未用项目工具）报告了以下关键基线论文，需要用项目工具验证其**存在性、内容准确性、引用数**。

### Ch2 信道估计待验证论文

| 论文 | 年份 | 声称内容 | 声称引用 |
|------|------|---------|---------|
| Amirabadi "Deep Learning for channel estimation in FSO" | 2019 | DNN信道估计GG模型 | 61 |
| Elfiky "Symbol Detection and CE for SOC using NN and Autoencoder" (IEEE TMLCN) | 2024 | NN估计+AE检测, LEO+GG | 16 |
| Rustum "Hybrid STA with FNN/CNN for robust CE in FSO+LEO OFDM" (IET Comm) | 2026 | STA+DL两阶段, BER达10^-6 | 0 |
| Mohammed "FSO turbulent channel estimation based on CNN+BiLSTM" (JOC) | 2026 | CNN+BiLSTM, 强湍流鲁棒 | 0 |

### Ch3 信道均衡待验证论文

| 论文 | 年份 | 声称内容 | 声称引用 |
|------|------|---------|---------|
| Almogahed "Performance improvement of MDM-FSO with DFE" | 2022 | MMSE-DFE, 10Gbps | 28 |
| Ahmad "Robust FSO with OAM+DNFIS+DCNN" (Scientific Reports) | 2026 | DL均衡BER降55% | 0 |
| 佟欣 "空间激光通信中变步长CMA-LMS均衡算法" | 2020 | CMA-LMS混合 | 10 |
| Balakrishnan "OFDM-FSO with ZF equalization over GG turbulence" | 2026 | GG+OFDM+ZF | 0 |

## 检索任务

### 任务A: Ch2 论文验证

```bash
cd /mnt/d/code/study/research-protocol

# A1: 验证 Amirabadi 2019
bash tools/search --query "Amirabadi deep learning channel estimation free space optical 2019" --limit 10

# A2: 验证 Elfiky 2024
bash tools/search --query "Elfiky symbol detection channel estimation space optical neural network autoencoder" --limit 10

# A3: 验证 Rustum 2026
bash tools/search --query "Rustum STA FNN CNN channel estimation FSO LEO OFDM 2026" --limit 10

# A4: 验证 Mohammed 2026
bash tools/search --query "Mohammed CNN BiLSTM FSO turbulent channel estimation 2026" --limit 10

# A5: 中文核心文献验证 — 曹明华2020 GG+FTN
bash tools/search --source cnki --query "曹明华 Gamma-Gamma 超奈奎斯特" --limit 10

# A6: 中文核心文献验证 — 孙晶2018 相干+GG
bash tools/search --source cnki --query "孙晶 相干光通信 Gamma-Gamma 分集" --limit 10
```

### 任务B: Ch3 论文验证

```bash
cd /mnt/d/code/study/research-protocol

# B1: 验证 Almogahed 2022 DFE
bash tools/search --query "Almogahed DFE MMSE MDM free space optical 2022" --limit 10

# B2: 验证 Ahmad 2026 DL均衡
bash tools/search --query "Ahmad OAM DNFIS DCNN FSO equalization 2026" --limit 10

# B3: 验证佟欣2020 CMA-LMS
bash tools/search --source cnki --query "佟欣 CMA-LMS 空间激光通信" --limit 10

# B4: 验证Balakrishnan 2026 OFDM+ZF
bash tools/search --query "Balakrishnan OFDM ZF equalization FSO Gamma-Gamma 2026" --limit 10

# B5: 补充检索 — GG湍流+相干PSK+均衡方法对比（核心创新空白验证）
bash tools/search --query "equalization comparison coherent PSK atmospheric turbulence FSO" --limit 20

# B6: 中文补充 — 相干检测+均衡
bash tools/search --source cnki --query "相干检测 自由空间光 均衡" --limit 20
```

### 任务C: 创新空白验证

上一轮报告了以下创新空白，需要确认是否真实：

**Ch2空白**：星地链路DL信道估计的系统性研究不足，传统LS/MMSE/Kalman在GG下对比缺失
**Ch3空白**：GG湍流+相干PSK+多种均衡方法(CMA/MMSE/DFE/MLP)的系统性对比几乎找不到

```bash
# C1: 验证Ch2空白
bash tools/search --query "LS MMSE Kalman channel estimation comparison Gamma-Gamma FSO" --limit 20

# C2: 验证Ch3空白
bash tools/search --query "CMA MMSE DFE equalization comparison coherent FSO turbulence" --limit 20

# C3: 中文验证Ch3空白
bash tools/search --source cnki --query "信道均衡 方法对比 激光通信" --limit 20
```

## 产出格式

```markdown
# [R009] Ch2+Ch3 关键基线论文验证

## Ch2 论文验证结果

### Amirabadi 2019
- 是否找到：是/否
- 实际标题：
- 期刊/年份：
- 引用数（实际）：
- 核心内容确认：[一句话]
- 与声称是否一致：是/否（差异点）

### [其他论文同格式]

## Ch3 论文验证结果
[同上格式]

## 创新空白验证
### Ch2空白
- 搜索结果摘要
- 空白是否确认：是/否/部分

### Ch3空白
- 搜索结果摘要
- 空白是否确认：是/否/部分

## 综合结论
1. 哪些论文确认可用作基线？
2. 哪些论文不存在或内容与声称不符？
3. 创新空白是否真实？
4. 对开题报告写作的建议
```

## 约束

- **必须用项目工具**：`bash tools/search` 和 `bash tools/blit`，不要用 web search
- 从项目根目录调用：`cd /mnt/d/code/study/research-protocol && bash tools/...`
- 中文输出
- 3000字以内
- 产出文件：`.sessions/thesis-direction-pivot/R009-ch2-ch3-baseline-verify.md`
