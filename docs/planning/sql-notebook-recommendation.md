# Local SQL exercises in Jupyter: recommendation

Date: 2026-10-28
Status: planning only; no SQL notebooks or database downloads are published yet.

## Recommended approach

Use a local SQLite database for introductory SQL practice. Students do not need a
separate database server, account, or network connection to run queries after the
notebook environment and Java dependencies have been installed. Both Python and
Java can access the same SQLite database format. Keep the SQL questions and seed
data identical across the two language versions.

This fits a short introduction covering SELECT, filtering, ordering, joins,
aggregation, and basic data modification. No reserved Recitation slot is assigned
by this recommendation.

## Python notebook

Use the existing Python (CS301) kernel and Python's `sqlite3` module. It normally
ships with Python, but verify that the chosen uv-managed installation includes it.
The following is an illustrative setup cell, not a complete exercise notebook:

```python
import sqlite3
from pathlib import Path

# Show the resolved path so students can spot an incorrect working directory.
db_path = Path("practice.db").resolve()
print(db_path)
connection = sqlite3.connect(db_path)
connection.execute("PRAGMA foreign_keys = ON")
```

Teacher-provided helpers should display column names and query results, so students
can concentrate on SQL. Provide separate helpers for read queries and changes to
data, with explicit commit/rollback behavior. Close the connection when finished.
A missing path creates an empty database, so the final setup should also verify
that expected tables exist before students begin.

Reference: [Python sqlite3 documentation](https://docs.python.org/3.13/library/sqlite3.html).

## Java notebook

Use the existing Java/IJava kernel with the Xerial SQLite JDBC driver. IJava's
`%maven` magic can load a Maven artifact and its transitive dependencies without
requiring students to create a Maven project. The instructor should select, pin,
and test a specific driver version before distributing the notebook; do not use
an unversioned dependency or a placeholder in the student release.

After loading the driver, an illustrative connection cell is:

```java
// Run from the same exercise folder as the Python version.
var dbPath = java.nio.file.Path.of("practice.db").toAbsolutePath().normalize();
System.out.println(dbPath);
var connection = java.sql.DriverManager.getConnection("jdbc:sqlite:" + dbPath);
try (var statement = connection.createStatement()) {
    statement.execute("PRAGMA foreign_keys = ON");
}
```

Prewrite the JDBC result-display and update helpers. Close each Statement and
ResultSet after use, and close the connection before resetting the database.
The initial dependency download requires internet access; verify the cached
configuration offline before describing a classroom exercise as offline-ready.

References: [Xerial SQLite JDBC](https://github.com/xerial/sqlite-jdbc),
[IJava dependency magics](https://github.com/SpencerPark/IJava/blob/master/docs/magics.md).

## Distribution and classroom workflow

Proposed files, to be created later:

- `sql-practice-python.ipynb`: Python setup, common SQL questions, display helpers.
- `sql-practice-java.ipynb`: Java setup, the same questions and expected results.
- `seed.sql`: canonical schema and small, readable sample data.
- `README.md`: how to open a notebook, choose its kernel, and reset the exercise.

Each student should create their own working `practice.db` from the seed. Both
language notebooks can use that file when run from the same folder. Prefer running
one notebook connection at a time during basic exercises: uncommitted writes can
lock the database or remain invisible to another connection. The two notebooks
use separate kernels and different connection/display code; sharing a database
does not make their host-language cells interchangeable.

Provide a clearly labeled reset cell that closes connections and recreates only
the exercise database from `seed.sql`. Explain that reset discards exercise changes.
Keep a deterministic starting state and tell students whether an exercise depends
on earlier updates. Unlike the website's temporary editor drafts, notebook outputs
and SQLite changes can persist on disk.

For a first release, use `sqlite3` and JDBC directly. A Python SQL-magic extension
such as JupySQL can be evaluated later if direct SQL cells are preferred; its
Python extension commands should not be copied into IJava notebooks.

## Small correctness checks before release

- Confirm both notebooks resolve the intended database path and load the same seed.
- Run all queries in both languages and compare expected rows. Use ORDER BY whenever
  a question requires a particular row order.
- Enable and verify `PRAGMA foreign_keys = ON` on every connection before starting
  a transaction when teaching foreign-key constraints.
- Explain SQLite-specific type and SQL behavior where it affects a question.
- Verify data modification, commit/rollback, reset, and rerunning cells.
- Test the selected Python, JDK >=17, IJava, and pinned JDBC versions on the
  supported student operating systems, including Windows PowerShell setup.

Reference: [SQLite foreign-key support](https://www.sqlite.org/foreignkeys.html).

## Validation boundary

This document records a recommendation supported by official documentation. It
does not establish that IJava, the JDBC dependency, or a complete two-language
exercise has been installed and tested in this project. Notebook creation,
dependency selection, sample data, and cross-platform verification remain future work.
