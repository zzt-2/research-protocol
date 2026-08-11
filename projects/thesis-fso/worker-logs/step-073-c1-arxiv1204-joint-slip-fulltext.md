# Step 073 — arXiv 1204.2660 joint phase/LDPC slip 全文精读

> 2026-08-09 | T027 | `FULLTEXT_READ` | CP009 / epoch 9
> Collision：`PARTIAL_CORE_ONLY`

## 1. Identity / acquisition / quality

- fresh task-control validator：`PASS`。
- `python -B tools/paper_download.py --arxiv 1204.2660 --dry-run` 后实际获取成功：`arxiv_latex / good`。
- source=`papers/arxiv/1204.2660/source.tar.gz`；content=`papers/arxiv/1204.2660/content.md`，217 行。
- metadata 因 converter 未抽 title 而 `unverifiable`；原始 `after_dani.tex` title 与派遣题名 exact match，作者 Shachar Shayovitz / Dan Raphaeli；official arXiv receipt为 v1、2012-04-12。
- hashes：source `98FE854224644299161DDB97A511CC970218A6E3F08BB72373F7A84D72274F28`；content `B3ACE64A42B505FA38EED962D55C6C51C72233499390F80943439271D34B042F`。

## 2. Fulltext facts（10）

1. Channel=`r_k=c_k e^{jtheta_k}+n_k`，MPSK/AWGN，phase为 Wiener `theta_k=theta_{k-1}+Delta_k`。
2. 论文的 slip 是 single-Tikhonov approximation在星座似然歧义时丢失其他 modes并跟错 phase trajectory；不是显式离散 change-point injection。
3. Modified model=`alpha*Tikhonov+(1-alpha)*Uniform`；uniform mass表示 tracked trajectory之外的 hypotheses，`1-alpha`可解释为 slip probability。
4. forward/backward每个 symbol更新 confidence，但全 K-symbol codeword无条件执行；没有 event trigger。
5. Algorithm 1 以 amp-to-variance 最大成分为 lead，用 `D(f_lead||f_i)<=T_D`聚类，再做 CMVM；未选质量进入 uniform。
6. pilot之后在 high-SNR 假设下令 `alpha=1`以重获 trajectory；这是固定机制，不是 failure-conditioned fallback。
7. `P_u(c_k)=A+B+C+D`把 forward/backward的 tracked/uniform 四种组合加权，给 LDPC symbol likelihood；decoder priors `P_d`再参与后续 phase messages。
8. 实验=`LDPC 4608/rate .889 + BPSK + sigma_Delta .1 rad/symbol + pilot 1/80 + T_D 2.2 + DP L=8`。
9. complexity=`40M ops + 5M LUT / symbol / iteration`；iteration count、latency、memory未给。
10. 算法不输出 boundary/direction/affected range，不做 finite segment/suffix rotation，不提供 clean no-op或 failure fallback。

## 3. 八字段

| input | trigger | localization | candidate/action | decoder interaction | fallback | budget | output |
|---|---|---|---|---|---|---|---|
| `r_k`, pilots, MPSK/Wiener params, LDPC `P_d`, `T_D` | none；unconditional whole-codeword iterations | per-symbol confidence only；no boundary/direction output | lead trajectory + KL cluster + CMVM + uniform remainder | joint `P_u <-> P_d` factor-graph messages | pilot high-SNR recapture assumption；no rollback | `40M ops + 5M LUT`/symbol/iteration；total calls unknown | symbol LLR/decoded bits；no local-repair outcome |

## 4. Local-vs-joint 与 collision

它是 **whole-codeword unconditional joint inference**：per-symbol phase confidence并不等于 event-triggered localization；algorithmic forward/backward也不等于 slip direction。它与 OFC 2014 同属 decoder-interacting slip-aware core：OFC用 explicit Markov slip state/max-log-MAP，本文用 continuous Wiener phase/Tikhonov+uniform approximation；两者都无 boundary、bounded suffix action与 fallback。

```text
collision_verdict = PARTIAL_CORE_ONLY
exact_chain       = false
claim_ceiling     = SLICE
```

任何“decoder-aided slip inference”泛称已被本文占用；Q1 只有在完整 `trigger/localization/bounded action/selective re-decode/fallback/budgeted local output` 上才仍可能有增量。本全文不证明 Q1 defect或Step 4a Go。

## 5. 成本、参数与保护边界

- 可复现参数：LDPC length/rate、BPSK、Wiener `sigma_Delta`、pilot spacing、`T_D`、DP levels及三算法per-symbol-per-iteration complexity。
- 不可冻结：iteration/decoder-call数、stop rule、latency/memory、multi-slip law、SNR/EsN0 sampling、frame count/CI、threshold sensitivity、model mismatch。
- 本轮只写指定 read note 与 worker log；downloader按 canonical paper path写入 source/content/metadata。未改中央 owner/治理/代码，未运行实验，未 stage/commit/push。

## Terminal

`FULLTEXT_READ / PARTIAL_CORE_ONLY`
