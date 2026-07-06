"""探索性 MVE 脚本区 (gw-feasibility §4a 维度 D 最小可行实验).

每个子目录是一个独立 MVE, 与 simulation/experiments/ (毕设正式仿真) 区分:
  - 脚本可复用 ../common/ 资产 (gg_block, qam16 等), 但本身是临时验证脚本
  - "可用临时脚本, 不需正式仿真环境" (gw-feasibility §D)
  - 非论文级正式产物; 结论支撑 §4a Go/Kill 决策即可

命名约定: 子目录用 {方向}-{方法} 连字符形式 (如 n1-pcs-gain). 含连字符故不可作
Python 包 import; 子脚本用 importlib 加载同目录主模块 (见 _validate_estimator.py).

当前:
  n1-pcs-gain/   N1 离线静态 PCS (MB) 在 GG 湍流下 AIR gain — §4a D MVE FAIL (S012/D007)
"""
