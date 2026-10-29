#!/usr/bin/env bash
# Run the Recitation 2 merge contracts in every supported language.
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SOL="$ROOT/material/week2/solutions/p3"
WORK="$ROOT/.tmp/week2-verify"
mkdir -p "$WORK"
# Keep generated binaries, compiler copies, and caches outside the source tree.
for file in "$SOL"/*; do [ -f "$file" ] && cp "$file" "$WORK/"; done
mkdir -p "$WORK/csproj"
cp "$SOL/csproj/"*.cs "$SOL/csproj/"*.csproj "$WORK/csproj/"
fail=0
run() {
    if (cd "$WORK" && eval "$2") >"$WORK/$1.log" 2>&1; then
        echo "PASS week2 $1"
    else
        echo "FAIL week2 $1"; cat "$WORK/$1.log"; fail=$((fail+1))
    fi
}
cmp "$SOL/cs.solution.cs" "$SOL/csproj/Solution.cs" || exit 1
run c 'gcc -std=c11 -Wall -Wextra c.solution.c c.test.c -o ctest && ./ctest'
run cpp 'g++ -std=c++17 -Wall -Wextra cpp.solution.cpp cpp.test.cpp -o cpptest && ./cpptest'
run cs 'dotnet run --project csproj'
run java 'cp java.solution.java Solution.java && javac Solution.java Main.java && java Main'
run py 'python3 py.test.py'
run js 'node js.test.js'
if [ "$fail" -ne 0 ]; then exit 1; fi
echo 'ALL 6 WEEK 2 HARNESSES PASSED'
