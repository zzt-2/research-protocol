# Algorithm box — 缩放酉短导频偏振估计与解复用

## 输入与输出

**输入**：receiver-known 双偏振平衡导频矩阵 `X_p∈C^{2×N_p}`、对应接收导频 `Y_p∈C^{2×N_p}`、双偏振 payload observations `y∈C^{2×N}`。
**输出**：解复用符号 `z∈C^{2×N}`、公共尺度估计 `g_hat`、适用性诊断 `rho`、numerical-valid flag。`rho` 不驱动本章分支。

## 伪代码

```text
Algorithm: Short-pilot scaled-unitary polarization estimation and demultiplexing
1. Validate X_p, Y_p, y: shape=(2,N), all values finite.
2. G ← X_p X_p^H.
3. If det(G)=0: return INVALID / request general-LS-family fallback.
4. H_LS ← Y_p X_p^H G^{-1}       # implemented by linear solve
5. If det(H_LS)=0 or H_LS is nonfinite: return INVALID.
6. [U, diag(s1,s2), V^H] ← SVD(H_LS), with s1≥s2≥0.
7. If s2=0: return INVALID.
8. g_hat ← (s1+s2)/2;  rho ← s1/s2.
9. If g_hat≤0 or any output is nonfinite: return INVALID.
10. H_SU ← g_hat U V^H.
11. W ← V U^H / g_hat.
12. z ← W y.
13. If z is nonfinite: return INVALID; otherwise return z,g_hat,rho,VALID.
```

## 数学身份

对 `H_LS` 的 Frobenius nearest scaled-unitary problem 的解为

`Q*=UV^H,  g*=(s1+s2)/2`，

故 `H_SU=g*Q*`。在 exact balanced pilots 下，`unconstrained LS → 上述投影` 与 direct constrained scaled-unitary LS 是同一 estimator 的两种表述，不得计成两个方法或两项贡献。

## B2 身份审计

B2 对相同 `H_LS=U diag(s1,s2)V^H` 使用 `floor=tau·s1`。在冻结 `tau=1` 时，两个奇异值都变成 `s1`，所以 `H_B2=s1UV^H`、`W_B2=VU^H/s1`。C4 同样采用 `UV^H`，但尺度为 `(s1+s2)/2`。因此 confirmation 的 C4 相对 B2 改善只能归于公共尺度估计，不能归于新的偏振旋转。

## Fail-closed 与 fallback 边界

- 当前实现对 exact rank deficiency、exact zero singular value、NaN/Inf fail closed。
- 当前没有经 development 冻结的 near-zero tolerance 或 `rho≤tau_SU` guard。
- “request general-LS-family fallback”是接口语义；本算法框不声称已实现或验证 near-unitary 自动切换。

## 复杂度

- pilot-LS：形成两个 2×2 矩阵并解一个固定 2×2 线性系统；随 `N_p` 为 `O(N_p)`，固定矩阵部分为常数阶。
- 结构投影：一次 2×2 complex SVD、两个奇异值求均值和固定 2×2 乘法，均为常数阶。
- payload 解复用：2×2 矩阵乘 `N` 个双偏振符号，`O(N)`。
- 不把 Python runtime 或固定小矩阵 proxy 写成硬件时延结论。

公式/实现来源：`scaled_unitary.py:32-88`、`development.py:125-182`、Step4a 报告 `:49-81,156-178`。
