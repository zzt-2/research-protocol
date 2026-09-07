# 扩容日志-C —— 参考文献落位批（Phase C）

> 2026-09-07 | EXECUTE（加密期 C 批）| 状态：确定性复查全 PASS，停机待用户抽查引用 + 待拍板 6 项
> 执行依据：bib-phaseC-落位任务报告.md §1—§6 + bib-logs/ledger.md（主仓）；文献批视角日志 = bib-logs/L005。

## 一、结果

- **46 处 [@TODO-主题] 全部换为核实键 + 50 处既有句内补挂，共 96 处插入**；全稿引用 34→**137** 唯一键（Ch1 122 / Ch2 24 / Ch3 20 / Ch4 20 / Ch5 0 / Ch6 0）。
- 零文字改动：剥离 [@…] 后新旧正文逐字相同（脚本级证明）；标题/\tag/表题注/图引/式引计数全同；CRLF 完好；备份 .bak-C 四份。
- 纪律：仅用 ledger 核实:Crossref/REPAIRED 键（103 新键逐一过纪律门控）；核实:未 禁用；老 34 键零改动；references.bib 未动。

## 二、TODO→键映射表（46 处）

### 01-绪论.md（31 处）

| TODO | 位置（节） | 落键 |
|---|---|---|
| turb-modeling | 1.2.1 建模谱系 | d3-jakeman1978; d3-phillips1982; d3-andrews1999; d3-andrews2001 |
| turb-corrtime | 1.2.1 空时相关 | d6-garrido2014correlated |
| turb-simulation | 1.2.1 分步仿真/外场 | d6-lane1992phase; d6-schmidt2010numerical（另有 ituR1621 挂"形状参数"分句） |
| ao-correction | 1.2.1 AO 信标/无传感器 | d3-weyrauch2005; selim2026 |
| ao-residual | 1.2.1 AO 残差统计 | stotts2021 |
| diversity-combining | 1.2.1 合并方式 | d3-navidpour2007; d3-tsiftsis2009 |
| aperture-averaging | 1.2.1 孔径平均 | d3-lee2004（谱系最贴候选，无孔径平均专文） |
| mthpower | 1.2.2 升幂主线 | d2-lygagnon2006mth; d2-seimetz2006mth; d2-zhang2016flexible |
| bps | 1.2.2 BPS | d2-fatadin2010qpska; d2-fatadin2014barycenter; d2-bilal2014multistage |
| bps-cycle | 1.2.2 周跳 | d2-borjeson2020cycleslip; melo2018 |
| decision-directed | 1.2.2 判决导向 | d2-kazovsky1985ddpll; d2-norimatsu1995ddpll; d2-mori2009dd; d2-mousapasandi2010ddpe |
| dd-pilot | 1.2.2 导频+判决分阶段 | johst2024（近似对号，登记） |
| kalman-cpr | 1.2.2 Kalman 细化 | d2-pakala2014ekf; d2-pakala2016ekf; d2-jignesh2016ukf |
| kalman-impl | 1.2.2 平方根/定点 | sun2020（老键复引，完美贴合） |
| cfo-cpr-joint | 1.2.2 联合估计 | d2-zhou2013joint; d2-meiyappan2012ml; d2-xie2012dpll |
| cfo-estimation | 1.2.2 频偏估计手段 | wang2024oe |
| doppler-tracking | 1.2.2 星地多普勒 | pech2025 |
| pilot-cpr | 1.2.2 导频插值 | d2-yi2007pilot; d2-shieh2008mlpilot |
| pilot-design | 1.2.2 导频图案权衡 | d2-pajovic2015multipilot; d6-jansen2008pilot |
| cma-variants | 1.2.3 恒模/多模变体 | d4-godard1980（挂"最常用起点"分句）; d4-yang2002mma; d4-dirosa2021rde |
| cma-singularity | 1.2.3 奇异点 | d4-kikuchi2011cma; d4-kaneda2009（kaneda 近似，登记） |
| mimo-equalization | 1.2.3 蝶形/频域 | d4-fludger2008; d5-ziachahabi2011ptl |
| mimo-cpr-order | 1.2.3 EQ/CPR 次序 | torbatian2022（近似对号，登记） |
| pdm-systems | 1.2.3 PDM 系统 | d4-tsukamoto2005 |
| pmd-tracking | 1.2.3 偏振跟踪 | d4-kikuchi2015sop |
| pdm-cond | 1.2.3 条件数 | d4-yi2014stokespdl |
| polarization-turbulence | 1.2.3 湍流×偏振 | d4-arikawa2018pdm |
| realtime-dsp | 1.2.4 平台转换 | d5-bower2011dsp; d5-pfau2006realtime; d5-yoshida2014adaptive |
| verification-hil | 1.2.4 验证途径 | d5-song2022oe |
| fpga-receiver | 1.2.4 FPGA 模块集成 | d5-leven2006fpga; ge2026opll; d5-song2023jlt; d5-dong2026jlt |
| fpga-pipeline | 1.2.4 并行/流水 | d5-zhou2011timing; d5-zhang2025sfd |

### 02-系统与信道模型.md（11 处实例 / 8 主题）

| TODO | 落键 |
|---|---|
| 分块fading（2 处） | d6-garrido2014correlated（空间→时间折算）; d3-andrews2001（块内准不变） |
| gg模型出典（2 处） | d6-andrews2001scint（建模出处）; d3-jakeman1978（强湍流尾部极限） |
| 实时dsp（噪声合并口径） | d6-oliver1965noise; d5-ye2024quant |
| 双偏振mimo（2 处） | d6-jones1941calculus; d6-poole1986pmd; d4-fludger2008（混合来源）; d4-arikawa2018pdm（湍流无差别性） |
| 激光器线宽 | d6-henry1982linewidth |
| 相位噪声模型 | petkovic2022（老键复引） |
| fec参考ber | d6-simon2002fading |
| 16apsk | du2025nda（老键复引） |

### 04-结构约束双偏振解复用.md（4 处）

| TODO | 落键 |
|---|---|
| 短训练序列设计 | d4-zhao2010crs; d4-zhu2013implicit |
| 矩阵扰动分析 | d4-xie2010pdl（近似对号，登记） |
| 谱正则化估计 | d4-yi2014stokespdl（近似对号，登记） |
| 极分解与酉矩阵估计 | roudas2010; d4-tanomura2023unitary |

（Ch3 无 TODO；本批在 Ch3 补挂 9 处既有句：torbatian2022 / d2-zhou2013joint / d6-henry1982linewidth / d6-jansen2008pilot / d2-lygagnon2006mth / d2-seimetz2006mth / d2-fatadin2013differential / d2-fatadin2014sliding / d2-yi2007pilot / d2-zafra2014vv。）

## 三、非 TODO 补挂要点（50 处中代表性位置）

- 1.1（冻结区例外，零文字改动，可一键回退 .bak-C）：tarhouni2025fsoMesh（星座回传）、boroson2026overview（FSO 总览）、israel2024lcrd-char（LCRD）、d1-lct-edrs-alphasat-sentinel + lustica2025edrs-copernicus（EDRS 业务化）、d1-edrs-c; satoh2026lucas-operations; itahashi2025lucas-status（工程化总结句）、d1-tesat-lct-5g6（相干灵敏度→距离）、walsh2022leotracking（数字域补偿）、d5-schaefer2016oe（实时 DSP 实例）。
- 1.2.1：stotts2023（总起）、d3-tyson1996/2002（AO 制约）、xu2025 + mosnier2025fso + elfiky2024 + correia2024（数字基带段）、d3-fried1965/noll1976/berkefeld2010（AO 段）、d3-sandalidis2008/munoz2006/larsson2024/lee2004（分集段）、d3-zhu2002（1.1 湍流句）。
- Ch2/Ch4 既有句补挂 20 处（详见 place_c.py 替换表，.verify-c/ 留档）。

## 四、待拍板项（6 项，详见 L005 §六）

1. 总量 137 vs 170–180 缺口处置（二次核实批 / 接受 / 增写 1.1 解锁 d1×16）——首要。
2. Ch1 122 vs 130+（同上成因）。
3. 近似对号 5 处认可与否（johst2024 / torbatian2022 / d4-xie2010pdl / d4-yi2014stokespdl / d4-kaneda2009）。
4. 1.1 冻结区例外认可与否（本批 1.1 插入 12 新键/9 标记位（6 扩键+3 新标记），V029 实测行号 5/7/15/21；原自报"10 处引用标记"为漏计——第 12 键 d3-zhu2002 原误记于 1.2.1 组；零文字改动经整节剥离比较证实）。
5. petkovic2022 是否替换（本批按指令不动；oezbilgin2025 需先核实）。
6. DOI 同文双键（d1-esa-ogs-ao≡d3-berkefeld2010、d1-lcrd-initial-operations≡israel2024lcrd-char）注释时机。

## 五、队列

C 落位批完成 → **F3 图批解锁**（规划→绘制→回填；表 1.1 与图 1.2 分工随此批）→ P4' 组装重转（references.bib→main.bib 同步 137 键；Ch1 编号迁移；图表合同补登）。
