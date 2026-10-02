# Proposed two-segment certificate, before new computations

The coefficient rows are (1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(5,2).
Put z=1/8. The actual orbit is h=qx-y integral and physical time is t=x.

E1 is the edge of parent P1 with six laps (0,0,0,0,0,1),
x in [1/8,5/24], y=7/8-3x. Its seventh lap is 1. The seven fractional
forms are x, 7/8-3x, 7/8-2x, 7/8-x, 7/8, 3/4-3x, 3/4-x.
All should remain in the closed band [1/8,7/8]. The fifth fixes separation
at exactly 1/8. Projecting this same edge to the orbit gives
[(q-4)/8,(5q-6)/24]. Its first integer is h1=ceil((q-4)/8)=(q+3)//8.
Accept if 24h1<=5q-6 and recover t=(8h1+7)/(8(q+3)).
The interval width is (q+3)/12, at least one for q>=9. Of q=2,...,8,
only q=5 should fail. An alternative symbolic check uses q=8a+r:
h1=a+epsilon_r, epsilon_r=1 for r>=5 and zero otherwise. The upper-end
margin after multiplication by 24 is 16a+5r-6-24epsilon_r.

E2 is the edge of parent P3 with six laps (0,0,0,1,1,1),
x in [3/8,1/2], y=9/8-2x. Its seventh lap is 2. The seven fractional
forms are x, 9/8-2x, 9/8-x, 1/8, 1/8+x, 5/4-x, 1/4+x.
Its fourth fixes separation at exactly 1/8. The orbit interval is
[3(q-1)/8,(4q-1)/8]. Its first integer is h2=(3q+4)//8.
Accept if 8h2<=4q-1 and recover t=(8h2+9)/(8(q+2)).
For the sole remaining q=5, h2=2 and t=25/56. Expected physical laps
are (0,2,2,3,3,5,6), and fractional numerators over 56 are
(25,13,38,7,32,45,39).

Select by the two ordered closed interval tests, not by searching orbit labels.
The physical lap for row (a_i,b_i) is m_i+b_i h. An exact continuous phase
certificate and universal integer coverage would establish one physical
witness for all q>=2 without the seven-form spectrum. The discarded geometry
remains necessary for stronger questions such as optimization or all safe times.
