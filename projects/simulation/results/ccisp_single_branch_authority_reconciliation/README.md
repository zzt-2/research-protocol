# CCISP single-branch authority reconciliation

This directory contains a scheduling-only deterministic recomputation from immutable commit
`67970307a051dd8149e1a750498a20674dfcfe6f`.

- Source: raw `performance-*.json` and `timing-*.json` blobs under
  `projects/simulation/results/2b_fixed_point_branch_routed_cpr_closure/` in that commit.
- Excluded: every fixed-point field and claim.
- Recompute: `python tools/recompute_ccisp_single_branch_evidence.py --output projects/simulation/results/ccisp_single_branch_authority_reconciliation/recomputed-evidence.json`
- Evidence population: 990 cells/shards, 400 windows per cell, 396,000 windows total.
- Terminal: `THESIS_ENGINEERING_METHOD_READY` after independent verification recorded in RDL V020.

The raw source remains immutable in Git history; this directory is a compact, auditable projection for the
CCISP select-before-execute single-branch receiver architecture.
