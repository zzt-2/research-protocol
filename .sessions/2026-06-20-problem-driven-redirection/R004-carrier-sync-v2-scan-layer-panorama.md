# [R004] 载波同步 D015 v2（D017）扫描层全景表

> 2026-07-02 | 关联：专题 2026-06-20-problem-driven-redirection / D017（D015 v2）路径 A 扫描层 / S024 v1 中间结论
> 来源：S027（本轮）执行 D017 扫描层（穷举门控 A 前的全景盘点）

## 调研问题

D017 v2 要求扫描层"列全载波同步近年顶刊所在子地带代表论文清单 + 综述全文 open problem 段，全列出候选切入点分类"，到**穷举门控 A 停下让用户确认全景**才进判读层。本轮回答：载波同步领域全景下，有哪些候选切入点，分别属于哪一档（够 D005 / 不够 / 撞 D006 / 撞旧 Kill / 范围出界）？

## 扫描层数据来源

| 来源 | 数量 | 子 agent |
|---|---|---|
| **sat.1553 综述 forward cited-by**（openalex+S2 union） | 5 篇（1 真 cited-by L003 / 2 无法核验 L004/L005 / 2 不相关 L001/L002）| 主线 + 子 agent 3 核验 |
| **CPE 锚 Kikuchi 2008 JLT**（ref [12]/[49]）cited-by union | 120 篇（50 OA + 100 S2，S2-only 70）| 子 agent 1 |
| **CFO 锚 Paillier 2020 JLT**（D006 反证 baseline）cited-by union | 43 篇（34 OA + 31 S2，S2-only 9）| 子 agent 1 |
| **帧同步锚 TWC 2024** cited-by union | 57 篇（全 RF/NTN 出界）| 子 agent 2 |
| **帧同步锚 Schmidl-Cox 1997**（ref [68]）cited-by union | 150 篇（OFDM/RF 主导）| 子 agent 2 |
| **Pilot 锚 Spalvieri [57] + Martins [58]** cited-by | 85 + 6 篇（偏光纤长距）| 子 agent 2 |
| **OPLL 锚 10.3390/photonics10121312 重跑**（S024 bug 修后）| 2 篇（0→2 修复确认，仍极低）| 子 agent 2 |
| **S024 已有领域全景**（3 档宽检索合并去重）| 37 篇 | S024 阶段 7 |

## 候选切入点分类表（D017 v2 扫描层产出，穷举门控 A 输入）

### 档位说明
- **够 D005**：星地光 + 载波同步 + abstract 层有 ≥2dB 增量声称（或等效灵敏度/penalty 指标）
- **不够**：在主题内但 abstract 层无 ≥2dB 增量（普遍 <2dB / 未量化 / 仅 MSE/范围指标）
- **撞 D006**：把湍流相位纳入载波同步算法设计（联合建模，D006 Kill 的 Q12 family）
- **撞旧 Kill**：撞 D010/D011/D012（Q1/Q2/Q3，ISL/feeder 范围出界搬星地）或 D008（4B，ABR 对 σ² 平缓）
- **范围出界**：纯 RF / 光纤长距 / feeder 系统级 / ISL 真空

### A. 够 D005 档（星地光 + 载波同步 + abstract 层 ≥2dB 信号）
**0 个**。载波同步子环节扫描层覆盖 400+ 篇 cited-by，**abstract 层无一篇声称星地光 + 载波同步 + ≥2dB 灵敏度增量**（子 agent 1/2 共同结论）。

> ⚠️ 这是 abstract 层结论（D017 v2 红线 7：abstract 层判不出/矛盾时强制升级到全文/综述层）。综述 sat.1553 自报 open problem（L440/L558/L788）作者都说"to quantify the potential gain"——增量未量化不等于不存在，留判读层精读验证。

### B. 不够 D005 档（主题内但 abstract 层 <2dB / 未量化）

| # | 切入点 | 来源 | abstract 信号 | 不够原因 |
|---|---|---|---|---|
| B1 | 自适应 pilot 窗口（动态调 pilot 符号数适应大 SNR 波动）| sat.1553 L440 自报 open problem + 综述 §4.2 末 | pilot vs V&V scenario 4 ~1dB | ~1dB 未达 2-4dB，综述作者自承"to quantify the potential gain" |
| B2 | deep fade 时 FOE 停止更新策略 | sat.1553 L558 自报 + F2-L002 帧同步 FOE 重锁 | 单支路 +2.9dBm 但靠分集 | 靠分集硬件（多望远镜），星地单孔径受限未量化 |
| B3 | 子系统协同（pilot 同时喂相位补偿+均衡+依赖帧同步对齐）| sat.1553 L788 conclusion open problem | 定性 | 系统级协同非单一算法，A1 归属待查 |
| B4 | 双反馈环 + V&V 前馈级联载波恢复 | `10.1016/j.optcom.2023.129312`（2023，Paillier cited-by）| 无 abstract，dB 未知 | 无 abstract，待精读核验 |
| B5 | 短时谱分析粗频偏估计（CFO 新算法）| `10.1016/j.optcom.2024.130981`（2024，Paillier cited-by）| 无 abstract | 无 abstract，待精读核验 |
| B6 | 高 Doppler rate（频漂率）相干接收机 Z 变换建模 | `10.1109/ICSOS66026.2025.11443174`（ICSOS 2025，S2-only 需核验）| 针对 LEO 下行频漂率 | 无 dB 声称，建模为主 |
| B7 | Gardner TED 与 Doppler 相关性频偏估计 | `10.1364/ofc.2026.w2a.62`（OFC 2026 会议）| 宽估范围+抗噪 | 仅会议 poster，无 dB |
| B8 | RL+几何整形自相干电域自消除（对湍流相位/频偏免疫）| `10.1364/jocn.468220`（2022 JOCN）| 自消除结构免疫湍流 | 无 dB 声称，自相干路线 |
| B9 | 低复杂度虚拟载波自相干 + 数字分辨率增强 | `10.1109/jlt.2023.3270673`（2023 JLT）| 降量化噪声 | 自相干路线，无 dB |
| B10 | 16-QAM pilot-assisted RLS 载波同步 | `10.1007/s11107-024-01019-2`（2024）| **无 abstract，唯一待精读核验 dB** | 待精读 |
| B11 | NDA-ML STO+CPE 联估 M-APSK FSO | `10.1109/LPT.2024.3523478`（2025 PTL，S2-only 需核验）| MSE 近 CRLB | MSE 指标非 dB |
| B12 | In/Out-of-Band 频域 pilot 相位噪声估计 | `10.1109/tcomm.2022.3171809`（2022 TCOMM）| 信号-导频功率比最优理论 | 理论分析，无系统 dB |

### C. 撞 D006 档（联合建模进载波同步算法，D006 Kill 的 Q12 family）

| # | 切入点 | 来源 | 撞 D006 依据 |
|---|---|---|---|
| C1 | 2.6 OPLL 联合建模（湍流相位进 OPLL 环路）| S024 C3 核查 | D006 L341 直接命中 |
| C2 | 2.1 TS-KF 扩状态搬星地 | S024 | D010 自判（Q1 Kill，搬星地=C3 撞 Q12/B1）|
| C3 | 2.2 CPR 换 KF 搬星地 | S024 | D011 自判（Q2 Kill）|
| C4 | 批1.1 综述 B1 gap（湍流相位+piston+多普勒联合建模）| S024 C3 核查 | D006 L324 逐字命中 |

### D. 撞旧 Kill / 范围出界档

| # | 切入点 | 来源 | 撞哪个 |
|---|---|---|---|
| D1 | F2-L008 PS-RCM 星地 Doppler 破坏载波谱分离 + PS 高 SNR 趋零 | S024 | 撞 N1（gain≈0）|
| D2 | TWC 2024 帧同步 cited-by 57 篇 | 子 agent 2 | 全 RF/NTN/OTFS 出界 |
| D3 | Schmidl-Cox 1997 cited-by 150 篇 | 子 agent 2 | OFDM/RF 主导出界 |
| D4 | Spalvieri/Martins pilot cited-by 85+6 篇 | 子 agent 2 | 偏光纤长距（EEPN/CPR-review）出界 |
| D5 | Kikuchi 2008 cited-by S2-only 70 篇多数 | 子 agent 1 | 偏光纤长距/小众，星地光命中稀 |
| D6 | CNN DL 相位噪声缓解（wireless backhaul）| `10.1109/ICCWorkshops59551.2024.10615713` | wireless backhaul 出界 |
| D7 | OFDM-FSO 三重自相关同步 | `10.1109/LPT.2025.3644328` | OFDM-FSO，偏帧同步精度非载波同步算法核心 |

## 子环节饱和度观察（扫描层事实，非方向判读）

| 子环节 | 领域做得多？ | 具体点占住？ | D017 v2 4 档判读 |
|---|---|---|---|
| **CPE 相位估计** | ✅ 多（Kikuchi 120 cited-by）| ⚠️ BPS/V&V 已收敛，新角度需结合场景 | 第 1 档边缘——做得多但纯算法层新点稀，靠场景结合 |
| **CFO 频偏补偿** | ✅ 多（Paillier 43 cited-by）| ⚠️ LEO 高 Doppler rate 是相对未饱和切口（B4-B7）| 第 1 档边缘——做得多，CFO 子环节 2022+ 有 6 篇后续，角度集中 LEO Doppler rate |
| **OPLL 光锁相环** | ⚠️ 少（cited-by 0→2 极低）| ✅ sin 鉴相器切入点锚团队留白 | 第 3 档（做得少）——但 D006 红线把联合建模路堵死，残余幅度衰落鲁棒性路窄 |
| **帧同步/载波恢复联合** | ✅ 多（Schmidl-Cox 150）| ❌ 全 RF/OFDM 出界，星地光命中 ≤2 | 第 4 档（星地光领域做得少+点被 RF 占）|
| **Pilot 自适应窗口** | ✅ 多（Spalvieri 85）| ❌ 偏光纤长距，L440 open problem 无后续直接量化 | 第 2/3 档边缘——光纤做得多，星地光 pilot 自适应无后续 |

## 关键发现（扫描层事实）

1. **abstract 层无 ≥2dB 星地光载波同步增量声称**（A 档 = 0）——但这是 abstract 层结论，综述自报 open problem 增量未量化，留判读层精读验证（D017 v2 红线 7）
2. **CFO 子环节"相对未饱和"**：LEO 高 Doppler rate（频漂率）+ 粗/细频偏分离估计有 6 篇 2022+ 后续（B4-B7），角度集中，是扫描层最亮的子环节
3. **CPE 子环节"算法层已收敛"**：纯 CPE 算法创新少，多被 BPS/V&V 工程实现吸收，新角度需结合场景
4. **OPLL 锚团队留白仍成立**：sin 鉴相器幅度衰落鲁棒性线作者 2025 已转频偏（Z-ODPLL），但 D006 红线把联合建模路堵死
5. **载波同步论文报指标习惯**：普遍以相位噪声容限 / BER-vs-OSNR penalty / 估计范围报，**不按 dB 灵敏度增量报**——判读层筛选增量声称时建议放宽到这些等效指标
6. **S024 "够格点不可达"判读 v2 复核**：扫描层 400+ 篇 cited-by 覆盖下，A 档仍 = 0，**S024 v1 中间结论在 abstract 层成立**——但 v2 升级到全文/综述层（B 档 12 个待精读）后可能改变

## 对决策的影响

### 对 D017 穷举门控 A 的影响
扫描层已穷举 5 子环节（CPE/CFO/OPLL/帧同步/pilot）× 多锚 cited-by + S024 已有 37 篇 + sat.1553 综述 open problem，**全景盘点完成**，可进穷举门控 A 让用户确认全景。

### B 档 12 个待判读层精读候选的优先级建议（主线技术判断，供用户参考）
- **CFO 子环节（B4-B7）** 优先级最高——扫描层最亮，角度集中（LEO Doppler rate），4 篇待精读
- **B10 16-QAM pilot RLS** 唯一无 abstract 待精读核验 dB 的，跨 Q2 16-QAM 种子联读（D011 登记）
- **B1-B3 综述背书 3 点**（sat.1553 L440/L558/L788）S024 已留，仍是定性 open problem

### 不在本轮范围（扫描层纪律）
- ❌ 不精读全文（判读层的事，需用户确认全景后才进）
- ❌ 不判 Go/Kill（方向判读是主线+用户的事）
- ❌ 不立 Q#（D017 守"判读层精读验证才立"）

## 结论

载波同步 D015 v2 扫描层全景盘点完成。**A 档（abstract 层 ≥2dB）= 0，B 档（主题内 <2dB/未量化）= 12 个待判读层精读候选，C 档（撞 D006）= 4 个，D 档（撞旧 Kill/范围出界）= 7 类**。CFO 子环节（LEO Doppler rate）是扫描层最亮的切口。全景交付用户确认（穷举门控 A），确认后进判读层精读 B 档候选。
