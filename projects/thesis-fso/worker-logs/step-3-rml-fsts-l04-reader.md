# L04 全文精读报告：Space-Ground Coherent Optical Links

> Groundwork Step 3 单篇 reader｜角色：C4 space-ground transfer physics｜判定：**PASS**

## 0. Preflight 与证据边界

- 派遣题名：*Space-Ground Coherent Optical Links: Ground Receiver Performance With Adaptive Optics and Digital Phase-Locked Loop*。
- DOI：`10.1109/JLT.2020.3003561`；本地 metadata 的 `id`、`doi` 均一致（`metadata.json:L3-L5`）。
- canonical 正文：`D:\code\study\research-protocol\papers\doi\10.1109_jlt.2020.3003561\content.md`。
- 实测 SHA256：`62E3BFDF6B803069342B49DC6D9F666899BD7257841E42D9A5003CFDFF5A9662`；实测 46,966 bytes、243 行，与派遣 preflight 完全一致。
- `content.md` 缺题名/front matter；按许可仅核对同目录 `source.tar.gz!bare_jrnl.tex`，其 `\title{}` 与派遣题名逐字一致（`source.tar.gz!bare_jrnl.tex:L453`），作者行见 `L470`，JLT 页眉目标见 `L498`。metadata 同时说明来源为 arXiv LaTeX、质量 good，但题名检查不可验证（`metadata.json:L6-L15`）。
- **PASS 理由**：canonical 哈希、字节数、DOI、归档内题名四项一致。**限制**：本地转换件没有最终出版 front matter、页码和参考文献表；发表年份/期刊按派遣 DOI 书目信息，并由 TeX 的 JLT journal 模板线索旁证，不把模板中的 `Vol. xx/2019` 占位符当正式出版数据。

## 1. 十六项全文提取

### 1–5. 书目信息

1. **DOI / 来源**：`10.1109/JLT.2020.3003561`；本地来源为 arXiv `1911.11851` 的 LaTeX 转换件（`metadata.json:L3-L10`）。
2. **canonical 源路径**：`D:\code\study\research-protocol\papers\doi\10.1109_jlt.2020.3003561\content.md`；本报告未读取 worktree 内任何同 DOI 副本或旧 read-note。
3. **发表状态**：正式期刊论文（已有 IEEE DOI）；但本地归档是作者 LaTeX/预印本形态，不是带最终卷期页码的 publisher PDF。
4. **发表渠道**：IEEE *Journal of Lightwave Technology*（JLT）；归档 TeX 使用 `IEEEtran[journal]`，并以 JLT 为页眉目标（`source.tar.gz!bare_jrnl.tex:L52,L498`）。
5. **年份 / 期刊**：2020 / *Journal of Lightwave Technology*。年份来自派遣 DOI 书目信息；正文转换件自身未保留最终出版年。

### 6. 核心贡献

论文首先把 35 层 split-step 湍流传播、12 阶径向 Zernike AO 闭环与相干接收连成端到端链路，产生相关的耦合效率和传播相位噪声 2 s 时序，用于替代只依赖统计分布的地面接收机评价（`content.md:L35-L57,L64-L84`）。

其次，它提出并参数化一个确定性数字载波同步链：数字 AGC 把平均输入功率稳定到 DPLL 设计假定的单位增益，二阶 DPLL 捕获 100 MHz 残余频偏并跟踪相位；论文在 AWGN 理论界、真实湍流幅度起伏与传播相位噪声下分别验证锁定、相位误差和 BER（`content.md:L113-L144,L159-L199`）。

### 7. 方法概述

卫星端差分编码 BPSK，经 1550 nm LEO 下行和大气湍流后，由地面 AO 改善入射场与 LO 的空间匹配；intradyne I/Q 采样后，数字 AGC、DPLL、BPSK 判决和差分解码依次处理（`content.md:L29-L31,L107-L121`）。DPLL 使用 BPSK 的低 SNR 近似相位鉴别器、二阶环路滤波器和一阶 NCO，并从阻尼系数、归一化环路带宽和自然频率反解环路增益（`content.md:L131-L156`）。这是一条确定性通信 DSP/控制链，不含 DRL、监督学习或可训练网络。

### 8. 实验设置

- **场景**：LEO-to-ground，仰角 20°，接收口径 50 cm，卫星横向速度 6.5 km/s，1550 nm（Table 1，`content.md:L37-L52`）。
- **湍流**：Hufnagel–Valley/ITU-R P.1621-1 型 `C_n^2(h)`，Bufton 风场，`C_0=10^-13 m^-2/3`、`v_RMS=20 m/s`、`v_G=10 m/s`、`v_T=20 m/s`、`r_0=0.039 m`、`L_0=5 m`、闪烁指数 0.684（`content.md:L35-L55`）。
- **传播/AO**：TURANDOT，35 层离散相屏与 Fresnel split-step；AO 校正至 Zernike mode 91（12 个径向阶），5 kHz、2-frame delay，忽略 WFS 噪声（`content.md:L55-L57`）。
- **信号**：差分编码 BPSK，10 Gb/s / 10 Gbaud，符号率采样，理想定时恢复；LO 功率高于信号功率，主噪声建模为 AWGN shot noise（`content.md:L29,L95,L105-L111,L143`）。
- **频偏**：总 Doppler 参考范围约 ±4.5 GHz，但假定 coarse stage 已预补偿；DPLL 只处理最大恒定残余 100 MHz（`content.md:L17,L105`）。
- **时序/扫描**：同一组 2 s AO 后耦合效率与相位噪声时序用于端到端性能；对平均 SNR 扫描，锁定后统计相位误差/BER（`content.md:L82,L166,L172,L189,L199`）。随机种子、独立 realization 数和每个 SNR 点 bit 数未报告。

### 9. Baseline / 对照逐项归类

| 对照 | 性质 | 自实现 / 引用 / 无 | 用途与证据 |
|---|---|---|---|
| 无 AO vs 12-radial-order AO | 同一传播器条件对照 | 自行仿真 | 平均耦合损失由 -23 dB 改善至 -4.5 dB（`content.md:L84-L92`） |
| DPLL 相位方差 vs CRB | 理论下界 | 引用 Gardner | AWGN 稳态 sanity check（`content.md:L165-L168`） |
| DPLL 相位方差 vs BPSK squaring-loss bound | 理论近似 | 引用 Simon/Gardner | SNR 扫描验证设计（`content.md:L165-L168`） |
| `Δf=100 MHz` vs `Δf=0` | 同一接收机消融 | 自行仿真 | 检查频偏补偿是否引入 BER penalty（`content.md:L199-L201`） |
| 有/无传播相位噪声 | 同一接收机消融 | 自行仿真 | 检查 AO 后 piston-like phase noise 的影响（`content.md:L189-L195`） |
| 理想同步差分 BPSK/AWGN BER | 理论参考 | 引用/标准公式；非另一实现 | 量化湍流 fading 的 2.3 dB penalty（`content.md:L199-L201`） |
| FFT+Mth-power / analog OPLL / 其他 carrier recovery | 相关工作 | **未实现、未对比** | 仅 Introduction 讨论（`content.md:L15-L17`） |

因此：论文没有“多个载波恢复算法公平调参”的算法 baseline；主要证据来自理论界、理想条件和组件开关对照。

### 10. 关键结论

- AO 将平均 flux penalty 从 -23 dB 降至 -4.5 dB，但仍保留慢幅度起伏；传播相位噪声相干时间约 1 ms，远慢于 10 Gbaud（`content.md:L84-L97`）。
- 无湍流时，100 MHz 初始频偏在 8 dB SNR 下约 1.4 ms 锁定，与 pull-in-time 公式一致；约 -9 dB 以下 DPLL 失锁（`content.md:L161-L168`）。
- 加入 AO 后残余幅度起伏，100 MHz/8 dB 下仍约 1.4 ms 捕获；8 dB 以上相位误差方差贴近理论界，但 fading 使最低稳定 SNR 门槛上移约 5 dB（`content.md:L183-L191`）。
- 加入模拟传播相位噪声后，相位误差变化可忽略（`content.md:L193-L195`）。
- 在该 2 s 时序上，100 MHz 相对理想同步不增加 BER；但 turbulence fading 相对理想差分 BPSK/AWGN 在 BER=`10^-4` 造成 2.3 dB 功率 penalty（`content.md:L197-L205`）。

### 11. 与 RML-FSTS 的关系

- **FACT / source-domain**：本文解决的是 AO 后 LEO-to-ground 相干 BPSK 的幅度衰落、传播相位噪声与残余 Doppler 下，AGC+DPLL 是否能捕获/跟踪的问题（`content.md:L17,L170-L205`）。
- **FACT / role**：可作为 C4 space-ground transfer physics，提供 target 场景的幅相时标、AO 残余、Doppler 分层处理和稳定门槛证据。
- **INFERENCE / transfer**：其结果提示空间下行中慢 fading 会通过信号幅度依赖的相位鉴别增益抬高失锁门槛，AGC 是进入固定增益 DPLL 前的接口条件；这是迁移设计的物理约束，不是 FSTS 方法证据。
- **UNKNOWN / target-FSO**：本文不研究多 lag 排序、conditioned-single-lag、lag ranking crossover 或 RML-FSTS；这些 target 命题仍为 INFERENCE/UNKNOWN。本文不能证明 target defect、novelty 或 Go，也不是 coherent-FSO FSTS 直接竞品。

### 12. 实现关键细节

| 模块 | 公式 / 数值 | 证据 |
|---|---|---|
| 接收场 | `E_RX=A_TX exp(χ+jφ_res)`，`φ_res=φ_tur-φ_AO` | `content.md:L64-L67` |
| LO/耦合 | Gaussian LO，`w_0=D/2.2`；`C(t)=∫_P E_LO*E_RX dr`，`ρ=|C|²`，`φ=arg C` | `content.md:L66-L78` |
| I/Q 输入 | `s_I∝√ρ cos(ΔωkT+φ_m+φ)`，`s_Q∝√ρ sin(...)`；`φ_m∈{0,π}` | `content.md:L107-L111` |
| AGC | `e=|s_agc|²-P_ref`，`P_ref=1`，`G_0=0.1`，`g=exp(-v/2)`，NCO=`1/(z-1)` | `content.md:L123-L129` |
| 相位鉴别器 | MAP：`ε=s_Q tanh(s_I)`；低 SNR 近似 `ε=s_Is_Q`；无噪声响应 `ε=(K_d/2)sin(2φ)` | `content.md:L131-L138` |
| 环路 | `F(z)=K_1(1+K_2/(z-1))`；NCO=`K_0/(z-1)`，`K_0=1` | `content.md:L140` |
| 参数映射 | `B_LT=(K+K_2)/4`，`ξ=0.5√(K/K_2)`，`ω_nT=√(KK_2)`，`K=K_dK_1K_0` | `content.md:L142-L143` |
| 捕获时间 | `T_p=2Δω²/(ξω_n³)`；目标 `Δf=100 MHz` | `content.md:L143-L144` |
| DPLL 参数 | `T=0.1 ns`，`ξ=1/√2`，`B_L=5 MHz`，`B_LT=0.0005`，`ω_n=9.3 MHz`，`K_1=1.3×10^-3`，`K_2=6.7×10^-4`，loop 10 GHz | `content.md:L143-L156` |
| 方差基准 | `σ_CRB²=B_LT/(E_s/N_0)`；BPSK 界为其乘以 `2γ/(2γ+1)` | `content.md:L165-L166` |

### 13. 适配 / 不适配 / 未来原料启示

- **适配**：作为 C4，可复用端到端耦合变量 `ρ(t),φ(t)`、AO 后参数时标、AGC↔DPLL 增益契约、coarse CFO 与 residual CFO 分层，以及稳定门槛/BER 的评价组织。
- **不适配**：BPSK 专用相位鉴别器、符号率单采样、恒定 100 MHz residual CFO、理想 timing recovery、单一固定湍流工况，不能直接代表 target-FSO 的 lag 候选集合、时变 lag 排序或更高阶调制。
- **未来原料（非设计结论）**：可将 `ρ(t)` 视为改变估计器有效增益/可靠度的 condition，将相位噪声相干时间与符号时间的强时标分离作为 lag 设计需检查的约束；但是否产生 lag-ranking crossover 必须由 target 数据/模型另证。

### 14. 开源代码

未报告公共代码仓库或下载链接。论文说明 TURANDOT 是 ONERA 与 CNES 合作开发的端到端传播代码（`content.md:L55`），但未声明开放源代码；因此 **code availability = UNKNOWN / 未报告**，不得写成已开源。

### 15. 身份 / 全文验证

- identity：DOI 与 metadata 一致；归档 TeX 题名与派遣逐字一致；作者为 Laurie Paillier 等（`metadata.json:L3-L6`; `source.tar.gz!bare_jrnl.tex:L453,L470`）。
- integrity：canonical SHA256/bytes 与派遣完全一致；正文从 Introduction 到 Conclusion、Acknowledgment 与作者简介连续（`content.md:L7-L243`）。
- completeness caveat：转换件缺题名、摘要、最终卷期页码和参考文献表；因此是“主文内容足够完整”，不是“publisher 版式/书目信息完整”。

### 16. FACT / INFERENCE / UNKNOWN 总表

| 域 | 等级 | 声称 | 是否可承重 |
|---|---|---|---|
| source-domain | FACT | 指定 AO+AGC+DPLL 在该单一代表性 LEO 场景中捕获 100 MHz，8 dB 以上相位方差接近理论界 | 可，限本文参数与 2 s 模拟时序（`content.md:L183-L191`） |
| source-domain | FACT | fading 抬高最低稳定 SNR 约 5 dB；BER=`10^-4` 时造成 2.3 dB penalty | 可，限本文对照（`content.md:L189-L199`） |
| source-domain | FACT | AO 后传播 phase noise 在本文配置中影响可忽略 | 可，不能外推所有 turbulence/AO（`content.md:L193-L195`） |
| target-FSO | INFERENCE | 幅度 condition 可能改变固定增益估计器的可靠度/稳定性 | 仅作迁移假设，需 target 验证 |
| target-FSO | UNKNOWN | lag-ranking crossover 是否存在 | 不可；本文无 lag 排名实验 |
| target-FSO | UNKNOWN | conditioned-single-lag 是否失败 | 不可；本文无该方法/对照 |
| target-FSO | UNKNOWN | RML-FSTS 是否新颖、是否 Go | 不可；本文仅 C4 transfer physics |

## 2. 七个强制子表

### A. 真实信号输入

| 输入 | 形式 / 维度 | 真实性与来源 |
|---|---|---|
| BPSK 数据 | 差分编码 bit；`φ_m(k)∈{0,π}` | 链路系统输入（`content.md:L29,L109`） |
| AO 后耦合效率 | `ρ(k)=|C(k)|²`，2 s correlated series | 35-layer TURANDOT + AO 端到端模拟（`content.md:L55-L82`） |
| AO 后传播相位 | `φ(k)=arg C(k)`，约 1 ms coherence | 同一传播/AO 模拟（`content.md:L76-L97`） |
| residual CFO | 最大恒定 100 MHz；总约 9 GHz Doppler 被 coarse stage 大部预补偿 | 文献量级 + 本文设定（`content.md:L105`） |
| 噪声 | LO-dominant shot noise，AWGN | 建模假设（`content.md:L109`） |
| 数字 I/Q | `s_I,s_Q`，symbol-rate samples | coherent intradyne 后输入（`content.md:L107-L115`） |

### B. 真实估计器 / 控制输出（非 action space）

| 输出 | 产生模块 | 作用 |
|---|---|---|
| AGC 控制量 `v(k)` 与增益 `g(k)` | 功率误差 + 一阶 NCO | 把输出功率拉到 `P_ref=1`（`content.md:L125-L129`） |
| 相位误差 `ε(k)` | BPSK phase detector | 驱动环路；幅度通过 `K_d` 影响鉴别增益（`content.md:L137-L138`） |
| 载波相位/频率校正 | loop filter + NCO | 捕获 residual CFO、跟踪相位（`content.md:L133-L140`） |
| 判决 bits | BPSK detector + differential decoder | 消除 PSK rotational ambiguity 后恢复数据（`content.md:L121,L197-L199`） |

以上是确定性估计量/控制信号，**不是学习型 action space**。

### C. 奖励与真实目标 / 评价量

| 项 | 定义 |
|---|---|
| Reward | **N/A**：非学习型方法，无 reward、policy 或 optimizer |
| 控制目标 | 最小化接收载波与 LO 的 residual phase error，并稳定捕获 frequency offset（`content.md:L133`） |
| 锁定指标 | pull-in time `T_p=2Δω²/(ξω_n³)`；100 MHz 目标实测/预测约 1.4 ms（`content.md:L143-L144,L161`） |
| 估计指标 | steady-state phase-error variance，与 CRB/BPSK squaring-loss bound 对照（`content.md:L165-L168`） |
| 通信指标 | BER vs average `E_s/N_0`；报告 BER=`10^-4` 的 2.3 dB turbulence penalty（`content.md:L197-L201`） |
| 稳定性指标 | lock/no-lock critical SNR；fading 使门槛上移约 5 dB（`content.md:L166,L189`） |

### D. 假设、位置与迁移影响

| 假设 | 位置 | 对 target-FSO 迁移影响 |
|---|---|---|
| 大部分 ±4.5 GHz Doppler 已由 ephemeris/coarse estimator 预补偿 | `content.md:L17,L105` | 只覆盖 residual synchronization；不能宣称全频偏 acquisition |
| 最大 residual CFO 为恒定 100 MHz | `content.md:L105` | 未覆盖 pass 内 CFO slope/jerk；target 若时变需另证 |
| 10 Gbaud、symbol-rate sampling、ideal timing recovery | `content.md:L95,L109,L143,L205` | 排除了 timing–carrier 交互和 oversampling 信息 |
| LO power 大，shot noise 为主且建模 AWGN | `content.md:L109` | 未覆盖背景光、器件噪声、混合噪声主导区 |
| `ρ,φ` 在单个 symbol 内恒定 | `content.md:L111` | 依赖 turbulence 与 symbol-rate 的强时标分离 |
| WFS noise 可忽略（高 flux） | `content.md:L57` | 低 flux AO sensing 场景不可直接迁移 |
| 发射激光/booster 相位噪声不讨论 | `content.md:L29` | source laser linewidth 与 atmospheric phase 的耦合未知 |
| DPLL 设计假设 `K_d=1`，由 AGC 强化 | `content.md:L144,L176` | AGC tracking error 是稳定性的接口风险 |
| 单一 20° elevation、固定强 turbulence 参数 | `content.md:L35-L55` | 不支持跨仰角、跨站点、跨季节泛化 |

### E. 网络 / DSP 链、参数与复杂度

| 项 | 内容 |
|---|---|
| Neural network | **N/A**：无神经网络、训练或 learned parameter |
| DSP 链 | ADC I/Q → digital AGC → BPSK DPLL → symbol detector → differential decoder（`content.md:L31,L113-L121`） |
| AO 链 | WFS → RTC → DM，5 kHz、2-frame delay、Zernike 至 mode 91（`content.md:L31,L57`） |
| AGC complexity | 每 symbol：功率、误差、常数增益、integrator、指数 gain；论文未给 operation count |
| DPLL complexity | 每 symbol：I/Q 乘法型 detector、二阶 filter、integrator、complex phase correction；10 GHz loop rate（`content.md:L137-L154`） |
| 传播复杂度 | 35 phase screens 的 Fresnel split-step + AO 仿真；时间/内存未报告（`content.md:L55`） |
| 实时性证据 | 仅 loop rate 与 lock time；无硬件资源、latency、功耗或 wall-clock benchmark |

### F. 适配性

| 维度 | 判定 | 理由 |
|---|---|---|
| C4 space-ground transfer physics | **适配** | 端到端 AO 后 `ρ(t),φ(t)`、Doppler residual、fading-induced stability shift 均直接相关 |
| coherent receiver DSP contract | **部分适配** | AGC↔DPLL 增益契约可复用；但 BPSK/单采样/理想 timing 边界很窄 |
| target lag failure evidence | **不适配** | 无 lag 候选、排名、conditioning 或 crossover 实验 |
| target method competitor | **不适配** | 是确定性 AGC+DPLL，不是 FSTS/RML-FSTS 或学习估计器 |
| novelty / Go evidence | **不适配** | 没有 target M-C-A 或近期 FSTS baseline 对比 |
| 写作架构标杆 | **适配** | 系统模型→算法→理想 sanity check→真实扰动→BER 的证据递进清晰 |

### G. 本文自身 M/C/A 与 canonical 四判据

| 项 | 本文定位 |
|---|---|
| M | 数字 AGC + 二阶 BPSK DPLL 的 closed-loop carrier synchronization |
| C | 10 Gb/s/10 Gbaud BPSK LEO-to-ground coherent FSO；AO 后 amplitude fading、turbulent phase noise 与 100 MHz residual CFO |
| A | 既有 ground-space coherent studies 多用统计 turbulence model，或未专门刻画 carrier synchronization；analog OPLL 研究又未纳入 turbulence-induced random amplitude fluctuations（`content.md:L13-L17`） |
| A 定位 | **source-domain 的 characterization/robustness 缺口**；不是 target lag-ranking defect |
| 方法产出形态 | 可实现的确定性 DSP block diagram、环路公式与参数；加端到端 simulation evidence |

| canonical 判据 | ✅/❌ | 理由 |
|---|---:|---|
| 具体 M-C-A | ✅ | M、C、A 均具体且论文逐层回应 |
| 可复用方法产出 | ✅ | AGC/DPLL 架构、公式、参数表和接口假设齐全 |
| 近期 baseline | ❌ | 没有实现/公平调参的 contemporaneous carrier-recovery competitor；只有理论界、理想同步与组件开关 |
| 可量化对标 | ✅ | lock time、phase variance、critical SNR、BER/power penalty 均量化 |

**本文自身 canonical 总判定：3/4，因近期算法 baseline 缺失而非全通过。** 即使本文自身问题有较强证据，也不等于 target Q、novelty 或 Go 成立。

## 3. 通信参数表

| 类别 | 全值 | 来源 |
|---|---|---|
| 链路 / 场景 | LEO-to-ground coherent optical downlink；elevation 20°；satellite transverse velocity 6.5 km/s；Rx aperture 50 cm | `content.md:L29-L35`, Table 1 `L37-L52` |
| 波长 | 1550 nm | Table 1 `content.md:L37-L52` |
| 调制 | differentially encoded BPSK；coherent intradyne detection + differential decoding | `content.md:L29-L31,L197-L199` |
| 比特率 / 符号率 | 10 Gb/s / 10 Gbaud | `content.md:L95,L143,L205` |
| 采样率 | symbol-rate；`T=0.1 ns`，DPLL loop 10 GHz | `content.md:L109,L146-L156` |
| training / frame | training **N/A**；frame length **未报告**；传播/AO performance series 2 s，AGC illustration 10 ms | `content.md:L82,L178-L180` |
| CFO | 总 Doppler 约 -4.5…+4.5 GHz（引用）；coarse precomp 假定；residual constant CFO 最大 100 MHz | `content.md:L105` |
| 相位噪声 | atmospheric phase `φ=arg C`；coherence time ~1 ms；laser phase noise不讨论；line width 未报告 | `content.md:L76-L78,L95,L29` |
| 接收功率 / SNR | 绝对接收功率未报告；AO 后平均 flux penalty -4.5 dB（无 AO -23 dB）；SNR sweep，8 dB 关键点，30 dB 仅 AGC 图示 | `content.md:L57,L84,L163,L180,L185-L191` |
| turbulence | Hufnagel–Valley/ITU-R；`C_0=10^-13 m^-2/3`，`v_RMS=20 m/s`，`v_G=10 m/s`，`v_T=20 m/s`，`r_0=0.039 m`，`L_0=5 m`，`σ_I²=0.684` | `content.md:L35-L52` |
| spatial diversity | 未报告；单接收 aperture / 单 coherent branch | 全文系统架构 `content.md:L25-L31` |
| AO | Zernike to mode 91 / 12 radial orders；5 kHz；2-frame delay；WFS noise neglected | `content.md:L57` |
| channel / propagation | 35-layer TURANDOT Fresnel split-step；top-of-atmosphere plane wave；2 s correlated `ρ,φ` | `content.md:L55-L82` |
| AGC | `P_ref=1`，`G_0=0.1`，exponential gain | `content.md:L125-L129,L176` |
| DPLL | `ξ=1/√2`，`B_L=5 MHz`，`B_LT=0.0005`，`ω_n=9.3 MHz`，`K_1=1.3e-3`，`K_2=6.7e-4` | `content.md:L142-L156` |
| 关键输出 | 100 MHz lock ~1.4 ms；no-turbulence lock threshold ~-9 dB；fading threshold +~5 dB；BER 1e-4 penalty 2.3 dB | `content.md:L161-L166,L189,L199` |

## 4. 实验完备性审查（≤20 行）

| 项 | 审查 |
|---|---|
| Claims + scope | 明确限 10 Gb/s BPSK、代表性 LEO 下行、AO 后 2 s 时序；结论却偶有“robust/simple”概括，外推需谨慎。 |
| Seeds / 次数 | 未报告 seed、独立 turbulence realizations 或 Monte Carlo 次数。 |
| Error bar / 统计检验 | 无 confidence interval、error bar 或显著性检验。 |
| Baseline 数量 | 0 个竞争载波恢复实现；3 类理论/理想参照 + 3 类条件开关对照。 |
| Baseline 类型/来源 | CRB、BPSK squaring-loss、理想 AWGN BER 来自经典理论；with/without AO/CFO/phase-noise 为自仿真。 |
| 公平调参 | 不适用竞争算法；DPLL 仅单组设计参数，无与替代算法的统一预算。 |
| 消融 | 有 AGC 输入/输出、AO 开关、CFO 开关、phase-noise 开关；无 DPLL 组件/参数消融。 |
| 参数扫描 | 扫 average SNR；未扫 elevation、`C_n²`、AO order/rate、CFO、laser linewidth、loop bandwidth。 |
| 信道/参数来源 | turbulence 取 literature/ITU-R，AO inspired by Vedrenne；关键值有表，但只一工况。 |
| 场景多样性 | 单 elevation、单 aperture、单 modulation、单 2 s realization，泛化证据弱。 |
| 复杂度 | 无 operation count、runtime、memory、hardware latency/power。 |
| Verification | **2/3**：理论界与端到端物理模拟相互校验，但无公开代码且最终参考表/bit-count 不完整。 |
| Validation | **2/3**：物理传播、AO 与接收环路构成端到端链，但仅单一 20° LEO-to-ground、BPSK、2 s 工况，无外场验证。 |
| Uncertainty | **1/3**：单 realization，未报告 seed、独立时序数、error bar、置信区间或统计检验。 |

## 5. 写作架构标杆提取

### 5.1 三级标题与篇幅

- 一级叙事：Introduction → Modeling of a coherent LEO-to-ground link → Coherent detection and baseband DSP design → System performance with AO → Conclusion（`content.md:L7,L21,L99,L170,L203`）。
- 二级结构：System Modeling 下 3 节（overall architecture / channel modeling / coupling impact）；DSP 下 5 节（I/Q model / receiver architecture / AGC / DPLL / no-turbulence characterization）；Performance 下 4 节（AGC / CFO / turbulent phase noise / BER）。
- 三级标题：转换正文没有显式 `###`；三级组织由段落内“定义→公式→参数→图表解释”承担。对于需要更强导航的 RML-FSTS，不宜机械复制其无三级标题做法。
- 依据确定性词数统计（主干 6,277 words）：Introduction 820（13.1%）；Modeling 1,748（27.8%）；DSP 2,387（38.0%）；Performance 920（14.7%）；Conclusion 402（6.4%）。方法/模型合计 65.8%，符合工程期刊重可复现机制的写法。

### 5.2 System Model / Problem / Algorithm 组织

- **Problem** 不单独开章：Introduction 先从 coherent space link → Doppler → atmosphere/AO residual → prior carrier-sync omissions 收窄，最后提出“真实 turbulence 下 phase locking feasibility”及本文方案（`content.md:L9-L19`）。
- **System model** 从光学端到端物理图开始，再把 turbulence 参数、传播器、AO、场耦合压成 DSP 可消费的 `ρ(t),φ(t)`；这是跨层接口最值得借鉴的部分（`content.md:L25-L82`）。
- **Algorithm** 先写接收 I/Q 数学形式，再总体 block diagram，再分别展开 AGC/DPLL；先在 AWGN constant-amplitude 下 sanity check，最后进入真实扰动（`content.md:L99-L172`）。
- Problem 与 Algorithm 的连接变量非常明确：amplitude-dependent detector gain `K_d` 由 AGC 稳定，residual phase/frequency 由 DPLL 控制（`content.md:L137-L144,L176`）。

### 5.3 参数、符号与公式呈现

- 先给物理符号：`C_n², r_0, σ_I², L_0`，统一放 Table 1；再给场 `E_RX,E_LO`、重叠积分 `C(t)`，最终压缩成 `ρ,φ`。
- DSP 章先定义 `Δf,Δω,T,φ_m` 和 I/Q，再引入 AGC/DPLL 内部量；DPLL 由 block-level formula 转到 physical design variables `ξ,B_L,ω_n`，最终放 Table 2。
- 公式引入模式：物理意义句 → 公式 → 变量解释 → 下游用途；关键公式均编号/label，正文回指 Eq. 并用于数值预测（尤其 `T_p≈1.4 ms`）。
- 推导深度适中：完整写系统输入输出和环路参数映射，不展开经典 PLL/CRB 的基础证明，而以 Gardner/Simon 承接。

### 5.4 图表类型、数量与 caption 模式

- **15 幅 Figure、2 张 Table**。图型序列：2 个系统架构图；1 个四联幅相场图；耦合 time series；CDF/PDF；phase-noise time series；receiver/AGC/DPLL 三个 block diagram；2 个 acquisition traces；2 个 phase-error-vs-SNR 曲线；AGC input/output trace；BER-vs-SNR。
- Caption 多采用“对象 + 条件 + 比较维度”：例如 duration、AO order/rate、SNR、with/without turbulence。优点是脱离正文仍能判断横向对照；不足是部分 caption 没写样本数/重复次数。
- Table 1 专放 channel/physics，Table 2 专放 DPLL design；没有把结果数字塞进大表，结果主要由曲线承载。

### 5.5 Baseline、消融、指标与复杂度组织

- Baseline 不是集中一节：理论界直接贴在相应结果图旁；ideal/switch-off conditions 作为同图曲线。结构紧凑，但竞争格局弱。
- 消融顺序遵循因果链：先看 AO 对 coupling，再看 AGC 对 amplitude，再看 CFO acquisition，再单独打开 turbulent phase noise，最后看 BER。
- 指标由内到外：loop lock time → phase-error variance → stability threshold → BER/power penalty，形成 control metric 到 communication metric 的闭环。
- 复杂度只由结构和运行率隐含；没有独立 complexity subsection 或 operation/hardware 表。此点不宜作为写作标杆照搬。

### 5.6 Introduction 与 Conclusion 叙述链

- Introduction：coherent optical value → space-link precedent → Doppler/OPLL → atmosphere/AO residual → prior work缺口 → AGC+DPLL 方案/边界 → section roadmap（`content.md:L9-L19`）。
- Conclusion：重述场景与模型 → 汇总 AO、捕获时间、BER、phase-noise 结论 → 给出方法定位 → 明示三项边界/未来工作：open-loop algorithms、higher-order modulation、non-ideal timing recovery（`content.md:L203-L205`）。
- 可借鉴点：结论不引入新指标；每个未来方向都从正文明确假设退出，而非泛泛列愿望。

### 5.7 共同基础引用候选（只列、不检索）

因任务禁止读取其他 GW notes，本报告无法确认“本 GW 是否已覆盖”，以下仅列本文中明显承担基础公式/模型的候选，覆盖状态均为 **UNKNOWN**：Gardner (2005, PLL design/CRB)、Simon (2006, carrier synchronization/BPSK squaring loss)、Simon (1979, low-SNR detector)、Roddier (1999, AO)、Noll (1976, Zernike modes)、Winick (1986, coherent overlap coupling)、Shaklan (1988, Gaussian mode coupling)、Vedrenne et al. (2012/2016, TURANDOT/AO design)、ITU-R P.1621-1 / Hufnagel–Valley turbulence、Shoji et al. (2012, Doppler/OPLL)、Belmonte (2009/2016, coherent ground-space channel)、Valencia (2015) 与 Conroy (2018, FSO coherent DSP)。未检索、未核实题名，也不据此新增主张。

## 6. Step 3 边界结论

本文在本 GW 中应固定为 **C4 space-ground transfer physics + 写作架构标杆**。它能承重的只有：AO 后耦合/相位时序如何进入相干 DSP、AGC 与 DPLL 的接口假设、fading 对 lock threshold/BER 的影响，以及从物理模型到通信指标的写作组织。它**不能**承重 target-FSO 的 conditioned-single-lag failure、lag-ranking crossover、RML-FSTS novelty 或 Go；这些结论保持 **INFERENCE/UNKNOWN**。本报告不设计 RML-FSTS，也未进入 Step 3.5/4a。
