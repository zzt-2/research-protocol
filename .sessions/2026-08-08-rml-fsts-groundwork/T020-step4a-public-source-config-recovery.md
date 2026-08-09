# Task Brief: RML-FSTS Step 4a public source-config recovery

> 来源: D011-D012 / V007 / H006 / S005 | 日期: 2026-08-09
> 时间上限: 15 分钟；到点必须写止损结论，不得无限检索
> 产出: `projects/thesis-fso/worker-logs/step-4a-rml-fsts-public-source-config-recovery.md`

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-20-research-direction-lab-system/topic-index.md
  control_epoch: 37
  action_class: NEW_TOPIC_RECOVERY
  mission_checkpoint: CP024
```
<!-- RDL-TASK-CONTROL:END -->

## 任务

只回答 D012 `SC1`：公开可取得的一手/作者材料能否闭合 Wang 2023 DOI `10.1109/JPHOT.2023.3265847` 的 executable receiver/channel source configuration。你是 evidence-recovery executor，不是方法设计者；不得运行 estimator/grid/MVE，不得用典型值补空白，不得修改任何 owner、代码、合同、paper 正文或 protected logs。

开始前完整读取并遵守：

1. `using-superpowers`、`research-direction-lab`、`session-governance` skills；
2. 本 T、D011-D012、V007、H006、S005；
3. `projects/thesis-fso/worker-logs/step-4a-rml-fsts-source-calibration.md` 与 `step-4a-rml-fsts-physical-transfer.md`；
4. canonical Wang `D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/content.md`、`metadata.json`；
5. `tools-guide.md` 中 search/download 纪律。

先运行并记录：

```powershell
python C:\Users\zzt\.agents\skills\research-direction-lab\scripts\validate_task_control.py `
  .sessions/2026-08-08-rml-fsts-groundwork/T020-step4a-public-source-config-recovery.md `
  --repo-root D:\code\study\research-protocol\.worktrees\rdl-method-production-v2
```

非 PASS 立即停止并只写 setup blocker。

## 有界检索面

按下列顺序搜索；可使用 web search，但技术断言只接受 primary/authoritative source，并对网页断言以 DOI/Crossref/DataCite/ORCID/仓库原始文件交叉验证。主控不得接收大段网页，最终聊天摘要保持精简，完整证据留 worker log。

1. exact title/DOI/IEEE article number `10101698` 的 supplementary material、DataPort、Code Ocean、GitHub/Gitee、Zenodo/Figshare/OSF、institutional repository；
2. Liqian Wang（ORCID `0000-0002-2512-2851`）、Jichen Wang（`0009-0008-3197-0196`）、Xinyu Tang（`0000-0002-4992-666X`）的公开代码、数据、学位论文、同一平台论文；
3. exact-paper references/citing work 中由同一作者团队给出的 phase-screen/SMF/receiver-noise implementation；
4. IEEE 页面公开附件/API/media manifest 与作者版 PDF；
5. 若发现精确 artifact，核对 license/source identity；论文/PDF 下载必须用项目 `tools/download`，PDF 转换必须用 `tools/convert`。不要手工在 `papers/` 创建目录，不 clone 未确认身份的仓库。

止损：至少覆盖 `publisher/DOI metadata`、`author identity/institutional`、`code/data repository` 三类独立 surface；连续两类只得到正文镜像/无附件后仍完成剩余一类，然后停止。不得联系作者、发邮件、提交表单、上传材料或绕过登录/访问控制。

## SC1 字段级验收

为每一字段写 `EXACT_CLOSED / RELATED_ONLY / NOT_FOUND / CONTRADICTED`，并给 URL、本地 path/hash（若有）、source identity 与精确摘录位置：

1. carrier wavelength、input field/beam geometry；
2. phase-screen spectrum/normalization、screen count/spacing、FFT grid/extent、subharmonics、propagator；
3. aperture 与 SMF mode/overlap，branch independence/covariance、per-frame/state lifecycle；
4. received optical-power reference plane 与 per-pol/per-branch accounting；
5. BPD/optical-hybrid/TIA gains、shot/thermal/background/dark terms、temperature/load/noise density；
6. equivalent noise/filter bandwidth、sample/matched-filter convention、ADC scaling/quantization；
7. 能否从明确方程和数值唯一计算 `P_rx[dBm] -> E[|w[k]|^2]`；
8. Fig. 10 source power/action ticks 与 B0 numeric tolerance（恢复图轴仅是辅助，不能替代 1–7）。

`SC1=PASS` 只在 1–7 全部由 exact-paper 或可证明同一 executable source chain 闭合，且无需典型值/结果拟合时成立。相似论文、同作者但不同平台、一般 phase-screen 公式、scalar Gamma-Gamma、图像 digitization 均只能 `RELATED_ONLY`。

## 输出格式

```markdown
# RML-FSTS public source-config recovery
## Verdict
## Control validation and search ledger
## Exact-paper artifacts
## Author/same-platform evidence
## SC1 field closure matrix
## B0 calibration consequence
## Dead ends and stop rule
## Artifact/provenance ledger
## Next legal action
```

Verdict 只允许：

- `SC1_PASS_EXACT_EXECUTABLE_CONFIG_RECOVERED`
- `SC1_NOT_CLOSED_PUBLIC_SOURCE_EXHAUSTED`
- `SC1_INVALID_SOURCE_IDENTITY`
- `SETUP_BLOCKED`

只写指定 worker log；不 commit/push。任何 exact artifact 发现须在 log 给出 URL/hash/license，不自行扩大目录或实验范围。
