#!/usr/bin/env bash
# Run the Recitation 5 hash-table contract in every supported language.
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
fail=0
for task in hashtable; do
    SOL="$ROOT/material/week5/solutions/$task"
    WORK="$ROOT/.tmp/week5-verify/$task"
    rm -rf "$WORK"
    mkdir -p "$WORK/csproj"
    # Keep generated binaries, compiler copies, and caches outside the source tree.
    for file in "$SOL"/*; do [ -f "$file" ] && cp "$file" "$WORK/"; done
    cp "$SOL/csproj/"*.cs "$SOL/csproj/"*.csproj "$WORK/csproj/"
    cmp "$SOL/cs.solution.cs" "$SOL/csproj/Solution.cs" || exit 1
    run() {
        if (cd "$WORK" && eval "$2") >"$WORK/$1.log" 2>&1; then
            echo "PASS week5 $task $1"
        else
            echo "FAIL week5 $task $1"; cat "$WORK/$1.log"; fail=$((fail+1))
        fi
    }
    run c 'gcc -std=c11 -Wall -Wextra -Werror c.solution.c c.test.c -o ctest && ./ctest && gcc -std=c11 -Wall -Wextra -Werror -c c.stub.c -o stub.o'
    # The C++ harness includes cpp.solution.cpp, because the class definition is the interface.
    run cpp 'g++ -std=c++17 -Wall -Wextra -Werror cpp.test.cpp -o cpptest && ./cpptest && g++ -std=c++17 -Wall -Wextra -Werror -fsyntax-only cpp.stub.cpp'
    run cs 'dotnet run --project csproj'
    run java 'cp java.solution.java HashTable.java && javac HashTable.java Main.java && java Main'
    run py 'python3 py.test.py'
    run js 'node js.test.js'
done
if [ "$fail" -ne 0 ]; then exit 1; fi
echo 'ALL 6 WEEK 5 HARNESSES PASSED'
