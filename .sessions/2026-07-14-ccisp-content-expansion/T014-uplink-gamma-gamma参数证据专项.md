# Task Brief: 上行 Gamma--Gamma 参数证据专项

> 来源: S001 | 产出位置: `.sessions/2026-07-14-ccisp-content-expansion/R008-uplink-gamma-gamma参数证据与处理选项.md`
> 日期: 2026-07-15
> 唯一文档: 执行方可读取本任务列出的仓库文件、Git 历史和本地论文；外部检索与论文全文精读必须委托子 Agent

---

## 0. TL;DR（执行方先读）

你在 `D:\code\study\research-protocol`，论文工程是 `projects\simulation\paper\ccisp2026`。

**你的任务**：只读判断上行 Gamma--Gamma 参数 \((1.2,0.9)\)、\((1.0,0.7)\) 能否建立站得住的直接文献、物理映射或可复算设计场景依据，并给出诚实的论文处理选项。

**产出**：一份参数证据审计与处理选项报告，写入 `R008-uplink-gamma-gamma参数证据与处理选项.md`，供主控决定是否保留、重标、重标定或删除上行场景。

**最高纪律（违反一条即失败）**：

1. 目标是检验证据，不是为既定数字事后编理由；没有证据必须写 BLOCKED。
2. 禁止修改论文、参数、Skill、仿真代码、结果 JSON、图片或数据；禁止运行新仿真。
3. 禁止把 sat.1553 的 lognormal/scintillation-index 参数说成 Gamma--Gamma \((\alpha,\beta)\)；必须核对符号和模型。
4. 主对话禁止直接 WebSearch/webReader；外部检索和论文全文精读必须委托子 Agent，返回结构化摘要与精确来源。
5. 结果表现（例如上行增益更大）不能反向充当选参依据。

## 1. 背景（了解即可，不要据此先入为主）

当前论文 `sections/system_model.tex:14` 把 \((1.2,0.9)\)、\((1.0,0.7)\) 称为 moderate/strong uplink regimes。导师批注：“(α,β)哪来的”。

已知历史事实：

- 两组参数首次由 commit `a46e03db`（2026-07-07）加入，用于回应导师“上行受湍流影响远大于下行”的意见。
- `projects/simulation/params.py:157-199` 明写：参考 sat.1553 的上行强度数字后，“务实选”两组比下行 strong \((1.5,0.8)\) 更极端的 GG 参数；两组均标 `SourceType.assumption`、`AuditFlag.WARNING`。
- `papers/doi/10.1002_sat.1553/content.md:141-157` 给出的是 lognormal/pointing 场景的 \(\sigma_p^2=0.15/0.25\)，未给这两组 Gamma--Gamma 参数。
- 既有审计 `R007-自适应CPR定位参数溯源与精炼边界.md` 已判定：两组不是文献直接值，也没有已记录的 \(\sigma_p^2\to(\alpha,\beta)\) 映射。

## 2. 任务详情

### 2.1 必须回答的问题

#### A. 直接文献路线

1. 是否存在论文、标准、学位论文或权威教材，在可比的上行 FSO、归一化辐照度 Gamma--Gamma 模型中直接采用 \((1.2,0.9)\) 或 \((1.0,0.7)\)？
2. 若数值命中，模型、波型、孔径平均、路径方向、归一化和物理场景是否可比？只命中数字不算 PASS。
3. 回查“Trinh 2017”、sat.1553 引用链及本地引用文献，排除二手转录和项目文档循环引用。

#### B. 物理映射路线

1. Gamma--Gamma \(\alpha,\beta\) 的标准映射需要哪些输入：Rytov variance、plane/spherical wave、\(C_n^2(z)\)、路径、波长、接收孔径/aperture averaging 等？
2. sat.1553 的 \(\sigma_p^2\) 究竟是什么量，能否作为该映射输入？若不能，明确阻断原因。
3. 在不补造输入的前提下，是否存在一组可复算、量纲闭合的公式得到或接近这两组数值？容差必须在计算前声明，不能看完结果再放宽。
4. 如果存在多解或模型依赖，必须报告非唯一性，不得挑一个最接近既有数值的模型冒充推导。

#### C. 设计场景路线

1. 若不能闭合直接来源或物理映射，能否将它们诚实定义为 `representative stress-test regimes`，而不是实际/典型上行参数？
2. 这种设计场景需要什么独立于结果的可复算选择准则，例如预先指定的 scintillation-index bracket、相对下行 strong 的严重度梯度或覆盖区间？
3. 现有数值是否满足该准则？区分：历史真实选参理由、当前可验证数值性质、事后新增的设计解释。
4. 若要让场景真正物理标定，需要补哪些输入、是否必须更换参数并重跑全部相关结果？只列影响，不执行。

#### D. 论文处理路线

至少比较四个选项：

1. 保留 exact pairs，并给直接可核验文献；
2. 保留 exact pairs，但降级为明确的设计压力场景；
3. 用物理标定后的新 pairs 替换（标出必须重跑的范围）；
4. 删除上行两档及相关结果。

不得以“哪种故事更好看”为判据。按真实性、可复算性、改动成本和对核心贡献的必要性比较。

### 2.2 执行方式

1. 先读根目录 `AGENTS.md`，使用 `session-governance`、`paper-writing`；只读检查 `_registry.yaml` 与当前专题 `topic-index/decisions/voice/verifications`。
2. 用 `git show/log -S` 和 `rg` 追溯两组数值首次引入、所有理由表述及是否有候选扫描记录。
3. 读取 sat.1553 原文相关段落及其引用链；对任何物理量先做符号/定义卡。
4. 本地论文精读、外部检索均派子 Agent。技术检索只依赖原论文、标准或权威教材，不依赖搜索摘要、博客和聚合网页。
5. 如做公式复算，只允许一次性只读计算；记录公式、所有输入、来源、单位和数值，不写入仿真代码或数据。
6. 最后由独立 Agent 复核：是否存在模型偷换、事后容差、循环引用、结果反向背书。

### 2.3 产出格式（强制）

```markdown
# [R008] 上行 Gamma--Gamma 参数证据与处理选项

## 1. 事实时间线
| 日期/commit | 记录 | 原始理由 | exact file:line | 证据性质 |

## 2. 物理量定义卡
| 符号 | 原文定义 | 模型 | 单位 | 能否映射到 GG alpha/beta | 证据 |

## 3. 直接来源检索表
| pair | 来源 | 是否 exact | 场景可比性 | DIRECT/PARTIAL/FAIL | 证据 |

## 4. 映射复算
- 公式与适用条件
- 输入及来源
- 预注册容差
- 结果
- 唯一性/敏感性
- PASS/BLOCKED

## 5. 设计场景审计
| 候选准则 | 是否独立于结果 | 现有 pairs 是否满足 | 是否为历史理由 | 可对外声称边界 |

## 6. 四路线比较
| 路线 | 真实性 | 可复算性 | 是否需重跑 | 影响范围 | PASS/BLOCKED |

## 7. 推荐 change contract
- 推荐路线
- exact affected files/claims
- 不应修改
- 进入 WRITE 前所需批准/证据
- stop conditions

## 8. 独立复核
- Critical/Important/Minor
- 总状态 PASS/PARTIAL/BLOCKED
```

## 3. 已知陷阱

1. `params.py` 曾把 sat.1553 的量写成“Rytov 方差”，但原文符号是 \(\sigma_p^2\)；必须以原文定义为准。
2. “更小的 \(\alpha,\beta\) 看起来湍流更强”只能说明排序直觉，不能证明上行物理场景或 exact pair 来源。
3. Gamma--Gamma scintillation index 的完整式包含交叉项；不得只用 \(1/\alpha+1/\beta\) 后声称精确标定。
4. 找到相同数字但出现在海洋湍流、RF、IM/DD、不同归一化或无上行路径的论文，不等于可迁移。
5. 已有 +2.48/+3.07 dB 结果发生在参数选定之后，不能用来证明参数合理。

## 4. 验收

- [ ] 两组参数的首次 commit、`params.py` 和 sat.1553 原文均有 exact file:line。
- [ ] 每条外部来源可落到原论文/标准具体页、式或表。
- [ ] DIRECT、DERIVED、DESIGN SCENARIO、UNRESOLVED 明确分开。
- [ ] 任何映射均列全输入、来源、单位、适用条件和预注册容差。
- [ ] 没有把结果表现当参数依据，没有把事后解释写成历史理由。
- [ ] 四条论文路线均给出影响范围和是否必须重跑。
- [ ] 独立复核完成；存在模型偷换或缺输入时结论为 BLOCKED。

## 附：产出回传位置

`.sessions/2026-07-14-ccisp-content-expansion/R008-uplink-gamma-gamma参数证据与处理选项.md`
