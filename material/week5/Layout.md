# Recitation 5 — Hash Tables and Introduction to Databases

Status: approved layout, revised. First approved with relational algebra and a
45-minute core (Exercise 2 gets 30 minutes, because students have needed more time
for coding). Lectures have since reached only the introduction to databases (data,
databases, database systems with data models, DDL, and DML, and DBMSs), so the
owner asked to shorten the database part: the relational algebra review and
exercise were replaced by an introduction-to-databases review and a 10-minute
concept exercise, and the core is now about 40 minutes. The relational algebra
version is in Git history (commit 4c33187) if a later session needs it.

This session covers the latter half of Week 4 (hash tables) and the first Week 5
lecture (introduction to databases). The Red-Black Tree, listed under Week 4 as
recitation Extra Content, appears only in the separate optional Extra section.

## 1. Scope and learning goals

Students should be able to:

- Explain what a hash function must do, compare the division and multiplication
  methods, and say what problem universal hashing solves (an adversary who knows
  a fixed hash function can force every key into one slot).
- Trace insertions under linear probing, quadratic probing, and double hashing,
  and explain primary clustering using the probe counts.
- Explain why deleting from an open-addressing table must leave a *deleted*
  marker (tombstone) instead of an empty slot, and what that costs later.
- Implement an open-addressing map with double hashing (`put`, `get`, `remove`)
  using only plain arrays, and state its expected and worst-case costs.
- Distinguish data, a database, a database system, and a DBMS, and tell a schema
  from an instance.
- Classify operations as DDL or DML, and match the problems of file-based storage
  to the DBMS features that solve them.

Prerequisites: arrays and modular arithmetic; "expected cost" from earlier weeks. No SQL and no database software are used in this session.

## 2. Proposed page order

1. **Overview:** scope, goals, prerequisites, suggested session path.
2. **Review A — Hash functions and open addressing.**
3. **Review B — Introduction to databases.**
4. **Core practice:** two exercises, about 40 minutes in total.
5. **Optional practice** (written, collapsed answers).
6. **Discussion and exit check.**
7. **Extra · Red-Black Trees** (optional, not examined; separated as in
   Recitations 3 and 4).

One page with direct anchors, following Recitations 1–4.

## 3. Concept review — approximately 12 minutes

### A. Hash functions and open addressing (about 7 minutes)

- **Goal:** map a key from a large universe into one of `m` slots so keys spread
  out evenly. Load factor α = n / m.
- **Division method:** `h(k) = k mod m`. Choose `m` prime and not close to a power
  of 2; with `m = 2^p` only the lowest `p` bits of the key matter.
- **Multiplication method:** `h(k) = ⌊m · frac(k · A)⌋` for a constant `0 < A < 1`.
  The choice of `m` matters less (powers of 2 are fine).
- **Universal hashing:** choose the hash function at random from a family such that
  any two distinct keys collide with probability at most 1/m. No fixed input can be
  bad for every choice, so the expected cost holds for every input.
- **Open addressing:** all keys live in the table itself; on a collision, follow a
  probe sequence `h(k, 0), h(k, 1), …`
  - Linear: `(h'(k) + i) mod m`; simple, but forms long runs (primary clustering).
  - Quadratic: `(h'(k) + c₁i + c₂i²) mod m`; avoids long runs, but keys with the
    same start share a sequence (secondary clustering) and, for bad `c₁, c₂, m`,
    may not reach every slot.
  - Double hashing: `(h₁(k) + i · h₂(k)) mod m`; with `m` prime and
    `1 ≤ h₂(k) < m`, the sequence visits every slot.
- **Insert / search / delete:** search stops at an empty slot. Delete therefore
  writes a DELETED marker: search skips over it, insert may reuse it.
- **Cost (uniform hashing assumption):** expected probes for an unsuccessful search
  at most 1 / (1 − α); worst case Θ(m). Tombstones count toward α for search time.
- **Perfect hashing** (one sentence plus a line in the table): for a static key set,
  two levels of universal hashing give O(1) worst-case search with O(n) expected
  space.

### B. Introduction to databases (about 5 minutes)

- Data, database, DBMS, and database system, each in one line.
- Why not files: a table pairing each file-system problem (redundancy and
  inconsistency, difficult access, integrity rules in code, partial updates after a
  failure, concurrent-access anomalies, security) with the DBMS feature that removes it.
- Data models (relational, entity-relationship, semi-structured); schema vs
  instance; physical, logical, and view levels; physical data independence.
- DDL (defines the schema; stored in the data dictionary) vs DML (queries and
  changes the instance; mostly declarative); SQL (Week 6) contains both.
- Inside a DBMS: storage manager (including indexes such as hash tables), query
  processor, transaction manager.

## 4. Core practice — approximately 40 minutes

### Exercise 1. Database concepts — 10 minutes (written)

Record types `Student(sid, sname, major)`, `Course(cid, title, dept)`, and
`Takes(sid, cid, grade)`.

1. **DDL or DML?** (3 min) Seven requests: create Student with key `sid`, add a
   student, list CS majors, restrict grades to A–F, change a major, remove the
   Takes record type, delete one student's enrollments. *Reference:* DDL (a), (d),
   (f); DML (b), (c), (e), (g); the constraint is DDL, and dropping a record type
   (DDL) differs from deleting its rows (DML).
2. **Schema or instance?** (2 min) Student's attributes and the unique-`sid` rule
   are schema; "student 3 is Chen" is instance; adding a student changes only the
   instance.
3. **Diagnose a file-based system** (5 min). Four stories: a major updated in one
   of two files (redundancy and inconsistency → one integrated database), a crash
   mid-transfer (atomicity → transactions and recovery), two editors overwriting
   each other (lost update → concurrency control), and a question that needs a new
   script (difficult access → declarative query language).
- Staged hint: does the request change the design or the contents?

### Exercise 2. Build an open-addressing hash table — 30 minutes

**Part A — trace (7 min, written).** `m = 11`, `h₁(k) = k mod 11`,
`h₂(k) = 1 + (k mod 10)`. Insert 22, 1, 13, 11, 24, 33 (verified by script):

| Probing | Final slots | Probes for 11, 24, 33 |
| --- | --- | --- |
| Linear | 0:22, 1:1, 2:13, 3:11, 4:24, 5:33 | 4, 3, 6 |
| Double hashing | 0:22, 1:1, 2:13, 4:11, 7:24, 8:33 | 3, 2, 3 |

Then: delete 11 by writing EMPTY into its slot and search for 33 under double
hashing. What goes wrong? (33 probes 0 → 4 → 8; the search stops at the now-empty
slot 4 and reports "not found".) This motivates the tombstone rule in Part B.

**Part B — implement (23 min, coding).**

- Task: a fixed-capacity map from non-negative integer keys to non-negative integer
  values, open addressing with double hashing as in Part A. Only plain arrays are
  allowed: no `dict`/`set`, `HashMap`/`HashSet`, `Dictionary`, `Map`/`Set`,
  `unordered_map`, or similar.
- Interface (same in all six languages, with names adapted to each language's style):
  - `HashTable(m)` — `m` is a prime ≥ 3.
  - `put(key, value) → bool`: insert or update; `false` only if the key is new and
    no EMPTY or DELETED slot remains.
  - `get(key) → int`: the value, or −1 if absent.
  - `remove(key) → bool`: `true` if the key was present.
  - `size() → int`.
- Starter: slot-state arrays (EMPTY / OCCUPIED / DELETED), `h1`, `h2`, and
  `probe(key, i)` are given. Students write the three probe loops.
- Two bugs to diagnose (each checked by a self-check and explained in a written
  Markdown cell):
  1. Delete writes EMPTY → the Part A failure (`m = 7`: put 10 → slot 3, put 17 →
     slot 2 after colliding at 3; remove 10; `get(17)` must still return its value).
  2. `put` stops at the first DELETED slot without checking further → a duplicate
     key. `put` must remember the first DELETED slot but keep probing until EMPTY
     (or `m` probes) to make sure the key is not already stored further along.
- Checks: empty table, update of an existing key (size unchanged), remove of a
  missing key, re-insert after remove, both bugs above, a completely full table
  (`put` of a new key fails, update still succeeds), a table holding only
  tombstones (search must stop after `m` probes, not loop forever), and a larger
  randomized run (e.g., m = 10,007, about 5,000 mixed operations) compared against
  a simple reference built from a plain list.
- Expected written evidence: expected O(1 / (1 − α)) probes per operation under
  uniform hashing and Θ(m) worst case; O(m) storage for the table itself; why `m`
  prime matters for double hashing; why tombstones eventually require rebuilding
  the table.
- Six languages (c, cpp, cs, java, py, js), matching stubs, references, and
  harnesses as in earlier weeks.

## 5. Optional practice (written)

1. With the division method and `m = 16`, which keys collide among 16, 32, 48, 64?
   Why does a prime `m` such as 17 help here?
2. Quadratic probing with `h(k, i) = (k + i²) mod 8`: starting from slot 0, list
   the slots reached. Can an insertion fail even though the table has an empty
   slot?
3. Why does a random choice from a universal family protect against an
   adversary, when no single fixed hash function can?
4. Physical data independence: adding a hash index on `Student.sid` and moving to
   faster disks changes no application program, only the physical level.

## 6. Discussion, feedback, and exit check

About 10–15 minutes: compare the linear and double-hashing probe counts from
Exercise 2A, and discuss which test cases catch each bug. Staged hints, self-checks,
and collapsed reference explanations provide the feedback path.

Exit check: "A DBMS has to find a student by `sid` quickly. Which structure from
today could it use, and what could that structure not answer quickly?" (A hash
index gives expected O(1) lookups but no range or order queries; those need an
ordered index such as a balanced search tree.)

## 7. Extra · Red-Black Trees (optional, not examined)

Proposed as a short, notes-only section:

- The five properties, and why they keep the height at most 2 log₂(n + 1).
- Left and right rotations as the local repair step.
- Insertion fix-up cases (uncle red: recolor; uncle black: one or two rotations)
  with one worked example inserting a short key sequence, figures as inline SVG.
- One short trace question with a collapsed answer. No coding task.

## 8. Next stage after approval

- Write `tools/site_src/recitation5-content.html` (shared notes/prompts/hints/
  answers, `data-web-only` for figures) and `tools/site_src/build_recitation5.py`,
  reusing the existing tabs, table styles, and Markdown conversion.
- Hash table solutions and contracts under `material/week5/solutions/hashtable/`;
  notebook checks under `material/week5/checks/`.
- Python/Java notebooks: Exercise 1 and Exercise 2A as Markdown answer cells,
  Exercise 2B as code cells with self-checks and a Markdown explanation cell. No
  SQL or database setup.
- Update `site_layout.py`, Home directory and `.hero-slots` badges, README
  inventory, AGENTS source map and counts (Recitation 5 is no longer a
  placeholder), `test_notebook_format.py`, `verify_notebooks.sh`,
  `test_code_ui.cjs`, and add `tools/verify_week5.sh`.
- Rebuild and run all checks listed in AGENTS, plus desktop/mobile screenshots.
  No commit without your authorization.

## 9. Decisions

1. **Database scope:** introduction to databases only; relational algebra moves to
   a later session once it has been taught.
2. **Red-Black Tree Extra:** included as notes plus a trace (default kept).
3. **Core length:** about 40 minutes (Exercise 1: 10, Exercise 2: 30).
