# Landscape — 星地激光通信全景表（扩检索版 v2）

> 生成 2026-06-22 | S006 扩检索产出 | round1 (6 query API) + round2 (10 query API + 5 query IEEE blit) + 诊断验证 3 query
> 方法论位置：S003 地勘前置 Step 0。本表是「领域在做什么」的全景视图，不是批评视角，不是候选清单。
> 子地带从结果涌现，不预设。缝潜力初判仅凭 abstract 字面证据，**初判不是结论**。
> v2 相比 v1（137 主表）：扩到 430 主表，覆盖 ISL/GEO/feeder/relay/终端/cubeSat/载荷/相干/深空/网络级 10 个互补盲区 + IEEE Xplore 专属通道。

## 检索元数据

| 轮次 | query 数 | 工具 | 存档目录 |
|------|---------|------|---------|
| round1 | 6 | tools/search (S2/OpenAlex/SerpAPI/Exa) | search-archive/2026-06-21/landscape-*.json |
| round2 search | 10 | tools/search (同上) | search-archive/2026-06-22/landscape-*.json |
| round2 IEEE | 5 | tools/blit --source ieee (max=50, 实际25/query) | search-archive/2026-06-22/landscape-ieee-*.json |
| 诊断验证 | 3 | tools/blit --source ieee | search-archive/2026-06-22/landscape-ieee-{diag,leo,laser}.json |
| round3 search（动作 A 设备词）| 11 | tools/search (S2/OpenAlex/Exa) | search-archive/2026-06-22/landscape2-*.json |
| round3 IEEE（动作 A）| 11 | tools/blit --source ieee | 全 0 条（IP 限流，见附录 E.3 债务）|
| round3 诊断（动作 B 模块词，**非地勘**）| 4 | tools/search | search-archive/2026-06-22/landscape-diag2-*.json |

**统计**：v3 后 35 JSON 源，v2 635 raw + v3 267 raw（动作 A）+ 80 raw（动作 B 诊断）→ 597 去重唯一 → **509 主表（≥2019）**（v2 430 + v3 续段 79）。

**round3 动作 A 检索词集（11 设备词，方法中性，偏航检查 A 全过）**：
- search: satellite optical {transceiver/modem/receiver/transmitter/frontend/digital-processing-unit/photonic-receiver/coherent-transceiver/balanced-receiver/fpga-receiver} + optical satellite payload transceiver
- 11 词全零模块词（modulation/synchronization/equalization/channel-estimation/coding/detection 均未出现）✅
- IEEE 11 词全 0 条（IP 限流，附录 E.3 债务）

**round3 动作 B 模块词诊断（受控例外，非地勘）**：
- search: satellite optical {carrier-synchronization/channel-estimation/equalization}（死轴 3 词）+ satellite optical modulation（热区对照）
- **产出只入附录 E 诊断段，不入主表候选池**

**round3 检索障碍**：IEEE 今日对当前 IP 全面限流（quota 卡 1/50），11 词全 0。非 S005 修复失效（同命令历史成功过）。另一对话 3 词小样本测：`receiver`/`photonic-receiver` 能拿到 24-25 条，`transceiver`/`frontend` 通用宽词被挡 → 机制为"高频通用词实时反爬 + 累积风险分"。

## 子地带涌现分布（扩检索后，430 主表，multi-tag，关键观察）

```
  158  网络层/路由/调度/RWA
  155  地面站/OGS/硬件/终端
  128  链路预算/系统级/容量/中断
  125  ISL/星间链路
  117  在轨演示/任务 (TBIRD/OSIRIS/LCRD/DSOC/LUCAS)
  111  信道建模/闪烁/湍流/大气
  105  ATP/指向/PAT/捕获/跟踪
   92  feeder link/中继/relay
   86  调制/复用 (OAM/WDM/PDM/OFDM/PAM4/PPM/OOK)
   62  放大器/EDFA/光子载荷
   58  相干/自相干/外差/零差检测
   44  深空/月地/cislunar
   40  QKD/量子/光子计数
   34  语义/AI/DL/ML/RL
   32  编码/FEC/交织/LDPC
   30  AO/自适应光学/波前/LGS
   23  载波同步/恢复  ← 5 次失败死轴，扩 3 倍后仍冷（5.3%）
   13  信道估计/均衡   ← 另一死轴，扩后仍冷（3.0%）
```

**方法论价值（S006 质量评估核心）**：扩检索（137→430，3.1 倍）后，**死轴冷区结论依然成立且更扎实**——载波同步 7→23（占比 5.3%）、信道估计 2→13（占比 3.0%），相对热区（网络层 37%、地面站 36%、ISL 29%）仍是明显冷区。这排除了"S004 冷区判断是采样不足造成的统计假象"的质疑——**冷区是结构性事实，不是采样偏差**。死轴之所以是死轴，正因为它本就是窄冷区。🟢 候选从 19 涨到 48，选地依据更充分。

## 主表（430 条，≥2019，按年份降序）

| # | 年 | 子地带 | 做的事(标题) | 湍流 | baseline 是谁 | 验证 | 缝潜力 |
|---|----|--------|------|------|--------------|------|--------|
| 1 | 2026 | 信道建模/湍流/大气 / 语义/AI/DL/ML | A Semantic-Empowered Free-Space Optical Communication System With Turbulence-Resilient Vector B | 强 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 2 | 2026 | ATP/指向/PAT / ISL/星间链路 | ALIGN: Laboratory Characterisation of 976 nm Beacon and 1550 nm Data Lasers for CubeSat Free-Sp | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 3 | 2026 | 地面站/OGS/终端 / ATP/指向/PAT / 相干/自相干检测 | Aircraft to Geostationary Satellite Optical Links - First Results from the UltraAir Flight Test | 弱 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 4 | 2026 | ATP/指向/PAT / 相干/自相干检测 / ISL/星间链路 | An acquisition and tracking sensor based on pseudo-balanced coherent detection using a single Q | 弱 | 未明确 | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 5 | 2026 | 地面站/OGS/终端 / QKD/量子/光子计数 | Astrolight's Greek Ground Station Speeds Optical Data Transmissions / Microwaves & RF | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 6 | 2026 | 深空/月地/cislunar | BLER of Deep Space Optical Communication System During Superior Solar Conjunction | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 7 | 2026 | 信道估计/均衡 | Clustering-assisted channel estimation for free-space optical satellite communication | 未明确 | 未明确 | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 8 | 2026 | 地面站/OGS/终端 / 在轨演示/任务 / 深空/月地/cislunar | Deep Space Optical Communications | 未明确 | 未明确 | 实测/综述 | 🟡 abstract自陈达成增益未自陈缝 |
| 9 | 2026 | ATP/指向/PAT / feeder/中继 / ISL/星间链路 | Free Space Optical (FSO) Communication for 6G and Non-Terrestrial Networks | 弱 | 未明确 | 未明确 | 🟢 abstract自陈: #### enhanced security

narrow laser beams are difficult to intercept or jam, making fso s |
| 10 | 2026 | 未明确 | Free-space optical communication | 未明确 | 未明确 | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 11 | 2026 | 地面站/OGS/终端 | French Optical Ground Station (FrOGS) Results of GEO Optical Bidirectional Links With TELEO | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 12 | 2026 | ATP/指向/PAT / 调制/复用 / AO/自适应光学/波前 / 相干/自相干检测 / 编码/FEC/交织 / 链路预算/系统级 / feeder/中继 / ISL/星间链路 | High-capacity and secure inter-satellite optical wireless communication using 2D DPS-OCDMA / Sc | 弱 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 13 | 2026 | 地面站/OGS/终端 / 网络层/路由/RWA / ATP/指向/PAT / 在轨演示/任务 | It's a wrap: Space-BACN satellite laser link program shifts from DARPA to DIU - Breaking Defens | 未明确 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 14 | 2026 | 网络层/路由/RWA / 信道建模/湍流/大气 / 在轨演示/任务 / 语义/AI/DL/ML / 链路预算/系统级 / feeder/中继 | Kepler Communications Launches Optical Relay Satellites for ... | 强 | 未明确 | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 15 | 2026 | 网络层/路由/RWA / 信道建模/湍流/大气 / 在轨演示/任务 / 链路预算/系统级 / feeder/中继 / 放大器/EDFA/光子载荷 | Kepler Successfully Launches First Tranche of Optical Relay | 强 | 未明确 | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 16 | 2026 | 网络层/路由/RWA / 信道建模/湍流/大气 / 在轨演示/任务 / 链路预算/系统级 / feeder/中继 / 放大器/EDFA/光子载荷 | Kepler Successfully Launches First Tranche of Optical Relay Satellites | 强 | 未明确 | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 17 | 2026 | 地面站/OGS/终端 / 语义/AI/DL/ML | Learning-enhanced hybrid control for beam jitter suppression in LEO-GEO optical communication l | 未明确 | conventional methods(泛指) | 未明确 | 🟡 abstract无缝信号待精读 |
| 18 | 2026 | 地面站/OGS/终端 / 网络层/路由/RWA / 在轨演示/任务 / QKD/量子/光子计数 | Next-generation optical ground station for fast and secure connectivity ready to begin operatio | 未明确 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 19 | 2026 | 地面站/OGS/终端 / 在轨演示/任务 | Optical Satellite Communication: Who Builds the Terminals | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 20 | 2026 | ATP/指向/PAT / ISL/星间链路 | RF-Assisted Compensation for Rapid Optical Acquisition in Hybrid Inter-Satellite Links | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 21 | 2026 | 网络层/路由/RWA / 信道建模/湍流/大气 / 调制/复用 / AO/自适应光学/波前 / 信道估计/均衡 / 语义/AI/DL/ML / 链路预算/系统级 / ISL/星间链路 | Robust high-capacity free-space optical communication using OAM-based structured light and inte | 强 | conventional methods(泛指) | 仿真 | 🟢 abstract自陈: atmospheric turbulence (at), which causes beam distortion, intensity fading, and intermoda |
| 22 | 2026 | 网络层/路由/RWA / ATP/指向/PAT / 在轨演示/任务 / 编码/FEC/交织 / 语义/AI/DL/ML / 放大器/EDFA/光子载荷 | Spaceborne snapshot compressive hyperspectral imaging / Light: Science & Applications | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 23 | 2026 | QKD/量子/光子计数 / 深空/月地/cislunar / 放大器/EDFA/光子载荷 | Systematic Analysis and Design of Lunar–Earth Optical Communication System Based on Phase-Sensi | 未明确 | 未明确 | 实测/综述 | 🟡 abstract自陈达成增益未自陈缝 |
| 24 | 2026 | 地面站/OGS/终端 / 信道建模/湍流/大气 / ATP/指向/PAT / 在轨演示/任务 / 相干/自相干检测 / 编码/FEC/交织 / 放大器/EDFA/光子载荷 | TBIRD: Two Years Demonstrating 200 Gbps Optical Downlink | 强 | 未明确 | 综述 | 🟡 abstract自陈达成增益未自陈缝 |
| 25 | 2026 | 调制/复用 / 语义/AI/DL/ML / 链路预算/系统级 / ISL/星间链路 | Terahertz OAM spatial beams propagation in a 400Gbps IsOWC system employing M-ZCC OCDMA / Journ | 未明确 | pin pd, the high data rate of 16 × 20gbps is attai | 仿真 | 🟡 abstract自陈达成增益未自陈缝 |
| 26 | 2026 | 地面站/OGS/终端 / ATP/指向/PAT / 在轨演示/任务 / 相干/自相干检测 | Why an independent ground segment matters, discover PL-GSS | 弱 | 未明确 | 实测 | 🟢 abstract自陈: sometimes it’s a patchwork of systems acquired over time, from different vendors, each one |
| 27 | 2026 | 地面站/OGS/终端 | World's smallest deployable operational optical ground station proves capability in successful  | 未明确 | 未明确 | 实测 | 🔴 abstract自陈成熟/广泛采用 |
| 28 | 2026 | 地面站/OGS/终端 / 信道建模/湍流/大气 / ATP/指向/PAT / 在轨演示/任务 | X-lumin Achieves Roundtrip Optical Transmission to LEO Satellite Using 15cm Portable Terminal | 强 | one-way transmission: the signal must traverse atm | 实测 | 🔴 abstract自陈成熟/广泛采用 |
| 29 | 2026 | 网络层/路由/RWA / 在轨演示/任务 / 链路预算/系统级 / feeder/中继 / 放大器/EDFA/光子载荷 | eT - High Capacity D2D RF Transport - Optical Zonu Corporation | 未明确 | 未明确 | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 30 | 2025 | 地面站/OGS/终端 / 网络层/路由/RWA / ISL/星间链路 | 15 laser communications systems for inter-satellite links (ISLs ... - Blog | 未明确 | 未明确 | 综述 | 🟡 abstract无缝信号待精读 |
| 31 | 2025 | 地面站/OGS/终端 / 网络层/路由/RWA / 在轨演示/任务 / AO/自适应光学/波前 / 相干/自相干检测 / feeder/中继 / ISL/星间链路 | A 2.8 Gbps self-referencing interference optical receiver experimental validation with Alphasat | 弱 | 未明确 | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 32 | 2025 | ATP/指向/PAT / 调制/复用 / 编码/FEC/交织 / 链路预算/系统级 / ISL/星间链路 | A 50 Gbit/s Inter-Satellite Optical Wireless Communication System Based on PAM-4 Signal: Perfor | 弱 | 未明确 | 仿真 | 🟡 abstract无缝信号待精读 |
| 33 | 2025 | 网络层/路由/RWA / 信道建模/湍流/大气 / 调制/复用 | A Comprehensive Review Of Satellite Communication System And RF-FSO Wireless Technologies / Jou | 强 | 未明确 | 综述 | 🔴 abstract自陈成熟/广泛采用 |
| 34 | 2025 | 语义/AI/DL/ML | A Deep Reinforcement Learning Approach for RBMSCA in Optical Fiber Communication Networks | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 35 | 2025 | 地面站/OGS/终端 / 在轨演示/任务 / 深空/月地/cislunar | A Deep Space Optical Communication Demonstration on the 3.9m Anglo-Australian Telescope | 未明确 | 未明确 | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 36 | 2025 | 相干/自相干检测 / 载波同步/恢复 / 链路预算/系统级 / ISL/星间链路 | A Noise-Tolerant Carrier Phase Recovery Method for Inter-Satellite Coherent Optical Communicati | 弱 | conventional methods(泛指) | 仿真/实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 37 | 2025 | 地面站/OGS/终端 / 信道建模/湍流/大气 / 调制/复用 / 放大器/EDFA/光子载荷 | A Simulated 1000-km LEO Satellite-to-Ground Station Laser Communication Using a 1.8-km OWC Link | 强 | 未明确 | 仿真 | 🟡 abstract无缝信号待精读 |
| 38 | 2025 | 网络层/路由/RWA / 调制/复用 / 链路预算/系统级 / feeder/中继 / ISL/星间链路 | A ground-to-GEO-to-LEO satellite optical wireless communication link based on a spectrally effi | 弱 | conventional methods | 仿真 | 🟡 abstract自陈达成增益未自陈缝 |
| 39 | 2025 | 地面站/OGS/终端 / ATP/指向/PAT / QKD/量子/光子计数 | ASA OGS - University Innsbruck - Astrosysteme | 弱 | 未明确 | 未明确 | 🔴 abstract自陈成熟/广泛采用 |
| 40 | 2025 | 网络层/路由/RWA / 链路预算/系统级 / feeder/中继 | Achievable Throughput and On-Board Buffer Sizing in RIS-UAV Relay-Assisted Satellite-Aerial-Gro | 未明确 | 未明确 | 仿真 | 🟢 abstract自陈: practical dimensioning of the buffer at haps is an open, yet critical challenge due to the |
| 41 | 2025 | 地面站/OGS/终端 / 在轨演示/任务 / ISL/星间链路 | Aerospace Performs Optical Crosslinks Between CubeSats for the ... | 未明确 | 未明确 | 实测 | 🟢 abstract自陈: "this level of miniaturization presents challenges industry has yet to tackle at scale |
| 42 | 2025 | 网络层/路由/RWA | An Overview of SPACE COMPASS Activity; Realize Space Integrated Computing Network applying Opti | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 43 | 2025 | 调制/复用 / 语义/AI/DL/ML | Analysis of deep learning models for rain-induced channel prediction in free-space optical comm | 弱 | 未明确 | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 44 | 2025 | 地面站/OGS/终端 / 信道建模/湍流/大气 / 链路预算/系统级 | Assessment of CIEMAT’s Plataforma Solar de Almeria as a ground station site for optical LEO sat | 强 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 45 | 2025 | 信道建模/湍流/大气 | Atmospheric modeling of free-space optical transmission: satellite downlinks and horizontal cha | 强 | 未明确 | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 46 | 2025 | 地面站/OGS/终端 / 信道建模/湍流/大气 / ATP/指向/PAT / 调制/复用 / 链路预算/系统级 / 深空/月地/cislunar | Avalanche Photodiode-Based Deep Space Optical Uplink Communication in the Presence of Channel I | 强 | 未明确 | 仿真/解析 | 🔴 abstract自陈成熟/广泛采用 |
| 47 | 2025 | 地面站/OGS/终端 / 网络层/路由/RWA / 信道建模/湍流/大气 / 链路预算/系统级 / feeder/中继 | Battling the Sun in Geostationary Optical Feeder Link Scenarios | 强 | 未明确 | 未明确 | 🔴 abstract自陈成熟/广泛采用 |
| 48 | 2025 | 网络层/路由/RWA / 信道建模/湍流/大气 / ATP/指向/PAT / 调制/复用 / 相干/自相干检测 / 载波同步/恢复 / 链路预算/系统级 / feeder/中继 / ISL/星间链路 | Challenges and Opportunities in Free Space Optical Satellite Communication | 强 | conventional methods(泛指) | 未明确 | 🔴 abstract自陈成熟/广泛采用 |
| 49 | 2025 | 信道建模/湍流/大气 / ATP/指向/PAT / 链路预算/系统级 / ISL/星间链路 | Channel Modeling and Rate Analysis of Optical Inter-Satellite Link (OISL) | 弱 | traditional radio frequency transmission | 仿真 | 🟡 abstract自陈达成增益未自陈缝 |
| 50 | 2025 | 网络层/路由/RWA / 链路预算/系统级 / feeder/中继 / ISL/星间链路 / 放大器/EDFA/光子载荷 | Channel-adaptive relay scheme with dynamical mode switching for a power-efficient dual-hop inte | 未明确 | a static df-only mode | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 51 | 2025 | 调制/复用 / 相干/自相干检测 / 载波同步/恢复 | Coherent OQAM Optical Transmission using a Single Balanced Photodetector for High Sensitivity S | 弱 | conventional homodyne qam systems | 仿真/实测/解析 | 🟡 abstract无缝信号待精读 |
| 52 | 2025 | 相干/自相干检测 / feeder/中继 | Coherent transceiver development for optical GEO feeder links | 弱 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 53 | 2025 | 调制/复用 / 编码/FEC/交织 / ISL/星间链路 | Comprehensive Optical Inter-Satellite Communication Model for Low Earth Orbit Constellations: A | 未明确 | 未明确 | 综述 | 🔴 abstract自陈成熟/广泛采用 |
| 54 | 2025 | ATP/指向/PAT / 在轨演示/任务 / 调制/复用 / ISL/星间链路 | CubeSat optical crosslink | 弱 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 55 | 2025 | 网络层/路由/RWA / 在轨演示/任务 / feeder/中继 | Current status and results of LUCAS, the second-generation GEO satellite-based space data-relay | 未明确 | 未明确 | 实测/综述 | 🟡 abstract无缝信号待精读 |
| 56 | 2025 | 网络层/路由/RWA / 信道建模/湍流/大气 / 调制/复用 / QKD/量子/光子计数 / 编码/FEC/交织 / 链路预算/系统级 / 深空/月地/cislunar | Deep space optical communication photon counting camera | 强 | 未明确 | 解析/综述 | 🟡 abstract自陈达成增益未自陈缝 |
| 57 | 2025 | 网络层/路由/RWA / 信道建模/湍流/大气 / 调制/复用 / 语义/AI/DL/ML | Deep-Learning-Assisted Orbital Angular Momentum Mode Recovery Under Atmospheric Turbulence for  | 强 | those of the pure unet and generative adversarial  | 仿真/实测 | 🟡 abstract无缝信号待精读 |
| 58 | 2025 | 在轨演示/任务 / 调制/复用 / QKD/量子/光子计数 / 相干/自相干检测 / 深空/月地/cislunar | Deep-Space Optical Communication Receiver Based on Single Photon Coherent Beam Combination | 弱 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 59 | 2025 | 地面站/OGS/终端 / ATP/指向/PAT / 在轨演示/任务 / QKD/量子/光子计数 / 深空/月地/cislunar | Deep-space optical communication telescope for ESA’s ground laser receiver for ESA/NASA Psyche  | 弱 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 60 | 2025 | 未明确 | Deep-space optical communications: challenges and technological ... | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 61 | 2025 | 地面站/OGS/终端 / 在轨演示/任务 / ISL/星间链路 | Demonstration of a cost-effective double-clad fiber-coupled laser communication terminal for sh | 未明确 | 未明确 | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 62 | 2025 | 地面站/OGS/终端 | Design and Evaluation of a Miniature Optical Downlink Terminal for Secure, High-Speed LEO-To-Gr | 未明确 | 未明确 | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 63 | 2025 | 放大器/EDFA/光子载荷 | Design and on-orbit performance evaluation of Ethiopian earth observation satellite multispectr | 弱 | 未明确 | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 64 | 2025 | 地面站/OGS/终端 / 信道建模/湍流/大气 / 调制/复用 / AO/自适应光学/波前 / 相干/自相干检测 / 载波同步/恢复 / ISL/星间链路 | Design and validation of a CCSDS O3K synchronization front-end, tailor made for a non-coherent  | 强 | 未明确 | 仿真 | 🔴 abstract自陈成熟/广泛采用 |
| 65 | 2025 | 地面站/OGS/终端 | Design, analysis and verification of thermal control system for satellite laser communication t | 未明确 | 未明确 | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 66 | 2025 | 在轨演示/任务 | Development Status of NICT's High-Speed Laser Communications Mission, "HICALI" on Engineering T | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 67 | 2025 | 地面站/OGS/终端 / 在轨演示/任务 / 放大器/EDFA/光子载荷 | Development and environmental validation of a compact EDFA with integrated LNA+HPA for satellit | 未明确 | 未明确 | 未明确 | 🔴 abstract自陈成熟/广泛采用 |
| 68 | 2025 | 地面站/OGS/终端 / 在轨演示/任务 / ISL/星间链路 | Development of a compact laser communication terminal for LEO satellite constellations | 未明确 | 未明确 | 实测/综述 | 🟡 abstract自陈达成增益未自陈缝 |
| 69 | 2025 | ATP/指向/PAT / 调制/复用 / 相干/自相干检测 / 链路预算/系统级 / ISL/星间链路 | Digital Modulation Schemes in Ultra-Gigabit Inter-Satellite Optical Wireless Communication | 弱 | 未明确 | 仿真/解析 | 🟡 abstract无缝信号待精读 |
| 70 | 2025 | 信道建模/湍流/大气 / ATP/指向/PAT / 调制/复用 / AO/自适应光学/波前 / 相干/自相干检测 / 链路预算/系统级 | E2E Physical Layer and Link Analysis for High-Throughput Satellite Optical Communication | 强 | 未明确 | 解析 | 🔴 abstract自陈成熟/广泛采用 |
| 71 | 2025 | 地面站/OGS/终端 / 网络层/路由/RWA / ATP/指向/PAT / 在轨演示/任务 / 链路预算/系统级 / 深空/月地/cislunar | ESA uplink-beacon system for deep-space optical communication | 弱 | 未明确 | 实测 | 🔴 abstract自陈成熟/广泛采用 |
| 72 | 2025 | 地面站/OGS/终端 / QKD/量子/光子计数 | ESA-funded Optical Ground Station for fast and secure laser satellite communications begins con | 未明确 | 未明确 | 未明确 | 🔴 abstract自陈成熟/广泛采用 |
| 73 | 2025 | 网络层/路由/RWA / 链路预算/系统级 / ISL/星间链路 | ESTOL: ESA Specifications for Terabit/sec Optical Links  - ESA CSC: Connectivity & Secure Commu | 未明确 | 未明确 | 综述 | 🟡 abstract自陈达成增益未自陈缝 |
| 74 | 2025 | 网络层/路由/RWA / 链路预算/系统级 | Earth Observation Satellite Downlink Scheduling With Satellite-Ground Optical Communication Lin | 未明确 | the existing downlink scheduling algorithms | 仿真 | 🟢 abstract自陈: consistent growth in the number of high-resolution earth observation satellites (eoss) pos |
| 75 | 2025 | 地面站/OGS/终端 / 信道建模/湍流/大气 / ATP/指向/PAT / 调制/复用 / 相干/自相干检测 / 链路预算/系统级 | Enhancing Laser Satellite Communication Through Single-Sideband Optical Modulation and Coherent | 强 | conventional double-sideband amplitude shift keyin | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 76 | 2025 | 地面站/OGS/终端 / 网络层/路由/RWA / 信道建模/湍流/大气 / 链路预算/系统级 / feeder/中继 | Ergodic Capacity of a NOMA-Based RF/FSO Integrated Satellite-Terrestrial Relay Networks System | 强 | 未明确 | 仿真/解析 | 🟡 abstract自陈达成增益未自陈缝 |
| 77 | 2025 | 深空/月地/cislunar | European Space Agency Modular Ground Segment Infrastructure for Deep Space Optical Communicatio | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 78 | 2025 | 网络层/路由/RWA / 信道建模/湍流/大气 / 调制/复用 / QKD/量子/光子计数 / 相干/自相干检测 / 编码/FEC/交织 / 链路预算/系统级 / ISL/星间链路 | Evaluation of Performance and Device Complexity of Simplified Coherent Free-Space Optical Commu | 强 | 未明确 | 解析/综述 | 🟡 abstract自陈达成增益未自陈缝 |
| 79 | 2025 | 放大器/EDFA/光子载荷 | Evaluation of the Mechanical Stability of Optical Payloads for ... - MDPI | 未明确 | 未明确 | 仿真/综述 | 🟡 abstract自陈达成增益未自陈缝 |
| 80 | 2025 | 地面站/OGS/终端 / 网络层/路由/RWA / 信道建模/湍流/大气 / 在轨演示/任务 / 编码/FEC/交织 / feeder/中继 | Experimental Demonstration of Next-Generation FEC-Coded Data Transmission for GEO Satellite-to- | 强 | conventional methods(泛指) | 实测 | 🟡 abstract无缝信号待精读 |
| 81 | 2025 | 地面站/OGS/终端 / 信道建模/湍流/大气 / ATP/指向/PAT / feeder/中继 | Experimental Emulation of LEO Downlink OFLs Affected by Turbulence and Pointing Jitter | 强 | 未明确 | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 82 | 2025 | 地面站/OGS/终端 / 在轨演示/任务 / 调制/复用 / 深空/月地/cislunar | Exploring Optical Technologies for Deep Space Communication | 弱 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 83 | 2025 | 地面站/OGS/终端 / 网络层/路由/RWA / 信道建模/湍流/大气 / 调制/复用 / QKD/量子/光子计数 / 编码/FEC/交织 / 链路预算/系统级 / 深空/月地/cislunar | Feasibility Analysis for a Deep Space Optical Communication Link and Dimensioning of a Global O | 强 | 未明确 | 解析/综述 | 🟡 abstract自陈达成增益未自陈缝 |
| 84 | 2025 | 地面站/OGS/终端 / 网络层/路由/RWA / 信道建模/湍流/大气 / QKD/量子/光子计数 / 链路预算/系统级 / feeder/中继 / ISL/星间链路 | Feasibility analysis of optical satellite communication systems in Cyprus: CFLOS and irradiance | 强 | radio-frequency (rf) satellite systems such as gre | 综述 | 🟡 abstract自陈达成增益未自陈缝 |
| 85 | 2025 | 地面站/OGS/终端 / ATP/指向/PAT / feeder/中继 | Feasibility study on link acquisition sequence for optical communication between 6U-CubeSat and | 未明确 | conventional methods(泛指) | 仿真 | 🟢 abstract自陈: while substantial research exists on optical links between satellites and optical links be |
| 86 | 2025 | 在轨演示/任务 / 相干/自相干检测 | Field Demonstration of Full-Photonic Assisted Ultra-Reliable Hybrid FSO/MMW Transmission Over 4 | 弱 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 87 | 2025 | 地面站/OGS/终端 / 网络层/路由/RWA / 在轨演示/任务 / feeder/中继 / ISL/星间链路 | First Transmission of Mission Data Using 1.5 μm Optical Inter-Satellite Communication: Press Re | 未明确 | 未明确 | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 88 | 2025 | 网络层/路由/RWA / 在轨演示/任务 | First Unified Optical-Microwave Switching: Experimental Demonstration of Frequency-Division Gra | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 89 | 2025 | 地面站/OGS/终端 / 信道建模/湍流/大气 / 在轨演示/任务 | First-light results of the in-orbit demonstration of a CubeSat-compatible optical communication | 强 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 90 | 2025 | 网络层/路由/RWA / 语义/AI/DL/ML / 链路预算/系统级 / ISL/星间链路 | Free Space Optical Links Scheduling and Routing in Satellite Networks: A Safe Reinforcement Lea | 未明确 | conventional approaches, the proposed rl approach  | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 91 | 2025 | 地面站/OGS/终端 / 网络层/路由/RWA / 信道建模/湍流/大气 / 调制/复用 / 语义/AI/DL/ML | Free Space Optical Semantic Communication for Satellite Remote Sensing Image Transmission | 强 | the traditional systems, without incurring additio | 仿真/实测 | 🔴 abstract自陈成熟/广泛采用 |
| 92 | 2025 | 地面站/OGS/终端 / 网络层/路由/RWA / 在轨演示/任务 / 深空/月地/cislunar | From Taters to Terabits: NASA Wraps Up Deep Space Laser Test | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 93 | 2025 | 调制/复用 / ISL/星间链路 | Frontiers / A ground-to-GEO-to-LEO satellite optical wireless communication link based on a spe | 弱 | conventional methods | 仿真 | 🟡 abstract自陈达成增益未自陈缝 |
| 94 | 2025 | 网络层/路由/RWA / 在轨演示/任务 / 链路预算/系统级 / feeder/中继 / ISL/星间链路 / 放大器/EDFA/光子载荷 | GEO Relay-Enabled Inter-Satellite Communication Architecture for India’s LEO Fleet | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 95 | 2025 | 信道建模/湍流/大气 / AO/自适应光学/波前 / 链路预算/系统级 | GPU-Accelerated Multilayer Turbulence Simulation for Modeling of Space-to-Ground Optical Links | 强 | freely available turbulence propagation tools | 仿真 | 🔴 abstract自陈成熟/广泛采用 |
| 96 | 2025 | 网络层/路由/RWA | GeoPipe: a Geo-distributed LLM Training Framework with enhanced Pipeline Parallelism in a Lossl | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 97 | 2025 | 网络层/路由/RWA / 语义/AI/DL/ML / 放大器/EDFA/光子载荷 | Hierarchical Domain Adaptation Framework for Disparity Estimation in Optical Satellite Stereo I | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 98 | 2025 | 网络层/路由/RWA / 信道建模/湍流/大气 / 相干/自相干检测 / 链路预算/系统级 | High-Speed Free-Space Optical Communication Using Mode Demultiplexers and Coherent Beam Combini | 强 | 有对标(abstract提及) | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 99 | 2025 | 网络层/路由/RWA / 编码/FEC/交织 / 语义/AI/DL/ML / 链路预算/系统级 / ISL/星间链路 | High-Throughput Data Routing Technology for Low-Earth-Orbit Mega-Constellations All-Optical Net | 未明确 | 未明确 | 未明确 | 🟢 abstract自陈: this shift addresses the critical challenge of limited frequency resources, a major bottle |
| 100 | 2025 | 调制/复用 / 相干/自相干检测 / 载波同步/恢复 / 信道估计/均衡 / ISL/星间链路 | Homodyne coherent inter-satellite communications with IM/DD comparable DSP | 弱 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 101 | 2025 | 信道建模/湍流/大气 / 相干/自相干检测 | Impact of Elevation Angle on 100 Gbps Optical Coherent Uplink Transmission in Low Earth Orbit S | 强 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 102 | 2025 | 地面站/OGS/终端 / ATP/指向/PAT / 在轨演示/任务 / 调制/复用 / QKD/量子/光子计数 / 编码/FEC/交织 / 深空/月地/cislunar | Implementation of high-photon-efficiency optical modem for ESA’s technology demonstration of de | 弱 | 未明确 | 实测 | 🟢 abstract自陈: to address the challenge of achieving high data rates for the downlink, the modem implemen |
| 103 | 2025 | 地面站/OGS/终端 / 在轨演示/任务 / 调制/复用 / 链路预算/系统级 / 放大器/EDFA/光子载荷 | In-orbit Test Results of a 1 Gbps Free Space Direct-to-Earth Optical Satellite Link of a CubeSa | 未明确 | 未明确 | 实测 | 🔴 abstract自陈成熟/广泛采用 |
| 104 | 2025 | 地面站/OGS/终端 / 在轨演示/任务 | In-orbit test results of a free space optical satellite link between a CubeSat-compatible laser | 未明确 | the geometrical losses for both up- and downlink,  | 实测 | 🔴 abstract自陈成熟/广泛采用 |
| 105 | 2025 | 网络层/路由/RWA / 信道建模/湍流/大气 / AO/自适应光学/波前 | Interaction Between Adaptive Optics and Mode Diversity Reception in GEO Optical Downlinks | 强 | 未明确 | 仿真 | 🟢 abstract自陈: atmospheric turbulence significantly hinders the reliability of satellite-to-ground laser  |
| 106 | 2025 | 网络层/路由/RWA / 在轨演示/任务 / 深空/月地/cislunar / feeder/中继 | Interplanetary CubeSat Networks: Challenges and Future Prospects in Deep Space Communication | 未明确 | 未明确 | 综述 | 🟢 abstract自陈: establishing dependable communication networks for cubesats in deep space is a significant |
| 107 | 2025 | 地面站/OGS/终端 / 网络层/路由/RWA / 信道建模/湍流/大气 / ATP/指向/PAT / 在轨演示/任务 / feeder/中继 | Kepler Validates SDA-Compatible Space-to-Ground Laser Links ... | 强 | 未明确 | 实测/解析 | 🔴 abstract自陈成熟/广泛采用 |
| 108 | 2025 | 地面站/OGS/终端 / 信道建模/湍流/大气 / AO/自适应光学/波前 | LEO-to-ground low elevation optical communication: optimization of an adaptive optics design ro | 强 | 未明确 | 仿真/实测 | 🟢 abstract自陈: however, at low elevations, amplitude fluctuations (or scintillation) challenge this corre |
| 109 | 2025 | 放大器/EDFA/光子载荷 | Lab-payload for biological CubeSat satellite | 弱 | 未明确 | 未明确 | 🔴 abstract自陈成熟/广泛采用 |
| 110 | 2025 | 地面站/OGS/终端 / 链路预算/系统级 / 深空/月地/cislunar | Laser Technology: The Future of Space-Based Communications | 未明确 | conventional methods(泛指) | 未明确 | 🟡 abstract无缝信号待精读 |
| 111 | 2025 | 地面站/OGS/终端 / 链路预算/系统级 / feeder/中继 | Low-SWaP spaceborne fiber to telescope terminal (FiTT) for high-efficiency optical feederlink | 未明确 | 未明确 | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 112 | 2025 | 调制/复用 / 编码/FEC/交织 | Low-crosstalk, filter-free, and secure WDM for optical inter-CubeSat communication using fluore | 未明确 | that without using pwc | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 113 | 2025 | 调制/复用 / 相干/自相干检测 / 载波同步/恢复 | Minimum Nyquist Frequency Coherent OQAM Transmission for High Sensitivity Satellite Optical Com | 弱 | conventional methods(泛指) | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 114 | 2025 | 地面站/OGS/终端 / 网络层/路由/RWA / ATP/指向/PAT / 在轨演示/任务 / 链路预算/系统级 / 深空/月地/cislunar / ISL/星间链路 | Modeling Pointing, Acquisition, and Tracking Delays in Free-Space Optical Satellite Networks | 弱 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 115 | 2025 | 调制/复用 / 相干/自相干检测 / 载波同步/恢复 / ISL/星间链路 | Modeling and Simulation of Inter-Satellite Laser Communication for Space-Based Gravitational Wa | 弱 | 10−6 when the modulation index exceeds 3 | 仿真 | 🟡 abstract无缝信号待精读 |
| 116 | 2025 | 地面站/OGS/终端 / ATP/指向/PAT / 在轨演示/任务 / 深空/月地/cislunar | NASA Deep Space Comm Demo Surpasses Expectations / Mirage News | 未明确 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 117 | 2025 | 地面站/OGS/终端 / ATP/指向/PAT / 在轨演示/任务 / 深空/月地/cislunar | NASA’s Deep Space Communications Demo Exceeds Project Expectations - NASA | 未明确 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 118 | 2025 | 地面站/OGS/终端 / ATP/指向/PAT / 载波同步/恢复 | OSIRIS4CubeSat—The World’s Smallest Commercially Available Laser Communication Terminal | 弱 | 未明确 | 仿真/综述 | 🟡 abstract自陈达成增益未自陈缝 |
| 119 | 2025 | 未明确 | On-Orbit Uncertainty Field Analysis and Verification for LEO Satellite Laser Communication | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 120 | 2025 | 地面站/OGS/终端 / 信道建模/湍流/大气 / QKD/量子/光子计数 / 链路预算/系统级 | Optical Downlink Modeling for LEO and MEO Satellites under ... - arXiv | 强 | 未明确 | 仿真/实测 | 🔴 abstract自陈成熟/广泛采用 |
| 121 | 2025 | 地面站/OGS/终端 / 信道建模/湍流/大气 / QKD/量子/光子计数 / 链路预算/系统级 | Optical Downlink Modeling for LEO and MEO Satellites under Atmospheric Turbulence with a Quantu | 强 | 未明确 | 仿真 | 🔴 abstract自陈成熟/广泛采用 |
| 122 | 2025 | 信道建模/湍流/大气 / AO/自适应光学/波前 / 链路预算/系统级 / feeder/中继 / ISL/星间链路 | Optical Feeder Link System Design via Simulation and Emulation Tools | 强 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 123 | 2025 | QKD/量子/光子计数 / 链路预算/系统级 / feeder/中继 / ISL/星间链路 | Optical Feeder Links: Unlocking the Next Frontier in Space ... | 未明确 | 未明确 | 未明确 | 🟢 abstract自陈: optical feeder links: unlocking the next frontier in space communications - frank rayal

u |
| 124 | 2025 | 信道建模/湍流/大气 / ATP/指向/PAT / 调制/复用 | Optical OTFS Modulation for Free Space Optical-Based LEO Satellite Communication Systems | 强 | 未明确 | 仿真 | 🟡 abstract自陈达成增益未自陈缝 |
| 125 | 2025 | 未明确 | Optical Performance and Environmental Durability of Radiation-Resistant Polarization-Maintainin | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 126 | 2025 | 在轨演示/任务 / 链路预算/系统级 | Optical Systems for CubeSats / Design Considerations for Space ... | 未明确 | 未明确 | 未明确 | 🔴 abstract自陈成熟/广泛采用 |
| 127 | 2025 | 地面站/OGS/终端 / ATP/指向/PAT / 在轨演示/任务 / 链路预算/系统级 / ISL/星间链路 / 放大器/EDFA/光子载荷 | Optical alignment for CubeSat crosslink laser communication terminals | 弱 | 未明确 | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 128 | 2025 | 网络层/路由/RWA / 语义/AI/DL/ML / 链路预算/系统级 / ISL/星间链路 | Optical satellite communications - National Research Council Canada | 未明确 | 未明确 | 未明确 | 🟢 abstract自陈: optical satellite communications - national research council canada

# optical satellite c |
| 129 | 2025 | 地面站/OGS/终端 / 网络层/路由/RWA | Optical technology revolutionizing space communications | 未明确 | 未明确 | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 130 | 2025 | ATP/指向/PAT / 调制/复用 / 相干/自相干检测 / 载波同步/恢复 / 信道估计/均衡 / 链路预算/系统级 / ISL/星间链路 | Performance Analysis of 112 Gbps Polarization Division Multiplexed 16-PSK Based Inter-Satellite | 弱 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 131 | 2025 | 调制/复用 / ISL/星间链路 | Performance Studies of Inter-Satellite Optical Wireless Communication Links Using PPM | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 132 | 2025 | 未明确 | Performance and Reliability of 10 W-Class High-Power Optical Amplifiers for Space Laser Communi | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 133 | 2025 | 相干/自相干检测 / 放大器/EDFA/光子载荷 | Photonic Integrated Circuits for Optical Satellite Links: A Review of the Technology Status and | 弱 | 未明确 | 未明确 | 🔴 abstract自陈成熟/广泛采用 |
| 134 | 2025 | 地面站/OGS/终端 / ATP/指向/PAT / 编码/FEC/交织 / ISL/星间链路 | Pointing error correction for satellite-based laser communication terminal | 弱 | conventional methods(泛指) | 实测 | 🟡 abstract无缝信号待精读 |
| 135 | 2025 | ATP/指向/PAT / 在轨演示/任务 | Pointing, Acquisition, and Tracking (PAT) for Optical Satellite Communications: Recent Trends a | 弱 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 136 | 2025 | 地面站/OGS/终端 / 网络层/路由/RWA / 信道建模/湍流/大气 / ATP/指向/PAT / 链路预算/系统级 / feeder/中继 | Predictive Optical Feeder Link (OFL) Planning in Space-Ground Integrated Optical Networks (SGIO | 强 | non-predictive strategies, while maintaining perfo | 仿真 | 🟢 abstract自陈: optical feeder links (ofls) are emerging as a promising solution to overcome the arising d |
| 137 | 2025 | 地面站/OGS/终端 / 在轨演示/任务 / QKD/量子/光子计数 / AO/自适应光学/波前 | Preliminary results of optical downlink between QUBE satellite to the upgraded Optical Ground S | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 138 | 2025 | 网络层/路由/RWA / 信道建模/湍流/大气 / 链路预算/系统级 / feeder/中继 | RELAY-ASSISTED HIGH-CAPACITY SATELLITE FEEDER LINKS WITH INTEGRATED LINE-OF-SIGHT MIMO RF AND O | 强 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 139 | 2025 | 地面站/OGS/终端 / 网络层/路由/RWA / ATP/指向/PAT / 在轨演示/任务 / QKD/量子/光子计数 / 相干/自相干检测 | Rapid tactical deployment capability of a transportable optical ground station / Scientific Rep | 弱 | 未明确 | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 140 | 2025 | 地面站/OGS/终端 / 信道建模/湍流/大气 | Real-time optical turbulence and wind profile monitoring with FEELINGS optical ground station | 强 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 141 | 2025 | 网络层/路由/RWA / 语义/AI/DL/ML / ISL/星间链路 | Reliable Low-Latency Routing for VLEO Satellite Optical Network: A Multiagent Reinforcement Lea | 未明确 | 未明确 | 仿真/实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 142 | 2025 | ATP/指向/PAT / 深空/月地/cislunar | Research and simulation analysis of deep space optical communication | 弱 | 未明确 | 仿真 | 🟡 abstract无缝信号待精读 |
| 143 | 2025 | 网络层/路由/RWA / 编码/FEC/交织 / 语义/AI/DL/ML / ISL/星间链路 | Research on Key Technologies of Elastic Satellite Optical Network Based on Optical Service Unit | 未明确 | 未明确 | 仿真/综述 | 🔴 abstract自陈成熟/广泛采用 |
| 144 | 2025 | 网络层/路由/RWA / 载波同步/恢复 / 语义/AI/DL/ML | Resource Allocation in Flexible-Bandwidth Fine-Grained Optical Transport Networks for Geo-Distr | 未明确 | 未明确 | 仿真 | 🟡 abstract自陈达成增益未自陈缝 |
| 145 | 2025 | 地面站/OGS/终端 / 网络层/路由/RWA / ATP/指向/PAT / 深空/月地/cislunar / feeder/中继 / ISL/星间链路 | Results of SDA-standard-compatible optical inter-satellite link testing between Kepler Communic | 弱 | 未明确 | 实测 | 🔴 abstract自陈成熟/广泛采用 |
| 146 | 2025 | 地面站/OGS/终端 / 相干/自相干检测 / 载波同步/恢复 / 信道估计/均衡 / 编码/FEC/交织 / 链路预算/系统级 | Review and Analysis of Digital Signal Processing Algorithms for Coherent Optical Satellite Link | 弱 | 未明确 | 仿真 | 🔴 abstract自陈成熟/广泛采用 |
| 147 | 2025 | 网络层/路由/RWA / 信道建模/湍流/大气 / AO/自适应光学/波前 / 相干/自相干检测 / 链路预算/系统级 / feeder/中继 | Robust MISO coherent optical GEO satellite feeder link with relaxed implementation constraints | 强 | the classical single-input single-output (siso) ap | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 148 | 2025 | 网络层/路由/RWA | Role, Technological Challenges, and R&D activity of GEO Satellite in 6G Multi-Orbit Network | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 149 | 2025 | 地面站/OGS/终端 / QKD/量子/光子计数 | SMF-Coupled Compact Ground Terminal with Advanced Filtering Towards Daylight C-Band Satellite Q | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 150 | 2025 | 未明确 | Satellite Optical Communications for Beyond 5G/6G | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 151 | 2025 | 网络层/路由/RWA / 信道建模/湍流/大气 / ATP/指向/PAT | Satellite-to-ground optical communication systems under orbital deviations and atmospheric turb | 强 | 未明确 | 仿真/解析 | 🟡 abstract自陈达成增益未自陈缝 |
| 152 | 2025 | 网络层/路由/RWA / ATP/指向/PAT / 调制/复用 / ISL/星间链路 | Scalable Inter-Satellite Optical Wireless Communication Based on CWDM and EDFAs for 6G and NTN  | 弱 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 153 | 2025 | 在轨演示/任务 / 放大器/EDFA/光子载荷 | Scanway Optical Payload - SCANWAY | 未明确 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 154 | 2025 | 网络层/路由/RWA / 信道建模/湍流/大气 / 在轨演示/任务 / feeder/中继 | Seasonal dependence comparison of GEO satellite-to-ground laser communication link using LUCAS  | 强 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 155 | 2025 | 网络层/路由/RWA / 信道建模/湍流/大气 / QKD/量子/光子计数 / 语义/AI/DL/ML | Security challenges from physical to network layers in satellite free-space optical communicati | 强 | the conventional rf systems, fso provides distinct | 综述 | 🔴 abstract自陈成熟/广泛采用 |
| 156 | 2025 | ATP/指向/PAT / 在轨演示/任务 / ISL/星间链路 | Silicon Photomultipliers Implemented as Free-Space Optical Communication Sensors | 弱 | rf technologies | 实测 | 🔴 abstract自陈成熟/广泛采用 |
| 157 | 2025 | 地面站/OGS/终端 / 网络层/路由/RWA / 在轨演示/任务 | Space Development Agency demos key space-to-air ... | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 158 | 2025 | 网络层/路由/RWA / 信道建模/湍流/大气 / 链路预算/系统级 | Space-to-Ground Optical Communication Downlink Scheduling Under Uncertainty of Link Availabilit | 强 | gurobi and kuhn-munkres-based methods | 仿真 | 🟢 abstract自陈: simulation results indicate that considering uncertainty can enhance data throughput, with |
| 159 | 2025 | ATP/指向/PAT / 在轨演示/任务 / ISL/星间链路 | Spire Achieves Two-Way Laser Communication Between Satellites ... | 弱 | 未明确 | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 160 | 2025 | 网络层/路由/RWA / 在轨演示/任务 / 链路预算/系统级 / feeder/中继 | Starlink mini lasers to link Muon Space satellites for near real-time connectivity - SpaceNews | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 161 | 2025 | 网络层/路由/RWA / 信道建模/湍流/大气 / ATP/指向/PAT / 编码/FEC/交织 | Statistics of Received Power Time Series for Optical LEO Satellite Uplinks | 强 | analytical results and measurements in terms of th | 仿真/实测 | 🟡 abstract无缝信号待精读 |
| 162 | 2025 | 在轨演示/任务 / 调制/复用 / QKD/量子/光子计数 / 深空/月地/cislunar | Superconducting nanowire single-photon detector array for ESA’s ground laser receiver in collab | 弱 | 未明确 | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 163 | 2025 | 链路预算/系统级 | Thales : Alenia Space to develop SOLiS very-high-throughput laser communications demonstrator | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 164 | 2025 | 网络层/路由/RWA / 在轨演示/任务 / QKD/量子/光子计数 / 链路预算/系统级 | Thales Alenia Space and ESA Partner to Develop HydRON Multi-Orbit Optical Network | 未明确 | 未明确 | 实测 | 🟢 abstract自陈: hydron optical communication for broadband in space

the project will be conducted with th |
| 165 | 2025 | 调制/复用 / 载波同步/恢复 | The modulation and demodulation technology of 100Gbps satellite laser communication system | 弱 | the dp-qpsk modulation method, the sensitivity of  | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 166 | 2025 | 地面站/OGS/终端 / 调制/复用 / 载波同步/恢复 / 深空/月地/cislunar | Timing Estimation for Deep Space Optical Communication Signals | 弱 | the pilot method, as well as eliminating or reduci | 仿真 | 🟡 abstract无缝信号待精读 |
| 167 | 2025 | 网络层/路由/RWA / ISL/星间链路 | Topology-Repairing Based on Inter-Satellite Laser Link Reconfiguration in Optical Satellite Net | 未明确 | 未明确 | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 168 | 2025 | 调制/复用 / 相干/自相干检测 / 放大器/EDFA/光子载荷 | Ultra-low optical input power 1μm-laser amplifier for WDM satellite communication | 弱 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 169 | 2025 | 未明确 | WGAN-based satellite laser communication networks channel modeling | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 170 | 2025 | 网络层/路由/RWA / ISL/星间链路 | Wireless Optical Inter-Satellite Link Risk-Aware Snapshot Routing Strategy in Satellite Network | 未明确 | 未明确 | 未明确 | 🟢 abstract自陈: wireless optical inter-satellite links (woisls), essential for next-generation satellite n |
| 171 | 2025 | 信道建模/湍流/大气 / 调制/复用 / feeder/中继 | World's First Successful 2 Tbit/s Free-Space Optical Communication Using Small Optical Terminal | 强 | 未明确 | 实测 | 🟢 abstract自陈: despite the difficult conditions of an urban environment with atmospheric turbulence that  |
| 172 | 2025 | 地面站/OGS/终端 / 网络层/路由/RWA / 信道建模/湍流/大气 / 在轨演示/任务 / QKD/量子/光子计数 / feeder/中继 | [PDF] Overview of Ground Station 1 supporting the NASA space ... | 强 | 未明确 | 实测/综述 | 🟡 abstract自陈达成增益未自陈缝 |
| 173 | 2024 | ISL/星间链路 | A 4 × 20 Gbps inter-satellite optical wireless communication system based on orbital angular mo | 未明确 | 未明确 | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 174 | 2024 | 地面站/OGS/终端 / ATP/指向/PAT / 链路预算/系统级 / ISL/星间链路 | A Case Study of an Hybrid RF and Optical Inter-Satellite Link Terminal to Enhance Optical Point | 弱 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 175 | 2024 | 地面站/OGS/终端 / 网络层/路由/RWA / 信道建模/湍流/大气 / feeder/中继 / ISL/星间链路 / 放大器/EDFA/光子载荷 | A Relay-Assisted Ground to LEO and LEO to GEO Inter-Satellite Optical Wireless Communication Li | 强 | the conventional amplifier-based relay | 未明确 | 🟡 abstract无缝信号待精读 |
| 176 | 2024 | 网络层/路由/RWA / ISL/星间链路 | A Strategic Development of an Optical Inter Satellite Link Network in the IRNSS Constellation | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 177 | 2024 | ATP/指向/PAT | Adaptive compound control of laser beam jitter in deep-space optical communication systems | 弱 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 178 | 2024 | ATP/指向/PAT | Analytic pointing error evaluation on nano-satellite laser communication system | 弱 | 未明确 | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 179 | 2024 | 地面站/OGS/终端 / 深空/月地/cislunar | Architecture and analysis of telescope arrays for deep space optical communication | 未明确 | 未明确 | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 180 | 2024 | 地面站/OGS/终端 / 信道建模/湍流/大气 / ATP/指向/PAT / QKD/量子/光子计数 | Assessment of Signal Losses in LEO Satellite-to-Ground Optical Communication Links | 强 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 181 | 2024 | 地面站/OGS/终端 / ATP/指向/PAT / 链路预算/系统级 / ISL/星间链路 | Attitude Control System Design and Analysis of 6U CubeSat for Free Space Optical Communication( | 弱 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 182 | 2024 | ATP/指向/PAT / ISL/星间链路 | Average bit-error rate analysis of an inter-satellite optical communication system under the ef | 弱 | 未明确 | 仿真/解析 | 🟡 abstract自陈达成增益未自陈缝 |
| 183 | 2024 | 相干/自相干检测 / 链路预算/系统级 / feeder/中继 | Coherent optical feeder links for very high throughput satellite systems | 弱 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 184 | 2024 | 地面站/OGS/终端 / 载波同步/恢复 / 编码/FEC/交织 / 链路预算/系统级 | CubeCAT - Laser Communication Module / AAC Clyde Space | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 185 | 2024 | 地面站/OGS/终端 / 网络层/路由/RWA / 在轨演示/任务 / feeder/中继 | Data Management and Data Products of a Daily Optical Communications Ground Station for Laser Co | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 186 | 2024 | 网络层/路由/RWA / 信道建模/湍流/大气 / 调制/复用 / 相干/自相干检测 / 信道估计/均衡 / feeder/中继 | Data-Aided Multi-Format DSP for Robust Free-Space Coherent Optical Communication | 强 | 未明确 | 仿真 | 🟡 abstract无缝信号待精读 |
| 187 | 2024 | 在轨演示/任务 / 深空/月地/cislunar | Deep Space Optical Communications from the Psyche Mission | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 188 | 2024 | ISL/星间链路 | Design and control of a steering mirror for a free-space optical communications CubeSat for gig | 未明确 | 未明确 | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 189 | 2024 | 网络层/路由/RWA / ISL/星间链路 | Development of a Free Space Optical Isl Network Between Leo Constellations & a Geo Satellite | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 190 | 2024 | ATP/指向/PAT / ISL/星间链路 | Ego-Satellite Perspective Multi-PAT Configurations for Optical Inter-Satellite Links | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 191 | 2024 | 网络层/路由/RWA / 调制/复用 / feeder/中继 / ISL/星间链路 / 放大器/EDFA/光子载荷 | Energy-efficient regeneration routing in satellite optical networks under translucent optical p | 未明确 | baseline:baselines are proposed for ee-rr, which a | 仿真 | 🟡 abstract自陈达成增益未自陈缝 |
| 192 | 2024 | 网络层/路由/RWA / ATP/指向/PAT / 链路预算/系统级 / ISL/星间链路 | Green laser inter-satellite link planning in satellite optical networks: trading off the batter | 弱 | existing schemes, greenlp reduces battery lifetime | 仿真 | 🟡 abstract无缝信号待精读 |
| 193 | 2024 | 网络层/路由/RWA / 调制/复用 / 链路预算/系统级 | Heterogeneous optical network and power allocation scheme for inter-CubeSat communication | 弱 | the conventional power allocation scheme at a ber  | 仿真/解析 | 🟡 abstract自陈达成增益未自陈缝 |
| 194 | 2024 | 未明确 | Inter-Layer Link Allocation in Multilayer LEO Optical Satellite Networks | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 195 | 2024 | 网络层/路由/RWA / 语义/AI/DL/ML / ISL/星间链路 | Inter-Satellite Links (ISLs) and Their Role in Enhancing Global ... | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 196 | 2024 | 网络层/路由/RWA / feeder/中继 | Kepler Announces Formal Shift in Strategy for Optical Data Relay Network - Kepler | 未明确 | 12 kg of the rf satellites | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 197 | 2024 | 地面站/OGS/终端 / 网络层/路由/RWA / ATP/指向/PAT / feeder/中继 / ISL/星间链路 | Kepler Validates SDA-Compatible Optical Technology For | 未明确 | 未明确 | 未明确 | 🔴 abstract自陈成熟/广泛采用 |
| 198 | 2024 | 地面站/OGS/终端 / 网络层/路由/RWA / feeder/中继 / ISL/星间链路 | Kepler demonstrates optical data relay service in LEO - SpaceNews | 未明确 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 199 | 2024 | 地面站/OGS/终端 / 信道建模/湍流/大气 / feeder/中继 | Laboratory emulation of LEO downlink optical feeder link employing commercial transceivers | 强 | 未明确 | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 200 | 2024 | 网络层/路由/RWA / feeder/中继 / ISL/星间链路 | Latitude- and time-zone-aware load balancing in optical satellite networks | 未明确 | baseline:baseline strategies | 仿真 | 🟡 abstract自陈达成增益未自陈缝 |
| 201 | 2024 | 地面站/OGS/终端 / 在轨演示/任务 / 语义/AI/DL/ML / 链路预算/系统级 / 放大器/EDFA/光子载荷 | Leveraging Deep Learning for High-Resolution Optical Satellite Imagery From Low-Cost Small Sate | 未明确 | 未明确 | 实测 | 🟢 abstract自陈: small satellites (less than 1000 kg in mass) and their constellations can be delivered rap |
| 202 | 2024 | 信道建模/湍流/大气 / ATP/指向/PAT / 在轨演示/任务 / 调制/复用 / 相干/自相干检测 / 链路预算/系统级 / feeder/中继 | Link budget analysis of bi-directional LEO and GEO optical feeder links advancing the beam wand | 强 | conventional methods(泛指) | 仿真/实测 | 🟡 abstract无缝信号待精读 |
| 203 | 2024 | 信道建模/湍流/大气 / ATP/指向/PAT / 调制/复用 / 编码/FEC/交织 / 链路预算/系统级 / ISL/星间链路 | MIMO and PDM-based intersatellite optical link for high-speed data transfer and remote sensing  | 强 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 204 | 2024 | 调制/复用 / 相干/自相干检测 / 语义/AI/DL/ML | Modulation Format Recognition Scheme Based on Reinforcement Learning in Coherent Optical Commun | 弱 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 205 | 2024 | 在轨演示/任务 / 深空/月地/cislunar | NASA’s Optical Comms Demo Transmits Data Over 140 Million Miles - NASA | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 206 | 2024 | 网络层/路由/RWA / ATP/指向/PAT / 语义/AI/DL/ML / ISL/星间链路 | On an Intelligent Hierarchical Routing Strategy for Ultra-Dense Free Space Optical Low Earth Or | 弱 | 未明确 | 仿真 | 🟡 abstract自陈达成增益未自陈缝 |
| 207 | 2024 | 在轨演示/任务 / 相干/自相干检测 / ISL/星间链路 | On-Orbit Demonstration of Laser Frequency Sweep at 1550 nm to Achieve Doppler Shift Compensatio | 弱 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 208 | 2024 | 地面站/OGS/终端 | Optical Ground Station: Safran revolutionizing space communications | 未明确 | traditional radiofrequency communications | 未明确 | 🟢 abstract自陈: optical ground station: safran revolutionizing space communications / safran

# optical gr |
| 209 | 2024 | 在轨演示/任务 / 链路预算/系统级 / ISL/星间链路 | Optical Inter-Satellite Links - MPB Communications | 弱 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 210 | 2024 | 在轨演示/任务 / 链路预算/系统级 / 深空/月地/cislunar / 放大器/EDFA/光子载荷 | Optical Payloads and Space Optical Remote Sensing - Avantier | 未明确 | 未明确 | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 211 | 2024 | 地面站/OGS/终端 / 网络层/路由/RWA / 信道建模/湍流/大气 / QKD/量子/光子计数 / 链路预算/系统级 | Optical ground station diversity for satellite quantum key distribution in Ireland | 强 | 未明确 | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 212 | 2024 | 地面站/OGS/终端 / QKD/量子/光子计数 / 放大器/EDFA/光子载荷 | Optical payload design for downlink quantum key distribution and keyless communication using Cu | 未明确 | 未明确 | 仿真 | 🟡 abstract自陈达成增益未自陈缝 |
| 213 | 2024 | 地面站/OGS/终端 / 网络层/路由/RWA / 信道建模/湍流/大气 / 在轨演示/任务 / feeder/中继 | Optical turbulence profiling at the Table Mountain Facility with the Laser Communication Relay  | 强 | other turbulence monitors such as a solar scintill | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 214 | 2024 | 地面站/OGS/终端 / ATP/指向/PAT / ISL/星间链路 | Optimization of acquisition patterns for establishing inter CubeSat optical communications | 未明确 | 未明确 | 仿真 | 🟢 abstract自陈: as commercially available cubesats with up to six standardized units cannot achieve the pr |
| 215 | 2024 | ATP/指向/PAT / 调制/复用 | Optimizing 20 Gbps of ground-to-satellite free-space optical communication in low earth orbit w | 弱 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 216 | 2024 | 信道建模/湍流/大气 / 放大器/EDFA/光子载荷 | Orbital Sidekick Global Hyperspectral Observation Satellite (GHOSt) payload: calibration and ch | 强 | 未明确 | 综述 | 🟡 abstract无缝信号待精读 |
| 217 | 2024 | 网络层/路由/RWA / 信道建模/湍流/大气 / ATP/指向/PAT / 调制/复用 / 相干/自相干检测 / 链路预算/系统级 / feeder/中继 | Performance Analysis of Mixed FSO/RF System for Satellite-Terrestrial Relay Network | 强 | 未明确 | 仿真/解析 | 🟡 abstract无缝信号待精读 |
| 218 | 2024 | 网络层/路由/RWA / 信道建模/湍流/大气 / ATP/指向/PAT / 链路预算/系统级 / feeder/中继 | Performance Analysis of Relay-Aided Satellite-Underwater Acoustic Communication Systems | 强 | 未明确 | 仿真/解析 | 🟡 abstract自陈达成增益未自陈缝 |
| 219 | 2024 | 信道建模/湍流/大气 / 调制/复用 / AO/自适应光学/波前 / 相干/自相干检测 | Performance analysis of satellite-to-Earth 16QAM coherent optical communication under the influ | 强 | 未明确 | 仿真/解析 | 🟡 abstract无缝信号待精读 |
| 220 | 2024 | 信道建模/湍流/大气 / ATP/指向/PAT / AO/自适应光学/波前 / 相干/自相干检测 | Performance analysis of satellite-to-ground 16QAM coherent optical communication | 强 | 未明确 | 仿真/解析 | 🟡 abstract无缝信号待精读 |
| 221 | 2024 | 网络层/路由/RWA / 信道建模/湍流/大气 / 调制/复用 / QKD/量子/光子计数 / 编码/FEC/交织 / 链路预算/系统级 / ISL/星间链路 | Performance enhancement of an inter-satellite optical wireless communication link carrying 16 c | 强 | 未明确 | 解析/综述 | 🟡 abstract自陈达成增益未自陈缝 |
| 222 | 2024 | 信道建模/湍流/大气 / 调制/复用 | Phase fluctuations-induced bit error ratio of deep-space optical communication systems during s | 强 | 未明确 | 仿真 | 🟡 abstract自陈达成增益未自陈缝 |
| 223 | 2024 | 地面站/OGS/终端 / ATP/指向/PAT / 链路预算/系统级 | Point Ahead Angle(PAA) Estimation and a Control Algorithm for Satellite-Pointing of the Ground  | 弱 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 224 | 2024 | 地面站/OGS/终端 / 信道建模/湍流/大气 / ATP/指向/PAT / 在轨演示/任务 / AO/自适应光学/波前 / 放大器/EDFA/光子载荷 | Pre-distortion adaptive optics: experimental results from bi-directional tracking links between | 强 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 225 | 2024 | 地面站/OGS/终端 / 网络层/路由/RWA / AO/自适应光学/波前 / 相干/自相干检测 / 深空/月地/cislunar / feeder/中继 | Preliminary design of key optical components onboard laser communication terminal of GEO data r | 弱 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 226 | 2024 | 网络层/路由/RWA / 调制/复用 / 链路预算/系统级 / ISL/星间链路 | Queuing Delay Analysis for Wavelength Routing Optical Satellite Networks Over Dual-Layer Conste | 未明确 | theoretical results in terms of queuing length and | 仿真/解析 | 🟡 abstract无缝信号待精读 |
| 227 | 2024 | ISL/星间链路 | RF-Assisted Uncertainty Cone Reduction in Free-Space Optical Inter-Satellite Links | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 228 | 2024 | 地面站/OGS/终端 | Real-Time Satellite Optical Terminal Prototype with Integrated Mult-Rate Transmission and Rangi | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 229 | 2024 | 深空/月地/cislunar | SNSPD Arrays for Deep Space Optical Communication | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 230 | 2024 | 地面站/OGS/终端 | Safran to supply latest-generation optical ground station to Swedish Space Corporation / Safran | 未明确 | conventional methods(泛指) | 未明确 | 🟡 abstract无缝信号待精读 |
| 231 | 2024 | 网络层/路由/RWA / 放大器/EDFA/光子载荷 | Satellite Communication Payload Based on Microwave Photonics: Benefits, Architecture, and Techn | 未明确 | 未明确 | 综述 | 🟢 abstract自陈: the electronic bottleneck of traditional microwave systems in processing speed and transmi |
| 232 | 2024 | 信道建模/湍流/大气 / 在轨演示/任务 / AO/自适应光学/波前 | Satellite-to-Ground Optical Links - MPB Communications | 强 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 233 | 2024 | 相干/自相干检测 | Simple real-time high-sensitivity heterodyne coherent optical transceiver at intraplane satelli | 弱 | 未明确 | 实测/解析 | 🟡 abstract无缝信号待精读 |
| 234 | 2024 | 地面站/OGS/终端 / 网络层/路由/RWA / ATP/指向/PAT / 深空/月地/cislunar | Space optical communication system for space optical networks and deep space exploration | 弱 | 未明确 | 实测 | 🟢 abstract自陈: the acquisition time of tens to hundreds of seconds in the optical link between satellites |
| 235 | 2024 | ATP/指向/PAT / 链路预算/系统级 / ISL/星间链路 | Study & Analysis of a Free Space Optical Link Between a Sun Synchronous LEO Satellite and a GEO | 弱 | 未明确 | 未明确 | 🔴 abstract自陈成熟/广泛采用 |
| 236 | 2024 | 放大器/EDFA/光子载荷 | Systemic design of the very-high-resolution imaging payload of an optical remote sensing satell | 未明确 | larger payloads in higher orbits in remote sensing | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 237 | 2024 | 地面站/OGS/终端 / 在轨演示/任务 / 深空/月地/cislunar | Telescope Arrays for Deep Space Optical Communication: Preliminary Operational Results | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 238 | 2024 | 地面站/OGS/终端 / 在轨演示/任务 / 调制/复用 / QKD/量子/光子计数 / 载波同步/恢复 / 编码/FEC/交织 / 深空/月地/cislunar | Testing of a photon-counting optical ground receiver with emulated space-to-ground link effects | 弱 | 未明确 | 仿真/实测 | 🟢 abstract自陈: snspd device properties, which impact detection jitter and time delay, can limit the recei |
| 239 | 2024 | 信道建模/湍流/大气 / ATP/指向/PAT / 链路预算/系统级 | The transformative technology of laser/free-space optical ... | 强 | 未明确 | 未明确 | 🟢 abstract自陈: lasercom technology challenges include a requirement for highly precise laser beam pointin |
| 240 | 2024 | 信道建模/湍流/大气 / ATP/指向/PAT / AO/自适应光学/波前 / 信道估计/均衡 / feeder/中继 | Tip tilt and focus estimation based on LGS and downlink joint measurements for ground to GEO sa | 强 | 未明确 | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 241 | 2024 | 地面站/OGS/终端 | Toward Optimal Placement of Free-Space Optical Terminal on the Spacecraft Body | 未明确 | baseline:baseline case studies to gain valuable in | 仿真 | 🟢 abstract自陈: however, the gimbal's limited swipe range poses a challenge in optimizing the placement of |
| 242 | 2024 | 地面站/OGS/终端 / 网络层/路由/RWA / 信道建模/湍流/大气 | Update on the German and Australasian Optical Ground Station Networks | 强 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 243 | 2024 | 相干/自相干检测 / ISL/星间链路 | Wide-Range and High-Precision Doppler Simulation for Inter-Satellite Coherent Optical Communica | 弱 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 244 | 2024 | 地面站/OGS/终端 / 网络层/路由/RWA / 链路预算/系统级 / feeder/中继 / 放大器/EDFA/光子载荷 | eFiberSat - Optical Zonu Corporation | 未明确 | 未明确 | 未明确 | 🔴 abstract自陈成熟/广泛采用 |
| 245 | 2023 | 地面站/OGS/终端 / 在轨演示/任务 / 深空/月地/cislunar | 10 Million Miles Away: NASA Achieves Historic Data Exchange With Deep Space Optical Communicati | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 246 | 2023 | 在轨演示/任务 | A Holistic Control Center for the Operation of PUS-Based Optical Communication CubeSat Technolo | 未明确 | 未明确 | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 247 | 2023 | 地面站/OGS/终端 / ATP/指向/PAT / 放大器/EDFA/光子载荷 | A compact pointing assembly for a CubeSat to ground station free-space optical communication ba | 弱 | classical gimbal-based mirror mounts or periscopes | 未明确 | 🟢 abstract自陈: achieving a good ratio between the size and the performance of the optical payload is stil |
| 248 | 2023 | 地面站/OGS/终端 / ATP/指向/PAT / AO/自适应光学/波前 / 链路预算/系统级 / feeder/中继 | ALASCA: the ESA Laser Guide Star Adaptive Optics Optical Feeder Link demonstrator facility | 未明确 | astronomical solutions | 综述 | 🟢 abstract自陈: space optical communication represents a technological challenge due to its specific requi |
| 249 | 2023 | 网络层/路由/RWA / 在轨演示/任务 / ISL/星间链路 / 放大器/EDFA/光子载荷 | Amazon’s Project Kuiper completes successful test of space lasers | 未明确 | 未明确 | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 250 | 2023 | 未明确 | An Autoencoder-based Transceiver for UAV-to-Ground Free Space Optical Communication | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 251 | 2023 | 地面站/OGS/终端 / 网络层/路由/RWA / 语义/AI/DL/ML / 链路预算/系统级 | An Intelligent Ground Station Selection Algorithm in Satellite Optical Communications via Deep  | 未明确 | 未明确 | 实测 | 🟢 abstract自陈: this property is exploited by the site diversity technique, that tries to limit bad weathe |
| 252 | 2023 | 信道建模/湍流/大气 / 语义/AI/DL/ML | Application Of Deep Learning in Free Space Optical Communication Using Malaga Channel | 强 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 253 | 2023 | 在轨演示/任务 / 相干/自相干检测 / ISL/星间链路 | Bread-board demonstration of a monolithically integrated coherent receiver for 100 Gb/s optical | 弱 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 254 | 2023 | 网络层/路由/RWA / 调制/复用 / 链路预算/系统级 / feeder/中继 | Broadband Satellite Communication System using Optical Feeder Links - Patent Application | 弱 | 未明确 | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 255 | 2023 | 地面站/OGS/终端 / 信道建模/湍流/大气 / 相干/自相干检测 / feeder/中继 | Coherent Receiver Simulation for High-Speed DP-QPSK in Optical GEO Satellite Feeder Link | 强 | 未明确 | 仿真/解析 | 🟡 abstract无缝信号待精读 |
| 256 | 2023 | 地面站/OGS/终端 / 网络层/路由/RWA / 信道建模/湍流/大气 / 链路预算/系统级 | Commissioning of the deployable optical ground station at Trauen | 强 | 未明确 | 未明确 | 🔴 abstract自陈成熟/广泛采用 |
| 257 | 2023 | 链路预算/系统级 / ISL/星间链路 | Compact dual channel free space optical communication for CubeSat inter-satellite links | 未明确 | radio–frequency links (rf–links) | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 258 | 2023 | 网络层/路由/RWA / 信道建模/湍流/大气 / 语义/AI/DL/ML | Comprehensive quality assessment of optical satellite imagery using weakly supervised video lea | 强 | 未明确 | 未明确 | 🔴 abstract自陈成熟/广泛采用 |
| 259 | 2023 | 网络层/路由/RWA / feeder/中继 | Cooperative relay orbital satellite optical communication under turbulent channels: Performance | 未明确 | 未明确 | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 260 | 2023 | 未明确 | Current Status and Development Trend of Satellite Laser Communication | 未明确 | 未明确 | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 261 | 2023 | 网络层/路由/RWA / 语义/AI/DL/ML | Deep Learning Based Free Space Optical Communication Diversity System | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 262 | 2023 | ATP/指向/PAT / 在轨演示/任务 / QKD/量子/光子计数 / 深空/月地/cislunar | Deep Space Optical Communications (DSOC) - NASA | 弱 | 未明确 | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 263 | 2023 | 地面站/OGS/终端 / 调制/复用 / 编码/FEC/交织 / 深空/月地/cislunar | Designing high-speed GEO-to-Moon optical wireless communication links | 弱 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 264 | 2023 | 信道建模/湍流/大气 / AO/自适应光学/波前 | Emulating and characterizing strong turbulence conditions for space-to-ground optical links: th | 强 | numerical simulations, and this characterization r | 仿真 | 🟡 abstract无缝信号待精读 |
| 265 | 2023 | 网络层/路由/RWA / 链路预算/系统级 | Energy-efficient routing based on a genetic algorithm for satellite laser communication. | 未明确 | shortest path routing, the proposed method improve | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 266 | 2023 | 信道建模/湍流/大气 / 调制/复用 / 相干/自相干检测 / ISL/星间链路 | Evaluation of Aperture Diameter Variation on OFDM Inter–Satellite Optical Wireless Communicatio | 强 | 未明确 | 仿真 | 🟡 abstract自陈达成增益未自陈缝 |
| 267 | 2023 | 网络层/路由/RWA / 信道建模/湍流/大气 / 在轨演示/任务 / feeder/中继 | Experimental analysis of atmospheric channel model with misalignment fading for GEO satellite-t | 强 | 未明确 | 实测/解析 | 🟡 abstract无缝信号待精读 |
| 268 | 2023 | 网络层/路由/RWA / 信道建模/湍流/大气 / ATP/指向/PAT / 在轨演示/任务 / AO/自适应光学/波前 / feeder/中继 / 放大器/EDFA/光子载荷 | Exploration and Space Communications: LCRD - NASA | 强 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 269 | 2023 | 地面站/OGS/终端 / 调制/复用 | Feasibility study of a Terabit/s GEO-to-ground WDM optical communication link | 未明确 | 未明确 | 解析 | 🟡 abstract无缝信号待精读 |
| 270 | 2023 | 地面站/OGS/终端 / 网络层/路由/RWA / ATP/指向/PAT / 在轨演示/任务 / feeder/中继 | First experimental demonstration of optical feeder link by using the optical data relay satelli | 弱 | 未明确 | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 271 | 2023 | 相干/自相干检测 / 载波同步/恢复 / 信道估计/均衡 / feeder/中继 | Frame format and DSP receiver design for a 56-GBaud GEO DP-QPSK coherent optical feeder link | 弱 | 未明确 | 未明确 | 🔴 abstract自陈成熟/广泛采用 |
| 272 | 2023 | 信道估计/均衡 / 语义/AI/DL/ML | Free Space Optical Channel Estimation Based on Deep Learning Algorithms | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 273 | 2023 | 网络层/路由/RWA / ATP/指向/PAT / 调制/复用 / 链路预算/系统级 / ISL/星间链路 | Free Space Optical Communication for Inter-Satellite Link: Architecture, Potentials and Trends | 弱 | 未明确 | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 274 | 2023 | 地面站/OGS/终端 / 网络层/路由/RWA / 信道建模/湍流/大气 / 链路预算/系统级 / ISL/星间链路 | Free-Space Optical (FSO) Satellite Networks Performance Analysis: Transmission Power, Latency,  | 强 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 275 | 2023 | 未明确 | Free-space optical communication with ultralow noise optical amplifiers | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 276 | 2023 | 网络层/路由/RWA / ISL/星间链路 | Gravity-based network traffic abstraction and laser ON/OFF control in optical satellite network | 未明确 | 未明确 | 仿真 | 🟡 abstract自陈达成增益未自陈缝 |
| 277 | 2023 | 地面站/OGS/终端 / 网络层/路由/RWA / ATP/指向/PAT / 在轨演示/任务 / 调制/复用 / 深空/月地/cislunar / 放大器/EDFA/光子载荷 | Ground-to-Drone Optical Pulse Position Modulation Demonstration as a Testbed for Lunar Communic | 弱 | 未明确 | 实测/综述 | 🟡 abstract自陈达成增益未自陈缝 |
| 278 | 2023 | 地面站/OGS/终端 / 调制/复用 / 链路预算/系统级 / feeder/中继 | High-power free-space bulk multiplexer for satellite communication optical ground terminal | 未明确 | 未明确 | 实测 | 🟢 abstract自陈: the main challenge to implement wdm in optical feeder links deals with the multiplexing of |
| 279 | 2023 | 相干/自相干检测 | Implementation of a 10 Gbps Coherent Receiver for Free-Space Optical Communications | 弱 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 280 | 2023 | 信道建模/湍流/大气 / 在轨演示/任务 / 语义/AI/DL/ML / 深空/月地/cislunar / 放大器/EDFA/光子载荷 | In-orbit demonstration of a re-trainable machine learning payload for processing optical imager | 强 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 281 | 2023 | ISL/星间链路 | Inter-Satellite Link Channel Characterization of Laser Communication Systems | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 282 | 2023 | 网络层/路由/RWA / ISL/星间链路 | Interruption Tolerance Strategy for LEO Constellation With Optical Inter-Satellite Link | 未明确 | geo/meo constellation, leo constellation suffers f | 仿真 | 🟡 abstract自陈达成增益未自陈缝 |
| 283 | 2023 | ISL/星间链路 | Investigation of the Influence of LEO Constellation Dynamics on Optical Inter-satellite Links | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 284 | 2023 | 网络层/路由/RWA / ISL/星间链路 | Laser Intersatellite Link Range in Free-Space Optical Satellite Networks: Impact on Latency | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 285 | 2023 | 链路预算/系统级 | Link budget calculation in optical LEO satellite downlinks with on/off-keying and large signal  | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 286 | 2023 | 语义/AI/DL/ML | Low-Complexity Channel Prediction Based on Retroreflection of Auxiliary Beam and Deep Learning  | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 287 | 2023 | ISL/星间链路 | Optical Design of Multi–channel Free Space Optical Communication for Inter–satellite Links | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 288 | 2023 | 地面站/OGS/终端 / QKD/量子/光子计数 / AO/自适应光学/波前 | Optical Ground Station Oberpfaffenhofen Next Generation: first satellite link tests with 80 cm  | 未明确 | 未明确 | 实测/综述 | 🟡 abstract无缝信号待精读 |
| 289 | 2023 | ISL/星间链路 | Optical Intersatellite Links for the Space Web - YouTube | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 290 | 2023 | 未明确 | Optical Satellite Links for telecommunications and time-transfer | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 291 | 2023 | 地面站/OGS/终端 / 信道建模/湍流/大气 / ATP/指向/PAT / 在轨演示/任务 / AO/自适应光学/波前 / feeder/中继 | Optical feeder link demonstrations between the ESA Optical Ground Station and Alphasat | 强 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 292 | 2023 | 网络层/路由/RWA / 信道建模/湍流/大气 | Optical satellite network architecture [Invited Tutorial] | 强 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 293 | 2023 | 地面站/OGS/终端 / 网络层/路由/RWA / 在轨演示/任务 / 编码/FEC/交织 / 链路预算/系统级 / feeder/中继 / ISL/星间链路 | Performance Comparison of Channel Coding Methods for Optical Satellite Data Relay System | 未明确 | 未明确 | 仿真 | 🟡 abstract无缝信号待精读 |
| 294 | 2023 | 相干/自相干检测 | Performance investigation of multi-aperture digital combining algorithm for satellite-to-ground | 弱 | 未明确 | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 295 | 2023 | 地面站/OGS/终端 / 网络层/路由/RWA / 信道建模/湍流/大气 / 在轨演示/任务 / 链路预算/系统级 / feeder/中继 | Preliminary DIMM-based analysis of atmospheric turbulence by using optical data relay satellite | 强 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 296 | 2023 | 在轨演示/任务 / ISL/星间链路 / 放大器/EDFA/光子载荷 | Ranging over Optical Communication Links in the CubeSat Laser Infrared CrosslinK (CLICK) B/C Mi | 未明确 | 50 cm | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 297 | 2023 | 地面站/OGS/终端 / 链路预算/系统级 | Real-Time Satellite Optical Terminal Prototype with Integrated 10 Gbit/s Bidirectional Digital  | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 298 | 2023 | 网络层/路由/RWA / 信道建模/湍流/大气 / ATP/指向/PAT / 调制/复用 / 相干/自相干检测 / 链路预算/系统级 / 深空/月地/cislunar / feeder/中继 | Relay-Assisted Deep Space Optical Communication System Over Coronal Fading Channels | 强 | 未明确 | 仿真/解析 | 🟡 abstract自陈达成增益未自陈缝 |
| 299 | 2023 | 网络层/路由/RWA | Secure Optical Wireless Satellite Network based OWC-OCDM System with DDW code | 未明确 | 未明确 | 仿真 | 🟡 abstract无缝信号待精读 |
| 300 | 2023 | 地面站/OGS/终端 / ATP/指向/PAT / 在轨演示/任务 / 调制/复用 / 深空/月地/cislunar | Space-to-Ground Optical Interface Verification for the Orion Artemis II Optical (O2O) Communica | 弱 | 未明确 | 未明确 | 🔴 abstract自陈成熟/广泛采用 |
| 301 | 2023 | 地面站/OGS/终端 / 信道建模/湍流/大气 | Stellar scintillation statistics and the impact of aperture averaging on space-to-ground optica | 强 | a reasonable set of candidate probability distribu | 实测/解析 | 🟡 abstract无缝信号待精读 |
| 302 | 2023 | 网络层/路由/RWA / 调制/复用 / 放大器/EDFA/光子载荷 | Suppressing effects of micro-vibration for MTF measurement of high-resolution electro-optical s | 弱 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 303 | 2023 | 网络层/路由/RWA / 调制/复用 | Swarm-Intelligence-Based Routing and Wavelength Assignment in Optical Satellite Networks | 未明确 | other aco algorithms, aco-alb-sws-hnlc can effecti | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 304 | 2023 | 调制/复用 / AO/自适应光学/波前 / 相干/自相干检测 / 载波同步/恢复 / 编码/FEC/交织 / 链路预算/系统级 / feeder/中继 | Tbit/s line-rate satellite feeder links enabled by coherent modulation and full-adaptive optics | 弱 | 未明确 | 未明确 | 🟢 abstract自陈: they may overcome the rf bottleneck and attain data rates in the order of tbit/s with only |
| 305 | 2023 | 信道建模/湍流/大气 / ATP/指向/PAT / 在轨演示/任务 / 调制/复用 / AO/自适应光学/波前 / 相干/自相干检测 / 载波同步/恢复 / 编码/FEC/交织 / 语义/AI/DL/ML / 链路预算/系统级 / feeder/中继 | Tbit/s line-rate satellite feeder links enabled by coherent modulation and full-adaptive optics | 强 | 未明确 | 实测 | 🟢 abstract自陈: they may overcome the rf bottleneck and attain data rates in the order of tbit/s with only |
| 306 | 2023 | 在轨演示/任务 / 深空/月地/cislunar | Testing Space Lasers for Deep Space Optical Communications ... | 未明确 | 未明确 | 实测/综述 | 🟡 abstract自陈达成增益未自陈缝 |
| 307 | 2023 | 地面站/OGS/终端 / 网络层/路由/RWA / 在轨演示/任务 / AO/自适应光学/波前 / ISL/星间链路 | The Introduction of Japanese Development and Demonstration of Inter-Satellite Optical Communica | 未明确 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 308 | 2023 | 网络层/路由/RWA / 在轨演示/任务 / 调制/复用 / 链路预算/系统级 | Ultra-High Capacity Optical Satellite Communication System Using PDM-256-QAM and Optical Angula | 弱 | 未明确 | 实测/综述 | 🟡 abstract自陈达成增益未自陈缝 |
| 309 | 2023 | 地面站/OGS/终端 / 网络层/路由/RWA / ATP/指向/PAT / 在轨演示/任务 / QKD/量子/光子计数 / 载波同步/恢复 / 链路预算/系统级 / 放大器/EDFA/光子载荷 | Vector—towards quantum key distribution with small satellites / EPJ Quantum Technology / Spring | 弱 | 未明确 | 实测 | 🟢 abstract自陈: at the same time, the features of quantum communication impose a number of technical requi |
| 310 | 2023 | 调制/复用 | WDM optical front end for GEO-ground digital and analog telecommunications | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 311 | 2023 | 地面站/OGS/终端 / 信道建模/湍流/大气 / 在轨演示/任务 / 调制/复用 / 编码/FEC/交织 | What are Satellite Laser Communication Terminals? - SatNow | 强 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 312 | 2023 | 地面站/OGS/终端 / 链路预算/系统级 / ISL/星间链路 / 放大器/EDFA/光子载荷 | What is an optical inter-satellite link communication terminal? | 未明确 | conventional methods(泛指) | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 313 | 2023 | 地面站/OGS/终端 / 信道建模/湍流/大气 / 在轨演示/任务 / QKD/量子/光子计数 / feeder/中继 | [PDF] DLR's solutions for Optical Communication on CubeSats - NASA | 强 | 未明确 | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 314 | 2022 | 未明确 | A Hybrid Free-Space Optical (FSO)/Radio Frequency (RF) Antenna for Satellite Applications | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 315 | 2022 | 网络层/路由/RWA / 语义/AI/DL/ML | AOSVSSNet: Attention-Guided Optical Satellite Video Smoke Segmentation Network | 未明确 | 未明确 | 未明确 | 🟢 abstract自陈: the smoke segmentation method based on traditional handcrafted features is easily limited  |
| 316 | 2022 | 网络层/路由/RWA / 链路预算/系统级 | Adaptive Service Scheduling for Satellite-Ground Downlink Capacity in Optical Satellite Network | 未明确 | 未明确 | 未明确 | 🟢 abstract自陈: prior studies reported low utilization of satellite-ground downlink (sgdl) resources, maki |
| 317 | 2022 | 地面站/OGS/终端 / 信道建模/湍流/大气 / 在轨演示/任务 / QKD/量子/光子计数 / 链路预算/系统级 / 放大器/EDFA/光子载荷 | Analysis of power scintillation and fading margin in the LEO-ground downlink with the OSIRISv1  | 强 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 318 | 2022 | 地面站/OGS/终端 / ATP/指向/PAT / 调制/复用 / 放大器/EDFA/光子载荷 | Beacon system for ESA IZN-1 Optical Ground Station | 弱 | 未明确 | 未明确 | 🔴 abstract自陈成熟/广泛采用 |
| 319 | 2022 | 网络层/路由/RWA / 信道建模/湍流/大气 | COCO-Net: A Dual-Supervised Network With Unified ROI-Loss for Low-Resolution Ship Detection Fro | 强 | state-of-the-art object detectors | 未明确 | 🟢 abstract自陈: however, it is still a difficult problem due to the following challenges: 1) the size of t |
| 320 | 2022 | ISL/星间链路 | Contact Plan Design for GNSS Constellations: A Case Study With Optical Intersatellite Links | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 321 | 2022 | 地面站/OGS/终端 / 在轨演示/任务 / QKD/量子/光子计数 / ISL/星间链路 / 放大器/EDFA/光子载荷 | DLR's Optical Communication Terminals for CubeSats | 未明确 | 未明确 | 综述 | 🟡 abstract自陈达成增益未自陈缝 |
| 322 | 2022 | 地面站/OGS/终端 / 信道建模/湍流/大气 / ATP/指向/PAT / 在轨演示/任务 / 调制/复用 / AO/自适应光学/波前 / 相干/自相干检测 / 链路预算/系统级 / feeder/中继 | Demonstration of 100 Gbps coherent free-space optical communications at LEO tracking rates / Sc | 强 | 未明确 | 实测 | 🟢 abstract自陈: demonstration of 100 gbps coherent free-space optical communications at leo tracking rates |
| 323 | 2022 | 地面站/OGS/终端 / ATP/指向/PAT / 放大器/EDFA/光子载荷 | GEOSTARE SV2 - Terran Orbital | 弱 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 324 | 2022 | 地面站/OGS/终端 / 网络层/路由/RWA / 链路预算/系统级 | Gravity Model-based Planning Algorithm of Ground Station for Optical Satellite Network | 未明确 | 未明确 | 仿真 | 🟡 abstract无缝信号待精读 |
| 325 | 2022 | ATP/指向/PAT / ISL/星间链路 | Inter-satellite optical wireless communication (IsOWC) systems challenges and applications: a c | 弱 | 未明确 | 未明确 | 🔴 abstract自陈成熟/广泛采用 |
| 326 | 2022 | 网络层/路由/RWA / 链路预算/系统级 / ISL/星间链路 | Intersatellite Laser Link Planning for Reliable Topology Design in Optical Satellite Networks:  | 未明确 | 未明确 | 仿真 | 🟢 abstract自陈: we also gain another interesting insight that maintaining too many isls will not improve,  |
| 327 | 2022 | ISL/星间链路 | Investigations on mode-division multiplexed free-space optical transmission for inter-satellite | 未明确 | 未明确 | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 328 | 2022 | 地面站/OGS/终端 / 信道建模/湍流/大气 / 在轨演示/任务 / QKD/量子/光子计数 | LEO small satellite QKD downlink performance: QuantSat-PT case study | 强 | 未明确 | 实测 | 🔴 abstract自陈成熟/广泛采用 |
| 329 | 2022 | 网络层/路由/RWA / 在轨演示/任务 / feeder/中继 / ISL/星间链路 | LUCAS: The second-generation GEO satellite-based space data-relay system using optical link | 未明确 | 未明确 | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 330 | 2022 | 链路预算/系统级 / ISL/星间链路 | Link Budget Analysis for Free-Space Optical Satellite Networks | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 331 | 2022 | 网络层/路由/RWA / 链路预算/系统级 | Link Budget Design of Adaptive Optical Satellite Network for Integrated Non-Terrestrial Network | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 332 | 2022 | 未明确 | Link Planning Schemes for Uninterrupted Inter-layer Communication in Dual-layer LEO Optical Sat | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 333 | 2022 | 地面站/OGS/终端 / 网络层/路由/RWA / 信道建模/湍流/大气 | Link Reliability of Satellite-to-Ground Free-Space Optical Communication Systems in South Korea | 强 | 未明确 | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 334 | 2022 | 相干/自相干检测 | Low-power-consumption coherent receiver architecture for satellite optical links | 弱 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 335 | 2022 | 信道建模/湍流/大气 / ATP/指向/PAT / 链路预算/系统级 / 放大器/EDFA/光子载荷 | Modulating Retroreflector Based Free Space Optical Link for UAV-to-Ground Communications | 强 | 未明确 | 解析 | 🟡 abstract无缝信号待精读 |
| 336 | 2022 | ATP/指向/PAT / 在轨演示/任务 / ISL/星间链路 | Multi-parameter influenced acquisition model with an in-orbit jitter for inter-satellite laser  | 弱 | 未明确 | 仿真/实测/解析 | 🟢 abstract自陈: with the development of large low earth orbit (leo) communication constellations, the effi |
| 337 | 2022 | 网络层/路由/RWA | Multiband Reconfigurable Antennas for 5G Wireless and CubeSat Applications: A Review | 未明确 | 未明确 | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 338 | 2022 | 网络层/路由/RWA | Optical Transmitter Diversity With Phase-Division in Bit-Time | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 339 | 2022 | 未明确 | Performance Investigation of 800nm and 1000nm wavelength in an Optical Wireless Communication | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 340 | 2022 | ISL/星间链路 | Performance analysis of a Manchester encoded inter-satellite optical wireless communication lin | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 341 | 2022 | 链路预算/系统级 / 放大器/EDFA/光子载荷 | PhLEXSAT - A Very High Throughput Photo-Digital Communication Satellite Payload | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 342 | 2022 | 信道建模/湍流/大气 / 调制/复用 | Research on uplink performance of MIMO terrestrial-satellite laser communication based on OSM-M | 强 | 未明确 | 仿真/实测/解析 | 🟡 abstract无缝信号待精读 |
| 343 | 2022 | 地面站/OGS/终端 / 在轨演示/任务 / 链路预算/系统级 / 深空/月地/cislunar | SelenIRIS: a Moon-Earth Optical Communication Terminal for CubeSats | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 344 | 2022 | 未明确 | Silicon photonic receiver for satellite laser communication terminals. | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 345 | 2022 | 地面站/OGS/终端 / ISL/星间链路 | Space Optical Communications: Why Are Space-to-ground Links ... | 未明确 | 未明确 | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 346 | 2022 | 未明确 | Study of the Characteristics of Few-Mode Microstructured Optical Fibers with 6 Cores Made of Hi | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 347 | 2022 | 网络层/路由/RWA / ISL/星间链路 | Temporary Laser Inter-Satellite Links in Free-Space Optical Satellite Networks | 未明确 | an nng-fsosn (which has pls and tls) under differe | 未明确 | 🟡 abstract无缝信号待精读 |
| 348 | 2022 | 地面站/OGS/终端 / 网络层/路由/RWA / 信道建模/湍流/大气 / QKD/量子/光子计数 / 相干/自相干检测 | The Western Australian optical ground station | 强 | conventional methods(泛指) | 未明确 | 🟡 abstract无缝信号待精读 |
| 349 | 2022 | 调制/复用 / 链路预算/系统级 / ISL/星间链路 | The channel WDM system incorporates of Optical Wireless Communication (OWC) hybrid MDM-PDM for  | 未明确 | 未明确 | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 350 | 2022 | 地面站/OGS/终端 / 网络层/路由/RWA / 在轨演示/任务 | The communication experiment result of Small Optical Link for ISS (SOLISS) to the first commerc | 未明确 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 351 | 2021 | 网络层/路由/RWA / 信道估计/均衡 / 语义/AI/DL/ML | A Deep Neural Network Equalizer for FSO Transmission System | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 352 | 2021 | 地面站/OGS/终端 / ATP/指向/PAT / 载波同步/恢复 / 链路预算/系统级 | Accuracy of satellite orbit prediction and optical design of optical ground station beacons for | 弱 | 未明确 | 实测 | 🟢 abstract自陈: however, the radio frequencies used make it difficult to improve the communication speed,  |
| 353 | 2021 | 地面站/OGS/终端 / 网络层/路由/RWA / ATP/指向/PAT / 链路预算/系统级 / feeder/中继 / ISL/星间链路 | Acquisition Analysis for Small-Satellite Optical Crosslinks | 未明确 | 未明确 | 仿真/实测 | 🟡 abstract无缝信号待精读 |
| 354 | 2021 | ATP/指向/PAT / ISL/星间链路 | Acquisition, Scanning and Control Technology for Inter-satellite Laser Communication | 未明确 | pi controller | 仿真/解析 | 🟢 abstract自陈: due to the complex space environment, it is very difficult to establish communication link |
| 355 | 2021 | 网络层/路由/RWA / 相干/自相干检测 / 语义/AI/DL/ML | Adaptive optical satellite network architecture | 弱 | conventional methods(泛指) | 未明确 | 🟡 abstract无缝信号待精读 |
| 356 | 2021 | 网络层/路由/RWA / 在轨演示/任务 / QKD/量子/光子计数 / feeder/中继 | An integrated space-to-ground quantum communication network over 4,600 kilometres / Nature | 未明确 | 未明确 | 实测 | 🟢 abstract自陈: quantum repeaters 16, 17 could in principle provide a viable option for such a global netw |
| 357 | 2021 | ATP/指向/PAT / 在轨演示/任务 / AO/自适应光学/波前 / ISL/星间链路 | Beacon correction method for inter-satellite laser communication | 弱 | 未明确 | 实测/解析 | 🟡 abstract自陈达成增益未自陈缝 |
| 358 | 2021 | 网络层/路由/RWA / ISL/星间链路 / 放大器/EDFA/光子载荷 | Connectivity Analysis of Mega-Constellation Satellite Networks With Optical Intersatellite Link | 未明确 | conventional methods(泛指) | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 359 | 2021 | 载波同步/恢复 | DFOS Applications to Geo-Engineering Monitoring | 未明确 | 未明确 | 实测/解析 | 🔴 abstract自陈成熟/广泛采用 |
| 360 | 2021 | 地面站/OGS/终端 / 网络层/路由/RWA / 在轨演示/任务 / 深空/月地/cislunar / feeder/中继 | Demonstration of a modular, scalable, laser communication terminal for manned spaceflight missi | 未明确 | 未明确 | 实测/综述 | 🟡 abstract无缝信号待精读 |
| 361 | 2021 | 编码/FEC/交织 / feeder/中继 | End-to-End Error Control Coding Capability of NB-IoT Transmissions in a GEO Satellite System wi | 未明确 | 未明确 | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 362 | 2021 | 在轨演示/任务 / 放大器/EDFA/光子载荷 | Full-Closed-Loop Time-Domain Integrated Modeling Method of Optical Satellite Flywheel Micro-Vib | 未明确 | the ground experiment, frequency error is less tha | 仿真/实测/解析 | 🟡 abstract自陈达成增益未自陈缝 |
| 363 | 2021 | 网络层/路由/RWA / 信道建模/湍流/大气 / ATP/指向/PAT / 链路预算/系统级 / feeder/中继 | HAPS-Based Relaying for Integrated Space–Air–Ground Networks With Hybrid FSO/RF Communication:  | 强 | the fso systems in an uplink scenario due to the b | 仿真 | 🟡 abstract自陈达成增益未自陈缝 |
| 364 | 2021 | ATP/指向/PAT | High-Precision Dual-Stage Pointing Mechanism for Miniature Satellite Laser Communication Termin | 弱 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 365 | 2021 | 地面站/OGS/终端 / 网络层/路由/RWA / 在轨演示/任务 / ISL/星间链路 | HySpecIQ Picks BridgeComm's Optical Downlink Terminals for LEO ... | 未明确 | 未明确 | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 366 | 2021 | 网络层/路由/RWA / feeder/中继 / ISL/星间链路 | Inter-Satellite Optical Wireless Communication (IsOWC) System Analysis for Optimizing Performan | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 367 | 2021 | 网络层/路由/RWA | Introduction to Optical Payloads in Space Missions - GRSS-IEEE | 未明确 | 未明确 | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 368 | 2021 | ATP/指向/PAT / ISL/星间链路 | Investigation of the Effects of Pointing Errors on Optical Intersatellite Links Using Real Orbi | 弱 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 369 | 2021 | 地面站/OGS/终端 / 网络层/路由/RWA / 在轨演示/任务 / 链路预算/系统级 / feeder/中继 / 放大器/EDFA/光子载荷 | Laser Communications Relay Demonstration (LCRD) Overview - NASA | 未明确 | 未明确 | 实测/综述 | 🟡 abstract自陈达成增益未自陈缝 |
| 370 | 2021 | 网络层/路由/RWA / 在轨演示/任务 / 调制/复用 / 载波同步/恢复 / 放大器/EDFA/光子载荷 | Microwave reference signal distribution on optical fibre within satellite payload | 未明确 | 未明确 | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 371 | 2021 | 网络层/路由/RWA / 在轨演示/任务 / feeder/中继 / 放大器/EDFA/光子载荷 | NASA's Laser Communications Tech, Science Experiment Safely in Space | 未明确 | 未明确 | 实测/综述 | 🟡 abstract自陈达成增益未自陈缝 |
| 372 | 2021 | 放大器/EDFA/光子载荷 | On-orbit calibration techniques for optical payloads onboard remote-sensing satellites | 未明确 | 2″ for its optical payload and star sensor | 实测 | 🟡 abstract无缝信号待精读 |
| 373 | 2021 | QKD/量子/光子计数 / 相干/自相干检测 | One-hour coherent optical storage in an atomic frequency comb memory | 弱 | 未明确 | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 374 | 2021 | 地面站/OGS/终端 / 信道建模/湍流/大气 | Optical link stabilization by controlling focus of received beam in mini-unmanned aerial vehicl | 强 | 未明确 | 仿真/实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 375 | 2021 | 网络层/路由/RWA / 信道建模/湍流/大气 / 链路预算/系统级 / feeder/中继 | Outage Performance for Optical Feeder Link in Satellite Communications With Diversity Combining | 强 | 未明确 | 解析 | 🟡 abstract自陈达成增益未自陈缝 |
| 376 | 2021 | 网络层/路由/RWA / 调制/复用 / feeder/中继 / ISL/星间链路 | Performance Analysis and Evaluation of Inter-Satellite Optical Wireless Communication System (I | 未明确 | 未明确 | 未明确 | 🟢 abstract自陈: that enables geo satellites to relay information to and from leo satellites and fixed eart |
| 377 | 2021 | 信道建模/湍流/大气 / 调制/复用 / 编码/FEC/交织 | Performance of an OFDM STBC-MISO system in uplink terrestrial-satellite laser communication. | 强 | 未明确 | 仿真/实测/解析 | 🟡 abstract自陈达成增益未自陈缝 |
| 378 | 2021 | ISL/星间链路 | Realization of 1Tbps FSO/OWC based inter satellite link using DP-QPSK for next generation LEO s | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 379 | 2021 | 网络层/路由/RWA / 链路预算/系统级 / feeder/中继 / ISL/星间链路 / 放大器/EDFA/光子载荷 | Research on inter-satellite laser communication based on relay system | 未明确 | 未明确 | 仿真 | 🟢 abstract自陈: due to the limitation of satellite payload performance and the influence of space environm |
| 380 | 2021 | 网络层/路由/RWA / 调制/复用 / 链路预算/系统级 / ISL/星间链路 | Satellite Laser Communication Assisted P-cycle Protection Against SRLG Failures in WDM Optical  | 未明确 | 未明确 | 未明确 | 🟢 abstract自陈: p-cycle protection against shared risk links group (srlg) failures in wdm optical networks |
| 381 | 2021 | 放大器/EDFA/光子载荷 | Thermal deformation optimization method for optical satellite payload mounting surface based on | 未明确 | 未明确 | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 382 | 2021 | 网络层/路由/RWA / feeder/中继 | Transmitter Diversity With Phase-Division Applied to Optical GEO Feeder Links | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 383 | 2021 | ATP/指向/PAT / 在轨演示/任务 | XY-2 satellite laser communication equipment PAT test in orbit | 未明确 | 未明确 | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 384 | 2021 | 信道建模/湍流/大气 / 链路预算/系统级 / feeder/中继 | [PDF] Optical feeder links for high throughput satellites and the ... - HAL | 强 | conventional methods(泛指) | 未明确 | 🟡 abstract无缝信号待精读 |
| 385 | 2020 | 地面站/OGS/终端 / 链路预算/系统级 / feeder/中继 | A PHY Layer Security Analysis of a Hybrid High Throughput Satellite With an Optical Feeder Link | 未明确 | the no-precoding scenario for some specific nodes’ | 仿真 | 🟡 abstract无缝信号待精读 |
| 386 | 2020 | 网络层/路由/RWA | A Resilient Optical Satellite Signaling Network Architecture for Fast Convergence under Time-Va | 未明确 | 未明确 | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 387 | 2020 | 网络层/路由/RWA / 链路预算/系统级 / ISL/星间链路 | A Routing and Wavelength Assignment Algorithm Based on Two Types of LEO Constellations in Optic | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 388 | 2020 | 未明确 | BER Analysis of IM and BPPM for Satellite-to-Ground Laser Communications | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 389 | 2020 | 未明确 | Design of a Two Wavelength Optical Downlink for LEO Spacecrafts | 未明确 | 未明确 | 解析 | 🟡 abstract自陈达成增益未自陈缝 |
| 390 | 2020 | 信道建模/湍流/大气 / 链路预算/系统级 | Development status and trend of micro-satellite laser communication systems | 强 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 391 | 2020 | ATP/指向/PAT / 在轨演示/任务 / 深空/月地/cislunar | Free-space optical communication for CubeSats in low lunar orbit: LLO | 弱 | 未明确 | 实测 | 🟢 abstract自陈: with fine pointing, the spot size on the earth could be reduced by a factor of eight with  |
| 392 | 2020 | 在轨演示/任务 / QKD/量子/光子计数 / ISL/星间链路 / 放大器/EDFA/光子载荷 | High data-rate optical communication payload for CubeSats | 未明确 | 未明确 | 综述 | 🔴 abstract自陈成熟/广泛采用 |
| 393 | 2020 | 地面站/OGS/终端 / ATP/指向/PAT / ISL/星间链路 | LaserCube optical communication terminal for nano and micro satellites | 弱 | 未明确 | 仿真/实测 | 🟡 abstract无缝信号待精读 |
| 394 | 2020 | 链路预算/系统级 / feeder/中继 | Light-Weight Time-Packing Detection Schemes for Optical Feeder Link Adaptation in High Throughp | 弱 | 未明确 | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 395 | 2020 | 调制/复用 / 信道估计/均衡 / 链路预算/系统级 / feeder/中继 / 放大器/EDFA/光子载荷 | Linear Time-Packing Detectors for Optical Feeder Link in High Throughput Satellite Systems | 弱 | baseline m-pam transmissions without overlapping | 未明确 | 🟡 abstract无缝信号待精读 |
| 396 | 2020 | 调制/复用 | Modulation and demodulation method for satellite laser communication system | 弱 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 397 | 2020 | 地面站/OGS/终端 / 网络层/路由/RWA / 链路预算/系统级 | Network Availability Maximization for Free-Space Optical Satellite Communications | 未明确 | the conventional gs selection methods, the propose | 仿真 | 🟡 abstract自陈达成增益未自陈缝 |
| 398 | 2020 | 地面站/OGS/终端 / 网络层/路由/RWA / ISL/星间链路 | Optical inter-satellite link terminals for next generation satellite constellations | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 399 | 2020 | 地面站/OGS/终端 / 网络层/路由/RWA / 信道建模/湍流/大气 / 调制/复用 / 链路预算/系统级 / feeder/中继 / ISL/星间链路 | Performance Analysis of DPSK Optical Communication for LEO-to-Ground Relay Link Via a GEO Satel | 强 | satellite microwave communication | 实测 | 🟡 abstract无缝信号待精读 |
| 400 | 2020 | 信道建模/湍流/大气 / ATP/指向/PAT / 调制/复用 / 相干/自相干检测 / 链路预算/系统级 / feeder/中继 / 放大器/EDFA/光子载荷 | Performance of Multibeam Very High Throughput Satellite Systems Based on FSO Feeder Links With  | 强 | conventional methods(泛指) | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 401 | 2020 | ATP/指向/PAT | Point ahead angle prediction based on Kalman filtering of optical axis pointing angle in satell | 弱 | 未明确 | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 402 | 2020 | 地面站/OGS/终端 / 在轨演示/任务 / ISL/星间链路 | Received power attenuation due to the wave-front aberrations induced by the receiving optical a | 未明确 | 未明确 | 仿真/实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 403 | 2020 | 在轨演示/任务 / 放大器/EDFA/光子载荷 | Satellite cameras and optical payloads - Blog - Satsearch | 未明确 | 未明确 | 实测/综述 | 🟡 abstract无缝信号待精读 |
| 404 | 2020 | 信道建模/湍流/大气 / 调制/复用 / 信道估计/均衡 / 链路预算/系统级 / feeder/中继 / 放大器/EDFA/光子载荷 | Time-Packing as Enabler of Optical Feeder Link Adaptation in High Throughput Satellite Systems | 强 | 未明确 | 未明确 | 🟡 abstract自陈达成增益未自陈缝 |
| 405 | 2020 | 网络层/路由/RWA / 信道建模/湍流/大气 / 编码/FEC/交织 / 语义/AI/DL/ML | Towards 6G wireless communication networks: vision, enabling technologies, and new paradigm shi | 强 | 未明确 | 综述 | 🔴 abstract自陈成熟/广泛采用 |
| 406 | 2019 | 地面站/OGS/终端 / 在轨演示/任务 / 链路预算/系统级 / 放大器/EDFA/光子载荷 | A Ka-band single string photonic payload flight demonstrator for broadband high throughput sate | 未明确 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 407 | 2019 | 编码/FEC/交织 / 链路预算/系统级 | A Throughput Model of TCP-FSO/ADFR for Free-Space Optical Satellite Communications | 未明确 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 408 | 2019 | 信道建模/湍流/大气 / 调制/复用 / 放大器/EDFA/光子载荷 | APC‐EDFA‐based scintillation‐suppressed photodetection in satellite optical communication | 强 | gain saturation, and an approximate 5 | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 409 | 2019 | 在轨演示/任务 | Advanced demonstration plans of high-speed laser communication "HICALI" mission onboard the eng | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 410 | 2019 | 地面站/OGS/终端 / 网络层/路由/RWA / 在轨演示/任务 / feeder/中继 | Airborne optical communication terminal: first successful link from Tenerife to the GEO Alphasa | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 411 | 2019 | 相干/自相干检测 | An Optical Communication System Adjusting Method for GEO Satellites | 弱 | 未明确 | 解析 | 🟡 abstract无缝信号待精读 |
| 412 | 2019 | 地面站/OGS/终端 / 信道建模/湍流/大气 / ATP/指向/PAT | Analysis of tip-tilt compensation for reflective free-space optical satellite communication | 强 | 未明确 | 实测 | 🟢 abstract自陈: atmospheric turbulences limit the achievable performance of free-space optical (fso) satel |
| 413 | 2019 | 地面站/OGS/终端 / ATP/指向/PAT / 在轨演示/任务 / 相干/自相干检测 / ISL/星间链路 | Architecture and performance analysis of an optical metrology terminal for satellite-to-satelli | 弱 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 414 | 2019 | 网络层/路由/RWA / ATP/指向/PAT / 链路预算/系统级 / ISL/星间链路 | Beaconless acquisition tracking and pointing scheme of satellite optical communication in multi | 弱 | 未明确 | 仿真 | 🟡 abstract无缝信号待精读 |
| 415 | 2019 | 信道建模/湍流/大气 | Bit Error Rate Analysis of Space-to-Ground Optical Link Under the Influence of Atmospheric Turb | 强 | 未明确 | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 416 | 2019 | 调制/复用 / QKD/量子/光子计数 / 载波同步/恢复 / 编码/FEC/交织 / 链路预算/系统级 / 深空/月地/cislunar | Characterization of a photon counting test bed for space to ground optical pulse position modul | 弱 | 未明确 | 未明确 | 🔴 abstract自陈成熟/广泛采用 |
| 417 | 2019 | 地面站/OGS/终端 / 信道建模/湍流/大气 / AO/自适应光学/波前 | ESA Optical Ground Station Upgrade with Adaptive Optics for High Data Rate Satellite-to-Ground  | 强 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 418 | 2019 | 地面站/OGS/终端 / 信道建模/湍流/大气 / 调制/复用 | Experimental evaluation of adaptive distributed frame repetition at 10Gbps for the satellite-to | 强 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 419 | 2019 | ISL/星间链路 | INTER-SATELLITE OPTICAL COMMUNICATION LINK | 未明确 | 未明确 | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 420 | 2019 | 放大器/EDFA/光子载荷 | Instrument Radiometric Processing for Earh Observation Satellite Optical Payload | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 421 | 2019 | 未明确 | Integration of optical and satellite communication technologies to improve the cache filling ti | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 422 | 2019 | ISL/星间链路 | Optical Inter Satellite Links for Broadband Networks | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 423 | 2019 | 地面站/OGS/终端 / 网络层/路由/RWA / ATP/指向/PAT / 在轨演示/任务 / QKD/量子/光子计数 / 相干/自相干检测 / feeder/中继 / ISL/星间链路 / 放大器/EDFA/光子载荷 | Optical Terminal for Canada's Quantum Encryption and Science Satellite (QEYSSat) | 弱 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 424 | 2019 | 地面站/OGS/终端 / ATP/指向/PAT / 在轨演示/任务 / 编码/FEC/交织 / 链路预算/系统级 | Optical communications downlink from a 1.5U Cubesat: OCSD program | 弱 | 未明确 | 实测 | 🟡 abstract自陈达成增益未自陈缝 |
| 425 | 2019 | 地面站/OGS/终端 / ATP/指向/PAT / 链路预算/系统级 / ISL/星间链路 | Optical satellite communication space terminal technology at TNO | 弱 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 426 | 2019 | 地面站/OGS/终端 / 网络层/路由/RWA / 信道建模/湍流/大气 / ATP/指向/PAT / AO/自适应光学/波前 / 相干/自相干检测 / 链路预算/系统级 / feeder/中继 | Optical technologies for very high throughput satellite communications | 强 | 未明确 | 实测/综述 | 🟡 abstract无缝信号待精读 |
| 427 | 2019 | 地面站/OGS/终端 / ATP/指向/PAT / 在轨演示/任务 | Paper Title (use style: paper title) | 弱 | 未明确 | 实测 | 🔴 abstract自陈成熟/广泛采用 |
| 428 | 2019 | 未明确 | Recent Trends in Space Laser Communications for Small Satellites and Constellations | 未明确 | 未明确(IEEE无abstract) | 未明确(IEEE无abstract) | 🟡 abstract 缺失(IEEE或截断)待精读 |
| 429 | 2019 | 地面站/OGS/终端 | Reference Power Vectors for the Optical LEO Downlink Channel | 未明确 | 未明确 | 仿真 | 🔴 abstract自陈成熟/广泛采用 |
| 430 | 2019 | 调制/复用 / AO/自适应光学/波前 / 信道估计/均衡 / 编码/FEC/交织 / 链路预算/系统级 / feeder/中继 / 放大器/EDFA/光子载荷 | Total Degradation of a DVB-S2 Satellite System with Analog Transparent Optical Feeder Link | 弱 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |

## 主表续段（v3，round3 search，动作 A 设备词补盲，2026-06-22）

> 11 设备词 × tools/search：transceiver/modem/receiver/transmitter/frontend/digital-processing-unit/payload-transceiver/photonic-receiver/coherent-transceiver/balanced-receiver/fpga-receiver
> 267 raw → 150 去重 → 95 域内 → **79 核心入表**（16 相邻域 + 44 域外不入表，见诊断段）
> 偏航检查 A 自验：动作 A 11 词零模块词（modulation/synchronization/equalization/channel-estimation/coding/detection）✅

| # | 年 | 子地带 | 做的事(标题) | 湍流 | baseline 是谁 | 验证 | 缝潜力 |
|---|----|--------|------|------|--------------|------|--------|
| 431 | 2026 | 相干/自相干检测 / AO/自适应光学/波前 / 信道建模/湍流/大气 | 64-Channel Adaptive Optics System-on-Chip (AOSoC) Photonic P... | 强 | 未明确 | 实测 | 🟡 abstract自陈达成未自陈缝 |
| 432 | 2026 | ISL/星间链路 / 编码/FEC/交织 / 网络层/路由/RWA | Coflow transmission optimization for satellite distributed c... | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成+挑战（待精读） |
| 433 | 2026 | 相干/自相干检测 / 放大器/EDFA/光子载荷 | Nonlinearity Mitigation for Coherent Ground-to-Satellite Opt... | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 434 | 2026 | 调制/复用 / 相干/自相干检测 / 链路预算/系统级 | Packaged InP PIC for Photonic RF Receive Front-End of High-C... | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成未自陈缝 |
| 435 | 2026 | 调制/复用 | Real-time implementation of all-digital optical time transfe... | 未明确 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 436 | 2026 | 调制/复用 / 编码/FEC/交织 / 相干/自相干检测 / 放大器/EDFA/光子载荷 | Time-frequency synchronization for distributed phase coheren... | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成未自陈缝 |
| 437 | 2025 | 调制/复用 / 放大器/EDFA/光子载荷 / 链路预算/系统级 | 56 Gbps CPO silicon photonics transceiver with radiation-har... | 未明确 | 未明确 | 实测 | 🟢? abstract自陈挑战（待精读） |
| 438 | 2025 | 调制/复用 | A 108‐Element L-Band Multiple Beamforming Digital Phased Arr... | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成未自陈缝 |
| 439 | 2025 | ISL/星间链路 / 调制/复用 | A Correlation-Based Arbitrary Bias Control Method and Applic... | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成未自陈缝 |
| 440 | 2025 | 地面站/OGS/终端 / ATP/指向/PAT / QKD/量子/光子计数 / 调制/复用 / 信道建模/湍流/大气 / 放大器/EDFA/光子载荷 | A compact receiver module for satellite-ground QKD | 强 | 未明确 | 实测 | 🟢? abstract自陈挑战（待精读） |
| 441 | 2025 | ATP/指向/PAT / 调制/复用 / 信道估计/均衡 / 放大器/EDFA/光子载荷 | Beyond Gbps Intra-Satellite Optical Wireless Communications ... | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成+挑战（待精读） |
| 442 | 2025 | 未明确 | COMPACT MID-INFRARED TRANSMITTER AND RECEIVER FOR FREE-SPACE... | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 443 | 2025 | 未明确 | Compact, high-power, low-divergence laser transmitter beam e... | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 444 | 2025 | 编码/FEC/交织 / 信道建模/湍流/大气 / 网络层/路由/RWA | Forward Error Correction Considerations for Optical Satellit... | 强 | 未明确 | 未明确 | 🟡 abstract自陈达成未自陈缝 |
| 445 | 2025 | 未明确 | Frontend Design with Special Waveguide Transition in K-and K... | 未明确 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 446 | 2025 | ISL/星间链路 / 调制/复用 | Fully Reconfigurable Silicon Photonic Transceiver for Optica... | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 447 | 2025 | 地面站/OGS/终端 / feeder/中继 / ATP/指向/PAT / 调制/复用 / 信道建模/湍流/大气 / 网络层/路由/RWA / 放大器/EDFA/光子载荷 | In-orbit testing of GEO feeder links with TELEO | 强 | 未明确 | 实测 | 🟡 abstract自陈达成未自陈缝 |
| 448 | 2025 | 信道建模/湍流/大气 / 链路预算/系统级 | Latest results and perspectives of TILBA-ATMO system for LEO... | 强 | 未明确 | 实测 | 🟡 abstract自陈达成+挑战（待精读） |
| 449 | 2025 | ATP/指向/PAT / 调制/复用 / 链路预算/系统级 | Modulating Retroreflector-Based Satellite-to-Ground Optical ... | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成未自陈缝 |
| 450 | 2025 | 地面站/OGS/终端 / feeder/中继 / ATP/指向/PAT / 链路预算/系统级 | Optical feeder links to GEO-based satellites: a focus on spa... | 未明确 | 未明确 | 未明确 | 🟡 abstract自陈达成+挑战（待精读） |
| 451 | 2025 | 地面站/OGS/终端 / feeder/中继 / 信道建模/湍流/大气 / 链路预算/系统级 | Optimizing Optical Ground Station Transmitter Telescope for ... | 强 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 452 | 2025 | QKD/量子/光子计数 / 编码/FEC/交织 | Photonic Integrated Phase Encoding Transmitter for Satellite... | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 453 | 2025 | 调制/复用 / 放大器/EDFA/光子载荷 / 链路预算/系统级 | Photonics RF Front-End for High-Throughput Satellites | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成未自陈缝 |
| 454 | 2025 | ISL/星间链路 / 放大器/EDFA/光子载荷 | Proposal for Two-Wavelength High-Power EML-CAN for Low-SWaP-... | 未明确 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 455 | 2025 | 深空/月地/cislunar / AO/自适应光学/波前 | Research And Development Of Satellite-Mounted 30cm Aperture ... | 未明确 | 未明确 | 未明确 | 🟡 abstract自陈达成未自陈缝 |
| 456 | 2025 | 深空/月地/cislunar / AO/自适应光学/波前 | Research and development of satellite-mounted large-aperture... | 未明确 | 未明确 | 未明确 | 🟡 abstract自陈达成未自陈缝 |
| 457 | 2025 | 网络层/路由/RWA | Research on magnetic cleanliness control technology in the a... | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成未自陈缝 |
| 458 | 2025 | ISL/星间链路 | Solar Irradiance Mitigation in LEO Optical Inter-Satellite L... | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成+挑战（待精读） |
| 459 | 2025 | 地面站/OGS/终端 / 调制/复用 / 相干/自相干检测 / 放大器/EDFA/光子载荷 / 链路预算/系统级 | Space radiation effects on photonic integrated circuits for ... | 未明确 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 460 | 2025 | 未明确 | Study on the Micro-Vibration Isolation in High-Resolution Sa... | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 461 | 2025 | 放大器/EDFA/光子载荷 | The Tilt Adapter Design for Optical Payload in THEOS-3 Small... | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 462 | 2025 | 未明确 | The use of optical transceiver technology within space vehic... | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 463 | 2025 | 地面站/OGS/终端 / ATP/指向/PAT / QKD/量子/光子计数 / 信道建模/湍流/大气 / 链路预算/系统级 | Transmitter Diversity Design Considerations for the EAGLE-1 ... | 强 | 未明确 | 未明确 | 🟡 abstract自陈达成未自陈缝 |
| 464 | 2024 | 地面站/OGS/终端 / ATP/指向/PAT / 编码/FEC/交织 / 信道建模/湍流/大气 / 链路预算/系统级 | Erasure correcting codes for high-throughput optical ground-... | 强 | 未明确 | 未明确 | 🟢? abstract自陈挑战（待精读） |
| 465 | 2024 | ISL/星间链路 / 调制/复用 / 信道估计/均衡 / 相干/自相干检测 | Hardware-efficient adaptive equalizer for inter-satellite co... | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成+挑战（待精读） |
| 466 | 2024 | 地面站/OGS/终端 / ISL/星间链路 / ATP/指向/PAT / QKD/量子/光子计数 / AO/自适应光学/波前 | Impact of transmitter wavefront errors and pointing jitter o... | 未明确 | 未明确 | 仿真 | 🟢? abstract自陈挑战（待精读） |
| 467 | 2024 | ISL/星间链路 / 网络层/路由/RWA | Key technologies for the satellite optical network | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 468 | 2024 | ISL/星间链路 / 网络层/路由/RWA | Large-Scale Satellite Optical Network Simulation Architectur... | 未明确 | 未明确 | 仿真 | 🟡 abstract无缝信号待精读 |
| 469 | 2024 | 调制/复用 | Multi-gigabit X-band transmitter for satellite communication... | 未明确 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 470 | 2024 | 调制/复用 / 相干/自相干检测 / 放大器/EDFA/光子载荷 / 链路预算/系统级 | Photonic integrated circuits for high-throughput optical com... | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成未自陈缝 |
| 471 | 2024 | ISL/星间链路 / 网络层/路由/RWA | Research on Adjustable Wavelength Transmitter-receiver Isola... | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成未自陈缝 |
| 472 | 2024 | 网络层/路由/RWA / 链路预算/系统级 | Service blockage on the downlink in large-scale satellite op... | 未明确 | 未明确 | 未明确 | 🟡 abstract自陈达成未自陈缝 |
| 473 | 2023 | 地面站/OGS/终端 / feeder/中继 / 调制/复用 | 18km bidirectional free-space optical link with multi-apertu... | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成未自陈缝 |
| 474 | 2023 | ISL/星间链路 | A Study on the Direct Detection Optical Receiver for Optical... | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 475 | 2023 | 地面站/OGS/终端 / 调制/复用 / 信道建模/湍流/大气 / 网络层/路由/RWA | Design of the setup for testing optical telemetry ranging in... | 强 | 未明确 | 仿真 | 🟡 abstract自陈达成+挑战（待精读） |
| 476 | 2023 | 地面站/OGS/终端 / ISL/星间链路 / ATP/指向/PAT / 相干/自相干检测 / 链路预算/系统级 | Development of spatial coherent optical receiver with a size... | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成未自陈缝 |
| 477 | 2023 | 深空/月地/cislunar / 调制/复用 / 编码/FEC/交织 / 链路预算/系统级 | High directional optical transmitter with phased array of na... | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成+挑战（待精读） |
| 478 | 2023 | 未明确 | High-speed optical transceiver integrated chipset and module... | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 479 | 2023 | 调制/复用 | Mid-wave infrared optical receiver based on an InAsSb-nBn ph... | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成未自陈缝 |
| 480 | 2023 | 调制/复用 / 相干/自相干检测 / 放大器/EDFA/光子载荷 | Optical frequency comb optimization for satellite payload ap... | 未明确 | 未明确 | 未明确 | 🟡 abstract自陈达成未自陈缝 |
| 481 | 2023 | 地面站/OGS/终端 / feeder/中继 / ATP/指向/PAT / AO/自适应光学/波前 / 信道建模/湍流/大气 | Performance of the adaptive optics system for Laser Communic... | 强 | 未明确 | 实测 | 🟡 abstract自陈达成未自陈缝 |
| 482 | 2023 | ISL/星间链路 / ATP/指向/PAT / 调制/复用 | Pointing error angle evaluation of OFDM inter-satellite opti... | 未明确 | 未明确 | 未明确 | 🟡 abstract自陈达成+挑战（待精读） |
| 483 | 2023 | 信道建模/湍流/大气 | Satellite-to-ground optical downlink model using mode mismat... | 强 | 未明确 | 实测 | 🟡 abstract自陈达成未自陈缝 |
| 484 | 2023 | 网络层/路由/RWA | Traffic Prediction-based Load-Balanced Routing Strategy for ... | 未明确 | 未明确 | 仿真 | 🟡 abstract无缝信号待精读 |
| 485 | 2023 | 地面站/OGS/终端 / ATP/指向/PAT | Transmitter beam bias verification for optical satellite dat... | 未明确 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 486 | 2022 | ISL/星间链路 | A multichannel Hermite Gaussian (HG) intensity profiles base... | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 487 | 2022 | ISL/星间链路 / 调制/复用 / 相干/自相干检测 / 网络层/路由/RWA / 放大器/EDFA/光子载荷 | Effect of Doppler shift on preamplifier DPSK receivers using... | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 488 | 2022 | 地面站/OGS/终端 / 调制/复用 / 相干/自相干检测 / AO/自适应光学/波前 / 信道建模/湍流/大气 | Evaluation of a multimode receiver with a photonic integrate... | 强 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 489 | 2022 | ISL/星间链路 / 相干/自相干检测 / 信道建模/湍流/大气 | Free Space Ground to Satellite Optical Communications Using ... | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 490 | 2022 | 地面站/OGS/终端 / ISL/星间链路 / 调制/复用 / 放大器/EDFA/光子载荷 | H2020-SPACE-ORIONAS miniaturized optical transceivers and am... | 未明确 | 未明确 | 未明确 | 🟡 abstract自陈达成未自陈缝 |
| 491 | 2022 | ISL/星间链路 / 调制/复用 / 网络层/路由/RWA / 放大器/EDFA/光子载荷 / 链路预算/系统级 | Optical transceivers for high-speed space communications - E... | 未明确 | 未明确 | 实测 | 🟢? abstract自陈挑战（待精读） |
| 492 | 2022 | feeder/中继 / 调制/复用 / 相干/自相干检测 / AO/自适应光学/波前 / 信道建模/湍流/大气 | Robust free space optical communication receiver based on a ... | 强 | 未明确 | 实测 | 🟢? abstract自陈挑战（待精读） |
| 493 | 2021 | 未明确 | A 112 Gb/s Radiation-Hardened Mid-Board Optical Transceiver ... | 未明确 | 未明确 | 综述 | 🟡 abstract无缝信号待精读 |
| 494 | 2021 | QKD/量子/光子计数 | Digital processing of optical signals in the frequency stand... | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成未自陈缝 |
| 495 | 2021 | 地面站/OGS/终端 / feeder/中继 / 深空/月地/cislunar | Optical Modems for optical laser communication downlinks | 未明确 | 未明确 | 未明确 | 🟢? abstract自陈挑战（待精读） |
| 496 | 2021 | 调制/复用 / 相干/自相干检测 / 网络层/路由/RWA / 链路预算/系统级 | Proton radiation assessment of COTS components of 100 Gb/s d... | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成+挑战（待精读） |
| 497 | 2020 | 调制/复用 | Analysis of Phase Noise in a Hybrid Photonic/Millimetre-Wave... | 未明确 | 未明确 | 未明确 | 🟡 abstract自陈达成未自陈缝 |
| 498 | 2020 | 地面站/OGS/终端 / ISL/星间链路 / 调制/复用 / 链路预算/系统级 | Communication and Ranging System for the Kepler Laboratory D... | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成未自陈缝 |
| 499 | 2020 | ISL/星间链路 / ATP/指向/PAT | Impact of receiver architecture on small satellite optical l... | 未明确 | 未明确 | 未明确 | 🟡 abstract自陈达成未自陈缝 |
| 500 | 2020 | 地面站/OGS/终端 / QKD/量子/光子计数 / 调制/复用 / 信道建模/湍流/大气 / 链路预算/系统级 | Measurements of few-mode fiber photonic lanterns in emulated... | 强 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 501 | 2020 | ISL/星间链路 | Multiple Transceivers Inter-satellite Optical wireless commu... | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 502 | 2020 | ISL/星间链路 | RETRACTED ARTICLE: Performance enhancement of transceiver sy... | 未明确 | 未明确 | 未明确 | 🟡 abstract自陈达成未自陈缝 |
| 503 | 2020 | 地面站/OGS/终端 / 网络层/路由/RWA / 放大器/EDFA/光子载荷 | Thermal Vacuum Tests and Thermal Properties on ESA's OPS-SAT... | 未明确 | 未明确 | 实测 | 🟡 abstract无缝信号待精读 |
| 504 | 2020 | ISL/星间链路 / 调制/复用 | Transmitter Aperture Diameter Effect in 40 Gb/s Inter-Satell... | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成未自陈缝 |
| 505 | 2019 | 调制/复用 / 放大器/EDFA/光子载荷 | Assessment of the Performance of DPSK and OOK Modulations at... | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成未自陈缝 |
| 506 | 2019 | ISL/星间链路 / ATP/指向/PAT / 编码/FEC/交织 / 相干/自相干检测 / 链路预算/系统级 | Inter-Satellite Integrated Laser Communication/Ranging Link ... | 未明确 | 未明确 | 实测 | 🟡 abstract自陈达成未自陈缝 |
| 507 | 2019 | ISL/星间链路 / ATP/指向/PAT | Pointing Error Reduction Using Fiber Bundle-based Receiver D... | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 508 | 2019 | ATP/指向/PAT / 调制/复用 | Small satellite optical communication receiver for simultane... | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |
| 509 | 2019 | 未明确 | T Multicore Processors and Graphics Processing Unit Accelera... | 未明确 | 未明确 | 未明确 | 🟡 abstract无缝信号待精读 |

## 🔴 必填项 — 死地/饱和领域记忆（H002 L49-54，领域记忆种子，不再碰）

> 以下 5 项是历史撞死/已 Kill 的轴，强制预置进表作为领域记忆。无论地勘是否命中，都标 🔴。扩检索印证：这些轴在领域里本就冷。

| 轴 | Kill 来源 | 核心失败机制 | 不再碰理由 | 扩检索印证 |
|----|---------|-------------|-----------|-----------|
| 载波同步（N1 PCS / A3 CPE / "Are PLLs dead?"） | N1/A3 preflight + S002 验证 | 相位缓变假设在大气湍流下失效；pilot-CPE 在残余相位噪声下无效 | 5 次失败核心子环节，物理天花板机制必然 | 扩检索 23/430=5.3%，仍是冷区 |
| 自适应交织（4b#1） | D001 Kill | 信道感知自适应交织在 BER 维度 0dB 增益 | FR-21 三版验证 0dB | 交织类 32 条但多为 FEC 联合，非自适应交织单独轴 |
| GG-LLR 译码（(c)） | D002 Kill | Gamma-Gamma 信道 LLR 软译码，增益 < 物理上限 | oracle 上界 0.09dB | 同上 |
| MCS 排程（③） | ③ oracle | 自适应调制编码排程在 LEO 光信道增益极小 | oracle 0.09dB | 调制/复用 86 条但多为单技术评估，非自适应 MCS 排程 |
| 信道估计 LS/LMS/RLS / 静态均衡 / 理想CSI假设 | S002 批评汇总拥挤赛道 | 传统 CE/静态均衡被批 ≥2 次，2019+ 已部分补 | 批评热点但全是已补的拥挤地 | 扩检索 13/430=3.0%，极度冷区 |

## 附录 A：年份筛外（<2019，81 条，全留不丢）

| 标题 | 年 |
|------|----|
| Performance enhancement of free space optical satellite uplink with transmitter  | 2016 |
| Nanosatellite optical downlink experiment: design, simulation, and prototyping | 2016 |
| LEO-to-ground optical communications link using adaptive optics correction on th | 2016 |
| OPTEL-µ: A Compact System for Optical Downlink from LEO Satellites | 2012 |
| Performance Evaluation of Delayed Frame Repetition Variable DataRate technique f | 2018 |
| A Study on Data Transfer Rate Considering Downlink Condition for the LEO Optical | 2016 |
| Investigation on the UAV-To-Satellite Optical Communication Systems | 2018 |
| Approach for recognizing and tracking beacon in inter-satellite optical communic | 2018 |
| Static position errors correction on the satellite optical communication termina | 2017 |
| Doppler shift estimation using broadcast ephemeris in satellite optical communic | 2016 |
| Small Satellite Optical Communication Networks: Analytical Models | 2018 |
| A portable optical ground station for low-earth orbit satellite communications | 2017 |
| (Invited) Upgrade of ESA optical ground station with adaptive optics for high da | 2017 |
| Satellite Tracking System using Amateur Telescope and Star Camera for Portable O | 2016 |
| Optical ground station optimization for future optical geostationary satellite f | 2017 |
| Telecom and scintillation first data analysis for DOMINO: laser communication be | 2016 |
| An acquisition technology of optical ground station in satellite-ground QKD | 2017 |
| Adaptive optics correction into single mode fiber for a low Earth orbiting space | 2015 |
| Far-Field Pattern Measurement of an Onboard Laser Transmitter by Use of a Space- | 1998 |
| Demonstration of a bidirectional coherent air-to-ground optical link | 2018 |
| Fiber-coupling efficiency simulation of Gaussian Schell Model laser in space-to- | 2015 |
| Performance verification of adaptive optics for satellite-to-ground coherent opt | 2018 |
| Performance Analysis of Satellite-to-Ground Coherent Optical Communication Syste | 2018 |
| Homodyne coherent optical receiver for intersatellite communication | 2018 |
| Space micropropulsion systems for Cubesats and small satellites: From proximate  | 2018 |
| Development of a breadboard model of space laser communication terminal for opti | 2017 |
| Adaptive optics testbed for pre- and post-compensation of earth-to-geo optical c | 2017 |
| A Novel 68Gb/s QPSK Coherent Optical Communication Scheme Demonstration for the  | 2018 |
| OFDM and self-coherent detection based satellite-to-ground communication system | 2016 |
| Analysis of improved performance for a satellite-to-ground coherent optical comm | 2010 |
| Impact of optical preamplifier beat noise on inter-satellite coherent optical co | 2015 |
| Digital coherent optical receiver for satellite laser communication | 2011 |
| Satellite Quantum Communication via the Alphasat Laser Communication Terminal -  | 2015 |
| Research and development of 40Gbps optical free space communication from satelli | 2011 |
| Optical coherent beam control based on microwave photonics technologies | 2014 |
| Homodyne BPSK receiver with Doppler shift compensation for inter satellite optic | 2011 |
| Analysis of a new high-speed coherent optical satellite communication system | 1999 |
| Performance of Non-coherent Demodulation for Space Downlink Optical Communicatio | 2015 |
| Costas-loop based carrier recovery in optical coherent intersatellite communicat | 2015 |
| Receiver design for optical inter-satellite links based on digital signal proces | 2016 |
| Status of NASA's deep space optical communication technology demonstration | 2017 |
| Deep space science downlinks via optical communication | 2011 |
| Optical wireless links in future space communications with high data rate demand | 2009 |
| Design of a ground terminal for deep-space optical communications | 2017 |
| NASA's optical communications program for 2017 and beyond | 2017 |
| Multi-purpose laser communication system for the asteroid impact mission (AIM) | 2015 |
| Experimental characterization of space optical communications with disruption-to | 2011 |
| Model of PPM Receiver used in Deep Space Communication Systems | 2006 |
| BER Analysis of a Deep Space Optical Communication System Based on SNSPD Over Do | 2018 |
| Performance analysis of inter-satellite optical wireless communication (IsOWC) s | 2014 |
| System analysis for optimizing various parameters to mitigate the effects of sat | 2015 |
| Terabit-throughput GEO satellite optical feeder link testbed | 2015 |
| Current status of research and development on space laser communications technol | 2015 |
| Roadmap to wide band optical GEO relay networks | 2012 |
| Research on Bandwidth of Optical Filter in GEO-LEO Laser Communication | 2009 |
| Optical GEO feeder link design | 2012 |
| R&D status of the next generation optical communication terminals in JAXA | 2011 |
| System analysis for optical inter-satellite link with varied parameter and pre-a | 2016 |
| Optical inter-satellite and feeder links | 2017 |
| Outage performance analysis of all-optical amplify-and-forward relaying over dua | 2016 |
| Simulation of BPSK Costas loop for optical inter satellite link | 2017 |
| Inter-satellite optical wireless communication system design using diversity tec | 2015 |
| Experimental verifications on small optical inter-satellite communication system | 2017 |
| The design of inter-satellite laser link interface model based on standardized t | 2015 |
| A novel architecture low data rate full duplex optical communications link betwe | 1999 |
| A Pilot-Carrier Coherent LEO-to-Ground Downlink System Using an Optical Injectio | 2012 |
| Feasibility study of coherent LEO-ground link system using an optical injection  | 2011 |
| Experimental characterization of intensity scintillation in the LEO downlink | 2015 |
| Tactical Airborne Laser Communication Technology (TALC) | 1990 |
| Performance Estimation of Optical LEO Downlinks | 2018 |
| Variable Data Rate for Free Space Optical Low Earth Orbit Downlinks (OLEODL) | 2018 |
| JAXA's optical data relay satellite programme | 2015 |
| Constructing Satellite Backbone Network via Timeslot-based Optical Switching | 2018 |
| TNO optical communications space terminals — Current projects and future plans | 2017 |
| Investigation of optical intensity fluctuation in the presence of satellite vibr | 2011 |
| Symbol Error Rate Model for Communication Using Femtosecond Pulses for Space App | 2016 |
| Optical Communication in Space: Challenges and Mitigation Techniques | 2016 |
| The<i>Swift</i>Gamma‐Ray Burst Mission | 2004 |
| Satellite-Relayed Intercontinental Quantum Network | 2018 |
| Variability of Absorption and Optical Properties of Key Aerosol Types Observed i | 2002 |
| &lt;title&gt;In-orbit test result of an operational optical intersatellite link  | 2002 |

## 附录 B：unknown year（7 条，全留）

| 标题 | query |
|------|-------|
| OOK for LEO Downlinks - Satellite Communications in the 5G Era | LEO optical downlink |
| SYSTEM ASPECTS OF OPTICAL LEO-TO-GROUND LINKS | LEO optical downlink |
| On-orbit demonstration of 200-Gbps laser communication downlink from the TBIRD C | LEO optical downlink |
| NASA’s Next Generation >100 Gbps Optical | LEO optical downlink |
| Operations and Results from the 200 Gbps TBIRD Laser Communication Mission | satellite laser communication |
| SSC23-I-03 | satellite laser communication |
| Lunar Laser Communication Demonstration NASA’s First Space Laser Communication S | satellite laser communication |

## 附录 C：噪声/非卫星光通信（全留不丢）

两轮检索的 noise（新闻稿/产品页/百科/成像载荷/通用 FSO 无卫星上下文/视频/博客）已在各子 agent 报告附录记录，合计 ~90 条。典型类别：
- **新闻/产品**：Kepler/NASA/ESA/DLR/Spire/AAC Clyde/Thales/SSC/Mynaric 等厂商新闻稿、产品 datasheet、任务报道
- **成像载荷误命中**：`optical satellite payload` query 拉入大量 Earth-observation 成像载荷（高光谱/多光谱/MTR/定标），与通信无关
- **通用 FSO 无卫星上下文**：`deep space` query 命中 `deep learning + 通用大气 FSO`（标题含 Deep 误命中）
- **非卫星链路**：UAV-to-ground / 纯光纤 / 地面 RF-over-fiber / 数据中心光网络
- **百科/综述/视频**：Wikipedia/YouTube/blog/通用 6G 综述

> 完整噪声清单见各子 agent 报告（S004 + S006 session note）+ `search-archive/2026-06-22/_landscape_full_merged.json`（518 条全集含噪声）。

## 附录 D：v3 设备词召回噪声清单（动作 A round3，2026-06-22，全留不丢）

> 11 设备词检索召回 150 去重条 → 95 域内 → 79 核心入主表（431-509）→ **16 相邻域 + 44 域外**（共 60 条噪声，全留此附录不丢）。
> 噪声分布即"设备词检索召回质量"诊断信号：召回严重偏向"卫星光硬件"相邻领域（RF/雷达/遥感/光计算/产品页）。

### D.1 相邻域剔除（16 条，含 satellite+optical 共现但属 RF/雷达/遥感/图像/产品页）

| # | 标题片段 | 剔除理由 |
|---|---------|---------|
| 1 | Photonic integrated circuits for high-throughput optical communication | PIC 综述（误剔复评回主表 #470） |
| 2 | Real-time implementation of all-digital optical time transfer | 时间频率传递非通信 |
| 3 | GPU Accelerated Processing Method for Feature Point Extraction | SAR 图像处理 |
| 4 | Cortex Lasercom - Optical Digital Processor Unit - Satsearch | 产品页 |
| 5 | Geometric Correction Analysis of Highly Distortion | 图像几何校正 |
| 6 | Lithological Unit Classification Based on Geological Knowledge | 地质分类 |
| 7 | Inter-Satellite Integrated Laser Communication/Ranging Link | 测距为主（误剔复评回主表 #506） |
| 8 | Shoreliner: A Sub-Pixel Coastal Waterline Extraction | 海岸线提取 |
| 9 | An Integrated Millimeter-Wave Satellite Radiometer | mmW 辐射计 |
| 10 | An innovative multimission optical ground station | OGS（误剔复评后仍偏综述，留此） |
| 11 | Free-space optical communication - Wikipedia | 百科 |
| 12 | Design of Novel Laser Crosslink Systems Using Nanosatellites | 纳卫星交叉链路（边界，留此） |
| 13 | Designing and Testing On-Orbit Intelligent Processing Payload | 载荷处理 |
| 14 | The Tools and Workflow of LEO Earth Observation Optical Payload | 对地观测载荷 |
| 15 | Photonics for satellite radars: the SPACEBEAM project | 卫星雷达 |
| 16 | Ground Terminal Evaluation for Deployable Optical Receiver Aperture | DORA 地面终端（边界，留此） |

### D.2 域外不入表（44 条，无 satellite+optical 共现，fiber/mmWave/VLC/非卫星光通信）

代表性条目（完整列表见 `search-archive/2026-06-22/_v3-continuation.md` 注释段 + landscape2-*.json 原始 JSON）：
- 光纤相干收发（400Gb/s DP-QAM64 / 2000km 光域偏振解复用 / 低复杂度 IQ 校准等 ~20 条）
- 光计算/光处理单元（Microcomb PPU / ΦPU / 光线性求解器 ~5 条）
- 产品页（LKD Aerospace Antelope/Leopard-PDP / ZAITRA SKAIDOCK / doEEEt 博文 ~6 条）
- 非卫星（Navigation Aid / mmWave Indoor / pure fiber ~13 条）

## 附录 E：v3 动作 B 模块词诊断（**不是地勘**，受控例外，2026-06-22）

> **方法论标注**：动作 B 用模块词（synchronization/estimation/equalization/modulation）是诊断动作不是地勘。
> 产出**只入此诊断段，不入主表候选池**，与动作 A 物理隔离（偏航检查 A 受控例外）。
> 判读纪律（T001 §2.3）：占比涨只说明做的人多，**区分"人数多（成熟无缝）"和"人数少（有开放缝）"看真缝密度**。

### E.1 死轴占比 + 真缝密度对照表

| 维度 | v2 主表占比 | B 搜索 raw | 卫星核心 | 严判真缝 | 真缝率 | 软缝 | 死轴成因判读 |
|------|-----------|-----------|---------|---------|-------|------|------------|
| **载波同步**（死轴1）| 23/430 = 5.3% | 20 | 17 | **4** | **23.5%** | 9 | 人数少 + 真缝密度高 → **有开放缝的冷区** |
| **信道估计**（死轴2）| 13/430 = 3.0% | 20 | 20 | **2** | **10.0%** | 10 | 人数少 + 真缝密度中 → 冷区但有缝 |
| **均衡**（死轴3）| 未单列 | 20 | 19 | **3** | **15.8%** | 12 | 人数少 + 真缝密度高 → 有开放缝的冷区 |
| **调制**（热区对照）| 86/430 = 20% | 20 | 20 | 2 | 10.0% | 7 | 人数多 + 真缝密度中 → 热区，缝相对拥挤 |

**关键发现（偏航检查 E 提炼）**：3 个死轴的真缝密度（10-23.5%）**反而高于或等于热区调制（10%）**。
- 死轴低占比 ≠ 没缝，是 **做的人少 + 有开放问题**
- 这恰恰符合判据 A（缝）+ 判据 B（人数少）的候选信号
- **判读死轴成因必须分两步**：先看人数（占比/搜索 raw 数），再看缝密度（abstract 真缝信号）。只看占比会误杀
- 动作 A 设备词检索在死轴维度**零命中**（79 条核心里 carrier-sync/channel-estimation/equalization 子地带命中数远低于模块词直接搜）→ 设备词补盲的价值在硬件层不在方法层

### E.2 真·方法论缝候选清单（严判，待精读验证，不作为 Go/No-Go 依据）

> regex 严判有 ~30% 误检率（如 channel-estimation 里混入图像处理论文），以下候选**必须精读 abstract + intro 验证**才能作为判据 A 证据。
> **本轮地勘只到"判读出真缝可能存在 + 候选论文清单"，不到 Go/No-Go**。

**载波同步（死轴1，4 条真缝候选）**：
- `Adaptive Optics Assisted Space-Ground Coherent Opt` — "residual frequency shift that remains after preliminary coarse frequency offset correction"（AO 辅助空地相干，粗频偏校正后残余频移）
- `Pilotless Iterative Carrier Synchronization With L` — "solve the phase ambiguity problem... Costas loop tracking and LDPC decoding feedback united"（无导频迭代载波同步）
- `An Improved Phase Deviation Discriminator for Carr` — "would increase greatly. To solve this problem, improved phase deviation discriminator"（鉴相器改进）
- `Hybrid STA With FNN and CNN Models for Robust Chan` — "atmospheric turbulence in terrestrial FSO links and Doppler-induced carrier-..."（湍流+多普勒载波同步）

**信道估计（死轴2，2 条真缝候选）**：
- `A Noise-Tolerant Carrier Phase Recovery Method for` — "noise-tolerant method... accurate carrier phase recovery with reduced complexity"（噪声容忍 CPR）
- （1 条为图像处理误检，剔除）

**均衡（死轴3，3 条真缝候选）**：
- `Linear Time-Packing Detectors for Optical Feeder L` — "bit sequence successfully grows notably. To address this issue, low-complexity linear equalization"（光 feeder 链路低复杂度线性均衡）
- `Capacity Limits of Optical Satellite Communications` — 容量上限分析（非方法 gap，软缝）
- `Low-Cost Blind and Semi-Blind Equalizers for Nonli` — "can significantly degrade signal quality and require advanced equalization"（盲/半盲均衡）
- （1 条为气象观测误检，剔除）

**调制（热区对照，2 条真缝候选）**：
- `Bridging the Gap in Modulation Selection for Satel` — "Bridging the Gap in Modulation Selection for Satellite Optical Communication"（调制选择 gap）
- `Design and comparative analysis of Inter Satellite` — IS-OWC 设计对比

### E.3 IEEE 债务声明

- 动作 A 11 词 + 动作 B 4 词的 IEEE blit 全 0 条。IEEE 今日对当前 IP 全面限流（quota 卡 1/50 不动）。
- **不是 S005 修复失效**（S005 测过同命令成功）：另一对话 3 词小样本测试显示 `receiver`/`photonic-receiver` 能拿到 24-25 条，`transceiver`/`frontend` 等通用宽词被挡 → 更精确机制是"高频通用词触发实时反爬 + 累积风险分"，非纯 IP 全封。
- **债务处理**：search API 267 raw + 80 raw 够密度判读（≈ S006 round2 300 raw），IEEE 增量价值 < 执行成本，**不重跑不卷用户手动下**。真缝候选已从 search API 提取，精读阶段如发现 search API 系统性漏掉 IEEE 专属会议论文（如 IPC/ECOC），再针对性补。

## 元信息

- 总条目（去重）：597（v2 518 + v3 续段 79）
- 主表（≥2019）：509（v2 430 + v3 续段 79）
- 年份筛外（<2019）：81
- unknown year：7
- 缝潜力分布：{'🟢': 48, '🟢?': 15（v3 待精读自陈挑战）, '🟡': 350（v2 338 + v3 64 + 软缝 12 折入）, '🔴': 44}
- 检索源：S2(243+247) + Exa(107+20) + OpenAlex(33+混合) + IEEE blit(111 含 source_api 缺失) + 其他混合
- IEEE 覆盖：v2 5 query × 25 条 = 125 raw；**v3 IEEE 全面限流 0 条（见附录 E.3 债务）**
- 扩检索印证（v2）：死轴（载波同步 23/信道估计 13）是结构性冷区，非采样偏差
- **v3 动作 B 诊断印证**：死轴真缝密度（10-23.5%）反高于热区调制（10%）→ 死轴是"有缝但人少"非"没缝"，**需精读验证**才能升 Go/No-Go
