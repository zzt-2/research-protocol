# Ch5 structured covariance correctness seam

This directory implements D045/T054 only: B1/B2/B3/C1 covariance estimators,
the `PostCh4Bundle` synthetic fixture, APSK Mahalanobis/log-det LLR, and
deterministic correctness/GMI-identity smoke.

`CORRECTNESS_ONLY / SYNTHETIC_RESIDUAL / NO_TARGET_OCCURRENCE_OR_METHOD_SIGNAL`

It does not test natural post-Ch4 residual occurrence, method headroom,
BER/FER gain, SNR/pilot/kappa sweeps, or LDPC performance.

T060 adds `post_ch4_ch3_bridge.py`, a receiver-visible bridge with the fixed
order `Ch4 demux/RDE -> per-pol Ch3 DA CPR -> pilot-only 8-fold ambiguity ->
known-pilot residual`. The Ch4 arm is caller-injected; this package does not
select a best arm. Payload truth is held in a separate offline object and is
excluded from the deployable bundle and both hashes.

T063 makes the Ch4 acquisition preamble and observation one continuous
shared-scalar -> unitary-Jones -> circular-AWGN realization. The deployable
bundle and `bundle_hash` include the complete frozen-arm snapshot (including
explicit null thresholds) and gate summary; `realization_hash` remains
independent of arm parameters.

`BRIDGE_CORRECTNESS_ONLY / TARGET_OCCURRENCE_NOT_RUN / NO_METHOD_SIGNAL`

Run from the repository root:

```powershell
python -m pytest projects\simulation\tests\test_ch5_apsk_structured_covariance.py -q
python projects\simulation\explore\ch5-apsk-structured-covariance\run_smoke.py
python -m pytest projects\simulation\tests\test_ch5_post_ch4_ch3_bridge.py -q
python projects\simulation\explore\ch5-apsk-structured-covariance\run_occurrence_smoke.py --mode correctness
```
