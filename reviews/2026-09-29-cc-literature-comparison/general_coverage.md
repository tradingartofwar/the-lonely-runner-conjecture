# General coverage review — September 29, 2026

Separately tasked AI literature review under `PROTOCOL.md`. This is a source
comparison, not an independent verification of the source's proof or programs.
The repo's two-parameter construction remains an internally reviewed proof
candidate. No physical scan or new optimization was run.

## Inspected result

Matthieu Rosenfeld, *The lonely runner conjecture holds for eight runners*,
[arXiv:2509.14111v2](https://arxiv.org/abs/2509.14111v2), revision October 16,
2025. Read the [HTML](https://arxiv.org/html/2509.14111v2) and
[PDF](https://arxiv.org/pdf/2509.14111v2): section 1, Conjecture 2 and Theorem 1;
section 4; section 6. The surrounding domain is seven distinct positive integer
moving speeds, common start, with a stationary reference. Theorem 1 asserts a
simultaneous distance at least 1/8. Section 4 uses a finite computer verification
with arithmetic bounds. That verification and its implementation were not
reproduced here.

Theorem 1's displayed wording says integers without repeating positivity;
Conjecture 2 and the preceding domain supply it. We use only positive speeds.
The arXiv revision date differs from the PDF's October 17, 2025 title date and
the HTML's August 24, 2026 title date. Pin the identifier and submission history;
do not use the rendering date as the revision date.

## Publication metadata needs the correct evidence label

The inspected arXiv abstract page does not list a journal reference. However,
search retrieval of the official AMS *Mathematics of Computation* journal index
lists this title and author with [DOI 10.1090/mcom/4243](https://doi.org/10.1090/mcom/4243)
and electronic publication August 10, 2026. Direct journal and DOI opens failed
(403 or inaccessible). Thus the electronic-publication entry was observed in
indexed publisher content; the journal article itself was not opened or compared
with arXiv. Avoid describing it unqualifiedly as only an unpublished preprint,
and avoid claiming a journal-version theorem comparison. The mathematical scope
comparison below rests on the inspected arXiv version.

## Application to our family — our deduction

Let p,q be positive integers with p != q. Each member of

\[
V(p,q)=(p,q,p+q,2p+q,3p+q,3p+2q,5p+2q)
\]

is a positive integer. The third member exceeds the first two. From the third
onward the increments are p,p,q,2p, all positive. The first two differ by
assumption. Therefore this is a set of seven distinct positive integers,
directly in the inspected theorem's scope. No change of coordinates, sign,
parameter order, or time scaling is needed to establish applicability. Our
gcd normalization is needed by our particular orbit recovery, not by this
theorem application.

Consequently, the family-wide stationary-reference existence statement is
already implied by Rosenfeld's reported result. It should not be presented as
new family coverage relative to the literature. The two-parameter extension
is progress in this repository's explicit construction.

This is a straightforward hypothesis check, not a claim that our code has
independently certified Rosenfeld's theorem. Nor does invoking the theorem
certify our two segments, exception list, endpoint handling, Bezout recovery,
physical lap formula, or operation counts. Those remain separate obligations
addressed by the local proof package.

## What remains a distinct question

| Question | Assessment |
| --- | --- |
| Existence of some stationary-reference 1/8-safe time for every pair | Covered by the inspected general literature result. |
| Our fixed P3/P1 segments, two exceptional primitive pairs, exact recovery and implementation | A concrete certificate to compare and review in its own right; this application of the general theorem does not supply those details. |
| Minimum distance exactly 1/8 at our selected time | Our certificate's output property; it is not the global optimum. |
| Exact optimum, all maximizers, or the full safe set for general p,q | Not established by the present witness package. |
| Novelty of the elementary family-specific certificate | OPEN. This review establishes prior existence coverage, not originality or absence of an earlier equivalent construction. |

Our construction is self-contained in the sense that its written safety,
coverage, and recovery proof does not use Rosenfeld's computational result as a
premise. Calling that an alternative elementary proof candidate for this family
is justified by the actual local argument. Calling it a newly solved family is
not. A theorem about existence and a reproducible compact witness procedure
answer different questions; their evidentiary statuses must stay attached.

## Exact-family search limits

Bounded searches used literal variations including `lonely runner` with
`5p+2q`, `5p + 2q`, `5A+2B`, `3a+2b`, `seven speeds` plus `two-parameter`,
and `two segments`, across both available search systems. No returned primary
source was identified as an exact match to our seven-form/two-segment
certificate. Results were often irrelevant, which signals weak recall for
formula searches rather than strong evidence of absence. Closest six-form
literature is assigned to a separate reviewer.

This was not an exhaustive search over symbol choices, affine parameter
changes, sign changes, permutations, or every literature reference. The lack
of a located match cannot support a novelty claim. There is no need to audit
later 9–15-runner claims to answer the fixed existence question.

## Information-loss checkpoint

The consequential distinction is **new construction versus new coverage**.
Compressing both to "we covered the full family" obscures the existing general
result and changes the apparent significance. Retain the source theorem and
hypothesis translation next to the local certificate. Also retain publication
metadata provenance separately from the version whose theorem was read. The
smallest adequate conclusion is that the literature already supplies existence,
while this project supplies a reviewable elementary construction candidate.

## Coordinator synthesis signoff

Read `notes/CC_LITERATURE_COMPARISON_2026_09_29.md` after drafting. Within this
reviewer's assigned general-coverage scope, no necessary correction was found.
The synthesis distinguishes existing family-wide existence from the local
explicit construction and keeps certificate originality open. Its Rosenfeld
version, reading, non-reproduction, indexed publication-entry, and failed
direct-publisher-access labels match the evidence inspected here. This signoff
does not extend to an independent audit of the other reviewers' source claims
or mathematical adaptations. No additional web retrieval or computation was
performed for this signoff.
