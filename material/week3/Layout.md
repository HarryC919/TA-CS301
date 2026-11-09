# Recitation 3 — Dynamic Programming and Greedy Algorithms

Status: approved layout. Implemented in `../../tools/site_src/recitation3-content.html`
and `../../site/recitation3.html`, with LCS/Huffman code under `solutions/` and generated
Python/Java notebooks under `../../site/notebooks/`. Open questions in §7 were resolved
with the proposed defaults (own 4-job instance, six-language Huffman, Huffman at the end
of the same notebooks, Sum of Products referenced by name only). Exercise timing
(15 + 25 minutes) was extended from the 30-minute target based on students' pace in
Recitation 2; keep calibrating.

## 1. Scope and learning goals

This Tuesday session covers the latter half of Week 2 (dynamic programming: Sum of
Products, Matrix Chain Multiplication) and the early Week 3 greedy lectures
(Activity Selection, Coin Change). Graph algorithms are outside this session.
Huffman coding appears only in the separate, optional Extra section.

Students should be able to:

- Follow a common path for a DP problem: define the subproblem, write the recurrence
  (the "key math function"), fix base cases and evaluation order, and reconstruct
  the answer.
- Count DP cost as (number of subproblems) × (work per subproblem).
- Explain what a greedy algorithm commits to, and why that commitment needs a proof.
- Give a counterexample when greedy fails (coin change with `{1, 3, 4}`) and explain
  why it succeeds for systems such as `{1, 5, 10, 25}`.
- Prove a greedy rule with an exchange argument (Earliest Due Date for `1 || Lmax`).
- Derive the LCS recurrence and implement a table fill plus traceback that returns
  one longest common subsequence.

Prerequisites: recursion, arrays/2-D arrays, sorting cost, and the lecture material
on DP and greedy already introduced. Big-O reasoning from Recitation 2 is reused.

## 2. Proposed page order

1. **Overview:** scope, goals, prerequisites, suggested session path.
2. **Review A — Solving a DP problem:** the five-step path, illustrated with Matrix
   Chain Multiplication (and a short reference to Sum of Products).
3. **Review B — Why greedy, and when it is right:** coin change as the running example.
4. **Core practice:** two exercises, about 40 minutes in total.
5. **Discussion and exit check.**
6. **Extra · Huffman coding:** new, clearly labeled optional section (not examined).

One page with direct anchors, following Recitations 1–2. The Extra section is
visually separated (its own banner/callout) so students do not treat it as core.

## 3. Concept review — approximately 12–15 minutes

### A. A common solution path for DP (about 6 minutes)

1. **Subproblem/state:** what does `OPT(i, j)` mean in words? Name the indices.
2. **Key math function (recurrence):** express `OPT` of a state through smaller
   states by enumerating the last/first decision.
3. **Base cases** and the **evaluation order** (top-down memoization vs bottom-up
   table; every dependency must be computed first).
4. **Answer location and reconstruction:** which cell holds the answer; how to store
   or recover the choices.
5. **Cost:** #states × work per state, plus table space.

Worked anchor: Matrix Chain Multiplication,
`m[i][j] = min over i ≤ k < j of m[i][k] + m[k+1][j] + p(i−1)·p(k)·p(j)`,
`m[i][i] = 0`, filled by increasing chain length; Θ(n²) states × O(n) choices = Θ(n³)
time, Θ(n²) space. Contrast with naive recursion recomputing overlapping
subproblems. Sum of Products is mentioned as a second lecture example of the same
path (see open question 1).

### B. Why greedy, and when it is right (about 7–9 minutes)

- Why: a greedy algorithm makes one locally best, irrevocable choice per step and
  never revisits it — usually simpler and faster than DP (e.g., sort + scan).
- Four proof methods: **exchange argument** (feasible and no worse; used in
  Exercise 1 and Huffman), **greedy stays ahead** (Activity Selection finish times;
  the measure must imply optimality), **greedy choice + optimal substructure** by
  induction (the overall frame), and the **cut property** (one-line preview of MSTs).
- Coin change, greedy "take the largest coin that fits":
  - Fails for `{1, 3, 4}` (6) and `{1, 10, 25}` (30); succeeds for `{1, 5, 10, 25}`.
  - Proof recipe: exchange rules bound the smaller coins' counts → their total R is
    below the next coin → an optimal solution takes ⌊N / c⌋ of it, like greedy → induct.
    Applied to divisibility chains (mixed-radix digits) and to US coins (not a chain,
    so the chain condition is sufficient, not necessary).
  - Optional "Try it": prove the 1–2–5 system greedy-optimal (collapsed answer).
  - Exact three-coin test for `{1, a, b}`, `b = qa + r`: greedy optimal ⇔ `r = 0` or
    `q + r ≥ a`; counterexample `N = a + b − 1` proves the failing direction only.
    Verified by brute force for all a < 30, b < 80.
  - Checklist ending with the DP fallback
    `C(a) = 1 + min over coins c ≤ a of C(a − c)`, `C(0) = 0`, Θ(amount · #coins).
  - Quick check: apply the three-coin test to `{1, 7, 10}`.
- Signed payment with change (negative counts) was considered and left out as tangential.

## 4. Core practice — approximately 40 minutes

### Exercise 1. Single-machine scheduling `1 || Lmax` — 15 minutes

- Format: short trace + written analysis; pseudocode supplied.
- Setup: n jobs, job j has processing time `p_j` and due date `d_j`; one machine,
  no preemption, all jobs available at time 0. Completion `C_j`, lateness
  `L_j = C_j − d_j`; minimize `Lmax = max_j L_j`.
- Supplied pseudocode: Earliest Due Date (EDD) — sort by `d_j`, run in that order,
  track the running completion time and maximum lateness.
- Tasks:
  1. Trace EDD on a 4-job instance and report the schedule and `Lmax`; compare one
     other order (e.g., shortest processing time first) that gives a larger `Lmax`.
  2. Analyze time and space complexity (Θ(n log n) dominated by sorting; Θ(n) scan).
  3. Explain why EDD is optimal: an adjacent-swap exchange argument — swapping an
     adjacent pair with `d_i > d_j` (i before j) never increases `Lmax`.
- Staged hints: what changes in a swap (only the two jobs' completion times); compare
  each new lateness with the old `L_i` or `L_j`.

### Exercise 2. Longest Common Subsequence — 25 minutes

- Part A, set up the key math function (about 10 minutes, written):
  - Define `L(i, j)` = LCS length of prefixes `X[1..i]` and `Y[1..j]`.
  - Guided questions: what if `X[i] = Y[j]`? What if not — which characters can be
    dropped? What are `L(0, j)` and `L(i, 0)`? In what order can the table be filled?
  - Fill a small table by hand (e.g., `X = "ABCBDAB"`, `Y = "BDCABA"`, length 4),
    or a smaller pair if timing requires.
- Part B, complete the code (about 15 minutes, coding):
  - Return one LCS string (not just its length). The starter provides the signature,
    table allocation, and loop skeleton; students fill the recurrence and write the
    traceback from `(m, n)`.
  - Because several LCSs may exist, checks verify the length and that the result is
    a subsequence of both inputs, not a specific string.
  - Edge cases: empty strings, no common character, identical strings, one string a
    subsequence of the other, repeated characters, and a 1,000 × 1,000 input for
    Θ(mn) time. Inputs are not modified.
  - Expected evidence: working code plus Θ(mn) time / Θ(mn) space explanation; mention
    that length-only needs just two rows, but reconstruction needs the full table
    (or extra work).
- Six languages (c, cpp, cs, java, py, js), matching existing conventions.

## 5. Discussion, feedback, and exit check

About 10–15 minutes: compare exchange-argument wording, review one common LCS bug
(off-by-one between table indices and string indices; traceback tie handling), and
connect "greedy fails" back to "use DP". Staged hints, self-checks, and collapsed
reference explanations provide the feedback path.

Exit check: "Greedy is optimal for `1 || Lmax` but not for coin change with
`{1, 3, 4}`. In one or two sentences, what does the EDD proof use that fails for
those coins?"

## 6. Extra · Huffman coding (optional, not examined)

A new recurring section type: a TA-provided algorithm extending the course idea,
for students who want to go further. It must not be a prerequisite for core work.

- **Why:** fixed-length codes waste bits when symbol frequencies are skewed; we want
  a prefix-free variable-length code minimizing total bits `Σ f(c)·depth(c)`.
  Prefix-free codes ↔ binary trees with symbols at leaves, so decoding is unambiguous.
- **How:** repeatedly merge the two least-frequent trees (a greedy choice) using a
  min-priority queue; n − 1 merges → O(n log n). Brief intuition for why the greedy
  choice is safe (the two rarest symbols can be deepest siblings — the same
  exchange idea as Exercise 1); no formal proof required.
- **Pseudocode** and a small worked example (e.g., 6 symbols with frequencies,
  resulting tree, code table, and total bits vs a fixed 3-bit code).
- **Build it:** students implement Huffman code construction.
  - Proposed interface: input frequencies `freq[0..n−1]` (n ≥ 1); return the code
    string for each symbol index. Single-symbol input gets code `"0"`.
  - Checks verify prefix-freeness and optimal total cost (codes are not unique,
    so exact strings are not compared), plus a small encode/decode round trip.
  - Six languages. Java/C++/C#/Python have standard priority queues; the C and
    JavaScript starters include a small provided min-heap helper so the task stays
    on Huffman itself.
- Collapsed reference solutions on the page; stubs and checks in the notebooks.

## 7. Open questions for review

1. **Sum of Products:** which formulation did the lecture use? I will reference it
   only by name in Review A unless you want it worked through as well.
2. **Exercise 1 instance:** fine to choose my own 4-job instance, or do you want the
   lecture's notation/example?
3. **Huffman languages:** six languages (as proposed) or Python/Java only to match
   the notebooks?
4. **Notebooks:** put the Huffman task at the end of the same Python/Java notebooks
   under an "Extra (optional)" heading (proposed), or ship separate notebooks?

## 8. Next stage after approval

- Write `tools/site_src/recitation3-content.html` (shared notes/prompts/hints/answers)
  and `tools/site_src/build_recitation3.py`, reusing Recitation 2's tabs and
  markdown conversion; solutions/contracts under `material/week3/solutions/`
  (LCS and Huffman), notebook checks under `material/week3/checks/`.
- Generate Python/Java notebooks; update `site_layout.py`, Home directory and
  `.hero-slots` badges, README inventory, AGENTS source map and counts,
  `test_notebook_format.py`, `verify_notebooks.sh`, `test_code_ui.cjs`, and add
  `tools/verify_week3.sh`.
- Rebuild and run all checks listed in AGENTS, plus desktop/mobile screenshots.
  No commit without your authorization.
