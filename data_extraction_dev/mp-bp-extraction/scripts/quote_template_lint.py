#!/usr/bin/env python3
"""
quote_template_lint.py — REMOVED in v1.6.

This lint flagged literal-ellipsis spans and Table-N-template patterns in
evidence_quote. v1.6 dropped the ellipsis prohibition entirely (papers
legitimately use elision in their own text) and the template-quote
prohibition (it was a cross-model concern that doesn't apply to Opus).

The file is retained as a no-op for backward compatibility — any caller
still invoking it exits 0 with a deprecation notice on stderr.

Usage: still callable; always exits 0.
"""
import sys

print(
    "quote_template_lint.py: deprecated in v1.6; ellipsis and template-quote "
    "checks are no longer enforced. Skipping.",
    file=sys.stderr,
)
sys.exit(0)
