# Landscape — 星地激光通信全景表

> 生成 2026-06-21 | S004 地勘产出 | 子 agent 检索 tools/search × 6 query | 主线合并落盘
> 方法论位置：S003 地勘前置 Step 0。本表是「领域在做什么」的全景视图，不是批评视角，不是候选清单。
> 子地带从结果涌现，不预设。缝潜力初判仅凭 abstract 字面证据，**初判不是结论**。

## 检索元数据

| query | 原始命中 | 存档 |
|-------|---------|------|
| satellite optical communication | 30 | search-archive/2026-06-21/landscape-satellite-optical-communication.json |
| satellite laser communication | 30 | search-archive/2026-06-21/landscape-satellite-laser-communication.json |
| LEO optical downlink | 30 | search-archive/2026-06-21/landscape-leo-optical-downlink.json |
| free-space optical satellite | 30 | search-archive/2026-06-21/landscape-free-space-optical-satellite.json |
| space-to-ground optical link | 30 | search-archive/2026-06-21/landscape-space-to-ground-optical-link.json |
| satellite optical ground station | 30 | search-archive/2026-06-21/landscape-satellite-optical-ground-station.json |

**统计**：6 query × 30 = 180 raw → 165 去重唯一（15 cross-query dups）→ **2019+ = 137 条**（<2019 = 21 条入附录，unknown year = 7 条保留）。

**IEEE blit 通道失败**：本机出口 IP 被 IEEE 封锁（HTTP 418，主线 curl 独立复测确认），校园网 IP 未生效，未跑任何 blit query（0/50 quota 消耗）。本轮仅靠 API 源覆盖——但 API 已命中 33/165 条 IEEE venue 内容，覆盖度可接受。换校园网环境后可补 blit。

**检索障碍**：SerpAPI 全程报 `google-search-results not installed, skipped`（6 query 均失败）；S2 + OpenAlex + Exa 正常。年份筛 2019+，Exa year 空时从 abstract regex 补。

## 子地带涌现分布（post-2019, multi-tag, 关键观察）

```
  65  地面站/OGS/硬件/终端
  48  网络层/路由/调度
  47  信道建模/闪烁/湍流
  46  ATP/指向/PAT/捕获
  35  在轨演示/任务 (TBIRD/OSIRIS/LCRD/DSOC)
  27  调制/复用 (OAM/WDM/PDM/OFDM/PAM4/PPM)
  18  QKD/量子
  15  AO/自适应光学/波前
  10  相干/自相干检测
   7  语义/AI/DL/ML
   7  载波同步/恢复  ← 5 次失败死轴，地勘里几乎不涌现
   7  编码/FEC/交织
   2  信道估计/均衡   ← 另一死轴，极度稀疏
```

**方法论价值（S004 质量评估核心）**：地勘全景照出——之前 5 次撞死的轴（载波同步 7 条 / 信道估计 2 条）在整个领域其实是**冷区**，热区在地面站/网络层/ATP/调制复用。这印证了 S002「热点都在死轴」的尴尬——死轴之所以是死轴，可能正因为它本就是窄冷区，撞 5 次也没涌出足够候选。

## 主表（137 条，≥2019，按年份降序）

| # | 年 | 子地带 | 做的事(标题) | 湍流 | baseline 是谁 | 验证 | 缝潜力 |
|---|----|--------|------|------|--------------|------|--------|
| 1 | 2026 | 地面站/OGS/硬件/终端 / QKD/量子 | Astrolight's Greek Ground Station Speeds Optical Data Transmissions / Microwaves & RF | 未明确 | 未明确 | 未明确 | 🟡 abstract 无缝信号，待精读 |
| 2 | 2026 | 信道估计/均衡 | Clustering-assisted channel estimation for free-space optical satellite communication | 未明确 | 未明确 | 未明确(abstract 缺失) | 🟡 abstract 缺失，待精读 |
| 3 | 2026 | ATP/指向/PAT/捕获 | Free Space Optical (FSO) Communication for 6G and Non-Terrestrial Networks | 弱 | 未明确 | 未明确 | 🟢 abstract 自陈: #### enhanced security

narrow laser beams are difficult to intercept or jam, making fso s |
| 4 | 2026 | 链路预算/系统级 | Free-space optical communication | 未明确 | 未明确 | 未明确 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 5 | 2026 | 网络层/路由/调度 / 在轨演示/任务 / 链路预算/系统级 | Kepler Successfully Launches First Tranche of Optical Relay | 强 | 未明确 | 实测 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 6 | 2026 | 网络层/路由/调度 / 地面站/OGS/硬件/终端 / 在轨演示/任务 / QKD/量子 | Next-generation optical ground station for fast and secure connectivity ready to begin ope | 未明确 | 未明确 | 实测 | 🟡 abstract 无缝信号，待精读 |
| 7 | 2026 | 信道建模/闪烁/湍流 / 调制/复用 / 网络层/路由/调度 / 信道估计/均衡 / AO/自适应光学/波前 / 语义/AI/DL/ML / 链路预算/系统级 | Robust high-capacity free-space optical communication using OAM-based structured light and | 强 | conventional methods (abstract 泛指) | 仿真 | 🟢 abstract 自陈: atmospheric turbulence (at), which causes beam distortion, intensity fading, and intermoda |
| 8 | 2026 | QKD/量子 / 链路预算/系统级 | Systematic Analysis and Design of Lunar–Earth Optical Communication System Based on Phase- | 未明确 | 未明确 | 实测/综述 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 9 | 2026 | ATP/指向/PAT/捕获 / 信道建模/闪烁/湍流 / 地面站/OGS/硬件/终端 / 在轨演示/任务 / 编码/FEC/交织 / 相干/自相干检测 / 链路预算/系统级 | TBIRD: Two Years Demonstrating 200 Gbps Optical Downlink | 强 | 未明确 | 综述 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 10 | 2026 | 调制/复用 / 语义/AI/DL/ML / 链路预算/系统级 | Terahertz OAM spatial beams propagation in a 400Gbps IsOWC system employing M-ZCC OCDMA /  | 未明确 | pin pd, the high data rate of 16 × 20gbps is attai | 仿真 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 11 | 2026 | ATP/指向/PAT/捕获 / 地面站/OGS/硬件/终端 / 在轨演示/任务 / 相干/自相干检测 / 链路预算/系统级 | Why an independent ground segment matters, discover PL-GSS | 弱 | 未明确 | 实测 | 🟢 abstract 自陈: sometimes it’s a patchwork of systems acquired over time, from different vendors, each one |
| 12 | 2026 | 地面站/OGS/硬件/终端 | World's smallest deployable operational optical ground station proves capability in succes | 未明确 | 未明确 | 实测 | 🔴 abstract 自陈成熟/广泛采用 |
| 13 | 2026 | ATP/指向/PAT/捕获 / 信道建模/闪烁/湍流 / 地面站/OGS/硬件/终端 / 在轨演示/任务 / 链路预算/系统级 | X-lumin Achieves Roundtrip Optical Transmission to LEO Satellite Using 15cm Portable Termi | 强 | one-way transmission: the signal must traverse atm | 实测 | 🔴 abstract 自陈成熟/广泛采用 |
| 14 | 2025 | 网络层/路由/调度 / 地面站/OGS/硬件/终端 / 在轨演示/任务 / 相干/自相干检测 / AO/自适应光学/波前 / 链路预算/系统级 | A 2.8 Gbps self-referencing interference optical receiver experimental validation with Alp | 弱 | 未明确 | 实测 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 15 | 2025 | 信道建模/闪烁/湍流 / 调制/复用 / 链路预算/系统级 | A Comprehensive Review Of Satellite Communication System And RF-FSO Wireless Technologies  | 强 | 未明确 | 综述 | 🔴 abstract 自陈成熟/广泛采用 |
| 16 | 2025 | 信道建模/闪烁/湍流 / 调制/复用 / 地面站/OGS/硬件/终端 / 链路预算/系统级 | A Simulated 1000-km LEO Satellite-to-Ground Station Laser Communication Using a 1.8-km OWC | 强 | 未明确 | 仿真 | 🟡 abstract 无缝信号，待精读 |
| 17 | 2025 | ATP/指向/PAT/捕获 / 地面站/OGS/硬件/终端 / QKD/量子 / 链路预算/系统级 | ASA OGS - University Innsbruck - Astrosysteme | 弱 | 未明确 | 未明确 | 🔴 abstract 自陈成熟/广泛采用 |
| 18 | 2025 | 地面站/OGS/硬件/终端 / 链路预算/系统级 | Assessment of CIEMAT’s Plataforma Solar de Almeria as a ground station site for optical LE | 强 | 未明确 | 未明确 | 🟡 abstract 无缝信号，待精读 |
| 19 | 2025 | 信道建模/闪烁/湍流 | Atmospheric modeling of free-space optical transmission: satellite downlinks and horizonta | 强 | 未明确 | 未明确(abstract 缺失) | 🟡 abstract 缺失，待精读 |
| 20 | 2025 | ATP/指向/PAT/捕获 / 信道建模/闪烁/湍流 / 调制/复用 / 网络层/路由/调度 / 载波同步/恢复 / 相干/自相干检测 / 链路预算/系统级 | Challenges and Opportunities in Free Space Optical Satellite Communication | 强 | conventional methods (abstract 泛指) | 未明确 | 🔴 abstract 自陈成熟/广泛采用 |
| 21 | 2025 | 地面站/OGS/硬件/终端 | Design and Evaluation of a Miniature Optical Downlink Terminal for Secure, High-Speed LEO- | 未明确 | 未明确 | 未明确(abstract 缺失) | 🟡 abstract 缺失，待精读 |
| 22 | 2025 | 地面站/OGS/硬件/终端 / 链路预算/系统级 | Design, analysis and verification of thermal control system for satellite laser communicat | 未明确 | 未明确 | 未明确(abstract 缺失) | 🟡 abstract 缺失，待精读 |
| 23 | 2025 | ATP/指向/PAT/捕获 / 信道建模/闪烁/湍流 / 调制/复用 / 相干/自相干检测 / AO/自适应光学/波前 / 链路预算/系统级 | E2E Physical Layer and Link Analysis for High-Throughput Satellite Optical Communication | 强 | 未明确 | 解析 | 🔴 abstract 自陈成熟/广泛采用 |
| 24 | 2025 | 地面站/OGS/硬件/终端 / QKD/量子 | ESA-funded Optical Ground Station for fast and secure laser satellite communications begin | 未明确 | 未明确 | 未明确 | 🔴 abstract 自陈成熟/广泛采用 |
| 25 | 2025 | 网络层/路由/调度 / 链路预算/系统级 | ESTOL: ESA Specifications for Terabit/sec Optical Links  - ESA CSC: Connectivity & Secure  | 未明确 | 未明确 | 综述 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 26 | 2025 | 网络层/路由/调度 / 链路预算/系统级 | Earth Observation Satellite Downlink Scheduling With Satellite-Ground Optical Communicatio | 未明确 | the existing downlink scheduling algorithms | 仿真 | 🟢 abstract 自陈: consistent growth in the number of high-resolution earth observation satellites (eoss) pos |
| 27 | 2025 | ATP/指向/PAT/捕获 / 信道建模/闪烁/湍流 / 地面站/OGS/硬件/终端 | Experimental Emulation of LEO Downlink OFLs Affected by Turbulence and Pointing Jitter | 强 | 未明确 | 实测 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 28 | 2025 | 网络层/路由/调度 / 地面站/OGS/硬件/终端 / 在轨演示/任务 / 链路预算/系统级 | First Transmission of Mission Data Using 1.5 μm Optical Inter-Satellite Communication: Pre | 未明确 | 未明确 | 未明确 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 29 | 2025 | 网络层/路由/调度 / 语义/AI/DL/ML | Free Space Optical Links Scheduling and Routing in Satellite Networks: A Safe Reinforcemen | 未明确 | conventional approaches, the proposed rl approach  | 未明确 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 30 | 2025 | 信道建模/闪烁/湍流 / 调制/复用 / 网络层/路由/调度 / 地面站/OGS/硬件/终端 / 语义/AI/DL/ML / 链路预算/系统级 | Free Space Optical Semantic Communication for Satellite Remote Sensing Image Transmission | 强 | the traditional systems, without incurring additio | 仿真/实测 | 🔴 abstract 自陈成熟/广泛采用 |
| 31 | 2025 | 调制/复用 | Frontiers / A ground-to-GEO-to-LEO satellite optical wireless communication link based on  | 弱 | conventional methods | 仿真 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 32 | 2025 | 信道建模/闪烁/湍流 / AO/自适应光学/波前 | GPU-Accelerated Multilayer Turbulence Simulation for Modeling of Space-to-Ground Optical L | 强 | freely available turbulence propagation tools | 仿真 | 🔴 abstract 自陈成熟/广泛采用 |
| 33 | 2025 | ATP/指向/PAT/捕获 / 信道建模/闪烁/湍流 / 网络层/路由/调度 / 地面站/OGS/硬件/终端 / 在轨演示/任务 | Kepler Validates SDA-Compatible Space-to-Ground Laser Links ... | 强 | 未明确 | 实测/解析 | 🔴 abstract 自陈成熟/广泛采用 |
| 34 | 2025 | 信道建模/闪烁/湍流 / 地面站/OGS/硬件/终端 / AO/自适应光学/波前 / 链路预算/系统级 | LEO-to-ground low elevation optical communication: optimization of an adaptive optics desi | 强 | 未明确 | 仿真/实测 | 🟢 abstract 自陈: however, at low elevations, amplitude fluctuations (or scintillation) challenge this corre |
| 35 | 2025 | 地面站/OGS/硬件/终端 | Laser Technology: The Future of Space-Based Communications | 未明确 | conventional methods (abstract 泛指) | 未明确 | 🟡 abstract 无缝信号，待精读 |
| 36 | 2025 | ATP/指向/PAT/捕获 / 网络层/路由/调度 / 地面站/OGS/硬件/终端 / 在轨演示/任务 / 链路预算/系统级 | Modeling Pointing, Acquisition, and Tracking Delays in Free-Space Optical Satellite Networ | 弱 | 未明确 | 未明确 | 🟡 abstract 无缝信号，待精读 |
| 37 | 2025 | 调制/复用 / 载波同步/恢复 / 相干/自相干检测 / 链路预算/系统级 | Modeling and Simulation of Inter-Satellite Laser Communication for Space-Based Gravitation | 弱 | 10−6 when the modulation index exceeds 3 | 仿真 | 🟡 abstract 无缝信号，待精读 |
| 38 | 2025 | ATP/指向/PAT/捕获 / 地面站/OGS/硬件/终端 / 载波同步/恢复 / 链路预算/系统级 | OSIRIS4CubeSat—The World’s Smallest Commercially Available Laser Communication Terminal | 弱 | 未明确 | 仿真/综述 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 39 | 2025 | 信道建模/闪烁/湍流 / 地面站/OGS/硬件/终端 / QKD/量子 / 链路预算/系统级 | Optical Downlink Modeling for LEO and MEO Satellites under ... - arXiv | 强 | 未明确 | 仿真/实测 | 🔴 abstract 自陈成熟/广泛采用 |
| 40 | 2025 | 信道建模/闪烁/湍流 / 地面站/OGS/硬件/终端 / QKD/量子 / 链路预算/系统级 | Optical Downlink Modeling for LEO and MEO Satellites under Atmospheric Turbulence with a Q | 强 | 未明确 | 仿真 | 🔴 abstract 自陈成熟/广泛采用 |
| 41 | 2025 | ATP/指向/PAT/捕获 / 信道建模/闪烁/湍流 / 调制/复用 / 链路预算/系统级 | Optical OTFS Modulation for Free Space Optical-Based LEO Satellite Communication Systems | 强 | 未明确 | 仿真 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 42 | 2025 | 网络层/路由/调度 / 地面站/OGS/硬件/终端 / 链路预算/系统级 | Optical technology revolutionizing space communications | 未明确 | 未明确 | 未明确 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 43 | 2025 | 地面站/OGS/硬件/终端 / 在轨演示/任务 / QKD/量子 / AO/自适应光学/波前 / 链路预算/系统级 | Preliminary results of optical downlink between QUBE satellite to the upgraded Optical Gro | 未明确 | 未明确 | 实测 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 44 | 2025 | 信道建模/闪烁/湍流 / 网络层/路由/调度 / 链路预算/系统级 | RELAY-ASSISTED HIGH-CAPACITY SATELLITE FEEDER LINKS WITH INTEGRATED LINE-OF-SIGHT MIMO RF  | 强 | 未明确 | 未明确 | 🟡 abstract 无缝信号，待精读 |
| 45 | 2025 | ATP/指向/PAT/捕获 / 网络层/路由/调度 / 地面站/OGS/硬件/终端 / 在轨演示/任务 / 相干/自相干检测 / QKD/量子 / 链路预算/系统级 | Rapid tactical deployment capability of a transportable optical ground station / Scientifi | 弱 | 未明确 | 实测 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 46 | 2025 | ATP/指向/PAT/捕获 / 信道建模/闪烁/湍流 / 网络层/路由/调度 / 链路预算/系统级 | Satellite-to-ground optical communication systems under orbital deviations and atmospheric | 强 | 未明确 | 仿真/解析 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 47 | 2025 | 信道建模/闪烁/湍流 / 网络层/路由/调度 / QKD/量子 / 语义/AI/DL/ML | Security challenges from physical to network layers in satellite free-space optical commun | 强 | the conventional rf systems, fso provides distinct | 综述 | 🔴 abstract 自陈成熟/广泛采用 |
| 48 | 2025 | 网络层/路由/调度 / 地面站/OGS/硬件/终端 / 在轨演示/任务 | Space Development Agency demos key space-to-air ... | 未明确 | 未明确 | 实测 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 49 | 2025 | 网络层/路由/调度 / 链路预算/系统级 | Space-to-Ground Optical Communication Downlink Scheduling Under Uncertainty of Link Availa | 强 | gurobi and kuhn-munkres-based methods | 仿真 | 🟢 abstract 自陈: simulation results indicate that considering uncertainty can enhance data throughput, with |
| 50 | 2025 | ATP/指向/PAT/捕获 / 在轨演示/任务 / 链路预算/系统级 | Spire Achieves Two-Way Laser Communication Between Satellites ... | 弱 | 未明确 | 实测 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 51 | 2025 | ATP/指向/PAT/捕获 / 信道建模/闪烁/湍流 / 网络层/路由/调度 / 编码/FEC/交织 | Statistics of Received Power Time Series for Optical LEO Satellite Uplinks | 强 | analytical results and measurements in terms of th | 仿真/实测 | 🟡 abstract 无缝信号，待精读 |
| 52 | 2025 | 未明确 | Thales : Alenia Space to develop SOLiS very-high-throughput laser communications demonstra | 未明确 | 未明确 | 未明确 | 🟡 abstract 无缝信号，待精读 |
| 53 | 2025 | 调制/复用 / 载波同步/恢复 / 链路预算/系统级 | The modulation and demodulation technology of 100Gbps satellite laser communication system | 弱 | the dp-qpsk modulation method, the sensitivity of  | 未明确 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 54 | 2025 | 信道建模/闪烁/湍流 / 调制/复用 / 链路预算/系统级 | World's First Successful 2 Tbit/s Free-Space Optical Communication Using Small Optical Ter | 强 | 未明确 | 实测 | 🟢 abstract 自陈: despite the difficult conditions of an urban environment with atmospheric turbulence that  |
| 55 | 2025 | 信道建模/闪烁/湍流 / 网络层/路由/调度 / 地面站/OGS/硬件/终端 / 在轨演示/任务 / QKD/量子 / 链路预算/系统级 | [PDF] Overview of Ground Station 1 supporting the NASA space ... | 强 | 未明确 | 实测/综述 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 56 | 2024 | 链路预算/系统级 | A 4 × 20 Gbps inter-satellite optical wireless communication system based on orbital angul | 未明确 | 未明确 | 未明确(abstract 缺失) | 🟡 abstract 缺失，待精读 |
| 57 | 2024 | ATP/指向/PAT/捕获 / 链路预算/系统级 | Analytic pointing error evaluation on nano-satellite laser communication system | 弱 | 未明确 | 未明确(abstract 缺失) | 🟡 abstract 缺失，待精读 |
| 58 | 2024 | ATP/指向/PAT/捕获 / 信道建模/闪烁/湍流 / 地面站/OGS/硬件/终端 / QKD/量子 | Assessment of Signal Losses in LEO Satellite-to-Ground Optical Communication Links | 强 | 未明确 | 未明确 | 🟡 abstract 无缝信号，待精读 |
| 59 | 2024 | ATP/指向/PAT/捕获 / 链路预算/系统级 | Average bit-error rate analysis of an inter-satellite optical communication system under t | 弱 | 未明确 | 仿真/解析 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 60 | 2024 | 未明确 | Design and control of a steering mirror for a free-space optical communications CubeSat fo | 未明确 | 未明确 | 未明确(abstract 缺失) | 🟡 abstract 缺失，待精读 |
| 61 | 2024 | 信道建模/闪烁/湍流 / 地面站/OGS/硬件/终端 | Laboratory emulation of LEO downlink optical feeder link employing commercial transceivers | 强 | 未明确 | 实测 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 62 | 2024 | ATP/指向/PAT/捕获 / 调制/复用 / 在轨演示/任务 / 相干/自相干检测 / 链路预算/系统级 | Link budget analysis of bi-directional LEO and GEO optical feeder links advancing the beam | 弱 | conventional methods (abstract 泛指) | 仿真/实测 | 🟡 abstract 无缝信号，待精读 |
| 63 | 2024 | ATP/指向/PAT/捕获 / 网络层/路由/调度 / 语义/AI/DL/ML | On an Intelligent Hierarchical Routing Strategy for Ultra-Dense Free Space Optical Low Ear | 弱 | 未明确 | 仿真 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 64 | 2024 | 地面站/OGS/硬件/终端 | Optical Ground Station: Safran revolutionizing space communications | 未明确 | traditional radiofrequency communications | 未明确 | 🟢 abstract 自陈: optical ground station: safran revolutionizing space communications / safran

# optical gr |
| 65 | 2024 | 网络层/路由/调度 / 地面站/OGS/硬件/终端 / QKD/量子 / 链路预算/系统级 | Optical ground station diversity for satellite quantum key distribution in Ireland | 强 | 未明确 | 未明确 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 66 | 2024 | ATP/指向/PAT/捕获 / 调制/复用 | Optimizing 20 Gbps of ground-to-satellite free-space optical communication in low earth or | 弱 | 未明确 | 未明确 | 🟡 abstract 无缝信号，待精读 |
| 67 | 2024 | ATP/指向/PAT/捕获 / 信道建模/闪烁/湍流 / 地面站/OGS/硬件/终端 / 在轨演示/任务 / AO/自适应光学/波前 / 链路预算/系统级 | Pre-distortion adaptive optics: experimental results from bi-directional tracking links be | 强 | 未明确 | 实测 | 🟡 abstract 无缝信号，待精读 |
| 68 | 2024 | 地面站/OGS/硬件/终端 / 链路预算/系统级 | Safran to supply latest-generation optical ground station to Swedish Space Corporation / S | 未明确 | conventional methods (abstract 泛指) | 未明确 | 🟡 abstract 无缝信号，待精读 |
| 69 | 2024 | 信道建模/闪烁/湍流 / 在轨演示/任务 / AO/自适应光学/波前 | Satellite-to-Ground Optical Links - MPB Communications | 强 | 未明确 | 实测 | 🟡 abstract 无缝信号，待精读 |
| 70 | 2024 | ATP/指向/PAT/捕获 / 链路预算/系统级 | Study & Analysis of a Free Space Optical Link Between a Sun Synchronous LEO Satellite and  | 弱 | 未明确 | 未明确 | 🔴 abstract 自陈成熟/广泛采用 |
| 71 | 2024 | 调制/复用 / 地面站/OGS/硬件/终端 / 在轨演示/任务 / 编码/FEC/交织 / 载波同步/恢复 / QKD/量子 / 链路预算/系统级 | Testing of a photon-counting optical ground receiver with emulated space-to-ground link ef | 弱 | 未明确 | 仿真/实测 | 🟢 abstract 自陈: snspd device properties, which impact detection jitter and time delay, can limit the recei |
| 72 | 2024 | ATP/指向/PAT/捕获 / 信道建模/闪烁/湍流 / 链路预算/系统级 | The transformative technology of laser/free-space optical ... | 强 | 未明确 | 未明确 | 🟡 abstract 无缝信号，待精读 |
| 73 | 2024 | 网络层/路由/调度 / 地面站/OGS/硬件/终端 | Update on the German and Australasian Optical Ground Station Networks | 强 | 未明确 | 未明确 | 🟡 abstract 无缝信号，待精读 |
| 74 | 2023 | 网络层/路由/调度 / 地面站/OGS/硬件/终端 / 语义/AI/DL/ML / 链路预算/系统级 | An Intelligent Ground Station Selection Algorithm in Satellite Optical Communications via  | 未明确 | 未明确 | 实测 | 🟢 abstract 自陈: this property is exploited by the site diversity technique, that tries to limit bad weathe |
| 75 | 2023 | 信道建模/闪烁/湍流 / 网络层/路由/调度 / 地面站/OGS/硬件/终端 / 链路预算/系统级 | Commissioning of the deployable optical ground station at Trauen | 强 | 未明确 | 未明确 | 🔴 abstract 自陈成熟/广泛采用 |
| 76 | 2023 | 未明确 | Current Status and Development Trend of Satellite Laser Communication | 未明确 | 未明确 | 未明确(abstract 缺失) | 🟡 abstract 缺失，待精读 |
| 77 | 2023 | 信道建模/闪烁/湍流 / AO/自适应光学/波前 | Emulating and characterizing strong turbulence conditions for space-to-ground optical link | 强 | numerical simulations, and this characterization r | 仿真 | 🟡 abstract 无缝信号，待精读 |
| 78 | 2023 | 网络层/路由/调度 / 链路预算/系统级 | Energy-efficient routing based on a genetic algorithm for satellite laser communication. | 未明确 | shortest path routing, the proposed method improve | 未明确 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 79 | 2023 | ATP/指向/PAT/捕获 / 信道建模/闪烁/湍流 / 网络层/路由/调度 / 在轨演示/任务 / AO/自适应光学/波前 | Exploration and Space Communications: LCRD - NASA | 强 | 未明确 | 实测 | 🟡 abstract 无缝信号，待精读 |
| 80 | 2023 | ATP/指向/PAT/捕获 / 调制/复用 / 网络层/路由/调度 | Free Space Optical Communication for Inter-Satellite Link: Architecture, Potentials and Tr | 弱 | 未明确 | 未明确 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 81 | 2023 | 信道建模/闪烁/湍流 / 网络层/路由/调度 / 地面站/OGS/硬件/终端 / 链路预算/系统级 | Free-Space Optical (FSO) Satellite Networks Performance Analysis: Transmission Power, Late | 强 | 未明确 | 未明确 | 🟡 abstract 无缝信号，待精读 |
| 82 | 2023 | ATP/指向/PAT/捕获 / 调制/复用 / 网络层/路由/调度 / 地面站/OGS/硬件/终端 / 在轨演示/任务 / 链路预算/系统级 | Ground-to-Drone Optical Pulse Position Modulation Demonstration as a Testbed for Lunar Com | 弱 | 未明确 | 实测/综述 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 83 | 2023 | 网络层/路由/调度 | Laser Intersatellite Link Range in Free-Space Optical Satellite Networks: Impact on Latenc | 未明确 | 未明确 | 未明确 | 🟡 abstract 无缝信号，待精读 |
| 84 | 2023 | 链路预算/系统级 | Link budget calculation in optical LEO satellite downlinks with on/off-keying and large si | 未明确 | 未明确 | 未明确 | 🟡 abstract 无缝信号，待精读 |
| 85 | 2023 | 地面站/OGS/硬件/终端 / QKD/量子 / AO/自适应光学/波前 / 链路预算/系统级 | Optical Ground Station Oberpfaffenhofen Next Generation: first satellite link tests with 8 | 未明确 | 未明确 | 实测/综述 | 🟡 abstract 无缝信号，待精读 |
| 86 | 2023 | 未明确 | Optical Intersatellite Links for the Space Web - YouTube | 未明确 | 未明确 | 未明确 | 🟡 abstract 无缝信号，待精读 |
| 87 | 2023 | ATP/指向/PAT/捕获 / 调制/复用 / 地面站/OGS/硬件/终端 / 在轨演示/任务 / 链路预算/系统级 | Space-to-Ground Optical Interface Verification for the Orion Artemis II Optical (O2O) Comm | 弱 | 未明确 | 未明确 | 🔴 abstract 自陈成熟/广泛采用 |
| 88 | 2023 | 信道建模/闪烁/湍流 / 地面站/OGS/硬件/终端 | Stellar scintillation statistics and the impact of aperture averaging on space-to-ground o | 强 | a reasonable set of candidate probability distribu | 实测/解析 | 🟡 abstract 无缝信号，待精读 |
| 89 | 2023 | 网络层/路由/调度 / 地面站/OGS/硬件/终端 / 在轨演示/任务 / AO/自适应光学/波前 / 链路预算/系统级 | The Introduction of Japanese Development and Demonstration of Inter-Satellite Optical Comm | 未明确 | 未明确 | 实测 | 🟡 abstract 无缝信号，待精读 |
| 90 | 2023 | 调制/复用 / 网络层/路由/调度 / 在轨演示/任务 / 链路预算/系统级 | Ultra-High Capacity Optical Satellite Communication System Using PDM-256-QAM and Optical A | 弱 | 未明确 | 实测/综述 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 91 | 2022 | 网络层/路由/调度 / 链路预算/系统级 | Adaptive Service Scheduling for Satellite-Ground Downlink Capacity in Optical Satellite Ne | 未明确 | 未明确 | 未明确 | 🟢 abstract 自陈: prior studies reported low utilization of satellite-ground downlink (sgdl) resources, maki |
| 92 | 2022 | 信道建模/闪烁/湍流 / 地面站/OGS/硬件/终端 / 在轨演示/任务 / QKD/量子 / 链路预算/系统级 | Analysis of power scintillation and fading margin in the LEO-ground downlink with the OSIR | 强 | 未明确 | 实测 | 🟡 abstract 无缝信号，待精读 |
| 93 | 2022 | ATP/指向/PAT/捕获 / 调制/复用 / 地面站/OGS/硬件/终端 / 链路预算/系统级 | Beacon system for ESA IZN-1 Optical Ground Station | 弱 | 未明确 | 未明确 | 🔴 abstract 自陈成熟/广泛采用 |
| 94 | 2022 | ATP/指向/PAT/捕获 / 信道建模/闪烁/湍流 / 调制/复用 / 地面站/OGS/硬件/终端 / 在轨演示/任务 / 相干/自相干检测 / AO/自适应光学/波前 / 链路预算/系统级 | Demonstration of 100 Gbps coherent free-space optical communications at LEO tracking rates | 强 | 未明确 | 实测 | 🟢 abstract 自陈: demonstration of 100 gbps coherent free-space optical communications at leo tracking rates |
| 95 | 2022 | ATP/指向/PAT/捕获 | Inter-satellite optical wireless communication (IsOWC) systems challenges and applications | 弱 | 未明确 | 未明确 | 🔴 abstract 自陈成熟/广泛采用 |
| 96 | 2022 | 信道建模/闪烁/湍流 / 地面站/OGS/硬件/终端 / 在轨演示/任务 / QKD/量子 | LEO small satellite QKD downlink performance: QuantSat-PT case study | 强 | 未明确 | 实测 | 🔴 abstract 自陈成熟/广泛采用 |
| 97 | 2022 | 链路预算/系统级 | Link Budget Analysis for Free-Space Optical Satellite Networks | 未明确 | 未明确 | 未明确 | 🟡 abstract 无缝信号，待精读 |
| 98 | 2022 | 信道建模/闪烁/湍流 / 网络层/路由/调度 / 地面站/OGS/硬件/终端 | Link Reliability of Satellite-to-Ground Free-Space Optical Communication Systems in South  | 强 | 未明确 | 未明确 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 99 | 2022 | ATP/指向/PAT/捕获 / 信道建模/闪烁/湍流 / 链路预算/系统级 | Modulating Retroreflector Based Free Space Optical Link for UAV-to-Ground Communications | 强 | 未明确 | 解析 | 🟡 abstract 无缝信号，待精读 |
| 100 | 2022 | ATP/指向/PAT/捕获 / 在轨演示/任务 / 链路预算/系统级 | Multi-parameter influenced acquisition model with an in-orbit jitter for inter-satellite l | 弱 | 未明确 | 仿真/实测/解析 | 🟢 abstract 自陈: with the development of large low earth orbit (leo) communication constellations, the effi |
| 101 | 2022 | ATP/指向/PAT/捕获 / 信道建模/闪烁/湍流 / 调制/复用 / 链路预算/系统级 | Research on uplink performance of MIMO terrestrial-satellite laser communication based on  | 强 | 未明确 | 仿真/实测/解析 | 🟡 abstract 无缝信号，待精读 |
| 102 | 2022 | 未明确 | Silicon photonic receiver for satellite laser communication terminals. | 未明确 | 未明确 | 未明确 | 🟡 abstract 无缝信号，待精读 |
| 103 | 2022 | 地面站/OGS/硬件/终端 | Space Optical Communications: Why Are Space-to-ground Links ... | 未明确 | 未明确 | 未明确 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 104 | 2022 | 网络层/路由/调度 | Temporary Laser Inter-Satellite Links in Free-Space Optical Satellite Networks | 未明确 | an nng-fsosn (which has pls and tls) under differe | 未明确 | 🟡 abstract 无缝信号，待精读 |
| 105 | 2022 | 信道建模/闪烁/湍流 / 网络层/路由/调度 / 地面站/OGS/硬件/终端 / 相干/自相干检测 / QKD/量子 | The Western Australian optical ground station | 强 | conventional methods (abstract 泛指) | 未明确 | 🟡 abstract 无缝信号，待精读 |
| 106 | 2022 | 网络层/路由/调度 / 地面站/OGS/硬件/终端 / 在轨演示/任务 | The communication experiment result of Small Optical Link for ISS (SOLISS) to the first co | 未明确 | 未明确 | 实测 | 🟡 abstract 无缝信号，待精读 |
| 107 | 2021 | ATP/指向/PAT/捕获 / 地面站/OGS/硬件/终端 / 载波同步/恢复 / 链路预算/系统级 | Accuracy of satellite orbit prediction and optical design of optical ground station beacon | 弱 | 未明确 | 实测 | 🟢 abstract 自陈: however, the radio frequencies used make it difficult to improve the communication speed,  |
| 108 | 2021 | ATP/指向/PAT/捕获 | Acquisition, Scanning and Control Technology for Inter-satellite Laser Communication | 未明确 | pi controller | 仿真/解析 | 🟢 abstract 自陈: due to the complex space environment, it is very difficult to establish communication link |
| 109 | 2021 | ATP/指向/PAT/捕获 / 在轨演示/任务 / AO/自适应光学/波前 / 链路预算/系统级 | Beacon correction method for inter-satellite laser communication | 弱 | 未明确 | 实测/解析 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 110 | 2021 | 网络层/路由/调度 / 地面站/OGS/硬件/终端 / 在轨演示/任务 / 链路预算/系统级 | Demonstration of a modular, scalable, laser communication terminal for manned spaceflight  | 未明确 | 未明确 | 实测/综述 | 🟡 abstract 无缝信号，待精读 |
| 111 | 2021 | ATP/指向/PAT/捕获 / 链路预算/系统级 | High-Precision Dual-Stage Pointing Mechanism for Miniature Satellite Laser Communication T | 弱 | 未明确 | 实测 | 🟡 abstract 无缝信号，待精读 |
| 112 | 2021 | 网络层/路由/调度 / 地面站/OGS/硬件/终端 / 在轨演示/任务 | HySpecIQ Picks BridgeComm's Optical Downlink Terminals for LEO ... | 未明确 | 未明确 | 未明确 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 113 | 2021 | 网络层/路由/调度 / 地面站/OGS/硬件/终端 / 在轨演示/任务 / 链路预算/系统级 | Laser Communications Relay Demonstration (LCRD) Overview - NASA | 未明确 | 未明确 | 实测/综述 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 114 | 2021 | 网络层/路由/调度 / 在轨演示/任务 / 链路预算/系统级 | NASA's Laser Communications Tech, Science Experiment Safely in Space | 未明确 | 未明确 | 实测/综述 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 115 | 2021 | 信道建模/闪烁/湍流 / 地面站/OGS/硬件/终端 | Optical link stabilization by controlling focus of received beam in mini-unmanned aerial v | 强 | 未明确 | 仿真/实测 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 116 | 2021 | 调制/复用 / 网络层/路由/调度 / 链路预算/系统级 | Performance Analysis and Evaluation of Inter-Satellite Optical Wireless Communication Syst | 未明确 | 未明确 | 未明确 | 🟢 abstract 自陈: that enables geo satellites to relay information to and from leo satellites and fixed eart |
| 117 | 2021 | ATP/指向/PAT/捕获 / 信道建模/闪烁/湍流 / 调制/复用 / 编码/FEC/交织 / 链路预算/系统级 | Performance of an OFDM STBC-MISO system in uplink terrestrial-satellite laser communicatio | 强 | 未明确 | 仿真/实测/解析 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 118 | 2021 | 网络层/路由/调度 / 链路预算/系统级 | Research on inter-satellite laser communication based on relay system | 未明确 | 未明确 | 仿真 | 🟢 abstract 自陈: due to the limitation of satellite payload performance and the influence of space environm |
| 119 | 2021 | 调制/复用 / 网络层/路由/调度 / 链路预算/系统级 | Satellite Laser Communication Assisted P-cycle Protection Against SRLG Failures in WDM Opt | 未明确 | 未明确 | 未明确 | 🟢 abstract 自陈: p-cycle protection against shared risk links group (srlg) failures in wdm optical networks |
| 120 | 2021 | ATP/指向/PAT/捕获 / 在轨演示/任务 | XY-2 satellite laser communication equipment PAT test in orbit | 未明确 | 未明确 | 未明确(abstract 缺失) | 🟡 abstract 缺失，待精读 |
| 121 | 2020 | 链路预算/系统级 | Design of a Two Wavelength Optical Downlink for LEO Spacecrafts | 未明确 | 未明确 | 解析 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 122 | 2020 | 信道建模/闪烁/湍流 / 链路预算/系统级 | Development status and trend of micro-satellite laser communication systems | 强 | 未明确 | 未明确 | 🟡 abstract 无缝信号，待精读 |
| 123 | 2020 | 网络层/路由/调度 / 地面站/OGS/硬件/终端 / 链路预算/系统级 | Network Availability Maximization for Free-Space Optical Satellite Communications | 未明确 | the conventional gs selection methods, the propose | 仿真 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 124 | 2020 | ATP/指向/PAT/捕获 | Point ahead angle prediction based on Kalman filtering of optical axis pointing angle in s | 弱 | 未明确 | 未明确(abstract 缺失) | 🟡 abstract 缺失，待精读 |
| 125 | 2020 | 地面站/OGS/硬件/终端 / 在轨演示/任务 | Received power attenuation due to the wave-front aberrations induced by the receiving opti | 未明确 | 未明确 | 仿真/实测 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 126 | 2019 | 编码/FEC/交织 / 链路预算/系统级 | A Throughput Model of TCP-FSO/ADFR for Free-Space Optical Satellite Communications | 未明确 | 未明确 | 实测 | 🟡 abstract 无缝信号，待精读 |
| 127 | 2019 | 信道建模/闪烁/湍流 | APC‐EDFA‐based scintillation‐suppressed photodetection in satellite optical communication | 强 | gain saturation, and an approximate 5 | 实测 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 128 | 2019 | ATP/指向/PAT/捕获 / 信道建模/闪烁/湍流 / 地面站/OGS/硬件/终端 / 链路预算/系统级 | Analysis of tip-tilt compensation for reflective free-space optical satellite communicatio | 强 | 未明确 | 实测 | 🟢 abstract 自陈: atmospheric turbulences limit the achievable performance of free-space optical (fso) satel |
| 129 | 2019 | ATP/指向/PAT/捕获 / 网络层/路由/调度 / 链路预算/系统级 | Beaconless acquisition tracking and pointing scheme of satellite optical communication in  | 弱 | 未明确 | 仿真 | 🟡 abstract 无缝信号，待精读 |
| 130 | 2019 | 信道建模/闪烁/湍流 | Bit Error Rate Analysis of Space-to-Ground Optical Link Under the Influence of Atmospheric | 强 | 未明确 | 未明确(abstract 缺失) | 🟡 abstract 缺失，待精读 |
| 131 | 2019 | 调制/复用 / 编码/FEC/交织 / 载波同步/恢复 / QKD/量子 / 链路预算/系统级 | Characterization of a photon counting test bed for space to ground optical pulse position  | 弱 | 未明确 | 未明确 | 🔴 abstract 自陈成熟/广泛采用 |
| 132 | 2019 | 信道建模/闪烁/湍流 / 地面站/OGS/硬件/终端 / AO/自适应光学/波前 / 链路预算/系统级 | ESA Optical Ground Station Upgrade with Adaptive Optics for High Data Rate Satellite-to-Gr | 强 | 未明确 | 未明确 | 🟡 abstract 无缝信号，待精读 |
| 133 | 2019 | 信道建模/闪烁/湍流 / 调制/复用 / 地面站/OGS/硬件/终端 / 链路预算/系统级 | Experimental evaluation of adaptive distributed frame repetition at 10Gbps for the satelli | 强 | 未明确 | 未明确 | 🟡 abstract 无缝信号，待精读 |
| 134 | 2019 | 未明确 | INTER-SATELLITE OPTICAL COMMUNICATION LINK | 未明确 | 未明确 | 未明确(abstract 缺失) | 🟡 abstract 缺失，待精读 |
| 135 | 2019 | ATP/指向/PAT/捕获 / 地面站/OGS/硬件/终端 / 在轨演示/任务 / 编码/FEC/交织 / 链路预算/系统级 | Optical communications downlink from a 1.5U Cubesat: OCSD program | 弱 | 未明确 | 实测 | 🟡 abstract 自陈达成增益，未自陈缝 |
| 136 | 2019 | ATP/指向/PAT/捕获 / 地面站/OGS/硬件/终端 / 在轨演示/任务 / 链路预算/系统级 | Paper Title (use style: paper title) | 弱 | 未明确 | 实测 | 🔴 abstract 自陈成熟/广泛采用 |
| 137 | 2019 | 地面站/OGS/硬件/终端 | Reference Power Vectors for the Optical LEO Downlink Channel | 未明确 | 未明确 | 仿真 | 🔴 abstract 自陈成熟/广泛采用 |

## 🔴 必填项 — 死地/饱和领域记忆（H002 L49-54，领域记忆种子，不再碰）

> 以下 5 项是历史撞死/已 Kill 的轴，本轮**强制预置进表**作为领域记忆。无论地勘是否命中，都标 🔴。

| 轴 | Kill 来源 | 核心失败机制 | 不再碰理由 |
|----|---------|-------------|-----------|
| 载波同步（N1 PCS / A3 CPE / "Are PLLs dead?"） | N1/A3 preflight + S002 验证 | 相位缓变假设在大气湍流下失效；pilot-CPE 在残余相位噪声下无效；KF 三元交集虽稀疏但属新颖性 ≠ 可做 | 5 次失败核心子环节，物理天花板机制必然 |
| 自适应交织（4b#1） | D001 Kill | 信道感知自适应交织在 BER 维度 0dB 增益，时延维度无先例 | FR-21 三版验证 0dB |
| GG-LLR 译码（(c)） | D002 Kill | Gamma-Gamma 信道 LLR 软译码，增益 < 物理上限 | oracle 上界 0.09dB |
| MCS 排程（③） | ③ oracle | 自适应调制编码排程在 LEO 光信道增益极小 | oracle 0.09dB |
| 信道估计 LS/LMS/RLS / 静态均衡 / 理想CSI假设 | S002 批评汇总拥挤赛道 | 传统 CE/静态均衡被批 ≥2 次，2019+ 已部分补，拥挤赛道 | 批评热点但全是已补的拥挤地 |

## 附录 A：年份筛外（<2019，全留不丢）

| 标题 | 年 | 剔除理由 |
|------|----|---------|
| Performance enhancement of free space optical satellite uplink with transmitter  | 2016 | 年份筛 <2019 |
| Nanosatellite optical downlink experiment: design, simulation, and prototyping | 2016 | 年份筛 <2019 |
| LEO-to-ground optical communications link using adaptive optics correction on th | 2016 | 年份筛 <2019 |
| OPTEL-µ: A Compact System for Optical Downlink from LEO Satellites | 2012 | 年份筛 <2019 |
| Performance Evaluation of Delayed Frame Repetition Variable DataRate technique f | 2018 | 年份筛 <2019 |
| A Study on Data Transfer Rate Considering Downlink Condition for the LEO Optical | 2016 | 年份筛 <2019 |
| Investigation on the UAV-To-Satellite Optical Communication Systems | 2018 | 年份筛 <2019 |
| Approach for recognizing and tracking beacon in inter-satellite optical communic | 2018 | 年份筛 <2019 |
| Static position errors correction on the satellite optical communication termina | 2017 | 年份筛 <2019 |
| Doppler shift estimation using broadcast ephemeris in satellite optical communic | 2016 | 年份筛 <2019 |
| Small Satellite Optical Communication Networks: Analytical Models | 2018 | 年份筛 <2019 |
| A portable optical ground station for low-earth orbit satellite communications | 2017 | 年份筛 <2019 |
| (Invited) Upgrade of ESA optical ground station with adaptive optics for high da | 2017 | 年份筛 <2019 |
| Satellite Tracking System using Amateur Telescope and Star Camera for Portable O | 2016 | 年份筛 <2019 |
| Optical ground station optimization for future optical geostationary satellite f | 2017 | 年份筛 <2019 |
| Telecom and scintillation first data analysis for DOMINO: laser communication be | 2016 | 年份筛 <2019 |
| An acquisition technology of optical ground station in satellite-ground QKD | 2017 | 年份筛 <2019 |
| Adaptive optics correction into single mode fiber for a low Earth orbiting space | 2015 | 年份筛 <2019 |
| Far-Field Pattern Measurement of an Onboard Laser Transmitter by Use of a Space- | 1998 | 年份筛 <2019 |
| Demonstration of a bidirectional coherent air-to-ground optical link | 2018 | 年份筛 <2019 |
| Fiber-coupling efficiency simulation of Gaussian Schell Model laser in space-to- | 2015 | 年份筛 <2019 |

## 附录 B：unknown year（全留）

| 标题 | query |
|------|-------|
| OOK for LEO Downlinks - Satellite Communications in the 5G Era | LEO optical downlink |
| SYSTEM ASPECTS OF OPTICAL LEO-TO-GROUND LINKS | LEO optical downlink |
| On-orbit demonstration of 200-Gbps laser communication downlink from the TBIRD C | LEO optical downlink |
| NASA’s Next Generation >100 Gbps Optical | LEO optical downlink |
| Operations and Results from the 200 Gbps TBIRD Laser Communication Mission | satellite laser communication |
| SSC23-I-03 | satellite laser communication |
| Lunar Laser Communication Demonstration NASA’s First Space Laser Communication S | satellite laser communication |

## 附录 C：噪声/非卫星光通信（全留不丢，来自 Agent 1/2 附录合并）

来自 Agent 1 附录（12 条新闻稿/营销/视频）：Kepler/NEC/ESTOL/SSC/YouTube/Spire/AAC Clyde/NASA×3/Thales/Lunar factsheet/HySpecIQ。
来自 Agent 2 附录（16 条含 <2019 + 非 satellite 链路）：Wikipedia/studyiq/无人机-地面/lunar testbed/UAV-FSO 等。

> 完整噪声清单见 `search-archive/2026-06-21/_landscape_deduped_merged.json`（165 条全集，含上述噪声）。

## 元信息

- 总条目（去重）：165
- 主表（≥2019）：137
- 年份筛外（<2019）：21
- unknown year：7
- 缝潜力分布：{'🟢': 19, '🟡': 96, '🔴': 22}
- 检索源：S2(109) + Exa(52) + 混合(4)；SerpAPI 全程失败；OpenAlex 在 total 计数但 source_api 未标注
- IEEE 覆盖：API 已命中 33/165 条 IEEE venue；blit 通道失败（HTTP 418）
