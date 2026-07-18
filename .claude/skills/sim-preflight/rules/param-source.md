# 参数真相源统一（T3 扩展规则）

> 新增 v1.2.0（2026-07-07）。本文件是 T3「参数溯源」的**精确缺口补强**——T3 守住了"参数必须从 params.py 导入 + 标 AuditFlag"，但**没守住"同一物理量跨场景从单一字段读"**。本规则补这两个失败模式。

## 触发证据（本次根因）

2026-07-07 载波同步 NDA-ML 项目发现：激光线宽（combined linewidth）这一个物理量，AWGN 路径从 `simulator/_b11_params.py:CLW_B11=500kHz` 派生 `SIGMA2_P_B11`，湍流路径从 `common/_config.py:LASER_LW=10kHz`（即 `params.py:SystemParams.LASER_LW`）派生。**两个源差 50 倍**，导致：
1. 同一仿真器内线宽参数不一致（AWGN=500kHz / 湍流=10kHz）
2. 简报写"激光线宽 500kHz"对 AWGN 成立、对湍流是错的（命中导师意见：场景描述与实验参数不一致）
3. 单点（500kHz）结论被误当通用结论（500kHz 湍流下 NDA 崩塌，但那是参数组合不真实的假象）

证据行号：
- `simulator/_b11_params.py:39` `CLW_B11 = 500e3`
- `params.py:80` `LASER_LW: float = 10e3`（audit_flag=WARNING）
- `common/_channel.py:17` `def doppler_phase(N, ..., lw=LASER_LW)` —— **函数默认参数固化**
- `simulator/sc_nda_ml_sim.py:65,74` `awgn_wiener_channel` 读 `P.SIGMA2_P_B11`（与湍流不同源）

## 两个失败模式（T3 没覆盖的）

### 失败模式 A：函数默认参数固化

```python
# ❌ 错误：LASER_LW 在 import 时绑定到默认参数，patch 模块属性无效
from ._config import LASER_LW
def doppler_phase(N, f_res=F_RESIDUAL, f_dot=DOPPLER_HIGH, lw=LASER_LW):
    ...
# 想改线宽时 patch common._channel.LASER_LW 无效，必须 patch doppler_phase.__defaults__
```

**问题**：参数真相源被"冻结"在函数定义时刻，调用方无法从 params.py 单一字段统一控制，外部 sweep 脚本被迫用 monkey-patch `__defaults__` 这种 hack（见 `run_linewidth_sweep.py:70-84`）。

**正确做法**：默认参数留 `None`，函数体内从 params.py 读：
```python
def doppler_phase(N, f_res=None, f_dot=None, lw=None):
    from params import SimulationConfig
    _c = SimulationConfig()
    f_res = f_res if f_res is not None else _c.doppler.F_RESIDUAL
    f_dot = f_dot if f_dot is not None else _c.doppler.DOPPLER_HIGH
    lw = lw if lw is not None else _c.system.LASER_LW
    ...
```

### 失败模式 B：跨模块同义常量派生

```python
# ❌ 错误：同一物理量"激光线宽"有两个数值源
# _b11_params.py（AWGN 路径用）
CLW_B11 = 500e3
SIGMA2_P_B11 = 2 * np.pi * CLW_B11 * T_S_B11

# params.py（湍流路径用）
class SystemParams:
    LASER_LW: float = 10e3   # 差 50 倍！
```

**问题**：同一物理量在不同模块用不同常量名 + 不同数值，跨场景比较时各自取各自的值，结果不可比。

**正确做法**：单一真相源。`params.py` 定义 `LASER_LW`（或合并为 `CLW`），所有路径（AWGN/湍流/sweep）都从这一个字段读。若不同场景确实需要不同线宽（如 B11 OFDM 25GBaud vs 星地单载波 2.5GBaud），必须显式建模为两个字段（`LASER_LW_OFDM` / `LASER_LW_SINGLE_CARRIER`），各自标 AuditFlag + 文献源，**禁止一个字段两个数值**。

## 自检命令（开始任何仿真任务前跑）

```bash
cd /d/code/study/research-protocol

# 1. 函数默认参数固化：找 def 签名里直接绑定的参数（非 None/非容器）
grep -rn "def .*=[^N]" projects/simulation/common/ --include="*.py" | \
  grep -v "=None\|=True\|=False\|=\[\]\|={}\|=()" | \
  grep -v "__defaults__"

# 2. 跨模块同义常量：物理量名相同但定义在多处
#    （线宽/符号率/噪声方差 这类高频混淆项）
grep -rn "LASER_LW\|CLW\|linewidth\|R_SYM\|BAUD\|T_S\b" \
  projects/simulation/ --include="*.py" | grep -v "import\|#"

# 3. 函数默认参数 = 模块常量（最危险，import 时冻结）
grep -rn "def [a-z_]*([^)]*=[A-Z_]" projects/simulation/ --include="*.py"
```

任一匹配 → **中断**（见 `interrupt.md` 第 9 条），向用户澄清"这个参数的真相源是哪个字段"。

## 前置门控 checklist（补充 tech.md）

开始任何代码任务前，T3 之外再加：

- [ ] 我要用的物理量（线宽/符号率/噪声/衰落），在 params.py 里只有**一个**字段定义（若多个，已确认它们是显式区分的不同场景，标注清楚）
- [ ] 我不会把模块级常量绑到函数默认参数上（默认参数留 None，函数体内读 params.py）
- [ ] 我写 sweep/ablation 脚本时，参数注入通过传参或显式重新初始化 SimulationConfig，不用 monkey-patch `__defaults__`

## 与 T3 / TL-13 的关系

| 规则 | 守什么 | 不守什么 |
|------|--------|----------|
| **T3 参数溯源** | 参数值有文献来源 + 标 AuditFlag | ❌ 不守"同一物理量单一字段" |
| **TL-13 信道共享** | 信道生成函数共用（`generate_shared_realization*`）| ❌ 不守"信道函数的参数从哪来" |
| **本规则（参数真相源统一）** | 同一物理量跨场景从单一字段读 + 函数默认参数不固化 | ✅ 补上 T3 和 TL-13 的交集缺口 |

本规则是 T3 + TL-13 的**交集补强**：T3 管"值有来源"，TL-13 管"信道函数共用"，本规则管"共用的信道函数读的参数也必须共用同一字段"。
