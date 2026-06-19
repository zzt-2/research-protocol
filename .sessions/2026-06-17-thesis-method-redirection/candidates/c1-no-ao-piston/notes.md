# C1 候选：A3 换设定去 AO 复活（pilot CPE 攻 piston 相位）

> 候选状态: **Killed（D001，2026-06-18）** | 门控日期: 2026-06-17 起，2026-06-18 Kill
> 本文件集中记录 C1 的所有门控/讨论/验证（按候选聚合约定）

## 候选定义

前序 A3（pilot CPE 补 AO 残余相位）死于"AO 把残余相位抹平到 negligible"（前序 D010）。C1 的赌注：**去掉 AO**，让 piston 相位（AO 本就不补的模式）变回主导损伤，给 pilot CPE 创造攻击空间。

## 门控历程

### Step 1（2026-06-17）：Kill 点 PASS（有保留）

无 AO baseline 有源（Belmonte 2009 / Paillier / JOSA 2017）；无 AO 主导损伤含 piston 相位（A3 pilot CPE 可攻）。保留：piston 必须进 DSP（多模/阵列接收，非 SMF 单耦否则 -23dB 砸信号）。与 C3 正交（piston vs tilt）。

### Step 2（2026-06-18）：FR-21 门控——数学推导 + 子 agent 验证 → Kill

**方法**：先纸笔（b 路径）分接收架构算上界，单耦无缝就 Kill；单耦判不清再派子 agent（a 路径）精读 Belmonte 2009 取 σ²_φ。

**结果**：数学推导 + 子 agent 验证合取判定 C1 Kill，**全程零参数拍脑袋**。

#### 数学推导（核心，可自证）

Paillier L68-70 混频效率 $\mathcal{C}(t) = \int_P E_{LO}^*(r,t) E_{RX}(r,t) dr$，$\rho(t)=|\mathcal{C}(t)|^2$。

接收场 Zernike 相位分解：$E_{RX}(r,t) = A(t)\exp(i(a_0(t)\cdot Z_0 + \sum_{k\ge 1} a_k(t) Z_k(r)))$，其中 $Z_0=1$ 是 piston。

代入取模：

$$\rho(t) = |A(t)|^2 \cdot \left|\int_P E_{LO}^*(r) \exp\!\big(i\sum_{k\ge 1} a_k Z_k(r)\big) dr\right|^2$$

**$a_0$（piston）完全从 ρ 消失**，因为 $|e^{ia_0}| \equiv 1$。

→ **数学事实**：piston 作为空间均匀相位，在单孔径 SMF 耦合的 ρ 里贡献为零。piston 只出现在 $\arg\mathcal{C}(t)$（载波相位）里。

#### 三层赌注全堵

| 层 | C1 的赌注 | 验证结果 | 来源 |
|---|---|---|---|
| ① | 去 AO → piston 相位变大 → 有缝 | AO 本来就不补 piston（SH 零空间 + 主动剔除），去 AO 对 piston 是 no-op | 子 agent 调研：Poyneer OSTI / Yue Sensors 21(10):3364 / DEPS NPS / Torres 2025 PhD；Paillier L96 引 Robert 2016 |
| ② | piston 够大，pilot CPE 能补换 dB（SMF 单耦） | 数学证 piston 对 ρ 零贡献 | 本轮数学推导 |
| ③ | 退一步作载波相位补（= A3 机制） | DPLL 能跟、negligible；且 ① 又说去 AO 不改 piston → = A3 死法重演 | Paillier L206（本地 verified）；前序 D010 |

#### 核心洞察

**C1 和 C3 攻的是同一组 Zernike 模式的不同名字**：去 AO 真正释放的是 tip/tilt/defocus/高阶（C3 攻的），不是 piston。C1 作为独立候选无新增攻击面——C3 已经在量级上 PASS。

### 子 agent 调研摘要（2026-06-18，≤600s）

验证"AO 是否校正 piston"，结果高置信：

- **Q1（AO 是否校正 piston）= 否（高置信，4 源独立一致）**
  - Shack-Hartmann 测局部斜率，piston 导数处处为零 → 传感器物理上看不见 piston
  - piston（+ 通常 tip/tilt）主动从 Zernike 控制矩阵剔除
  - "不校正" = 根本不进校正目标（零空间），不是"想校正但校不准"
- **Q2（AO 是否改 piston 方差）= 否（高置信定性）**：AO 不把 piston 纳入控制目标 → 加 AO 与不加 AO 对 piston 统计量相同

**未验证项（诚实，不影响判定）**：
- piston 方差常数 C 精确数值（Noll 1976 表格未逐行核对，口径不一）
- "AO-on vs AO-off 下 σ²_piston 数值相同"的显式并排表未直接看到
- Robert 2016（PhysRevA 93, 033860）正文未取到（APS 付费），仅 Paillier 二手引述核实存在
- Belmonte & Kahn 2009 正文未取到（opg.optica.org webReader 500），仅摘要

→ 判定只依赖"去 AO 不改 piston"的定性结论，不依赖数值，未验证项不阻塞。

## C1 最终状态

- Kill 点（2026-06-17）：PASS（有保留）
- FR-21 上界门控（2026-06-18）：**Kill**（数学 + 子 agent 合取，三层全堵）
- **C1 Killed（D001）**

## 不要做（继承到后续候选评估）

- ❌ 把 piston 当 SMF 单耦攻击对象（数学证零贡献）
- ❌ 假设"去 AO 改 piston 统计"（AO 本不补 piston）
- ❌ A3 换设定复活路径（去 AO 不释放 piston，只释放 tilt，归 C3）

## 衍生

**C6（多模/阵列分集接收下的 piston）占位挂起**（D002）：唯一能救 piston 的路径是换接收架构。新候选，不是 C1 续命。本轮不评估，C3 定下来再回头。
