# Execution and correction record

September 29, 2026. Live source head at start:
57997d4220226b44b9a89d8d8139926f15cca90c.

1. Verify the live branch, instructions, existing package layout and source
   Git identities. Restore exact package files into the local partial snapshot
   without changing them.
2. Freeze PROTOCOL.md before implementation or new controls. It specifies
   the interface, branch precedence, coefficient/physical inputs and CLI modes.
   INPUTS.json retains its SHA-256.
3. Assign arithmetic and contract reviewers. Both derive branch strictness
   and totality before reading the runtime. Arithmetic reconstruction uses
   endpoint interval intersection and coordinate congruences, with no
   production imports.
4. Implement cc_coefficients.py and its JSON CLI with explicit arithmetic
   gates. A frozen accepted CLI smoke control passes. Write five unittest
   methods and the validation harness. The first complete coordinator run
   passes without an implementation correction.
5. The arithmetic reviewer derives the baseline and large cases separately,
   then audits serialized outputs. All 27,401 field comparisons pass. The
   declared precedence changes 40 baseline failure identities but no verdict.
6. The contract reviewer reads the implementation, tests and saved records;
   no defect is found. It distinguishes static review and stored evidence from
   executing another test suite. Findings are shared; this is not blind review.
7. Write usage, reproduction and continuity records. Repeat only the frozen
   validation and audit for byte-for-byte reproduction.
8. Final note review replaces the ambiguous phrase "universal failure of a
   rule" with "failure of the rule's universal guarantee": one failed input
   refutes uniform success without saying that every input fails. It also
   makes the optional requested-pair recovery cost explicit. No code changed.
9. Rebase publication on 2445c5ea4082e146d9b4617826746e560cbaac63,
   the concurrent seventh visual section. Merge only its README and HANDOFF
   additions into our continuity edits; preserve every visual artifact through
   that commit's base tree. The mathematical input pin remains 57997d4.

## Review-harness adjustment

The first serialized audit reached CLI scope comparison and found two
assumed placements differed from the declared commands: the missing-q case
used p=2 rather than p=4, and invalid text `two` appeared in B rather than A.
The reviewer aligned these descriptors. No production behavior, mathematical
criterion, trial or protocol changed. Its report preserves the adjustment.

## Scope retained

The 480 coefficient cases are 216 old representatives, 216 prescribed
periodic shifts and 48 analytic large-slope controls. The 62 direct physical
cases are 54 archived configurations plus eight named controls. Fifteen
invalid API cases and 18 CLI records preserve error semantics, repeated-speed
flags and optimization mode. No wider scan, optimizer, changed reference,
outside contact, main merge or unattended work occurred.

The runtime has no proof-output dependency. Mathematical source identity and
checked runtime identity remain separate. Proof-candidate status, literature
attribution and originality limits are unchanged. The proposed row (3,8)
compiler transfer has not been run.
