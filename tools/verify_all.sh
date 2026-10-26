#!/usr/bin/env bash
# Run every problem x language test harness from .tmp/sol/ and report PASS/FAIL.
# Each harness runs inside its own problem directory with the contract command.
set -uo pipefail

TOOLS_ROOT="$(cd "$(dirname "$0")" && pwd)"
SOL="$TOOLS_ROOT/../material/week1/solutions"
LOGS="$TOOLS_ROOT/../.tmp/verify_logs"
rm -rf "$LOGS"
mkdir -p "$LOGS"

pass=0
fail=0
failures=()

run_check() { # problem lang command-string
  local problem="$1" lang="$2" cmd="$3"
  if ( cd "$SOL/$problem" && eval "$cmd" ) >"$LOGS/$problem-$lang.log" 2>&1; then
    echo "PASS  $problem  $lang"
    pass=$((pass + 1))
  else
    echo "FAIL  $problem  $lang   (log: $LOGS/$problem-$lang.log)"
    fail=$((fail + 1))
    failures+=("$problem/$lang")
  fi
}

cleanup_problem() {
  local d="$1"
  rm -f "$d/ctest" "$d/cpptest" "$d"/Solution.java "$d"/*.class
  rm -rf "$d/csproj/bin" "$d/csproj/obj" "$d/__pycache__"
}

for n in 1 2 3 4 5 6; do
  if [ ! -d "$SOL/p$n" ]; then
    echo "FAIL  p$n  (missing directory)"
    fail=$((fail + 1))
    failures+=("p$n/missing")
    continue
  fi
  run_check "p$n" c    'gcc -std=c11 -Wall c.solution.c c.test.c -o ctest && ./ctest'
  run_check "p$n" cpp  'g++ -std=c++17 -Wall cpp.solution.cpp cpp.test.cpp -o cpptest && ./cpptest'
  run_check "p$n" cs   'dotnet run --project csproj'
  run_check "p$n" java 'cp java.solution.java Solution.java && javac Solution.java Main.java && java Main'
  run_check "p$n" py   'python3 py.test.py'
  run_check "p$n" js   'node js.test.js'
  cleanup_problem "$SOL/p$n"
done

echo
echo "RESULT: $pass passed, $fail failed (of 36)"
if [ "$fail" -ne 0 ]; then
  printf 'FAILED: %s\n' "${failures[@]}"
  exit 1
fi
echo "ALL 36 HARNESSES PASSED"
