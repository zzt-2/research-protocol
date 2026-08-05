# RED receipt — T007 compute-graph absorption

- baseline commit: `64a88db2c2d1b8c98d9b20f648fc3c4f4d6f6759`
- task: `.sessions/2026-07-20-research-direction-lab-system/T007-ch5-concept-method-construction.md`
- raw output: `projects/thesis-fso/direction-lab/harvest/ch5-concept-method-batch-001.md` at the baseline commit
- observed terminal: `NO_CONSTRUCT_SURVIVES`
- observed P1 classification: `ENGINEERING_COMPONENT`, but not a survivor

## Failure reproduced

The baseline output treated “compiler CSE / one-line explicit sharing” as a
zero-cost strongest cheap alternative even though the recorded runtime is
CPython/NumPy and executes `rx ** M0` in two independent function calls. It
also treated intentionally matched output as evidence that no engineering
action exists, despite the candidate changing the measured caller cost path.

This is the behavior the GREEN regression must reverse without reviving P2–P5
or turning P1 into a `METHOD_SIGNAL`.
