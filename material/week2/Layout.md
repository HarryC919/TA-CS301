# Recitation 2 — Asymptotic Notation and Divide and Conquer

Status: approved layout. Implemented in `../../tools/site_src/recitation2-content.html`
and `../../site/recitation2.html`, with merge code under `solutions/` and generated
Python/Java notebooks under `../../site/notebooks/`. The timing estimates remain
to be calibrated with students.

## 1. Scope and learning goals

This Tuesday session connects Week 1's asymptotic notation with Week 2's divide
and conquer. Use actual lecture progress before recitation to set the depth.
Dynamic programming and Extra Content are outside this session's scope.

Students should be able to:

- Distinguish O, Ω, and Θ, and justify a tight bound for a simple running-time function.
- Separate an asymptotic bound from the choice of best, worst, or expected case.
- Identify divide, conquer, combine, and base-case steps in an algorithm.
- Explain a simple recurrence using work per level and recursion-tree depth.
- Implement a linear merge step and connect its cost to merge sort's recurrence.

Prerequisites: basic loops, arrays, functions, recursion, and the lecture material
already introduced. Briefly scaffold recursion if needed. Existing Recitation 1
sorting notes are a reference, not required pre-work.

## 2. Proposed page order

1. **Overview:** scope, learning goals, prerequisites, and the suggested practice path.
2. **Concept review:** notation, growth rates, and the divide-and-conquer framework.
3. **Core practice:** three exercises, targeting 30 minutes in total.
4. **Optional practice:** clearly separated from the timed core path.
5. **Discussion and takeaways:** reasoning, common errors, and a short exit check.

Keep notes and exercises on one page with direct anchors, following Recitation 1's
navigation pattern. Final delivery details are deferred until the content is approved.

## 3. Concept review — approximately 10–15 minutes

### A. Describe growth precisely

- O as an asymptotic upper bound, Ω as a lower bound, and Θ as a tight bound;
  introduce their constant-and-threshold definitions with one small example.
- Constants, lower-order terms, and the ordering of common growth rates.
- A valid O bound need not be tight. O does not mean “worst case,” and Ω does not
  mean “best case”; identify the running-time function being bounded first.

### B. Connect growth to recursive work

- Divide → conquer → combine, with an explicit base case and decreasing subproblem size.
- Use binary search as a bridge: one surviving half-sized subproblem and constant
  work per call. Note that this is more precisely decrease-and-conquer.
- Use merge sort as the main divide-and-conquer example: two recursive subproblems
  and linear combining work. Build the recurrence and explain its recursion tree.
- Briefly contrast balanced and highly unbalanced quicksort partitions, if quicksort
  has been taught before this session. Do not assume every recursive algorithm has
  logarithmic running time, or that splitting in half is sufficient by itself.

Use small traces and level-by-level reasoning; do not require the Master Theorem.
Reuse selected sorting examples rather than repeat Recitation 1's full walkthroughs.

## 4. Core practice — approximately 30 minutes

### Exercise 1. Is the bound valid, tight, or unjustified? — 6 minutes

- Format: short written reasoning, optionally discussed in pairs.
- Outline: classify a small number of O/Ω/Θ claims about simple functions and
  correct a claim that confuses bound notation with best/worst-case analysis.
- Expected evidence: a short growth argument; include one constant-and-threshold
  justification rather than requiring a formal proof for every item.

### Exercise 2. Where does the work go? — 8 minutes

- Format: complete an annotated recurrence and a small recursion tree.
- Outline: identify recursive-call count, subproblem size, and combining work for
  standard merge sort; account for work at each level and the number of levels.
- Expected evidence: explain the resulting Θ(n log n) time bound. Use powers of two
  for the first analysis and state a constant-size base case.
- Follow-up for discussion: why does binary search have a different bound even
  though it also halves the problem size?

### Exercise 3. Implement the combine step — 16 minutes

- Format: scaffolded coding plus a brief correctness/complexity explanation.
- Outline: merge two sorted integer arrays into a new sorted array, preserving all
  elements and leaving both inputs unchanged. Supply the interface and starter
  structure; students do not need to write the entire recursive merge sort.
- Include checks for empty inputs, unequal lengths, duplicates, and leftover elements.
- Expected evidence: working merge logic, a short explanation of why the next chosen
  element is safe, and linear time/output-space analysis in the total input length.
- Connect the helper's cost back to Exercise 2. No library sorting calls.

Timing is an initial estimate to calibrate when the full prompts and scaffolds are
written. Students may use hints and are not expected to finish optional exercises.

## 5. Optional practice — outside the 30-minute core path

- **Loop growth:** contrast sequential loops, triangular nested loops, and repeated
  halving/doubling; justify counts rather than classify by visual nesting alone.
- **Quicksort partition shapes:** compare a balanced split with repeated 0 and n−1
  splits and explain their different total work. Include only after lecture coverage;
  label any new derivation as scaffolded practice, not assumed prerequisite knowledge.

These extend the requested syllabus topics; they are not the separate non-exam
Extra Content listed in `../WeeklyContent.md`.

## 6. Discussion, feedback, and exit check

Reserve approximately 15 minutes for comparing reasoning, reviewing one merge bug,
and connecting code cost to the recurrence; leave remaining session time for questions.
Use staged hints and self-checks, with reference explanations available for review.
AI-assisted answers should still be explained and verified by the student.

Exit check: explain why “the array is halved, so the algorithm takes O(log n) time”
is insufficient without knowing the number of recursive calls and work per call.

## 7. Next stage after approval

- Expand this layout into concise notes and complete prompts, examples, hints,
  starter interfaces, reference explanations, and edge-case checks.
- Calibrate the core path against the 30-minute target; reduce subparts if necessary.
- Then implement the Recitation 2 page through the site source/build pipeline and
  agree on notebook delivery. Do not advertise downloads before artifacts exist.
- Rebuild and perform the applicable structural, code/notebook, and browser checks
  before marking the page ready. No site changes are part of this layout draft.

Reference for the merge-sort recurrence and recursion-tree explanation:
[MIT 6.006, Lecture 3: Insertion Sort, Merge Sort](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/resources/lecture-3-insertion-sort-merge-sort/).
