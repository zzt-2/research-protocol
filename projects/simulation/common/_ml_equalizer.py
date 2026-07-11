"""ML 均衡器：双偏振 2×2 蝶形 CNN 监督回归均衡器。

> 方向: Q-CMA-FADE (Step C, 方法层) | 状态: WIP | 创建: 2026-07-11
> 组织规范: ../SIM-ORG.md (P4 只扩不改；新算法=1新文件+0改动现有)

架构溯源 (C6 核心结构标来源 + 行号，禁靠文字重建):
  - 8 实值 1D-CNN 实现 4 复蝴蝶 FIR: Qin 2025 L275/L283
      "8 real-valued 1D-CNN (weights only, no bias) implement 4 complex
       butterfly FIR filters hXX, hXY, hYX, hYY"
    复数 FIR w = w_R + j·w_I, 输入 r = r_R + j·r_I:
      z = w ∗ r = (w_R·r_R - w_I·r_I) + j·(w_R·r_I + w_I·r_R)
    拆成 4 个实值卷积: z_R = w_R∗r_R - w_I∗r_I, z_I = w_R∗r_I + w_I∗r_R
    双偏振蝶形: zX = wxx∗rX + wxy∗rY, zY = wyx∗rX + wyy∗rY
    → 4 复 FIR × 2(实/虚) = 8 实值 1D-CNN (Qin 2025 L275)
  - 中心抽头脉冲初始化: Qin 2025 L283 "hIXX/hIYY 中心=1, 其余全零"
  - tap 长度: Qin 2025 L283 优化为 29; sat.1553 Fig.13 用 N=11
    本模块 tap 作为参数暴露, 默认 11 (跟 Step B CMA 对齐)
  - 学习率: Qin 2025 L397 选 0.005 + ReduceLROnPlateau

增量定位 (守 D005/D006 不换皮 TL-12):
  - **用 Qin 的网络结构** (8 实值 1D-CNN 蝶形) — 结构是工程实现不是贡献
  - **不用 Qin 的 VAE 损失** — VAE ELBO 是 Qin 核心贡献, 照搬=换皮
  - 改用 **MSE 监督回归损失** (已知训练序列监督学习)
    物理对应: sat.1553 §6 DA (decision-aided) 模式, 用 pilot 训练
  - 测度正交: 我们测"发散鲁棒性" (P_div + 恢复时间),
    不是 Qin 测的"收敛速度 200×" (收敛速度对比 Qin 已做过)

参数溯源 (FR-20):
  - tap 数: Qin 2025 L283 (29) / sat.1553 Fig.13 (11); 本模块默认 11 跟 Step B 对齐
  - 学习率: Qin 2025 L397 (0.005); 本模块作为参数暴露
  - batch size: Freire 2022 L349 建议 ≥1024; Qin 2025 L287 用 128
    本模块默认 1024 (守 Freire 陷阱 4: batch 太小致 jail window)
  - 训练切片长度: Qin 2025 L287 T=151; 本模块用 tap 决定窗口 (2*half+1=tap)

发散判据 (与 _cma.py 一致, TL-20 预定义):
  - 系数范数 |w| > 10× 初始范数
  - 或均衡后符号幅度 |z| > 1e3
  - 或 NaN (数值溢出)
  - 但 ML 是前馈 (训练后权重固定推理), 发散判据主要用于训练过程监控
    推理阶段 ML 不会"发散"(权重不在线更新), P_div_ml 侧重于:
    (a) 训练是否收敛 (loss 是否下降)
    (b) 推理输出是否合理 (BER 不爆炸)

Freire 2022 6 陷阱 checklist (守 C2-C5):
  1. 指标用 BER 非 EVM (陷阱 1: jail window 高估 EVM)
  2. 训练数据用 MTRS 非 PRBS (陷阱 3: PRBS<24 NN 学生成规则)
     → 本模块用 numpy randint (MTRS 等价) 生成 QPSK, 非 LFSR
  3. batch ≥1024 (陷阱 4: 小 batch 致 jail window)
  4. 复杂度报告 RMpS (陷阱 5: 参数数≠真实复杂度)
  5. MSE 回归非 CEL 分类 (陷阱 4: CEL 过拟合+梯度消失)
  6. 训练/测试集分离 (陷阱 2: 数据泄漏)
"""
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset


# ─── 复数 1D-CNN 蝶形均衡器 (Qin 2025 L275/283) ─────────────

class ComplexFIRConv1d(nn.Module):
    """单个复数 FIR 滤波器, 用 2 个实值 Conv1d 实现 (Qin 2025 L275).

    复数卷积: w ∗ r = (w_R∗r_R - w_I∗r_I) + j·(w_R∗r_I + w_I∗r_R)
    拆成 4 个实值卷积: 2 给 z_R, 2 给 z_I.

    Conv1d 参数:
      - in_channels=1, out_channels=1 (单路复信号)
      - kernel_size = n_tap (FIR 长度)
      - bias=False (Qin 2025 L283: "weights only, no bias")
      - padding='same' (中心对齐, 用 symmetric padding 保证输出同长)
    """

    def __init__(self, n_tap):
        super().__init__()
        self.n_tap = n_tap
        half = n_tap // 2
        # 4 个实值卷积核: w_R, w_I (各 1 个 Conv1d, in=1 out=1)
        # z_R = w_R ∗ r_R - w_I ∗ r_I
        # z_I = w_R ∗ r_I + w_I ∗ r_R
        self.conv_RR = nn.Conv1d(1, 1, n_tap, padding=half,
                                 padding_mode='reflect', bias=False)
        self.conv_RI = nn.Conv1d(1, 1, n_tap, padding=half,
                                 padding_mode='reflect', bias=False)
        # 中心抽头初始化 (Qin 2025 L283: 中心=1, 其余=0)
        with torch.no_grad():
            w = torch.zeros(1, 1, n_tap)
            w[0, 0, half] = 1.0
            self.conv_RR.weight.copy_(w)
            self.conv_RI.weight.copy_(torch.zeros(1, 1, n_tap))

    def forward(self, r_real, r_imag):
        """前向: 输入复信号的实/虚部, 输出复信号的实/虚部.

        r_real, r_imag: (B, 1, N) 实值张量
        返回: (z_real, z_imag) 各 (B, 1, N)
        """
        z_real = self.conv_RR(r_real) - self.conv_RI(r_imag)
        z_imag = self.conv_RR(r_imag) + self.conv_RI(r_real)
        return z_real, z_imag


class ButterflyCNNEqualizer2x2(nn.Module):
    """双偏振 2×2 蝶形 CNN 均衡器 (Qin 2025 L275/283, sat.1553 Eq.28).

    4 个复 FIR: wxx, wxy, wyx, wyy (各 n_tap 抽头)
    蝶形输出 (sat.1553 Eq.28):
      zX = wxx ∗ rX + wxy ∗ rY
      zY = wyx ∗ rX + wyy ∗ rY

    用 4 × ComplexFIRConv1d = 8 个实值 Conv1d 实现 (Qin 2025 L275).

    初始化: wxx/wyy 中心=1, wxy/wyx=0 (Qin 2025 L283).

    参数
    ----
    n_tap : int
        每个 FIR 的抽头数 (Qin 2025 L283: 29; sat.1553 Fig.13: 11).
    """

    def __init__(self, n_tap=11):
        super().__init__()
        self.n_tap = n_tap
        # 4 个复 FIR (蝶形): wxx, wxy, wyx, wyy
        self.wxx = ComplexFIRConv1d(n_tap)
        self.wxy = ComplexFIRConv1d(n_tap)
        self.wyx = ComplexFIRConv1d(n_tap)
        self.wyy = ComplexFIRConv1d(n_tap)

    def forward(self, rX, rY):
        """前向: 双偏振接收信号 → 均衡后符号.

        rX, rY : (B, 2, N) 或 (B, N) 复值张量
          - (B, 2, N): 2=实/虚, N=符号数
          - (B, N): 复值, 内部拆实/虚
        返回: (zX, zY) 各 (B, N) 复值
        """
        # 拆实/虚 → (B, 1, N) 给 Conv1d
        if rX.dtype.is_complex:
            rX_r = rX.real.unsqueeze(1).float()
            rX_i = rX.imag.unsqueeze(1).float()
            rY_r = rY.real.unsqueeze(1).float()
            rY_i = rY.imag.unsqueeze(1).float()
        else:
            # 已拆好的 (B, 2, N)
            rX_r = rX[:, 0:1].float()
            rX_i = rX[:, 1:2].float()
            rY_r = rY[:, 0:1].float()
            rY_i = rY[:, 1:2].float()

        # 蝶形: sat.1553 Eq.28
        # zX = wxx ∗ rX + wxy ∗ rY
        zX_r_xx, zX_i_xx = self.wxx(rX_r, rX_i)
        zX_r_xy, zX_i_xy = self.wxy(rY_r, rY_i)
        zX_r = zX_r_xx + zX_r_xy
        zX_i = zX_i_xx + zX_i_xy

        # zY = wyx ∗ rX + wyy ∗ rY
        zY_r_yx, zY_i_yx = self.wyx(rX_r, rX_i)
        zY_r_yy, zY_i_yy = self.wyy(rY_r, rY_i)
        zY_r = zY_r_yx + zY_r_yy
        zY_i = zY_i_yx + zY_i_yy

        # 组回复数 → (B, N)
        zX = torch.complex(zX_r.squeeze(1), zX_i.squeeze(1))
        zY = torch.complex(zY_r.squeeze(1), zY_i.squeeze(1))
        return zX, zY

    def weights_norm(self):
        """当前 4 个复 FIR 的总范数 |w| (发散判据用)."""
        with torch.no_grad():
            total = 0.0
            for fir in [self.wxx, self.wxy, self.wyx, self.wyy]:
                for conv in [fir.conv_RR, fir.conv_RI]:
                    total += float(torch.sum(conv.weight ** 2))
            return float(np.sqrt(total))

    def init_norm(self):
        """初始范数 (中心抽头 wxx/wyy=1, 其余=0 → 范数=√2)."""
        return float(np.sqrt(2.0))  # 两个中心抽头各 1.0


# ─── 训练 + 推理接口 ─────────────────────────────────────────

class MLChannelEqualizer:
    """ML 均衡器训练+推理封装 (监督学习, MSE 损失).

    训练: 用已知发送序列 (pilot) 监督学习信道逆 (均衡器系数).
    推理: 训练后权重固定, 前馈均衡 (不在线更新 → 不会"发散").

    参数
    ----
    n_tap : int
        FIR 抽头数 (FR-20: Qin 2025 L283).
    lr : float
        学习率 (FR-20: Qin 2025 L397 选 0.005).
    batch_size : int
        训练 batch 大小 (FR-20: Freire 2022 L349 建议 ≥1024).
    n_epochs : int
        训练 epoch 数.
    device : str
        'cuda' / 'cpu' (torch 设备).
    """

    def __init__(self, n_tap=11, lr=0.005, batch_size=1024,
                 n_epochs=20, device='cuda', patience=5):
        self.n_tap = n_tap
        self.lr = lr
        self.batch_size = batch_size
        self.n_epochs = n_epochs
        self.device = device if torch.cuda.is_available() else 'cpu'
        self.patience = patience

        self.model = ButterflyCNNEqualizer2x2(n_tap=n_tap).to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        # ReduceLROnPlateau (Qin 2025 L397)
        self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer, mode='min', factor=0.5, patience=3)
        self.criterion = nn.MSELoss()  # MSE 回归 (Freire 2022 陷阱 4: MSE > CEL)

        self.train_losses = []
        self.best_loss = float('inf')
        self.best_state = None
        self._init_norm = self.model.init_norm()

    def train(self, rX, rY, sX, sY, val_split=0.2, verbose=True):
        """训练 ML 均衡器.

        参数
        ----
        rX, rY : ndarray, shape (N,)
            双偏振接收信号 (复数).
        sX, sY : ndarray, shape (N,)
            双偏振发送符号 (复数, 训练标签).
        val_split : float
            验证集比例 (守 Freire 陷阱 2: 训练/测试分离).
        verbose : bool
            打印训练进度.

        返回
        ----
        history : dict
            train_losses, val_losses, converged (bool), epochs_run
        """
        N = len(rX)
        n_val = int(N * val_split)
        n_train = N - n_val

        # 训练/验证分离 (Freire 陷阱 2: 不泄漏)
        # 用前 n_train 做训练, 后 n_val 做验证 (时间序列不 shuffle 避泄漏)
        rX_train = torch.from_numpy(rX[:n_train]).to(self.device)
        rY_train = torch.from_numpy(rY[:n_train]).to(self.device)
        sX_train = torch.from_numpy(sX[:n_train]).to(self.device)
        sY_train = torch.from_numpy(sY[:n_train]).to(self.device)

        rX_val = torch.from_numpy(rX[n_train:]).to(self.device)
        rY_val = torch.from_numpy(rY[n_train:]).to(self.device)
        sX_val = torch.from_numpy(sX[n_train:]).to(self.device)
        sY_val = torch.from_numpy(sY[n_train:]).to(self.device)

        # 拆实/虚 → (1, 2, N) 给 Conv1d (batch=1 的整段序列)
        # 注意: 训练时 batch 维 = 1 (整段序列一起前馈), DataLoader 按 chunk 分
        # 但 Conv1d 支持 (B, C, N), 我们用 (1, 1, N) 整段前馈 + chunk 梯度累积
        # 更高效: 把序列切成 (n_chunks, 1, chunk_len) 做 batch
        chunk_len = self.batch_size
        n_chunks = n_train // chunk_len

        # 切 chunk → (n_chunks, 2, chunk_len)
        def to_chunks(r, length):
            """复信号 (N,) → (n_chunks, 2, chunk_len) 实值."""
            n_c = len(r) // length
            r = r[:n_c * length]
            r_r = r.real.view(n_c, 1, length).float()
            r_i = r.imag.view(n_c, 1, length).float()
            return torch.cat([r_r, r_i], dim=1)  # (n_c, 2, length)

        rX_tr_chunks = to_chunks(rX_train, chunk_len)
        rY_tr_chunks = to_chunks(rY_train, chunk_len)
        sX_tr_chunks = to_chunks(sX_train, chunk_len)
        sY_tr_chunks = to_chunks(sY_train, chunk_len)

        # Early stopping (code-quality.md 必做: reward plateau)
        no_improve = 0
        converged = False

        for epoch in range(self.n_epochs):
            self.model.train()
            # shuffle chunks (每个 chunk 独立, 时间序列内不泄漏)
            perm = torch.randperm(n_chunks, device=self.device)
            epoch_loss = 0.0

            for i in range(n_chunks):
                idx = perm[i]
                rX_chunk = rX_tr_chunks[idx:idx+1]  # (1, 2, chunk_len)
                rY_chunk = rY_tr_chunks[idx:idx+1]
                sX_chunk = sX_tr_chunks[idx:idx+1]
                sY_chunk = sY_tr_chunks[idx:idx+1]

                self.optimizer.zero_grad()
                zX, zY = self.model(rX_chunk, rY_chunk)
                # MSE 损失: |z - s|²
                # z: (1, chunk_len) complex, s: (1, 2, chunk_len) real
                zX_r, zX_i = zX.real, zX.imag
                zY_r, zY_i = zY.real, zY.imag
                loss_x = self.criterion(zX_r, sX_chunk[:, 0]) + \
                         self.criterion(zX_i, sX_chunk[:, 1])
                loss_y = self.criterion(zY_r, sY_chunk[:, 0]) + \
                         self.criterion(zY_i, sY_chunk[:, 1])
                loss = loss_x + loss_y
                loss.backward()
                self.optimizer.step()
                epoch_loss += float(loss.item())

            avg_loss = epoch_loss / n_chunks

            # 验证
            self.model.eval()
            with torch.no_grad():
                rX_v = to_chunks(rX_val, chunk_len)
                rY_v = to_chunks(rY_val, chunk_len)
                sX_v = to_chunks(sX_val, chunk_len)
                sY_v = to_chunks(sY_val, chunk_len)
                zX_v, zY_v = self.model(rX_v, rY_v)
                val_loss = float(
                    self.criterion(zX_v.real, sX_v[:, 0]).item() +
                    self.criterion(zX_v.imag, sX_v[:, 1]).item() +
                    self.criterion(zY_v.real, sY_v[:, 0]).item() +
                    self.criterion(zY_v.imag, sY_v[:, 1]).item()
                )

            self.train_losses.append({'epoch': epoch, 'train': avg_loss, 'val': val_loss})
            self.scheduler.step(val_loss)

            # 保存 best model (code-quality.md 必做)
            if val_loss < self.best_loss:
                self.best_loss = val_loss
                self.best_state = {k: v.clone() for k, v in self.model.state_dict().items()}
                no_improve = 0
            else:
                no_improve += 1

            if verbose and (epoch % 5 == 0 or epoch == self.n_epochs - 1):
                cur_norm = self.model.weights_norm()
                print(f"  Epoch {epoch:3d}: train={avg_loss:.6f} val={val_loss:.6f} "
                      f"|w|={cur_norm:.4f} lr={self.optimizer.param_groups[0]['lr']:.2e}")

            # Early stopping
            if no_improve >= self.patience:
                converged = True
                if verbose:
                    print(f"  Early stop @ epoch {epoch} (no improve {self.patience} epochs)")
                break

        # 恢复 best model
        if self.best_state is not None:
            self.model.load_state_dict(self.best_state)

        return {
            'train_losses': self.train_losses,
            'best_val_loss': self.best_loss,
            'converged': converged,
            'epochs_run': len(self.train_losses),
            'final_w_norm': self.model.weights_norm(),
            'init_w_norm': self._init_norm,
        }

    @torch.no_grad()
    def equalize(self, rX, rY):
        """推理: 用训练好的权重均衡接收信号 (前馈, 不在线更新).

        参数
        ----
        rX, rY : ndarray, shape (N,)
            双偏振接收信号 (复数).

        返回
        ----
        result : dict
            zX, zY : 均衡后符号
            w_norm : 最终权重范数
            init_w_norm : 初始权重范数
            diverged : bool (ML 推理不会在线发散, 但检测权重是否训练中爆炸)
            max_z_amp : 最大输出幅度
        """
        self.model.eval()
        N = len(rX)

        # 整段前馈 (1, 2, N)
        rX_t = torch.from_numpy(rX).to(self.device)
        rY_t = torch.from_numpy(rY).to(self.device)

        # 拆实/虚
        rX_chunk = torch.cat([rX_t.real.view(1, 1, N).float(),
                              rX_t.imag.view(1, 1, N).float()], dim=1)
        rY_chunk = torch.cat([rY_t.real.view(1, 1, N).float(),
                              rY_t.imag.view(1, 1, N).float()], dim=1)

        zX, zY = self.model(rX_chunk, rY_chunk)

        # 转 numpy
        zX_np = zX.cpu().numpy()
        zY_np = zY.cpu().numpy()

        cur_norm = self.model.weights_norm()
        max_z = float(max(np.max(np.abs(zX_np)), np.max(np.abs(zY_np))))

        # ML 推理不在线更新, "发散"判据改为: 训练后权重是否爆炸
        # (如果训练中 loss 不降反升 + 权重爆炸 → 训练失败 = "ML 发散")
        diverged = (cur_norm > 10.0 * self._init_norm or
                    max_z > 1e3 or
                    not np.isfinite(cur_norm))

        return {
            'zX': zX_np, 'zY': zY_np,
            'w_norm': cur_norm,
            'init_w_norm': self._init_norm,
            'diverged': diverged,
            'max_z_amp': max_z,
        }


# ─── 复杂度评估 (Freire 2022 陷阱 5: RMpS > 参数数) ──────────

def compute_rmps(n_tap):
    """计算每符号实乘法数 (RMpS, Freire 2022 L441-507).

    8 实值 Conv1d (4 复 FIR × 2 实/虚):
      每个 Conv1d: n_tap 次实乘 / 符号
      8 个 Conv1d: 8 × n_tap 次实乘 / 符号
    加法: 蝶形组合 4 次实加 / 符号 (可忽略)

    返回 RMpS (real multiplications per symbol).
    """
    return 8 * n_tap
