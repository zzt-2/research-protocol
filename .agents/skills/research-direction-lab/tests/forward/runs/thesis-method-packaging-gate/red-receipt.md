# Thesis method packaging gate — RED receipt

> Observed before the Skill implementation edit on 2026-08-03

## Source identity

- repository HEAD: `5b69a0e2531161e25fb0298b48a642212b82894f`
- `SKILL.md` Git blob: `78ea70c5eb42c326d6725b1d5daf4874d013ae10`
- `method-production.md` Git blob: `d4dfcc962553c9c2d1e95ed92e4a7f5cbc815f01`
- `thesis-harvest.md` Git blob: `064c3e2394b3ad1bf86b455abd07a24644db0293`

The new test was present in the working tree while the three Skill sources
above still matched these HEAD blobs.

## Command

```powershell
python -m pytest .agents/skills/research-direction-lab/tests/test_structure.py -k every_valid_package_gets_a_separate_thesis_chapter_capability_checkpoint -q
```

## Verbatim failure excerpt

```text
FAILED .agents/skills/research-direction-lab/tests/test_structure.py::test_every_valid_package_gets_a_separate_thesis_chapter_capability_checkpoint
AssertionError: assert '`THESIS_METHOD_READY`' in text
```

## Interpretation

This RED proves only the structural omission: normal package finalization had
no mandatory, separate thesis chapter-capability checkpoint. It does not claim
that every pre-patch agent would misclassify every engineering candidate.
