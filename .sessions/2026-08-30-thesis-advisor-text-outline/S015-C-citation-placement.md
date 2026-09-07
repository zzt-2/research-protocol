# [S015] C 落位批——参考文献落位 96 处、引用 34→137、TODO 清零

> 2026-09-07 | EXECUTE（加密期 C 批，PROMPT-020）| 状态：确定性复查全 PASS，停机待用户抽查 + 待拍板 6 项

## 目标

按 bib-phaseC-落位任务报告 §1—§6 + ledger 执行文献落位：46 处 TODO 换核实键 + 候选池补挂至目标数量（170–180 总量 / Ch1 130+ / 方法章 20–30），一句话内插入 [@key] 零文字改动，references.bib 不动。

## 记录

- 报到：topic-index / S014 / D037—D041 / voice；执行依据 = bib-phaseC 落位报告 §1—§6 + ledger（L001—L004、D1—D6、bib-candidates-R1、xia-benchmark-citations）；基线 = Ch1 30 / Ch2 8 / Ch3 10 / Ch4 2 实键 + 46 TODO。
- 候选池纪律裁剪：核实:未 全禁用 → 可用池 = 104 d1–d6 + 25 老库 REPAIRED = 129，**理论上限 163 < 目标 170–180**（缺口结构性，落位前已明确并登记）；1.1 无工程进展支线锚句 → 16 条 d1 键无处置（登记）。
- 对号：46 TODO → 谱系最近邻候选（D 文件主题标签 + 老库 79 映射交叉 REPAIRED 过滤）；近似对号 5 处显式登记（johst2024 / torbatian2022 / d4-xie2010pdl / d4-yi2014stokespdl / d4-kaneda2009）。
- 纪律门控（写前）：103 白名单键逐一对照 ledger 状态 = 全 Crossref/REPAIRED；DOI 查重发现两组同文双键（esa-ogs-ao≡berkefeld2010、lcrd-initial-operations≡israel2024lcrd-char），各只引其一。
- 落位（.verify-c/place_c.py，96 条替换 count==1 断言全过）：Ch1 56 / Ch2 14 / Ch3 9 / Ch4 17；改前 .bak-C 四份备份。
- 确定性复查（V028 全 PASS）：TODO=0；137 键全在库；+103 白名单内、老键零丢失；标题/\tag/表题注/图引/式引全同；**剥离 [@…] 后新旧正文逐字相同（零文字改动）**；CRLF 完好。
- 台账：ledger 103 行 candidate/keep→cited + 主题标签补齐 + Phase C 节 + 统计快照；L005（主仓）+ 扩容日志-C（章节稿，TODO→键全映射表）。
- 裁量：1.1 冻结区例外（插入 10 处引用标记、零文字改动、.bak-C 可一键回退）；aperture-averaging 无专文候选 → 挂 d3-lee2004（分集框架含孔径平均）；kalman-impl 挂老键 sun2020（平方根 UKF 完美贴合）；oezbilgin2025（PLL 湍流 TCOM）核实:未 禁用不引。

## 决策引用

- D042：新建（C 批落位裁量与缺口登记）
- D037：既定四批编排；落位报告 §1 纪律为唯一执行依据

## 范围确认

- 本轮是否在 scope boundary 内：是（D037 C 批既定任务；改动 = 四章 [@…] 插入 + 台账/日志；references.bib 与 Ch5/Ch6 零触碰；1.1 冻结区为例外登记）

## 后续

- 用户抽查：建议抽样 = 1.1 工程进展段（10 处新挂）、1.2.2 升幂/BPS 段（TODO 换键密集区）、Ch4 4.3 两个近似对号位、Ch2 2.3.1 分块 fading 两处。
- 待拍板 6 项见 L005 §六 / 扩容日志-C §四（首要 = 总量 137 vs 170–180 缺口处置：二次核实批 / 接受 / 增写 1.1）。
- 队列：F3 图批解锁（本批与其串行约束解除）→ P4' 组装重转（references.bib→main.bib 同步 137 键）。
