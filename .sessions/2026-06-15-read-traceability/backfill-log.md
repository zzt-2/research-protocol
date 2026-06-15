# Title 回填日志

> 2026-06-15 19:36 | backfill_titles.py | 81 篇

回填规则：metadata title 为空/URL/slug 且 content.md 有 high 置信真标题 → 回填 title + 重算 title_check。绝不碰 match/mismatch。

| 目录 | method | invalid | 新状态 | overlap | 旧 title | 新 title |
|---|---|---|---|---|---|---|
| 1909.11003 | arxiv_pdf | empty | match | 1.0 | `` | `Deep learning for channel estimation in FSO commun` |
| 2112.01738 | arxiv_pdf | url | match | 1.0 | `https://arxiv.org/pdf/2112.017` | `Joint User Scheduling and Beamforming Design for M` |
| 2204.13972 | arxiv_pdf | empty | match | 1.0 | `` | `Size Generalization for Resource Allocation with G` |
| 2207.12547 | arxiv_html | url | match | 1.0 | `https://arxiv.org/pdf/2207.125` | `The BUTTER Zone: An Empirical Study of Training Dy` |
| 2303.13773v2 | arxiv_html | url | match | 1.0 | `https://export.arxiv.org/pdf/2` | `Graph Neural Networks for the Offline Nanosatellit` |
| 2305.15611 | arxiv_html | empty | match | 1.0 | `` | `Tackling Size Generalization of Graph Neural Netwo` |
| 2312.15873 | arxiv_html | empty | match | 1.0 | `` | `Investigating Inter-Satellite Link Spanning Patter` |
| 2401.09711 | arxiv_html | url | match | 1.0 | `https://arxiv.org/pdf/2401.097` | `Joint Beam Direction Control and Radio Resource Al` |
| 2402.04056 | arxiv_html | empty | match | 1.0 | `` | `Collaborative Deep Reinforcement Learning for Reso` |
| 2403.05892 | arxiv_html | empty | match | 1.0 | `` | `Stacked Intelligent Metasurface Enabled LEO Satell` |
| 2404.07450 | arxiv_html | empty | match | 1.0 | `` | `Collaborative Ground-Space Communications via Evol` |
| 2404.12633 | arxiv_html | empty | match | 1.0 | `` | `FlagVNE: A Flexible and Generalizable Reinforcemen` |
| 2406.04601 | arxiv_html | empty | match | 1.0 | `` | `Enhancing Size Generalization in Graph Neural Netw` |
| 2406.11366 | arxiv_html | empty | match | 1.0 | `` | `$x$eoverse: A Real-time Simulation Platform for La` |
| 2406.17334 | arxiv_html | empty | match | 1.0 | `` | `Joint Admission Control and Resource Allocation of` |
| 2410.22999 | arxiv_html | empty | match | 1.0 | `` | `Towards Constraint-aware Learning for Resource All` |
| 2411.01338 | arxiv_html | empty | match | 1.0 | `` | `Deep Reinforcement Learning for Trajectory and Pha` |
| 2411.08896 | arxiv_html | empty | match | 1.0 | `` | `Demand-Aware Beam Hopping and Power Allocation for` |
| 2411.09600 | arxiv_html | url | match | 1.0 | `https://arxiv.org/pdf/2411.096` | `Latency Optimization in LEO Satellite Communicatio` |
| 2412.07555 | arxiv_html | url | match | 1.0 | `https://arxiv.org/pdf/2412.075` | `GSM: A GNN-based Space-MIMO Framework for Direct-t` |
| 2503.04233 | arxiv_html | empty | match | 1.0 | `` | `Learning Wideband User Scheduling and Hybrid Preco` |
| 2503.24203 | arxiv_html | empty | match | 1.0 | `` | `Traffic Engineering in Large-scale Networks with G` |
| 2504.08401 | arxiv_html | empty | match | 1.0 | `` | `Graph Reduction with Unsupervised Learning in Colu` |
| 2505.04401 | arxiv_html | empty | match | 1.0 | `` | `A Heuristic-Integrated DRL Approach for Phase Opti` |
| 2505.11978 | arxiv_html | empty | match | 1.0 | `` | `LLM-guided DRL for Multi-tier LEO Satellite Networ` |
| 2505.23599 | arxiv_html | empty | match | 1.0 | `` | `On Transferring Transferability: Towards a Theory ` |
| 2507.19234 | arxiv_html | empty | match | 1.0 | `` | `Virne: A Comprehensive Benchmark for RL-based Netw` |
| 2509.12716 | arxiv_html | empty | match | 1.0 | `` | `Joint AoI and Handover Optimization in Space-Air-G` |
| 2510.11109 | arxiv_html | empty | match | 1.0 | `` | `Graph Neural Network-Based Multicast Routing for O` |
| 2510.15210 | arxiv_pdf | empty | match | 1.0 | `` | `Structural Generalization for Microservice Routing` |
| 2510.27506 | arxiv_html | empty | match | 1.0 | `` | `Asynchronous Risk-Aware Multi-Agent Packet Routing` |
| 2512.07053 | arxiv_html | empty | match | 1.0 | `` | `Random Access for LEO Satellite Communication Syst` |
| 2512.09312 | arxiv_html | empty | match | 1.0 | `` | `Tyche: A Hybrid Computation Framework of Illuminat` |
| 2601.08254 | arxiv_html | empty | match | 1.0 | `` | `Large Artificial Intelligence Model--Guided Deep R` |
| 2601.10083 | arxiv_html | empty | match | 1.0 | `` | `Starfield: Demand-Aware Satellite Topology Design ` |
| 2601.18453 | arxiv_html | empty | match | 1.0 | `` | `Deep Reinforcement Learning for Hybrid RIS Assiste` |
| 2601.21914 | arxiv_html | empty | match | 1.0 | `` | `Joint Laser Inter-Satellite Link Matching and Traf` |
| 2601.21921 | arxiv_html | empty | match | 1.0 | `` | `Duality-Guided Graph Learning for Real-Time Joint ` |
| 2603.10983 | arxiv_html | empty | match | 1.0 | `` | `Federated Learning-driven Beam Management in LEO 6` |
| 2603.16470 | arxiv_html | empty | match | 1.0 | `` | `Multi-Agent Reinforcement Learning Counteracts Del` |
| 2604.12382 | arxiv_html | empty | match | 1.0 | `` | `Traffic-Aware Domain Partitioning and Load-Balance` |
| 2604.27478 | arxiv_html | empty | match | 1.0 | `` | `Toward Scalable SDN for LEO Mega-Constellations: A` |
| 2605.02413 | arxiv_html | empty | match | 1.0 | `` | `Spatial-Temporal Learning-Based Distributed Routin` |
| 2605.04448 | arxiv_html | empty | match | 1.0 | `` | `Queue-Aware and Resilient Routing in LEO Satellite` |
| 10.1016_j.ast.2026.112361 | all_failed | empty | match | 1.0 | `` | `Aerospace Science and Technology` |
| 10.1038_s41598-025-17852-y | all_failed | empty | match | 1.0 | `` | `OPEN Secure and energy-efficient transmission in U` |
| 10.1038_s41598-026-40704-2 | unpaywall | empty | match | 1.0 | `` | `orts Scientific Rep` |
| 10.1109_globecom52923.2024.10901096 | all_failed | empty | match | 1.0 | `` | `FlexSATE: Flexible and Distributed Traffic Enginee` |
| 10.1109_icc52391.2025.11160846 | all_failed | empty | match | 1.0 | `` | `Self-Attention-Based Deep Reinforcement Learning f` |
| 10.1109_iotm.001.2300111 | all_failed | empty | match | 1.0 | `` | `Optimization Design in RIS-Assisted Integrated Sat` |
| 10.1109_iwrfat65352.2025.11102822 | all_failed | empty | match | 1.0 | `` | `Robust Beamforming and Phase Shift Control in RIS-` |
| 10.1109_jiot.2024.3371395 | all_failed | empty | match | 1.0 | `` | `Fairness-Aware Computation Offloading With Traject` |
| 10.1109_jiot.2025.3610772 | all_failed | empty | match | 1.0 | `` | `Efficient Packet Routing for Large-Scale LEO Satel` |
| 10.1109_jlt.2008.927778 | firecrawl_scrape | empty | match | 1.0 | `` | `Phase Estimation Methods for Optical Coherent Dete` |
| 10.1109_jlt.2022.3167035 | firecrawl_scrape | empty | match | 1.0 | `` | `Joint Impact of Channel Estimation Errors and Poin` |
| 10.1109_jsac.2025.3528815 | all_failed | empty | match | 1.0 | `` | `Path-Based Graph Neural Network for Robust and Res` |
| 10.1109_taes.2025.3571400 | all_failed | empty | match | 1.0 | `` | `Dynamic Load-Balancing Routing Strategy for LEO Sa` |
| 10.1109_taes.2026.3652971 | all_failed | empty | match | 1.0 | `` | `60%. Compared with the baseline algorithm, the GRL` |
| 10.1109_ton.2025.3607939 | all_failed | empty | match | 1.0 | `` | `Learning-Based Adaptive Range Routing for Traffic ` |
| 10.1109_tsc.2023.3326539 | arxiv_html | empty | match | 1.0 | `` | `Joint Admission Control and Resource Allocation of` |
| 10.1109_tvt.2023.3333848 | all_failed | empty | match | 1.0 | `` | `A GNN-Enabled Multipath Routing Algorithm for Spat` |
| 10.1109_tvt.2024.3471658 | all_failed | empty | match | 1.0 | `` | `GRLR: Routing With Graph Neural Network and Reinfo` |
| 10.1109_twc.2022.3144360 | firecrawl_scrape | empty | match | 1.0 | `` | `Blind and Semi-Blind Channel Estimation/Equalizati` |
| 10.1109_twc.2025.3636875 | arxiv_html | empty | match | 1.0 | `` | `Graph-Aware Temporal Encoder Based Service Migrati` |
| 10.1109_vtc2025-fall65116.2025.11310192 | all_failed | empty | match | 1.0 | `` | `Deep Reinforcement Learning-based Energy Efficienc` |
| 10.1109_wcnc57260.2024.10570820 | all_failed | empty | match | 1.0 | `` | `Energy Efficiency Optimization in RIS-assisted ISA` |
| 10.4230_lipics.cp.2021.42 | firecrawl_scrape | empty | match | 1.0 | `` | `Data Driven VRP: A Neural Network Model to Learn H` |
| eydian-bipartite-2025 | manual | slug | match | 1.0 | `eydian-bipartite-2025` | `Handover Strategy for LEO Satellite Networks Using` |
| https-hal-science-hal-04852064v1-document | oa_pdf | url | match | 1.0 | `https://hal.science/hal-048520` | `Earth Observation Satellite Scheduling with Graph ` |
| https-iris-polito-it-retrieve-handle-11583-2975291 | oa_pdf | url | match | 1.0 | `https://iris.polito.it/retriev` | `POLITECNICO DI TORINO Repository ISTITUZIONALE` |
| https-mdpi-res-com-d-attachment-sensors-sensors-22 | oa_pdf | url | match | 1.0 | `https://mdpi-res.com/d_attachm` | `An Efficient Multi-Dimensional Resource Allocation` |
| https-orbilu-uni-lu-bitstream-10993-62321-1-confer | oa_pdf | url | match | 1.0 | `https://orbilu.uni.lu/bitstrea` | `Power Allocation and Beam Illumination Design for ` |
| https-re-public-polimi-it-retrieve-33667063-58a4-4 | oa_pdf | url | match | 1.0 | `https://re.public.polimi.it/re` | `RESEARCH ARTICLE` |
| jang-etri-2026 | manual | slug | unverifiable | 0.0 | `jang-etri-2026` | `O R I G I N A L A R T I C L E` |
| jang-wiopt-2025 | manual | slug | match | 1.0 | `jang-wiopt-2025` | `Optimized Handover Management for Reliable Connect` |
| lee-gnn-ictexpress-2025 | manual | slug | match | 1.0 | `lee-gnn-ictexpress-2025` | `Handover strategy for LEO satellite communication ` |
| lee-madrl-cl-2025 | manual | slug | match | 1.0 | `lee-madrl-cl-2025` | `Multi-Agent Deep Reinforcement Learning Based Hand` |
| network-00015 | manual | slug | match | 1.0 | `network-00015` | `Evaluation of TOPSIS Algorithm for Multi-Criteria ` |
| network-00049 | manual | slug | match | 1.0 | `network-00049` | `Real-Time Handover in LEO Satellite Networks via M` |
| sun-morl-2024 | manual | slug | match | 1.0 | `sun-morl-2024` | `Handover for Multi-Beam LEO Satellite Networks: A ` |
| zhou-clgnn-tvt-2025 | manual | slug | match | 1.0 | `zhou-clgnn-tvt-2025` | `Graph Neural Network-Based Continual Learning for ` |
