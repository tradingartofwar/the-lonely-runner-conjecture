# Proposed project: Compatibility representations for cooperating AI agents

**Status:** Proposed, not executed. October 17, 2026.  
**Origin:** Mission Control discussion following the runner-addition center-width result.  
**Mathematical source:** [Center-width rule](../experiments/runner-addition/center-width/RULE.md) and [center-selection handoff](CENTER_WIDTH_CENTER_SELECTION_HANDOFF_2026_10_17.md).

## Motivation and distinction

The Lonely Runner study separates the minimum interval half-width required to meet every possible added runner's safe bands, H_d(c), from the maximum half-width permitted by the fixed core, G_{S,d}(c). At a supplied rational center c, a universal core-safe interval exists exactly when H_d(c) <= G_{S,d}(c), under the source rule's assumptions.

**Proposed transfer, not a theorem:** in agent systems, ask whether a representation can expose what a task requires and what the agent configuration permits *before execution*. A proposed configuration x might encode tools, permissions, context, dependencies, ordering, shared state, and available actions. Schematically,

    H(x) = minimum capability required
    G(x) = capability permitted by constraints
    H(x) <= G(x)  (only if H and G are rigorously defined on a comparable scale).

This is an analogy, not an established numeric agent criterion. Real agent constraints may be multidimensional, logical, temporal, or relational; an arbitrary scalar score could erase the very distinctions being investigated. A more faithful initial representation may be a constraint-satisfaction problem or a typed compatibility relation, with a scalar margin only if justified.

## Representation Science hypothesis

Individual feasibility does not imply joint compatibility. A compressed handoff can preserve each agent's goal and tool inventory while omitting shared dependencies, permission boundaries, action ordering, version assumptions, or other relationships that determine whether the agents can jointly succeed.

**Candidate research principle:** For a specified class of coordination questions, a representation is sufficient only if it preserves the compatibility relations necessary to answer those questions. Whether compatibility is an independent representational invariant, analogous in role (not mathematical identity) to distance or connectivity, is an open research question.

This is aligned with Representation Science's distinction between marginal feasibility and joint compatibility. It is not evidence that the Lonely Runner formulas apply unchanged to agents.

## Proposed real-world experiment

Select one actual coordination failure or near miss from the existing GitHub/agent/handoff workflow, with available logs and a checkable outcome. Prefer consequential work already undertaken rather than inventing a toy failure.

Construct two representations of the same task:

- **Marginal description:** individual agents' goals, tool lists, and local capacities, without explicit cross-agent compatibility relationships.
- **Relational description:** the same facts plus dependencies, shared state, permissions, ordering constraints, provenance, and interface contracts necessary for joint execution.

Before revealing the outcome to evaluators, ask each representation to predict viability, identify likely failure modes, and recommend a configuration or handoff correction. Evaluate predictions against the actual record and, if safe and feasible, a controlled replay. Use identical task facts and budgets except for the explicitly manipulated representation. Record false positives, false negatives, and cases where both models succeed or fail.

Pre-register the case, outcome definition, evaluator independence limits, budgets, stop rules, and what counts as a consequential distinction. Do not interpret better prose as improved coordination. Distinguish detection, prevention, and retrospective explanation.

## Candidate research questions

1. Which compatibility relationships must survive compression for a specified coordination decision to remain answerable?
2. Can a relational representation predict an infeasible handoff before execution, when a marginal inventory cannot?
3. Can the representation identify a feasible reconfiguration (tool, permission, context, ordering, or handoff change)?
4. Does the advantage generalize across newly selected tasks, or does it depend on a single known failure?
5. When does a scalar required-versus-permitted model suffice, and when is a vector, graph, or constraint system necessary?

## Success and limits

A valuable outcome could be a falsified hypothesis, a failure taxonomy, a reproducible predictive advantage, or a concrete improvement to an agent handoff protocol. The project need not solve Lonely Runner, establish a universal law of representation, or require a new agent framework. Keep the mathematics of the center-width result distinct from this speculative transfer.

## Suggested next action

Mission Control and the agent/Representation Science workstream should choose **one real coordination case** and draft a frozen, falsifiable protocol. Preserve the original incident evidence. Do not start implementation or claim validation until the protocol and data boundaries are agreed.

**Cross-reference:** This proposal belongs to the Lonely Runner research history as a value-transfer lead. If adopted, mirror a linked experiment record into the representation-science repository rather than moving or deleting this originating note.
