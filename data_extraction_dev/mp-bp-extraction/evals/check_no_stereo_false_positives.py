#!/usr/bin/env python3
"""
v1.5 eval helper: confirm that validate_compound_name.py does NOT flag
rows 13–15 of v15_seeded_errors.csv, which contain legitimate
stereo / optical descriptors that start with '(' — (E)-, (S,S)-, (-)-.

Used by the 'v15-stereo-descriptors-not-flagged' eval.
"""
import re
import subprocess
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
SKILL_ROOT = HERE.parent
SCRIPT = SKILL_ROOT / "scripts" / "validate_compound_name.py"
FIXTURE = SKILL_ROOT / "evals" / "files" / "v15_seeded_errors.csv"

r = subprocess.run(
    ["python3", str(SCRIPT), str(FIXTURE)], capture_output=True, text=True
)

flagged_ids = set()
for line in r.stdout.splitlines():
    m = re.match(r"row (\d+):", line)
    if m:
        flagged_ids.add(m.group(1))

want_clean = {"13", "14", "15"}
unexpected = sorted(want_clean & flagged_ids)
if unexpected:
    print(f"UNEXPECTED FAILURES: {unexpected}")
    sys.exit(1)
print("UNEXPECTED FAILURES: NONE")
sys.exit(0)
