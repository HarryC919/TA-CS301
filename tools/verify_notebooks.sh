#!/usr/bin/env bash
# Rebuild the Recitation 1 notebooks, then run every self-check cell against
# the reference solution students will meet on the website. This keeps the
# shipped .ipynb files honest: a check cell that no longer matches the
# published examples or reference answers fails here.
#
# Python checks run the p{N} reference solution and the notebook's p{N}-check
# cell in one interpreter. Java checks compile the reference Solution class
# together with the check cell wrapped in a temporary Main class; the run must
# print at least one "OK:" line and no "FAIL:" line.
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SITE_NB="$ROOT/site/notebooks"
SOL="$ROOT/material/week1/solutions"
WORK="$ROOT/.tmp/nbverify"
LOGS="$WORK/logs"

pass=0
fail=0
failures=()

report() { # status label [log]
  if [ "$1" = PASS ]; then
    echo "PASS  $2"
    pass=$((pass + 1))
  else
    echo "FAIL  $2   (log: $3)"
    fail=$((fail + 1))
    failures+=("$2")
  fi
}

cell_source() { # notebook-path cell-id -> print the cell source to stdout
  python3 - "$2" "$1" <<'PY'
import json, sys
with open(sys.argv[2], encoding="utf-8") as handle:
    notebook = json.load(handle)
for cell in notebook["cells"]:
    if cell["id"] == sys.argv[1]:
        print(cell["source"], end="")
        break
else:
    sys.exit(f"cell {sys.argv[1]!r} not found in {sys.argv[2]}")
PY
}

rm -rf "$WORK"
mkdir -p "$LOGS"

python3 "$ROOT/tools/site_src/build_notebooks.py" || exit 1

if python3 - <<'PY'
import json
from pathlib import Path
for lang in ("python", "java"):
    path = Path(f"site/notebooks/recitation1-{lang}.ipynb")
    notebook = json.loads(path.read_text(encoding="utf-8"))
    assert notebook["nbformat"] == 4 and notebook["nbformat_minor"] >= 5
    ids = [cell["id"] for cell in notebook["cells"]]
    assert len(ids) == len(set(ids)), f"{path}: duplicate cell ids"
    for n in range(1, 7):
        for kind in ("brief", "stub", "check"):
            assert f"p{n}-{kind}" in ids, f"{path}: missing p{n}-{kind}"
print("notebook structure OK")
PY
then
  report PASS "structure"
else
  report FAIL "structure" "$LOGS/structure.log"
fi

for n in 1 2 3 4 5 6; do
  # Python: reference solution + shipped check cell in one namespace.
  mkdir -p "$WORK/python/p$n"
  cell_source "$SITE_NB/recitation1-python.ipynb" "p$n-check" > "$WORK/python/p$n/check.py"
  if ( cd "$WORK/python/p$n" \
       && { cat "$SOL/p$n/py.solution.py"; echo; cat check.py; } > run.py \
       && python3 run.py ); then
    report PASS "p$n python"
  else
    report FAIL "p$n python" "$LOGS/p$n-python.log"
  fi
  ( cd "$WORK/python/p$n" && python3 run.py ) >"$LOGS/p$n-python.log" 2>&1 || true

  # Java: reference Solution class + check cell wrapped in a Main class.
  mkdir -p "$WORK/java/p$n"
  cell_source "$SITE_NB/recitation1-java.ipynb" "p$n-check" > "$WORK/java/p$n/check.java"
  cp "$SOL/p$n/java.solution.java" "$WORK/java/p$n/Solution.java"
  python3 - "$WORK/java/p$n/check.java" "$WORK/java/p$n/Main.java" <<'PY'
import pathlib, sys
lines = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()
imports = [line for line in lines if line.startswith("import ")]
body = [line for line in lines if not line.startswith("import ")]
main = "\n".join(imports + [
    "public class Main {",
    "    public static void main(String[] args) {",
    *("    " + line for line in body),
    "    }",
    "}",
])
pathlib.Path(sys.argv[2]).write_text(main + "\n", encoding="utf-8")
PY
  if ( cd "$WORK/java/p$n" \
       && javac Solution.java Main.java \
       && java Main | tee run.out \
       && grep -q "OK:" run.out \
       && ! grep -q "FAIL:" run.out ); then
    report PASS "p$n java"
  else
    report FAIL "p$n java" "$LOGS/p$n-java.log"
  fi
  ( cd "$WORK/java/p$n" && java Main ) >"$LOGS/p$n-java.log" 2>&1 || true
done

echo
echo "RESULT: $pass passed, $fail failed (of 13)"
if [ "$fail" -ne 0 ]; then
  printf 'FAILED: %s\n' "${failures[@]}"
  exit 1
fi
echo "ALL NOTEBOOK CHECKS PASSED"
