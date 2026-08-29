# LDPC receiver-visible 接口与公平 comparator（Groundwork Step 1）

> 任务：T041 | 日期：2026-08-30 | 范围：外部 receiver/decoder authority；无实验、无实现
> 检索证据：`search-archive/2026-08-30/t041-ldpc-receiver-authority.json`（150 条元数据；8 必读 / 9 建议读 / 6 待确认 / 52 备选 / 75 排除）

## 一句话结论

Syndrome rescue 只有在项目先暴露“失败码字的完整 hard decision + syndrome + bit reliability”并在相同 message-update / decoder-call 预算下胜过额外迭代、普通 restart、bit-flipping 或 OSD 时，才可能形成 FER 方法；当前 adapter 只返回固定 20 轮后的 hard information bits，因此 C5-2 尚无可执行接口，固定/自适应 NOMS 可作首要 decoder comparator，完整 BICM-ID 只应作为显式计入 demapper–decoder 往返成本的高成本后备。

## 1. State / interface 表

| 状态 | 算法上的标准含义 | 合法 receiver-visible 来源 | 当前 Python adapter 事实 | 当前可用于部署动作？ |
|---|---|---|---|---|
| Channel LLR | demapper 给 decoder 的 bit-channel LLR | 接收样本、星座/标号、噪声或失配参数 | D0 `demap()` 生成 one-shot Gray-16QAM max-log LLR，输入预裁剪 30、decoder 内裁剪 20；符号约定为 positive means bit 1 | **是，但只对当前 16QAM adapter**；目标 `(8,8)-16APSK` 尚未落到该接口 |
| Hard information bits | decoder 对 `k` 个信息位的硬判决 | decoder 输出 | D0 `decode_fresh()` 只返回 `(16,1024)` hard info bits | **是** |
| Standard syndrome | 对完整码字硬判决 `ĉ` 计算 `s = Hĉ mod 2`；零 syndrome 只是 parity-valid，不等于发送真值正确 | decoder 的完整 codeword hard decision + parity-check matrix / rate-matching inverse | D0 不返回完整 hard codeword，也没有 syndrome API。旧 P08 `syndrome_check()` 只接受完整 lifted codeword；其 `encode_full_for_syndrome()` 从已知 info bits 编码，适合 correctness 检查，不能代表失败 decoder 的 syndrome | **否**；用 re-encode 后的合法码字算 syndrome 会恒为零，不能作为 rescue 触发 |
| Posterior LLR | decoder 聚合 channel prior 与校验消息后的 a-posteriori bit LLR | decoder variable-node output | 当前 decoder 配置 `hard_out=True, return_infobits=True, return_state=False`，adapter 丢弃 soft output | **否** |
| Extrinsic LLR | 给外部模块的新增证据；BICM-ID 中必须排除 demapper 已给的 a-priori/channel 信息，避免双计数 | decoder 明确导出的 extrinsic output，或经已核公式从 posterior 与 prior 分离 | 当前 adapter 无 soft output，也无 posterior/prior 分离合同 | **否** |
| 逐轮 message / residual / callback | 每轮或每 layer 的 V2C/C2V 消息、message residual、unsatisfied-check trajectory | decoder 内部显式 callback/state contract | 当前 adapter 明确 `return_state=False`，并拒绝 `message_state`/`warm_state`；Sionna 库级 callback/state 的完整语义未审 | **否；库级能力记 UNKNOWN** |
| 收敛/停止状态 | syndrome-zero、CRC pass、最大迭代、stall 等终止原因 | decoder 显式返回 stop reason | 当前路径固定跑 20 轮；P08 diag 明记 convergence=`N/A`。D0 receipt 的 `bp_iterations=20×codewords` 是配置预算，不是观测到的收敛轮数 | **否** |

当前接口证据指针：

- `projects/simulation/explore/coded-decoder-feedback/codec.py:150-163`：固定 `α=0.75` normalized min-sum，20 轮，hard info bits，`return_state=False`。
- `projects/simulation/explore/coded-decoder-feedback/codec.py:280-330`：fresh decode 仅物化 hard info bits 与配置型 receipt。
- `projects/simulation/explore/nda-awgn-tracking-sandbox/p08_coded_chain.py:150-236`：旧 adapter 的 syndrome correctness helper 与 fixed-iteration hard-out 诊断。

## 2. Method / comparator 表

| 对象 | Deployable input | 动作 | 输出 | 额外计算 | 主 comparator | 等成本廉价替代 | 最可能改善 BER/FER 的机制与 claim ceiling |
|---|---|---|---|---|---|---|---|
| **C5-2 syndrome-guided failed-codeword rescue** | failed codeword 的 full hard decision、nonzero syndrome / unsatisfied checks、bit reliability（通常 `|posterior LLR|` 或受影响 VN 消息）；不得使用 TX bits | 从 unsatisfied checks 与低可靠位构造小候选集，翻转/扰动后再解码或检查 | rescued hard codeword + parity/CRC 状态 + attempts | syndrome 计算、排序/候选生成、每次 retry 的完整 decoder 成本 | tuned fixed NOMS，固定 20 轮；失败帧再给与 rescue 相同的额外 message-update 预算 | 普通 random restart、额外 NOMS 迭代、weighted/gradient bit-flipping；若枚举可靠度候选，OSD 必须进入主比较 | 只有当错误由 trapping set / stall 主导且 syndrome 定位能提高“每次额外尝试”的命中率，才可能改善 FER/error floor。若优势来自更多迭代或更多重启，只能记计算换性能；若被 bit-flipping/OSD 吸收，降为 supporting/engineering |
| **C5-0 residual LLR calibration** | one-shot demapper LLR + receiver-only 噪声/幅度/几何统计；不能读 decoder truth | 对 LLR 做可部署的 scale/bias/clip 或小维度状态条件校准，一次送入 decoder | calibrated channel LLR | 每 bit 常数级；不增加 decoder call | 正确噪声方差的 one-shot demap + tuned fixed NOMS | 单个全局 scalar、per-SNR/offline LUT、LLR clipping、在线噪声方差重估 | 纠正 demapper mismatch 可改善 waterfall BER/FER；必须证明不是 evaluator 对 LLR 尺度敏感，也不是固定 scalar 已完全吸收。它不需要 syndrome/posterior 接口 |
| **Adaptive NOMS / layered or informed scheduling** | decoder 内部 V2C/C2V 消息、iteration/layer index；informed scheduling 还需 message residual | 按迭代/edge/layer 调整 normalization/offset 或 message-update 顺序 | hard bits；最好同时返回 soft output、stop reason | 动态参数、residual 维护、priority queue / layer control | 充分调优的 fixed NMS/OMS；标准 flooding 与 layered schedule | 在相同 edge-update 数下增加 fixed decoder iterations；静态 per-iteration α/β LUT | 可加快有效信息传播、缓解局部 stall；若只减少平均迭代而等更新预算 FER 不变，则是 B/C 级吞吐/能耗收益，不是 FER 方法。当前 adapter 不暴露所需 state，先属接口后备 |
| **完整 BICM-ID（高成本后备）** | equalized APSK samples、channel law/variance、demapper a-priori；decoder 必须返回真正 extrinsic LLR | demapper 与 decoder 多轮交换 extrinsic 信息，禁止把 posterior 原样反馈造成双计数 | updated bit LLR / hard codeword | 每个 outer iteration 增加一次 demapper + 若干 decoder iterations，并需 interleaver/state | one-shot APSK BICM + tuned NOMS | one-shot 更精确 max-log/log-MAP demapper、额外 decoder iterations、一次 LLR calibration | 对多环 APSK 的 bit-label ambiguity / iterative demapping loss 最有物理机会，但完整 BICM-ID 会吸收“选择性迭代解调”的收益。只有选择性触发在相近 FER 下显著降平均成本，或在相同总预算下提高 FER，才能单独命名 |

## 3. 吸收关系：哪些 baseline 会吃掉什么

| Comparator | 会吸收的增益来源 | 仍可能留下的最窄方法差异 |
|---|---|---|
| 普通 restart / 随机扰动 | 多次独立初始化、随机 tie-breaking 或重新跑同一 decoder 带来的成功概率 | syndrome/reliability 指引在**相同 retry 次数**下提高 rescue 命中率 |
| 额外迭代 | 仅因多做 message passing 而获得的 FER 改善 | 相同 edge-update 总数下的更优调度、参数或候选定位 |
| OSD | 按 reliability 排序并枚举低阶 test patterns 的 soft reprocessing 收益 | syndrome 限定候选若以更低 list/排序成本达到相同 FER，或同成本 FER 更好 |
| Bit-flipping / weighted bit-flipping | unsatisfied checks + bit reliability 驱动的局部翻转 | 新动作必须不只是换一个 flip metric；至少在触发、候选结构、重解码合同或成本—FER 曲线上有可陈述差别 |
| 固定 NOMS / OMS | 静态 normalization/offset 对 min-sum 近似误差的校正 | adaptive 参数必须在相同迭代/edge-update 预算下产生额外 FER，或形成明确平均复杂度收益 |
| 完整 BICM-ID | decoder extrinsic 回馈 demapper、重复解调和重复解码的全部迭代增益 | 选择性 BICM-ID 只能主张 event-triggered cost/latency 优势，或同总预算 FER 优势 |

## 4. 等成本合同

### 4.1 主预算单位

每个 codeword 至少记录：

`decoder_calls | configured_iterations | total_CN/VN_edge_updates | demapper_passes | restart_attempts | flip/OSD_candidates | sorting_work | peak_state_memory | stop_reason`

算法公平性的主口径是 `total_CN/VN_edge_updates`，因为 flooding、layered 与 informed schedule 的“1 iteration”不等价。`decoder_calls × configured_iterations` 只作当前 adapter 可取得的退化口径；wall-clock / energy 是实现相关的第二口径，不能替代算法预算。

### 4.2 四组冻结比较

1. **Base**：one-shot demap + tuned fixed NOMS，最多 20 轮。
2. **Equal-update**：把候选的全部 decoder edge updates 折算给 fixed NOMS；rescue 每多一次 decode，base 也得到等量 extra iterations 或 restart。
3. **Equal-attempt**：C5-2 与 random restart、weighted bit-flipping、OSD 使用相同 retry/list 数；报告每次额外尝试的 rescue success。
4. **Outer-loop**：选择性 BICM-ID 与 full BICM-ID 同时计 `demapper_passes + decoder edge updates`；另报平均、P95 与最坏成本，因为 event-triggered 平均值会隐藏失败帧长尾。

主指标是 FER；BER 仅作伴随指标。还须报告未收敛率、undetected error（若只有 syndrome，无 CRC 时尤其重要）、平均/P95 latency 与触发率。任何使用提前停止的方案，baseline 必须获得同一 syndrome/CRC stop rule。

## 5. Step 2 必读候选（8 篇）

| JSON ID | 文献与正式性 | 全文可得性 | Step 2 必须核对 |
|---|---|---|---|
| T041-001 | *The Syndrome Bit Flipping Algorithm for LDPC Codes*, IEEE Communications Letters, 2023, DOI `10.1109/LCOMM.2023.3272277`，正式 | OA 标记为是 | syndrome/bit metric、一次 rescue 的候选数与 decoder calls；对普通 BF、额外迭代、error-floor/trapping-set 的消融 |
| T041-002 | *Lowering the Error Floor of Quantized NR LDPC Decoders by a Post-Processing on Trapping Sets*, WCSP 2021, DOI `10.1109/WCSP52459.2021.9613326`，正式 | 元数据标非 OA；需合法获取 | stage-2 trigger、量化 posterior/reliability 来源、目标 trapping set；与更多 NMS 轮次/普通 BF 的成本匹配 |
| T041-003 | *Residual-Decaying-Based Informed Dynamic Scheduling for BP Decoding of LDPC Codes*, IEEE Access, 2019, DOI `10.1109/ACCESS.2019.2899106`，正式 | OA | residual 定义、decay 规则、一次 schedule step 等价多少 edge updates；与 flooding/layered/RBP 的同更新数 FER 与调度开销 |
| T041-004 | *On the Use of Ordered Statistics Decoders for LDPC Codes in Space Telecommand Links*, EURASIP JWCN, 2016, DOI `10.1186/s13638-016-0769-z`，正式 | OA | OSD order/list、reliability 输入、短码适用性；FER 与复杂度曲线，作为 rescue 的高成本上界 comparator |
| T041-005 | *Closing the Gap to the Capacity of APSK: Constellation Shaping and Degree Distributions*, arXiv:1210.4831, 2012 | arXiv 全文可得；**正式版本 UNKNOWN** | APSK ring/labeling、iterative demapping 假设、degree-distribution 是否与目标 5G-LDPC 不兼容；查正式发表版本与 EXIT/density-evolution 口径 |
| T041-006 | *Adaptive-Normalized/Offset Min-Sum Algorithm*, IEEE Communications Letters, 2010, DOI `10.1109/LCOMM.2010.07.100508`，正式 | 元数据标非 OA；需合法获取 | α/β 如何按 iteration/state 更新、是否需要 oracle SNR；与 tuned fixed NMS/OMS 的同迭代 FER/BER 与参数成本 |
| T041-007 | *Bit-Interleaved LDPC-Coded Modulation with Iterative Demapping and Decoding*, VTC Spring 2009, DOI `10.1109/VETECS.2009.5073425`，正式 | 元数据标非 OA；需合法获取 | demapper a-priori/extrinsic 方程、outer/inner iteration 分配、interleaver/labeling；one-shot demap + extra LDPC iteration 的等成本消融 |
| T041-008 | *Reduced-Complexity Decoding of LDPC Codes*, IEEE Transactions on Communications, 2005, DOI `10.1109/TCOMM.2005.852852`，正式 | 元数据标非 OA；需合法获取 | BP/MS/NMS/OMS 定义与 LLR 符号、fixed-factor 调优方式、复杂度基准；作为 fixed decoder 主 comparator 的 canonical authority |

说明：检索源为 S2/OpenAlex/arXiv；本轮 S2 多次限流，因此正式版本主要依靠 OpenAlex 返回 DOI 与 `publication_status`。T041-005 只有 arXiv 身份，不能在 Step 1 写成正式论文。

## 6. 当前 codec 进入实现前审查清单

- [ ] 目标链到底沿用 5G NR BG2 `k=1024,n=1536,Z=104`，还是改 DVB-S2(X)/自定义 LDPC；不得把旧 16QAM/P08 身份默认移植到 DP-(8,8)-16APSK。
- [ ] 从 decoder 取得**rate-matching inverse 后的完整 hard codeword**，并用与 BG/Z 对应的 `H` 计算 syndrome；禁止对 `info_hat` re-encode 后再算 syndrome。
- [ ] 核对 filler、punctured `2Z`、interleaver 与 transmitted 1536 bits 到 lifted codeword 的索引映射；syndrome 的列顺序必须与 `H` 一致。
- [ ] 确认 soft-output 模式的符号、形状与语义：channel prior、posterior、extrinsic 分别是什么；用 `extrinsic = posterior - prior` 前必须核对库定义，不能凭名称。
- [ ] 若做 NOMS/调度，确认每轮/每 layer 能否合法访问 V2C/C2V message、residual 与 callback；当前 adapter 不支持，Sionna 库级能力保持 UNKNOWN。
- [ ] 增加 stop reason：syndrome-zero / CRC-pass / max-iter / stall；若没有 CRC，单独统计 undetected codeword error，不能把 syndrome-zero 当 truth-correct。
- [ ] 冻结 iteration 的公平换算：flooding、layered、residual schedule 按 edge updates 对齐；当前 receipt 的 `20×codewords` 仅为配置计数。
- [ ] 冻结 retry 生命周期：每次 restart 是 fresh state 还是 warm state；当前 D0 强制 fresh 并禁止 message reuse。
- [ ] 实现 `(8,8)-16APSK` mapper/demapper 的 bit labeling、noise variance 与 LLR convention；当前 Gray-16QAM max-log 只可作旧 adapter 事实，不是目标平台 authority。
- [ ] BICM-ID 必须显式测试 decoder 输出是否为真正 extrinsic；防止 posterior double counting，并计入每次 demapper pass。
- [ ] 所有 rescue 触发只读 receiver observations；TX bits 只能进最终 BER/FER scoring，不得进入 syndrome、bit selection、stop 或 candidate ranking。

## 7. UNKNOWN

1. **Sionna 库级 state/callback 的完整语义与稳定 API：UNKNOWN。** 本轮只确认项目 adapter 关闭 state 且不返回 soft output；不据库签名推断可直接实现逐轮调度。
2. **失败 decoder 的 full-codeword hard output与 rate-matching inverse 是否可无侵入取得：UNKNOWN。** 旧 P08 syndrome helper 是 encoder correctness 工具，不是失败态接口。
3. **目标 Ch5 LDPC 身份：UNKNOWN。** 当前代码是 5G NR BG2/16QAM；共同平台已设计为 DP-(8,8)-16APSK+BICM/LDPC，但具体标准、码率、码长与 interleaver 尚未冻结。
4. **目标工作区是否由 trapping sets/error floor 主导：UNKNOWN。** 在 waterfall 区，syndrome rescue 可能被更多迭代或 OSD/bit-flipping 吸收；须待 Step 3/4a 先证 problem occurrence，不可由论文标题反推。
5. **APSK 文献 T041-005 的正式版本：UNKNOWN。** 当前只有 arXiv:1210.4831；需在 Step 2 查 canonical publication。
6. **完整 BICM-ID 对当前 target labeling/code 的增益与代价：UNKNOWN。** 现有检索只建立经典机制和 comparator 合法性，不证明 DP-(8,8)-16APSK 上 FER 会改善。
7. **固定 NOMS 的充分调优合同：UNKNOWN。** 旧 `α=0.75, offset=0, 20 iter` 是历史实现常数，尚非目标 APSK/LDPC 组合上的公平 tuned baseline。

## Step 1 边界

本文件只冻结外部 authority、可见状态、比较对象与进入 Step 2 的阅读池；不声称 C5-2/C5-0 已形成方法，不完成 Step 3/4a，不授权实验或实现。
