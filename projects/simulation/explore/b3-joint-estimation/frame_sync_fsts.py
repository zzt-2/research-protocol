"""帧同步 FSTS 相关峰（②，INVARIANT 14）。

jphot FSTS 帧同步（L101）:
- X/Y 极化用不同 TS（跨极化共轭对称）
- TS 先做 FS 定位起点，同时对齐分集支路时延
- 相关峰搜索（跨极化共轭相关 peak detection）

jphot TS 结构（L107/L289）:
- BN=16 符号一段，BL=20（共 320 总长 = BN·BL? 或两段）
- 跨极化共轭积消除调制相位
"""
import numpy as np


def fsts_frame_sync(branches, ts_template, bl=20):
    """FSTS 帧同步 + 支路时延对齐（jphot-L101 FS 相关峰搜索）。

    Args:
        branches: 各支路接收信号 list[np.ndarray]
        ts_template: FSTS 训练序列模板（X/Y 极化交织共轭对称，jphot-L107）
        bl: 块长（jphot-L289 BL=20）

    Returns:
        offsets: 各支路 TS 起点偏移（对齐支路时延）
        corr: 各支路相关峰序列（诊断用）
    数学: 跨极化共轭相关 peak detection，jphot-L101 "TS is firstly used for FS"
    """
    ts = np.asarray(ts_template, dtype=complex)
    N_ts = len(ts)
    offsets = []
    corrs = []

    for branch in branches:
        rx = np.asarray(branch, dtype=complex)
        N_rx = len(rx)
        # 滑动相关：对每个候选起点做共轭相关
        # jphot 跨极化共轭积消除调制（此处单极化简化：用 TS 模板做匹配相关）
        max_offset = N_rx - N_ts
        if max_offset <= 0:
            offsets.append(0)
            corrs.append(np.zeros(1))
            continue

        corr_curve = np.zeros(max_offset + 1)
        for i in range(max_offset + 1):
            seg = rx[i:i + N_ts]
            # 共轭相关（去载波残余相位后取模）
            prod = seg * np.conj(ts)
            corr_curve[i] = np.abs(np.sum(prod))

        offset = int(np.argmax(corr_curve))
        offsets.append(offset)
        corrs.append(corr_curve)

    return offsets, corrs


def build_fsts_template(ts_total=320, bl=20, bn=16):
    """构建 jphot FSTS 模板（跨极化共轭对称结构）。

    jphot-L107: X/Y 极化用不同 TS，共轭对称。
    此处简化：生成一个已知伪随机 QPSK 序列作模板（sandbox 信号生成与信道一致即可）。

    Args:
        ts_total: TS 总长（jphot-L299 = 320）
        bl: 块长（jphot-L289 = 20）
        bn: 每段符号数（jphot-L299 = 16）

    Returns:
        ts_template: 复数 TS 模板
    """
    # 用固定 seed 生成可复现 QPSK 伪随机序列
    rng = np.random.RandomState(2024)
    bits = rng.randint(0, 4, ts_total)
    # QPSK 星座点
    constellation = np.array([1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j]) / np.sqrt(2)
    ts = constellation[bits]
    return ts
