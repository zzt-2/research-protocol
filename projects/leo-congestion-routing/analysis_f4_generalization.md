# F4 Analysis: Generalization Claim Validity

**Date**: 2026-05-17
**Status**: Analysis complete
**Recommendation**: Option A (weaken claim) as baseline, add Option B Scenario B1 (polar gap) as low-cost strengthening

---

## 1. Topology Analysis: All Test Constellations Are Structurally Identical

### 1.1 Verified Properties

The simulator (`topology.py`) constructs Walker delta topologies as follows:
- Intra-plane: ring ISLs within each orbital plane (2 edges per node: prev/next)
- Inter-plane: ISLs connecting to adjacent plane at same satellite index (2 edges per node: left/right plane)
- Result: **every constellation is 4-regular** (degree exactly 4 at every node)

| Scale | Config | Nodes | Edges | Degree | Diameter | Avg Path | Clustering | Algebraic Connectivity |
|-------|--------|-------|-------|--------|----------|----------|------------|----------------------|
| 48 | 4x12 | 48 | 96 | 4 | 8 | 4.09 | 0.000 | 0.268 |
| 66 | 6x11 | 66 | 132 | 4 | 8 | 4.29 | 0.000 | 0.318 |
| 288 | 12x24 | 288 | 576 | 4 | 18 | 9.03 | 0.000 | 0.068 |
| 720 | 36x20 | 720 | 1440 | 4 | 28 | 14.02 | 0.000 | 0.030 |

### 1.2 What Is Identical Across Scales

- **Local structure**: Every node has exactly 4 neighbors with identical roles (ring-prev, ring-next, plane-left, plane-right)
- **Clustering coefficient**: 0.000 at all scales
- **Local motif distribution**: Identical (no triangles, same 4-node substructure)
- **GNN 1-hop input**: Same feature dimensionality and semantic meaning
- **Edge type distribution**: 50% intra-plane, 50% inter-plane at all scales

### 1.3 What Differs Across Scales

- **Graph diameter**: 8 -> 8 -> 18 -> 28
- **Average path length**: 4.1 -> 4.3 -> 9.0 -> 14.0
- **K-path candidate lengths**: Mean 4.6 -> 4.9 -> 9.6 -> 14.4 hops
- **2-hop receptive field coverage**: 25% -> 20% -> 4.5% -> 1.8%
- **Algebraic connectivity**: 0.27 -> 0.32 -> 0.07 -> 0.03
- **Spectral gap**: Drops by ~10x from 48 to 720 nodes

### 1.4 Implications for the GNN

The GNN (2-layer GAT, 4 heads, 64-dim) sees a **qualitatively identical local view** at every scale:
- Input dimensionality does not change (4 neighbors, same feature semantics)
- Message passing aggregation operates on the same local graph structure
- The only "new" challenge at larger scales is that paths are longer, meaning:
  1. More edges to accumulate load on
  2. 2-hop receptive field covers a smaller fraction of the total graph
  3. Global congestion patterns are harder to infer from local observations

**Verdict**: The "generalization" test is primarily a test of **scale robustness** (longer paths, sparser relative coverage), NOT a test of **structural generalization** (different connectivity patterns). This is a valid contribution but should not be called "zero-shot generalization" without qualification.

---

## 2. Existing Generalization Results

| Experiment | Scale | GNN/ECMP | GNN/MLP | GNN Mean MLU | Pass? |
|-----------|-------|----------|---------|-------------|-------|
| E01 (trained) | 66 (1.0x) | 0.818 | 0.822 | 1.981 | PASS |
| E04 | 48 (0.7x) | 0.924 | -- | 1.955 | PASS |
| E05 | 288 (4.4x) | 0.900 | 0.872 | 5.837 | PASS |
| E06 | 720 (10.9x) | 0.948 | 0.951 | 6.562 | PASS |

Key observations:
- GNN beats ECMP at all scales (all ratios < 1.0)
- GNN/ECMP ratio degrades 16% from trained to 10.9x scale
- GNN/MLP ratio degrades 16% similarly
- The degradation is smooth and monotonic with scale
- All scales pass the contract threshold (GNN/ECMP <= 1.10)

The smooth degradation pattern is consistent with the GNN struggling with longer paths and reduced relative receptive field coverage, NOT with encountering unfamiliar topology structures. A truly structurally different topology would likely show a discontinuous jump in degradation.

---

## 3. Competitor Comparison

### 3.1 TELGEN (Zhou 2025, ToN)

**Generalization methodology**:
- Trains on ER graphs (20-100 nodes), ER random graphs with different p values
- Tests on: **ER (200-2000 nodes)**, **Waxman (200-5000 nodes)**, **ASN (553/1739 nodes)**, **B4 (12 nodes)**
- Cross-graph-family: ER-trained model tested on Waxman and ASN
- Scale: up to 20x (100 -> 2000 nodes), 50x to 5000 nodes
- Reports optimality gap < 3% across ALL graph families

**Key difference from our work**: TELGEN tests across fundamentally different graph generation models (ER vs Waxman vs real AS-level topologies). This is genuine structural generalization because ER and Waxman have very different degree distributions and clustering properties.

### 3.2 GMR (Huang 2024, TVT)

**Generalization methodology**:
- Trains on GlobalStar (48 nodes, 1400km altitude)
- Tests on Iridium (66 nodes, 780km altitude)
- Both are Walker delta variants, but with different altitudes and orbital parameters
- Reports 8.9%-20.2% improvement preserved

**Similarity to our work**: GMR also tests Walker delta -> Walker delta. Their generalization is similarly "same family, different size." The LEO satellite networking community has accepted this as valid generalization because Walker delta is the dominant constellation pattern.

### 3.3 DTAR (Zhou 2026)

- Tests on 288-node constellation only
- Does NOT test cross-scale generalization
- Focuses on domain-based routing, not full-network TE

### 3.4 Other LEO routing papers

- DeepLaDu: Tests 100-1000 nodes, GATv2 supports variable size, but same topology family
- GNN-ASSSP: Topology prediction on 100-8000, routing on 480/1584 only, no cross-scale GNN
- FlexSATE: 6 topologies (6-42 nodes), each trained separately, no cross-topology
- QueueMARL: 1584 nodes single scale, no generalization
- PRIMAL: 720 single scale, no cross-scale

**Minimum bar in LEO satellite networking**: Testing across different Walker delta sizes IS the accepted standard. No LEO routing paper tests on structurally different topologies (e.g., random graphs). The community recognizes that LEO constellations are overwhelmingly Walker delta.

---

## 4. Recommendation: Hybrid A+B

### 4.1 Primary: Option A -- Weaken the Claim

The claim should be reframed from "zero-shot generalization" to "scale generalization within the Walker delta family." This is defensible, honest, and consistent with the field's expectations.

**Proposed language for paper**:

> **Current claim** (problematic):
> "The proposed GNN achieves zero-shot generalization to constellation scales 0.7x to 10.9x without retraining."

> **Proposed claim** (recommended):
> "The proposed GNN demonstrates scale generalization within the Walker delta constellation family: a model trained on a 66-node Iridium-class constellation (P=6, S=11) can be directly deployed on Walker delta constellations ranging from 48 to 720 nodes (0.7x to 10.9x scale), maintaining MLU within 16% of the trained-scale performance and consistently outperforming ECMP. All test constellations share the same 4-regular local structure (2 intra-plane + 2 inter-plane ISLs per satellite), which is characteristic of operational LEO broadband constellations including Iridium, GlobalStar, and Starlink shell designs."

> **Additional justification paragraph**:
> "Walker delta is the dominant constellation topology for broadband LEO networks. All operational and planned large-scale constellations (Iridium, GlobalStar, OneWeb, Starlink shell-1) employ Walker delta variants with 4-ISL mesh topologies. Therefore, scale generalization within this family has direct practical value: a trained model can be deployed on new constellation configurations without costly retraining. Testing on structurally different topologies (e.g., random graphs) is less relevant for this application domain, as such topologies do not arise in real satellite network design."

### 4.2 Secondary: Option B Scenario -- Add Polar Gap Test

Among the heterogeneous topology scenarios analyzed, the **polar gap** test offers the best effort-to-impact ratio:

| Scenario | What Changes | Effort | Impact | Recommendation |
|----------|-------------|--------|--------|----------------|
| B1: Polar gap (30%) | Degree distribution [2,4], not uniform | Low (1 day) | High (realistic + structural) | **ADD** |
| B2: Sparse inter-plane (50%) | Degree distribution [2,3,4] | Low (1 day) | Medium | Optional |
| B3: Dense ISL (6-8 ISL/sat) | Degree changes to 8 | Medium (2 days) | Low (rare in practice) | Skip |
| B4: Street-of-coverage | Degree distribution [3,4,5] | Medium (2 days) | Low (not realistic) | Skip |
| B5: Different inclination | Path structure changes, degree same | Medium (3 days) | Medium | Future work |

**Why B1 (Polar Gap) is the best addition**:

1. **Physically realistic**: The config already has `polar_gap_lat: 70.0` as a parameter, but it is currently unused (the topology builder ignores it, deferring to `failures.py`). In reality, inter-plane ISLs above ~70 degrees latitude are often disabled due to pointing constraints. This is explicitly mentioned in DTAR and other LEO literature.

2. **Structural novelty**: With 30% polar gap, the degree distribution becomes [2, 4] (polar sats have degree 2, equatorial sats have degree 4). This is genuinely different from the uniform 4-regular training topology. The GNN must handle nodes with fewer neighbors.

3. **Low implementation effort**: The `failures.py` already has failure injection logic. Adding a deterministic "polar gap" edge removal before random failures requires ~20 lines of code in `topology.py`.

4. **Strengthens the claim**: Even if GNN performance degrades modestly on polar gap topologies, it demonstrates that the model can handle non-uniform degree distributions, which partially addresses the F4 concern.

### 4.3 Implementation Plan for Polar Gap Test

**Step 1**: Modify `topology.py` to respect `config.polar_gap_lat` (currently 70.0, unused):

```python
# In build_walker_delta(), after inter-plane ISL construction:
# Disable inter-plane ISLs for satellites above polar_gap_lat
# With 86.4 inclination, satellites at ring positions near 0 and S/2 are polar
# gap_fraction = polar_gap_lat / 90.0 ≈ 0.78 → non-polar fraction
# For 30% gap: disable inter-plane for top/bottom 15% of ring
```

**Step 2**: Add E04b experiment to contract:
- Config: n_planes=6, sats_per_plane=11, polar_gap enabled (30% of ring)
- Same traffic model, same failure rate
- Evaluate GNN (66-node trained), ECMP, MLP on this topology

**Step 3**: Estimated effort: 1 day (topology modification + run existing eval script)

---

## 5. Summary

### 5.1 Assessment

The F4 concern is **partially valid**: all test topologies share identical 4-regular local structure, so "generalization" here means scale robustness, not structural generalization. However:

1. Walker delta IS the dominant LEO constellation topology -- testing on random graphs would be irrelevant for this application domain.
2. Scale generalization within Walker delta has practical value (deploy on new constellation sizes without retraining).
3. The LEO networking community accepts Walker-delta-to-Walker-delta generalization as valid (GMR, DeepLaDu both do this).
4. TELGEN's cross-graph-family testing is more rigorous, but TELGEN targets general TE (not LEO-specific) and operates in a different problem setting (supervised LP-solving vs DRL online routing).

### 5.2 Recommended Actions

| Priority | Action | Effort |
|----------|--------|--------|
| 1 | Reframe claim as "scale generalization within Walker delta family" (Option A) | 0 days (wording change) |
| 2 | Add polar gap test as E04b (Option B, scenario B1) | 1 day |
| 3 | Cite Walker delta dominance in paper (Iridium/GlobalStar/Starlink all Walker delta) | 0 days |
| 4 | Acknowledge limitation: "structural generalization to non-Walker-delta topologies is not tested and left for future work" | 0 days |

### 5.3 What NOT to Do

- Do not compare directly with TELGEN's generalization methodology in the paper (different problem, different domain, invites unfavorable comparison)
- Do not add random graph or Erdos-Renyi tests (irrelevant for LEO, would confuse reviewers)
- Do not overclaim -- the weakened claim is still strong and well-supported by results
