# Sealed four-weight prediction trial

**Question.** Can a rule built from a family definition predict a lonely time for a previously unseen lineup, with a reason that continues to hold as the speed parameters grow? The two teams worked separately. The setter chose the family and sampled instances without testing for witnesses. The solver saw only the public definition and later the strata and hashes. All statements target stationary runner zero and clearance at least $1/16$. By complement symmetry the total-speed runner has the same clearance.

**Public definition.** Use all 15 nonempty subset sums of positive integers $a,b,c,d$ with $b>a$, $c>a+b$, $d>a+b+c$, gcd one and $16\mid S=a+b+c+d$. The partial sums generalize the binary weights whose subset sums are $1,\ldots,15$. The total speed blocks every time with denominator dividing 16. There are 60 sealed lineups, three in each of four scale bands and five gap regimes. No holdout may be discarded. No sampled input has been opened when this protocol and predict.py are committed.

**Predeclared rules, in order.** The program returns the first applicable certificate and otherwise abstains. It never enumerates the 15 opponents, samples candidate times, or calls a clearance oracle.

1. If the three lower generators share a nonzero residue mod 5, anchor them at phase $1/5$, then move the total to the prescribed nearby phase $+1/15$ or $-1/15$. This should give exact clearance $1/15$.
2. In the first-lap range $S\le15a$, use $1/(S+a)$.
3. At half a lap the odd speeds are safe. Let $E$ be the least positive even subset sum and $O$ the largest odd subset sum. If $S\le15E$ and $O\le7E$, shift forward by $1/(16E)$.
4. Put $C=a+b+c$ and $g=\gcd(a,b,c)$. If $g(14a-C)\ge16a$, start at $1/(16a)$ and add a multiple of $1/g$ that puts the sole fast generator in $[1/16,(15a-C)/(16a)]$.
5. Try to align the fast generator while all three lower generators stay on their first laps. With $k=\lceil(d-a)/(16a)\rceil$, use $(16k+1)/(16d)$ if $C(16k+1)\le14d$. Together with rule 4 this covers the entire independently scaled binary-prefix subfamily $(a,2a,4a,d)$ under the public conditions.
6. For the four weights successively, choose the least possible nonnegative lap index leaving their unwrapped phases individually at least $1/16$ and their total at most $1-(5-i)/16$ through index $i$. Preserve the previous interval at each choice. Return the midpoint of the final interval, if nonempty.
7. If $a/b+(a+b)/c+(a+b+c)/d\le11/16$, align each new generator upward at phase $1/16$ using exactly one rounding per step.

**Scoring.** Generate the complete prediction list before computing any true clearances. For each predicted time verify all 15 physical distances with integer arithmetic. Any unsafe prediction falsifies that rule. Any abstention means the rule did not solve the whole family. Compare on identical inputs against (i) the simpler first-lap formula used unconditionally, (ii) the pre-existing one-output divisibility predictor frozen at 43c53db, and (iii) a larger budget scan of all reduced rational times up to denominator 32. The last uses all such time classes up to reflection (exact size reported by the scorer). If all three and the new method miss an instance, use an exact interval check for that instance. Report overlaps and misses, not just totals. The new rule can perform four winding calculations and bounded arithmetic selection; single-output competitors have different preprocessing costs. A universal success claim needs an argument for every legal set of parameters in addition to the sample results.

Sealed panel SHA-256: 8b68c80e3af724ccdd4436e682e052d357bba6e8b477922a00430abdda9e9830
Generator SHA-256: 9e2d5701b771ba0b52273a6e34db2d91754134c05fa275fe871ebd529d3ed8c0
Raw seed SHA-256: a34e9480ae761947d7f7001e7589704048822b95156708692d37454c48ffbde6

