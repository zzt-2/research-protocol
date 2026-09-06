# 第四章方法推导与算法卡

> 形态：公式卡、步骤卡和边界卡；不是连续正文。

## 1. 输入—输出卡

| 项目 | 内容 |
|---|---|
| 输入 | 已知双偏振导频 $X_p\in\mathbb C^{2\times N_p}$、接收导频 $Y_p\in\mathbb C^{2\times N_p}$、接收载荷 $Y\in\mathbb C^{2\times N}$ |
| 共同中间量 | 普通 LS 估计 $\hat H_{LS}$、奇异值分解 $U\operatorname{diag}(s_1,s_2)V^H$、结构方向 $\hat Q=UV^H$ |
| 主变体输出 | 前向误差尺度 $\hat g_F$、解复用矩阵 $W_F$、两路符号 $Z_F=W_FY$ |
| 强变体输出 | 导频重构校准量 $\hat a$、解复用矩阵 $W_P$、两路符号 $Z_P=W_PY$ |
| 基线输出 | 调参奇异值下限矩阵 $W_\tau$ 与两路符号 $Z_\tau=W_\tau Y$ |
| 接口 | 两路 post-demux、pre-CPR 符号；可送往后续每偏振 CPR，但未联合验证 |

## 2. 共同估计卡

### 2.1 普通 LS

\[
\hat H_{LS}=Y_pX_p^H\left(X_pX_p^H\right)^{-1}.
\]

### 2.2 共同结构方向

\[
\hat H_{LS}=U\operatorname{diag}(s_1,s_2)V^H,\qquad s_1\ge s_2>0,
\]

\[
\hat Q=UV^H,\qquad \rho=\frac{s_1}{s_2}.
\]

- $\hat Q$：两种结构尺度判据共享的方向。
- $\rho$：只报告结构偏离程度，不驱动在线分支。
- exact balanced pilots 下，LS 后投影与直接 constrained scaled-unitary LS 为同一 estimator 的两种表述。

## 3. 三条比较支路

### 3.1 主变体：前向误差尺度

**目标：**

\[
(\hat g_F,\hat Q)=\arg\min_{g\ge0,\,Q^HQ=I}\left\|\hat H_{LS}-gQ\right\|_F^2.
\]

**闭式解：**

\[
\hat g_F=\frac{s_1+s_2}{2},\qquad
\hat H_F=\hat g_F\hat Q,
\]

\[
W_F=\hat H_F^{-1}=\frac{\hat Q^H}{\hat g_F}=\frac{VU^H}{\hat g_F}.
\]

**身份：** 信道域结构投影；无经验调参；正文主变体。

### 3.2 强变体：导频重构尺度

**基准逆矩阵：** 使用 $\tau=1$ 的奇异值下限，

\[
W_0=\frac{VU^H}{s_1}=\frac{\hat Q^H}{s_1}.
\]

**当前导频的基准输出：**

\[
Z_p^{(0)}=W_0Y_p.
\]

**接收端闭式校准：**

\[
\hat a=\max\left(0,
\frac{\operatorname{Re}\langle Z_p^{(0)},X_p\rangle_F}
{\|Z_p^{(0)}\|_F^2}
\right),
\]

\[
W_P=\hat aW_0,\qquad Z_P=W_PY.
\]

**身份：** 输出域导频重构标定；$\hat a$ 逐观测变化；强变体与尺度判据消融。

**语义限制：** 实现返回的 `h_hat` 是 $\hat a$ 校准前的继承量，不能称为该变体的校准后信道估计。

### 3.3 独立基线：调参奇异值下限

\[
\tilde s_i=\max(s_i,\tau s_1),\qquad
W_\tau=V\operatorname{diag}(\tilde s_1^{-1},\tilde s_2^{-1})U^H.
\]

| 正式切片 | $\tau$ |
|---|---:|
| 中等湍流，$N_p=2$ | 0.5 |
| 中等湍流，$N_p=4,8,16$ | 1.0 |
| 弱/强湍流，$N_p=2$ | 1.0 |

- 参数来自独立调参样本。
- $\tau=1$ 时方向与结构变体同为 $UV^H$；$\tau=0.5$ 时不能再概括为“只差公共尺度”。

## 4. 可直接排版的算法步骤卡

```text
Input: Xp, Yp, Y; selected receiver branch
1. Validate shapes and finite values.
2. Compute H_LS = Yp Xp^H (Xp Xp^H)^(-1).
3. Compute H_LS = U diag(s1,s2) V^H; require s2 > 0.
4. Set Q = U V^H and diagnostic rho = s1/s2.
5a. 前向误差尺度支路：gF=(s1+s2)/2; WF=Q^H/gF.
5b. Pilot-reconstruction branch: W0=Q^H/s1;
    Zp0=W0Yp; a=max(0, Re<Zp0,Xp>F / ||Zp0||F^2); WP=aW0.
5c. Tuned-floor baseline: si_tilde=max(si,tau*s1);
    Wtau=V diag(1/si_tilde) U^H.
6. Apply only the selected comparison branch: Z=WY.
7. Return two demultiplexed streams and validity status.
```

> 步骤 5a/5b/5c 是实验中的并列比较支路，不是已实现的运行时选择器。

## 5. Fail-closed 卡

| 条件 | 处理 | 未覆盖项 |
|---|---|---|
| 导频 Gram 矩阵 exact rank deficient | 拒绝估计 | 未冻结 near-zero 容差 |
| LS/SVD 非有限或 $s_2\le0$ | 拒绝产生解复用矩阵 | 未验证自动 fallback |
| 导频重构分母非正/非有限 | 拒绝校准 | 不用固定 1.0 替代失败值 |
| 任一输出包含 NaN/Inf | 返回 invalid | 不宣称连续时变跟踪能力 |

## 6. 复杂度卡

| 模块 | 复杂度 | 可写边界 |
|---|---|---|
| 形成 pilot-LS | $O(N_p)$ + 固定 2×2 求解 | 不从 Python runtime 推硬件时延 |
| SVD/方向—尺度计算 | 固定 2×2 操作 | 常数阶，不等于零成本 |
| 导频重构校准 | $O(N_p)$ | 只使用 receiver-visible pilots |
| 载荷解复用 | $O(N)$ | 三支路均需 2×2 矩阵乘载荷 |

## 7. 公式—实现指针

| 公式/动作 | 实现指针 |
|---|---|
| LS 与 Frobenius scaled-unitary projection | `scaled_unitary.py:44-87` |
| 导频重构闭式校准 | `production_core.py:387-404` |
| 三支路接收机动作 | `production_core.py:407-470` |
| 正式参数映射 | `tables/ch4-formal-configuration.md` |
| 正式结果 | `data/ch4-formal-required-snr.csv` |
