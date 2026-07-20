# Communications domain profile

Use this profile for stable communications conventions. Keep the current
project's scenario, parameter values, code identities, paths, and execution
state in its project adapter.

## Information-access levels

- **Receiver-visible:** observations and metadata available to the deployed
  receiver at the decision time, such as received samples, known pilot
  symbols, declared framing, and causal receiver history.
- **Training-only:** labels, clean targets, channel realizations, or future
  samples used to fit a method but unavailable during deployed inference.
- **Evaluation-only:** reference bits, transmitted symbols, hidden channel
  states, or paired clean signals used only to score an output.
- **Oracle:** privileged information or retrospective selection used to
  estimate headroom. An oracle is a bound or diagnostic comparator, not a
  deployable method.

State the access level for every method. A performance claim between methods
is legal only when the receiver-visible information is matched, or when the
extra information is named as part of the contribution and claim scope.

## Metrics and units

- BER and FER are dimensionless rates. Report the evaluated bit or frame
  population and uncertainty or repeated-run spread when it matters.
- SNR and related power ratios must name the reference point and convention;
  logarithmic values use dB. Do not compare ratios defined at different points
  without an explicit conversion.
- GMI and achievable information measures state their normalization, such as
  bits per symbol or bits per channel use.
- EVM states whether it is linear, percent, or dB and how gain and phase
  alignment are handled.
- MSE and NMSE state the estimated quantity, normalization, and averaging
  dimensions.
- Latency, throughput, memory, and operation counts accompany performance
  claims when complexity or deployability is part of the contribution.

Prefer distributions, confidence intervals, or repeated-seed summaries over a
single favorable realization. Keep denominator, averaging, and stopping
conventions identical across compared methods.

## Common evaluation axes

Common axes include channel quality, channel dynamics, modulation and coding,
block or frame length, observation-window length, model mismatch, receiver
information availability, training-data regime, compute or latency budget,
and random realization. Select axes that expose the proposed mechanism and
state which axes remain untested; a narrow slice does not establish a
domain-wide conclusion.

## Comparator legality

A legal scientific comparison aligns:

- task, signal model, dataset split, and evaluated condition;
- receiver-visible information and causal availability;
- modulation, code, code rate, payload, and throughput convention;
- tuning opportunity, stopping rule, and test-set isolation;
- metric definition, aggregation, and uncertainty treatment; and
- material compute or latency constraints when efficiency is claimed.

Use a recognized conventional baseline and the strongest relevant reusable
baseline available for the claimed contribution. Label ablations as mechanism
tests rather than competitors. Keep oracle results visibly separate from
deployable results. A method that relies on evaluation-only truth cannot
support a deployed-receiver superiority claim.

## Claim boundaries

- **Uncoded versus coded:** uncoded BER establishes detector behavior before
  decoding; it does not establish coded BER, FER, coding gain, or end-to-end
  throughput. A coded claim names the code, rate, decoder, iteration or stopping
  convention, and interleaving assumptions.
- **Hard decision versus soft information:** hard decision performance does
  not establish soft-decoding quality. Soft information claims require the
  score or likelihood convention and, where relevant, calibration evidence;
  GMI or coded results should accompany claims about decoder usefulness.
- **Training versus inference:** training-only truth may justify learning but
  cannot be silently counted as receiver-visible input at evaluation time.
- **Matched versus mismatched conditions:** matched-condition evidence does
  not imply robustness. Robustness claims name the mismatch family and tested
  range.
- **Simulation versus deployment:** simulation establishes behavior under the
  declared model. Hardware, field, or real-time claims require evidence from
  the corresponding setting.

## Common thesis contribution forms

- A receiver or transmitter algorithm with a clearly isolated mechanism and
  a legal conventional comparator.
- An adaptive or robust method whose benefit is tied to a declared variation
  or mismatch axis.
- A method that reaches similar performance with less receiver information,
  training data, latency, memory, or computation.
- A joint design that demonstrates why the interaction between stages matters
  through component and end-to-end ablations.
- A performance-boundary or negative-result study that identifies when a
  method helps, fails, or has negligible headroom.
- A reproducible benchmark, model, dataset, or evaluation protocol that enables
  a previously unavailable scientific comparison and is validated by a real
  use case.

For every form, bind the contribution to its evidence scope, comparator class,
information-access level, and remaining limitations.
