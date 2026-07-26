# T009 synthesis

The task-control and D015 owner gates passed. A nearest-neighbour 16-APSK DPLL with
continuous VCO reproduced S011 at BER 0.003646; block resets worsened BER to
0.006536 (1.79x). The bounded deployability repair replaced TX-truth ambiguity
with known-pilot causal resolution and enforced one common data mask.

That repair removed the prerequisite A4 mechanism: DA won all nine validation
conditions. No reliable DA/NDA ordering crossover remained, and registered curves
did not provide legal FEC crossings. Per T009 section 4, execution stops as
`BLOCKED_IDENTITY`; P1-P3 primary test is not run and no method delta is claimed.

