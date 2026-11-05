#!/usr/bin/env bash
# Run the Recitation 3 LCS and Huffman contracts in every supported language.
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
fail=0
for task in lcs huffman; do
    SOL="$ROOT/material/week3/solutions/$task"
    WORK="$ROOT/.tmp/week3-verify/$task"
    rm -rf "$WORK"
    mkdir -p "$WORK/csproj"
    # Keep generated binaries, compiler copies, and caches outside the source tree.
    for file in "$SOL"/*; do [ -f "$file" ] && cp "$file" "$WORK/"; done
    cp "$SOL/csproj/"*.cs "$SOL/csproj/"*.csproj "$WORK/csproj/"
    cmp "$SOL/cs.solution.cs" "$SOL/csproj/Solution.cs" || exit 1
    run() {
        if (cd "$WORK" && eval "$2") >"$WORK/$1.log" 2>&1; then
            echo "PASS week3 $task $1"
        else
            echo "FAIL week3 $task $1"; cat "$WORK/$1.log"; fail=$((fail+1))
        fi
    }
    run c 'gcc -std=c11 -Wall -Wextra c.solution.c c.test.c -o ctest && ./ctest'
    run cpp 'g++ -std=c++17 -Wall -Wextra cpp.solution.cpp cpp.test.cpp -o cpptest && ./cpptest'
    run cs 'dotnet run --project csproj'
    run java 'cp java.solution.java Solution.java && javac Solution.java Main.java && java Main'
    run py 'python3 py.test.py'
    run js 'node js.test.js'
done
if [ "$fail" -ne 0 ]; then exit 1; fi
echo 'ALL 12 WEEK 3 HARNESSES PASSED'
