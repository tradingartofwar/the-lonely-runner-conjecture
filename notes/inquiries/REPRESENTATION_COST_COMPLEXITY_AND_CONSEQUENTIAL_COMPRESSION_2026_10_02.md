# Representation Cost, Complexity, and Consequential Compression

**Date:** October 2, 2026  
**Status:** Conceptual inquiry / working paper  
**Origin:** Driving conversation between Vance and his AI research partner after reviewing the current Compatibility Calculus work  
**Scope:** What the Lonely Runner investigation may be teaching us about complexity, representation, compression, and human–AI collaboration  
**Claim posture:** This paper develops hypotheses and design principles. It does not claim a theorem about representational lower bounds, computational complexity, Compatibility Calculus, or the Lonely Runner Conjecture.

## Abstract

The Lonely Runner investigation began with a simple mathematical question and gradually became a laboratory for a second question: **what must a representation preserve in order to remain adequate as interacting constraints multiply?**

The research repeatedly found that compact representations worked until a distinction they omitted became consequential. Blocking had to be separated from overlap. Total overlap had to be separated from placement. Marginal compatibility had to be separated from same-point compatibility. Positive-width regions had to be separated from isolated equality points. A compact sheet menu that worked well in a lower-rank setting lost cases when genuinely independent motion was introduced; richer orbit-interval and point representations recovered cases that the smaller language could not express.

This led Vance to a different interpretation of the apparent scaling problem. Perhaps a representation becoming larger as independent participants are added is not evidence that the representation has failed. It may be evidence that the underlying system contains more consequential relationships. If so, demanding that the complete representation remain small may itself be the wrong objective.

The human problem is then not to make the underlying representation as small as possible. It is to preserve the distinctions that reality requires while presenting a human with only the resolution needed for the current question or decision.

This paper develops that intuition and connects it to the broader idea of **consequential distinctions and reversible compression**.

---

## 1. Why Lonely Runner is a useful complexity laboratory

The Lonely Runner Conjecture has an unusual combination of properties.

Its local rules are simple. Runners move at constant speeds around a circular track. Yet the collective condition is difficult: for a selected runner to be lonely, all relevant distance constraints must hold at one shared physical time.

This creates a clean separation between:

- simple individual motion;
- many interacting constraints;
- compressed mathematical representations of those constraints;
- and an exact underlying reality against which those representations can be checked.

That last property is especially valuable.

In ordinary human systems, a poor representation can survive for a long time because reality is noisy, delayed, contested, or only partly observable. In the Lonely Runner setting, a proposed witness either maps to a real common time and satisfies the runner constraints or it does not.

Mathematics therefore provides unusually sharp feedback when a compression has lost consequential information.

---

## 2. The recurring research pattern

Across the investigation, a repeated pattern emerged:

> **represent → compress → test → encounter a failure → identify the lost distinction → enrich or replace the representation → test again**

Examples in the project include distinctions between:

- blocking and collective coverage;
- total overlap and local overlap;
- overlap amount and overlap placement;
- separate projection marginals and a common compatible point;
- torus phase information and physical clock/lap recovery;
- positive-width safe intervals and isolated safe equality points;
- a compact selected menu and the richer source geometry from which it was compressed.

The important observation is not that richer representations always win. More information can create unnecessary cost and obscure the question being asked.

The useful question is:

> **What is the smallest representation that still preserves every distinction capable of changing the answer to the present question?**

That is a question-specific notion of adequacy.

A representation adequate for finding one witness may be inadequate for describing every safe time. A representation adequate for one structured family may fail when another independent degree of freedom is introduced.

---

## 3. Vance's scaling intuition

During the October 2 discussion, Vance proposed a different way to interpret the growth of Compatibility Calculus representations:

> As the number of independent participants increases, the number of relationships that may need to be represented can grow very rapidly. A larger representation may therefore be the natural cost of the underlying complexity rather than a defect in the method.

This is an intuition, not a proved complexity result.

No exponential lower bound has been established here. The relevant growth could be linear, polynomial, combinatorial, exponential, or highly problem-dependent depending on what interactions must be retained and what question the representation must answer.

But the intuition changes the research question.

Instead of asking:

> **Can we force the full representation to remain compact as the system scales?**

we can ask:

> **How much information is actually required to preserve the consequential compatibility relationships for the operation we want to perform?**

The distinction matters.

A representation that grows because it is carrying real independent relationships is different from one that grows because it is poorly designed or redundantly encoded.

---

## 4. More participants are not the same as more independent structure

The project has already exposed an important version of this distinction.

Adding runners to a system generated by the same two underlying parameters increases the number of constraints without necessarily increasing the dimensional freedom of the underlying motion.

The later rank-three experiment introduced a genuinely independent third parameter. That was a different kind of scaling event.

The compact menu that had performed strongly in the two-parameter setting did not transfer perfectly. Richer supplied sheets covered the finite test domain, and later an exact source-class obstruction showed that even the full supplied sheet class could fail while a physical lonely time still existed. The subsequent orbit-interval construction retained continuous intervals, isolated points, and clock lifts and recovered the tested cases.

This suggests a useful diagnostic distinction:

> **constraint count and independent representational rank are different sources of complexity.**

A system can acquire more participants while remaining highly structured. Conversely, one additional independent degree of freedom can invalidate a compression that handled many dependent participants.

---

## 5. When representation growth is not a problem

Suppose a complete high-resolution representation eventually becomes enormous.

That fact alone does not establish failure.

If the underlying problem contains an enormous number of consequential compatibility relationships, a large representation may simply be the price of not destroying them.

The relevant questions become:

- Does the representation preserve the relationships needed for the intended operation?
- Does it avoid carrying distinctions that cannot affect that operation?
- Can it recover richer source information when the operation changes?
- Can it expose where compression has become unsafe?
- Can the system carry the representation without transferring its full cognitive burden to the human?

Under this view, compactness is an engineering objective, not an absolute epistemic virtue.

A smaller representation is better only when it remains adequate.

---

## 6. The human-scale mistake

Humans naturally prefer compact representations because working memory, attention, communication, and time are limited.

That preference can quietly become a criterion for what we think a good model should look like.

But reality has no obligation to fit comfortably inside human working memory.

A complex system may contain more consequential distinctions than a person can simultaneously carry.

Historically, that has forced a tradeoff:

> **To make a system cognitively manageable, we often discard relationships that may still matter.**

AI changes that constraint.

A machine-supported system can maintain a representation whose complete state would be unreasonable to present to a person.

This suggests a separation between two scaling targets:

### Underlying representation

Scale with the consequential relationships required by reality and by the supported operation.

### Human-facing representation

Scale with the question, decision, or action the person currently needs to make.

The two representations need not be the same size.

---

## 7. A proposed principle

The October 2 discussion produced the following working principle:

> **Representation should scale with the consequential relationships in reality, not with human preference for simplicity. Human-facing views should scale with the decision.**

This is a design principle, not a mathematical theorem.

It suggests that a human–AI system should not optimize globally for minimum representation size.

Instead it should optimize for something closer to:

> **minimum sufficient resolution for the supported question, with a recovery path to richer state when the question changes or a contradiction appears.**

That is closely related to reversible compression.

---

## 8. Reversible compression

Compression is necessary.

The problem is not that we summarize. The problem is when the summary destroys access to distinctions that later become consequential.

A useful AI-supported architecture can therefore maintain:

- a high-resolution source representation;
- smaller task-specific representations;
- explicit statements of what each compression retains and omits;
- failure tests that expose when the compression is inadequate;
- recovery maps back to richer state;
- and human-facing views matched to the current decision.

The goal is not perfect reversibility. Every representation omits something.

The goal is **practical reversibility for consequential information**.

Lonely Runner has repeatedly demonstrated why this matters. When a compact representation fails while the physical solution still exists, the failure can be treated as evidence about what the representation omitted rather than evidence that the underlying solution disappeared.

---

## 9. Compatibility Calculus under this interpretation

Compatibility Calculus should therefore not be judged only by whether it produces an elegant fixed-size language for arbitrarily large runner systems.

A more useful question is:

> **Can it tell us what information must remain jointly compatible, what can safely be compressed for a particular operation, and when a richer representation is required?**

Under this interpretation, CC may be useful even if its complete representation grows substantially with independent complexity.

The research task becomes partly one of finding structure:

- which relationships can be factored;
- which constraints share a low-dimensional representation;
- which compatibility conditions require higher-order state;
- which exceptional sets need explicit retention;
- and which questions permit much stronger compression than others.

The current work does not establish that CC is the best language for these tasks. Existing mathematical frameworks may be superior in particular settings, and the repository's representation rules explicitly permit CC to be modified or replaced.

---

## 10. Why real value changes the scaling decision

Vance's second intuition was practical:

> If preserving the necessary representation at scale becomes expensive, that may be entirely reasonable when the problem being solved has enough real value. If the problem has little consequence, there may be no reason to pay that representational cost.

This reframes scaling as an economic and consequential question as well as a mathematical one.

A large compatibility model might be unjustified merely to demonstrate that a framework can represent fifty more synthetic participants.

The same representational cost could be entirely reasonable in a system where incompatibility causes major scientific, engineering, financial, operational, or human consequences.

The question is not:

> **Can we represent everything?**

It is:

> **Which consequential problems justify carrying which level of structure?**

This connects representation design to value.

---

## 11. Lonely Runner's role

This suggests a clearer role for the Lonely Runner project.

Lonely Runner does not need to be discarded in favor of a supposedly more "real" complexity problem.

It is already a valuable laboratory because:

- the rules are simple;
- the interactions become difficult;
- complexity can be increased deliberately;
- different kinds of scaling can be separated;
- representations can be frozen before tests;
- failures can be checked exactly;
- and the physical/mathematical reality can correct the model quickly.

It is therefore useful for discovering principles of representation and compatibility.

A later external domain would answer a different question:

> **Do those principles transfer when the ground truth is messier and the consequences are real?**

Lonely Runner can be the laboratory. Another domain can be the transfer test.

---

## 12. Implications for synergistic intelligence

The larger human–AI implication may be more important than any particular notation.

A person does not need to consciously hold the full state of a complex system in order to reason responsibly about it if the surrounding AI-supported system can:

- preserve consequential distinctions;
- maintain provenance and uncertainty;
- recover omitted structure when needed;
- detect incompatibility introduced by compression;
- and present the smallest adequate view for the current decision.

This changes the role of AI from merely producing better summaries to **carrying representational complexity that would otherwise exceed human working memory**.

The human can remain engaged at the level where judgment, meaning, responsibility, and choice are actually required.

The machine can carry a much larger substrate underneath.

This does not eliminate complexity.

It changes who or what must carry it.

---

## 13. A stronger formulation of the compression problem

The usual aspiration is often:

> simplify the problem.

The Lonely Runner experience suggests a more careful aspiration:

> **Simplify the human interface to the problem without simplifying the underlying representation beyond what the consequences permit.**

That distinction may be central to scalable human–AI reasoning.

The goal is not maximum detail.

The goal is not minimum detail.

The goal is:

> **the minimum sufficient representation for each operation, connected to enough richer state that consequential distinctions can be restored when needed.**

---

## 14. What this paper does not establish

Several boundaries should remain explicit.

This paper does not establish:

- that representation size must grow exponentially with runner count;
- a lower bound on the information required to solve Lonely Runner;
- that Compatibility Calculus is a new mathematical field;
- that CC is more efficient than conventional mathematical methods;
- that the current CC representations generalize to arbitrary runner configurations;
- that the Lonely Runner Conjecture has been solved;
- or that the principles described here automatically transfer to other domains.

Those are separate questions.

The paper records a conceptual development produced by repeated contact between intuition, mathematical representation, exact counterexamples, and AI-supported continuity.

---

## 15. Questions worth carrying forward

The discussion leaves several useful research questions.

**Representational lower bounds.** For a declared operation, can we prove that certain compatibility information cannot be discarded?

**Question-specific complexity.** How much smaller can a representation become when the requested output is one witness rather than the complete safe set?

**Independent rank versus participant count.** Which matters more for representational growth in particular families?

**Adaptive representation.** Can a system begin with a cheap compression and enrich only the regions where compatibility tests expose information loss?

**Human interface.** Can a person reliably reason over a small view while the AI carries a much larger substrate, with recovery triggered by contradiction or consequence?

**Value threshold.** When is the cost of maintaining a high-resolution representation justified by the consequence of the problem?

These questions connect the mathematical project to the broader study of synergistic intelligence without claiming that one domain has already proved the other.

---

## Conclusion

The Lonely Runner project has enlarged our understanding of compression.

The original lesson was that compression can erase distinctions of consequence.

The newer lesson is stronger:

> **As independent complexity grows, the representation needed to preserve consequential relationships may legitimately grow with it.**

If that is true, the goal should not be to force reality into a representation small enough for a human to carry.

The goal should be to let the underlying representation remain as rich as the problem requires, while allowing the human to interact with a much smaller, decision-relevant view.

That is a different vision of simplification.

It does not remove complexity.

It places complexity where it can be carried, preserves the distinctions that matter, and compresses only at the interface where compression is useful.

In that sense, the Lonely Runner investigation may be teaching us something larger than how runners avoid one another on a circle.

It may be giving us a controlled environment for learning how humans and AI can reason together about realities that are too structurally rich for either ordinary conversation or human working memory to hold in full.
