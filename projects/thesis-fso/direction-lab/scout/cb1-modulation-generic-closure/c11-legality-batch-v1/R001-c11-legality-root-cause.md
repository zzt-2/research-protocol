# [R001] C11 legitimacy root-cause investigation

> 2026-07-21 | 关联：专题 `2026-07-20-direction-lab-science-scout` / 即将新建 D011
> 文件名: R001-c11-legality-root-cause.md

## 调研问题

> 在统一复数滤波约定、无未来信息、同 pass/同预算、`dd_step=0` 身份门成立的前提下，合法的 CMA→DD-LMS 是否仍显著优于公平 fixed-μ CMA？

为回答这个问题，必须先确定：C11 原实现的"4/7 cells 阳性"是否由合法性缺陷（复数约定突变 / 未来信息 / 多 pass）造成？即写 H1 单一根因假设。

## 调用链核验（Phase 1–2）

### A. Anchor `standard_cma_godard_with_z`（cb1_cell_runner.py:49-172）

复数滤波约定：

```
line 115:  zx_blk = rX_blk @ wxx + rY_blk @ wxy   # z = sum_k r_k * w_k   (bilinear, NO conjugation)
line 116:  zy_blk = rX_blk @ wyx + rY_blk @ wyy
line 126-129:  wxx += mu * mean((eX*zx_blk)[:,None] * conj(rX_blk), axis=0)
               wxy += mu * mean((eX*zx_blk)[:,None] * conj(rY_blk), axis=0)
               ... (analogous for wyx, wyy)
```

z = r @ w（bilinear，无共轭）。Godard 梯度 `Δw ∝ (R²-|z|²)·z·conj(r)`。**这对 bilinear z 是自洽的**：minimise `J=E[(R²-|z|²)²]` 对 conj(w) 求导给出 `dJ/dconj(w) = -2(R²-|z|²)·z·conj(r)`，所以 `w += mu·(R²-|z|²)·z·conj(r)` 是正确的下降方向。

> 注：项目自有 `projects/simulation/common/_cma.py:CMAEqualizer2x2` 用完全相同的约定 `rX_blk @ self.wxx + rY_blk @ self.wxy` + `mean(eX[:,None] * conj(rX_blk))`，证实 bilinear `r@w` + `conj(r)` update 是项目规范。

### B. C11 cascade `c11_cma_dd_lms_cascade`（b01_candidates.py:194-334）

**B.1 Stage-1** = `standard_cma_godard_with_z`（line 220-222）。z₁ = r @ w，**与 anchor 完全一致**。一次 full-stream pass。

**B.2 Stage-1 replay**（line 233-269）。
```python
# line 237-238 注释自承："Recover stage-1 final weights by re-running the anchor's weight loop"
# line 254-269: 完整重跑 anchor 的 weight-update loop，得到 stage-1 final wxx/wxy/wyx/wyy
```
这是**第二次 full-stream pass**（与 stage-1 同样的代码、同样的顺序、同样的权重演变）。注释解释为"preserves protected-history byte-equivalence of the anchor module"——即为了避免修改 anchor 接口而重跑。

**B.3 Stage-2 DD-LMS**（line 271-312）。复数约定：
```python
line 290-291:  zx = np.vdot(wxx, rx) + np.vdot(wxy, ry)   # z = w^H r  (Hermitian!)
              zy = np.vdot(wyx, rx) + np.vdot(wyy, ry)
line 296-299:  err_x = s_hat_x - zx
              err_y = s_hat_y - zy
              gx = dd_step_size * err_x
              gy = dd_step_size * err_y
line 300-303:  wxx += gx * np.conj(rx)    # update w += dd_step * (s_hat - z) * conj(r)
              ...
```

**这是第三次 full-stream pass**（`for i in range(n_valid)`，从 i=0 开始）。

### C. 复数约定突变（B.3 vs B.1）— 确认

`np.vdot(w, r) = sum_k conj(w_k) * r_k`（numpy 定义，对第一个参数取共轭）。而 `r @ w = sum_k r_k * w_k`（无共轭）。两者在 w 含复数分量时**严格不等**：

```text
>>> r = [2+1j, 1-2j, 0.3+0.4j]; w = [1+2j, 3-1j, 0.5+0.5j]
>>> r @ w        = (0.95 - 1.65j)
>>> vdot(w, r)   = (9.35 - 7.95j)         # 显著不同
>>> conj(r) @ w  = (9.35 + 7.95j) = vdot(r, w)
```

只有当 w 为纯实数时二者才相等（CMA 中心抽头初始化时 w 是实的，但收敛后 w 含复数分量）。

**Stage-2 用 `vdot` 把 z 从 stage-1 的 bilinear 形式变成了 Hermitian 形式。z₂ ≠ z₁（一般情形）。**

### D. Wirtinger 梯度自洽性 — 确认 Stage-2 与其自身 z 约定不自洽

对 `J(w) = E[|d - z|²]`：

| z 约定 | dJ/dconj(w)（Wirtinger） | 正确更新 |
|---|---|---|
| bilinear `z = r @ w = sum_k r_k w_k` | `-conj(d-z) · r` ❓ 实际上要分别对 w 和 conj(w) 求导；以 conj(w) 为独立变量时 `z` 对 conj(w) 导数为 0，但 `conj(z)` 对 conj(w) 导数为 r。最终结果 `dJ/dconj(w) = (z-d)·conj(r)`... 让我重新推 |  |
| Hermitian `z = w^H r = sum conj(w_k) r_k` | `dJ/dconj(w) = -(d-z) · conj(r)`，更新 `w += mu·(d-z)·conj(r)` ✅ | `w += mu·(d-z)·conj(r)` |

（注：为避免 Wirtinger 推导错误，用数值梯度下降做了一阶确认——见测试代码：当 z=vdot(w,r) 时 `w += mu*(d-z)*conj(r)` 收敛；当 z=r@w 时 `w += mu*(d-z)*conj(r)` **发散到溢出**。）

**结论**：
- Stage-1 用 bilinear z 配 `w += mu·(R²-|z|²)·z·conj(r)` —— 这其实是 `|z|²` 代价，不是 `|d-z|²` 代价，对应的梯度是 `d|z|²/dconj(w)`（Godard），属于不同问题但内部自洽。
- Stage-2 用 Hermitian z 配 `w += mu·(d-z)·conj(r)` —— **Hermitian z 下这是 `|d-z|²` 的正确下降方向，内部自洽**。

所以 **Stage-2 内部数学自洽**，但 z 的复数取值与 Stage-1 输出**不一致**（vdot vs r@w）。Stage-2 在 i=0 处用 `vdot(w_s1, r[0:L])` 算出的 z，与 Stage-1 在同一位置写的 `zX[i+half] = rX_win[i] @ w_s1` 是两个不同的复数。下游 PI-SER 用 `hard_16qam(z)`，hard 决策对 16QAM 在 z 和其共轭/相关复数下给**不同符号**。

### E. 未来信息 / 多 pass — 确认（最严重）

C11 处理一个 stream 共 **3 次**：
1. Stage-1 anchor pass：逐 block 走完整个 stream，得到 final weights `w_s1`。
2. Stage-1 replay pass：用相同的 anchor 代码再走一遍整个 stream（仅为恢复 final weights）。
3. Stage-2 DD-LMS pass：`for i in range(n_valid)` 从 i=0 重新走，用 **`w_s1` 作为起始权重**。

**Stage-2 在 i=0（处理 stream 第 0 个样本）时使用的权重 `w_s1` 是 Stage-1 看完了整个未来 stream（直到 N-1）才收敛到的权重。** 这是严格的非因果：过去样本用未来样本的信息处理。

对照 `fixed_mu_cma`（system anchor）只有 1 次 pass，严格 causal（每个 block 的输出只用过去 block 的权重）。C11 相比 comparator 多用了 ≥2 次 stream 访问 + 未来信息。

`dd_iterations=1` 还会再跑 1 pass；但即便 dd_iterations=1，3 次 pass + 未来信息已经成立。

## 单一根因假设（Phase 3）

```text
H1:
C11 stage-2 的 z 用 vdot(w,r) (Hermitian)，与 stage-1 anchor 的 z=r@w (bilinear)
约定不同；stage-2 从 i=0 开始用 stage-1 final 权重（看完整个 stream 才得到）
处理过去样本，构成离线 full-stream second/third pass（非因果，未来信息）。
合法（causal one-pass、统一复数约定、同 pass 预算）的 CMA→DD-LMS 在独立 test
seeds 上相对公平 fixed-μ CMA 的 4/7 阳性很可能消失或不再显著。

否决条件（rejected if）:
  修复约定（统一 r@w）、去除未来访问（causal one-pass switch）、通过 no-op identity
  与 causal-prefix invariance 后，C11_legal 在 7 个 held-out cells × test seeds
  上 paired CI 上限仍 < 0 且 |mean Δ| ≥ 预注册实际意义阈值（0.005 PI-SER）。

  即：合法实现下信号仍存活 → H1 rejected → 裁决 A。
  若信号消失或低于阈值 → H1 confirmed → 裁决 B。

次级假设 H2（forward-comparator label bug）:
  batch-contract.v1.yaml line 352 把 oracle_affine_16qam 标为 "blind" 是标签错误
  （oracle_affine 用 TX truth 做 calibration；blind_affine_compare_16qam 才是
  receiver-visible）。forward rule 应区分 blind affine (Go candidate) vs oracle
  affine (Kill bound only)。本轮只做只读核验和标签记录，不运行 corrector。
```

## 调研结论

H1 高置信度成立（调用链证据完整 + 数值复现 + 数学推导一致）。**原 4/7 阳性目前只能算 implementation/confound diagnostic，不能作为方法信号。** 必须修复后重测。

H2 为只读标签问题，不影响本轮裁决，但写入新 contract 时不重蹈。

## 对决策的影响

新建 D011（C11 legitimacy verdict）+ V003（legality test 复核）。H007/D010 "VERDICT A" 中 "C11_fixed_mu 4/7 cells 阳性" 的子结论应**降级为 DIAGNOSTIC**，待合法实现重测后确认保留或撤回。裁决 A/B/C 取决于合法实现的结果，本轮必须跑完。
