# Two added speeds at one sixth – test fixed before execution

Fix reference 0 and core speeds 1, 2, 4, 8, ... . Include every integer pair 1 <= r < s <= 128, including repetitions of a core constraint. Equality is allowed. The control (3,5) has optimum 1/6, by the consecutive speeds 1 through 5 and witness 1/6.

Enumerate reduced fractions a/q in (0,1/2] with q <= 256, in increasing q then a. Check the entire doubling orbit by following residues to a repeat. For each pair, record its first common witness or mark a catalog miss. Validate returned witnesses by an independent check using exact rational arithmetic. Report totals, largest first denominator and its cases. For each miss, intersect the closed allowed intervals for the extras and the dyadic prefix through 2^10. An empty intersection disproves the infinite-core statement. A nonempty intersection leaves it unresolved by this check. Preserve equality points.

Separately pursue a proof from the base-four set with digits 1 and 2, including the case of widely separated extra speeds. Any extensions after the bounded check are exploratory.
