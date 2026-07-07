# [S003] 阶段 0.2 数学同族性 + 0.3 架构定性（子 agent 数值重建 + 同族性分析 + 架构定性）

> 2026-07-08 | 阶段：B7 阶段 0.2+0.3 | 状态：0.2 通过（D002）+ 0.3 通过（D003），0.4-0.6 交下对话

## 目标

执行 H002 阶段 0.2（数学同族性 + B7 映射数值重建）+ 0.3（架构定性前馈 vs 环路）。用户先问了方向性问题（B7 是啥方向），澄清后继续。

## 记录

### 用户方向澄清（对话开头的疑问）

用户问："这个到底是啥方向？我没记错的话湍流这块定时同步做的很少啊?"

主线澄清：**B7 是 Doppler FOE（频偏估计）方向，不是定时同步，也不涉湍流**。B7 锚论文实验室用三角波激光器模拟纯 Doppler，无幅度/相位衰落建模。B7-Q1 作为独立会议候选（跟 NDA-ML 并列），不强行绑湍流叙事。用户确认"继续阶段 0（按原计划）"。

voice.md 已登记（profile "能力边界/知识盲区"再次验证——用户对物理层 DSP 自承"不咋了解"委托主线判断）。

### 阶段 0.2a 数值重建 B7 Fig.1a 映射（子 agent 1）

派子 agent 用 Gardner TED 公式扫 Doppler 频偏，数值重建 poster Fig.1a 那张 omitted 的图。

**关键结论**（V5 主线独立重算确认）：
- G(f_D) 以 **baud rate B = 25 GHz** 为周期
- 确定性铁证：G(0) = 0.132142（主线重算 = 子 agent 报 0.13214，bit-exact）
- FFT 主频能量占比：无噪 95.9% / OSNR 17dB 90.7%（主线重算，>50% 阈值）
- U 形曲线，最小值 @ 13GHz（半 baud 处），2:1 映射（解释了 poster 双候选算法）
- poster "(−B,B) 可逆"描述不精确（实际半周期 (0,B/2) 单调可逆），但算法自洽

**V5 核查记录**：子 agent 原始数字可信，归因合理（标注推测）。子 agent 初版 OSNR 17dB 单次噪声实现使能量比掉到 61.6%，改 6× 平均后稳定——数值实验噪声处理影响结论，已记录。

### 阶段 0.2b 数学同族性分析（子 agent 2，重派成功）

派子 agent 分析 B7 vs Gardner 1986 / VV / BPS 的数学关系。

**关键结论**：
- **B7 vs Gardner 1986 = 弱同族 (B)**：共享底层 TED 公式 `e=Re{mid·(curr−prev)*}`，但任务正交（B7 做 FOE 估频偏 f_D，1986 做 STR 检测定时误差 τ）+ 后处理不同构
- **B7 vs VV/BPS = 非同族**：任务不同（FOE vs CPR）+ 核心运算无共享结构（B7 S-curve 峰反演 vs VV mean-angle of rx^M vs BPS argmin decision-distance）
- **不存在 NDA-ML 式 mean-angle 等价陷阱**：NDA-ML 栽跟头是因跟 VV 同为 mean-angle + 同为 CPR，B7 两者都不共享
- **残留风险**：B7 未给 TED_gain(f_D) 解析式，无法 100% 排除跟 Leven M-th-power FOE [7] 等价 → sandbox 前补解析推导 + Leven 对比

### 阶段 0.2 判定（D002）

通过，进 0.3。理由：INVARIANT 11 要的深度数学同族性检查完成，结论 (B) 弱同族非 (C) 强同族陷阱；0.2a 数值重建验证 B7 机制真实（实测 > 文字）。

### 阶段 0.3 架构定性（主线分析）

**D006 红线精确边界**（读上游决策）：D006 Kill 的是"把湍流相位 φ_T 主动纳入载波同步环路 TF 联合建模"，**不是"所有反馈环"**。

**B7 DSP 链拆解**（poster 行 47 `proposed FOE → Gardner TR → MIMO EQ → MP FOC → CPR`）：
- proposed FOE（B7 创新）：poster 原算法是开环扫频，前馈合法
- Gardner TR（定时恢复）：反馈环，但跟踪符号时钟 τ 不是湍流相位 φ_T
- B7 锚方法本身不涉湍流（`_B7-gardner-ted-increment.md` 关键发现 5）

**架构决策（D003）**：
1. **proposed FOE = 前馈扫频**（避免环路 TF 纠缠 D006）
2. **Gardner TR = 保留反馈环**（跟踪 τ 不是 φ_T，不撞 D006；用户代码 Tx2Rx.m L176-214 复用）
3. **载波同步 CPR = 前馈 VV/BPS 或反馈 PLL，禁建模湍流相位**（Paillier 经验性忽略）

**B7 创新点在前馈化后仍成立**：0.2a 数值重建就是前馈扫频验证的，周期相关照样成立。

**不撞 D006 的三重理由**：B7 不涉湍流 + FOE 前馈无环路 TF + Gardner TR 是定时环非载波同步环。

### 阶段 0.3 判定（D003）

通过，进 0.4 公平对照框架。

### common 现有实现的概念错误（发现但未修，记一笔）

读 `projects/simulation/common/_recovery.py` 发现：
- `psa_foe_recovery`（L435）函数名叫 PSA FOE 但实现的是 **pilot-aided FOE（pilot 差分相位法）**，**不是 B7 poster 的 PSA = Power-Spectrum-Asymmetry（谱不对称法，Vieira 2023）**。概念错误。
- 这个函数是之前为 B7 预建的 baseline，但跟 B7 的真 baseline 不是一回事。sandbox 阶段做 PSA FOE baseline 时需重写（用谱不对称法），不能直接用这个 pilot-aided 版本。
- 本轮不修（阶段 0 不写代码），记进 0.4 / sandbox 的债务。

## 决策引用

- **D002**（新建）：B7 数学同族性 = 弱同族 (B) + 机制数值验证成立，0.2 通过
- **D003**（新建）：B7-Q1 架构 = FOE 前馈扫频 + Gardner TR 保留反馈环，不撞 D006，0.3 通过
- 无其他新建

## 范围确认

- 本轮是否在 scope boundary 内：**是**（0.2+0.3 是 H001/H002 阶段 0 的项目）
- 未修改 common/（阶段 0 不写代码，守 INVARIANT 6）
- 未进 sandbox（守 profile 第 9 次防线）

## 后续

1. **0.4 公平对照框架**（下对话）：fair gain 定义 + 工作点 BER 2e-2 vs HD-FEC + PSA FOE 怎么公平对照。注意 PSA FOE 真实现需重写（common 现有 `psa_foe_recovery` 是 pilot-aided 非谱不对称法，概念错）
2. **0.5 参数真相源**：Doppler range 0-23GHz / OSNR 10dB / LEO Doppler rate（读原文数值）/ 符号率线宽（跟 NDA-ML 统一 LASER_LW 单字段）。每个参数标 source_type + source + audit_flag
3. **0.6 文件组织**：`explore/b7-gardner-ted-foe/` 目录结构落盘确认
4. **残留风险带进 sandbox**：B7 TED_gain(f_D) 解析式缺失，sandbox 前补解析推导 + Leven 对比
5. **环境注意**：本机无 `~/.venvs/torch/`，用 `python`（scoop python311，numpy/scipy/mpl 齐全）

### 已知风险

- B7 映射数值重建已验证 0-23GHz 单偏振 QPSK；sandbox 若扩 DP-QPSK 或更大范围需重跑数值重建
- common 的 `psa_foe_recovery` 概念错（pilot-aided 非谱不对称），sandbox PSA FOE baseline 需重写
- Gardner TED 在 common 的 `gardner_ted_recovery`（L382）是标准形式（非用户代码的去直流变种），sandbox 时决定用哪个版本
