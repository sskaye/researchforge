"""Phase 5 — Independent-verifier dispatcher.

Per § 9b of merged_skill_proposal.md.

The verifier is an external entity (an LLM agent, a different
extractor instance, or a human) that takes a row + the article files +
the frozen prompt and returns a JSON verdict with six Yes/No/Cannot-
determine answers.

This module provides:
  - hashing the frozen prompt (anti-tampering)
  - running the verifier sanity-check set at the start of each batch
  - dispatching rows to the verifier callable
  - collecting verdicts

The actual verifier *implementation* is pluggable: pass any
`verifier_callable(row, article_text, prompt) -> dict` to
`run_verification`. For self-tests, a `mock_verifier_factory` is
provided that returns a deterministic verifier.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass
from typing import Callable

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.abspath(os.path.join(HERE, ".."))


# -----------------------------------------------------------------------
# Frozen prompt
# -----------------------------------------------------------------------

PROMPT_PATH = os.path.join(SKILL_ROOT, "reference", "verifier_prompt.md")
SANITY_SET_PATH = os.path.join(SKILL_ROOT, "reference",
                                "verifier_sanity_set.json")


def load_frozen_prompt(prompt_path: str | None = None) -> tuple[str, str]:
    """Return (prompt_text, sha256_hex)."""
    path = prompt_path or PROMPT_PATH
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return text, digest


def load_sanity_set(sanity_path: str | None = None) -> dict:
    """Load the JSON sanity set."""
    path = sanity_path or SANITY_SET_PATH
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# -----------------------------------------------------------------------
# Verdict normalization
# -----------------------------------------------------------------------

_YES_NO_CANNOT = {"Yes", "No", "Cannot-determine"}


@dataclass
class VerifierResult:
    row_id: str
    verdict: str             # "pass" | "fail" | "error"
    raw: dict                # the JSON returned by the verifier
    reason: str              # one-line summary
    error: str | None = None  # set when verdict == "error"


def normalize_verdict(raw: dict) -> tuple[str, str]:
    """Compute (verdict, summary) from a raw verifier JSON response.

    A row passes only if all six q1..q6 answers are exactly 'Yes'. Any
    'No' or 'Cannot-determine' fails the row.
    """
    failing: list[str] = []
    for i in range(1, 7):
        ans = raw.get(f"q{i}")
        if ans not in _YES_NO_CANNOT:
            return "error", f"q{i}_invalid_answer:{ans!r}"
        if ans != "Yes":
            failing.append(f"q{i}:{ans}")
    if failing:
        return "fail", "; ".join(failing)
    return "pass", "all_yes"


# -----------------------------------------------------------------------
# Run verification batch
# -----------------------------------------------------------------------

def run_verification(audit_pool: list[dict],
                     article_text_provider: Callable[[str], str],
                     verifier_callable: Callable[[dict, str, str], dict],
                     prompt_path: str | None = None,
                     sanity_path: str | None = None,
                     sanity_threshold: float = 0.9,
                     ) -> dict:
    """Run the verification batch.

    Steps:
      1. Load + hash the frozen prompt.
      2. Run the sanity set; abort the batch if <sanity_threshold of
         sanity rows verify as expected.
      3. For each row in audit_pool, invoke verifier_callable and
         normalize the verdict.

    Returns a dict with keys:
      prompt_hash, sanity_results, pass_count, fail_count, error_count,
      results (list of VerifierResult-shaped dicts).

    If the sanity check fails, the dict has 'aborted': True and
    no row-level results.
    """
    prompt_text, prompt_hash = load_frozen_prompt(prompt_path)
    sanity_data = load_sanity_set(sanity_path)

    # ---- Sanity-check pass ----
    sanity_pass = 0
    sanity_total = len(sanity_data["rows"])
    sanity_details = []
    for s in sanity_data["rows"]:
        expected = s["expected_verdict"]
        raw = verifier_callable(s["row"], _sanity_article_text(s),
                                prompt_text)
        actual, summary = normalize_verdict(raw)
        ok = (actual == expected)
        sanity_details.append({
            "sanity_id": s["sanity_id"],
            "expected": expected,
            "actual": actual,
            "summary": summary,
            "ok": ok,
        })
        if ok:
            sanity_pass += 1

    sanity_rate = sanity_pass / max(1, sanity_total)
    if sanity_rate < sanity_threshold:
        return {
            "prompt_hash": prompt_hash,
            "aborted": True,
            "abort_reason": "verifier_unreliable",
            "sanity_results": sanity_details,
            "sanity_rate": sanity_rate,
            "sanity_threshold": sanity_threshold,
        }

    # ---- Production rows ----
    results: list[dict] = []
    pass_n = 0
    fail_n = 0
    err_n = 0
    for row in audit_pool:
        row_id = row.get("candidate_id") or f"{row.get('article_id','?')}::{row.get('compound_name','?')[:60]}"
        article_text = article_text_provider(row.get("article_id", ""))
        try:
            raw = verifier_callable(row, article_text, prompt_text)
        except Exception as e:
            err_n += 1
            results.append({
                "row_id": row_id,
                "verdict": "error",
                "raw": None,
                "reason": f"verifier_exception:{type(e).__name__}:{e}",
                "error": str(e),
            })
            continue
        verdict, summary = normalize_verdict(raw)
        if verdict == "pass":
            pass_n += 1
        elif verdict == "fail":
            fail_n += 1
        else:
            err_n += 1
        results.append({
            "row_id": row_id,
            "verdict": verdict,
            "raw": raw,
            "reason": summary,
        })

    return {
        "prompt_hash": prompt_hash,
        "aborted": False,
        "sanity_results": sanity_details,
        "sanity_rate": sanity_rate,
        "pass_count": pass_n,
        "fail_count": fail_n,
        "error_count": err_n,
        "audited_count": len(results),
        "results": results,
    }


def _sanity_article_text(sanity_row: dict) -> str:
    """For sanity rows we don't have actual article text; we hand the
    verifier a synthetic 'article' built from the row's expected
    evidence and rationale. Mock verifiers use this; real LLM verifiers
    would need the actual article files."""
    parts = [
        f"source_paper={sanity_row.get('source_paper', '?')}",
        f"rationale={sanity_row.get('rationale', '')}",
    ]
    if "expected_failing_question" in sanity_row:
        parts.append(f"hint:expected_to_fail={sanity_row['expected_failing_question']}")
    return "\n".join(parts)


# -----------------------------------------------------------------------
# Mock verifier (for unit tests)
# -----------------------------------------------------------------------

def mock_verifier_factory(
    rule_set: str = "sanity_aware"
) -> Callable[[dict, str, str], dict]:
    """Return a deterministic mock verifier callable.

    rule_set:
      "sanity_aware" → If the row is from the sanity set (article_text
                       contains 'hint:expected_to_fail=qN' or
                       'rationale=...'), produces the expected verdict.
                       Production rows default to all-Yes pass.
      "always_pass"  → Always returns all-Yes.
      "always_fail"  → Always returns q1=No.
      "random_seed"  → Deterministic-random pass/fail using row_id hash.
    """
    def call(row: dict, article_text: str, prompt: str) -> dict:
        if rule_set == "always_pass":
            return _all_yes()
        if rule_set == "always_fail":
            r = _all_yes()
            r["q1"] = "No"
            r["q1_reason"] = "mock always-fail"
            r["verdict"] = "fail"
            return r
        if rule_set == "random_seed":
            # Deterministic pseudo-random based on a row identifier
            h = int(hashlib.sha256(
                (row.get("candidate_id") or
                 str(row.get("compound_name", ""))
                ).encode("utf-8")).hexdigest(), 16)
            if h % 100 < 5:
                r = _all_yes()
                r["q1"] = "No"
                r["q1_reason"] = "mock random failure"
                r["verdict"] = "fail"
                return r
            return _all_yes()
        # sanity_aware (default)
        m = re.search(r"hint:expected_to_fail=(q\d)", article_text,
                       re.IGNORECASE)
        if m:
            r = _all_yes()
            fq = m.group(1).lower()  # normalize to "q3"
            r[fq] = "No"
            r[f"{fq}_reason"] = "mock sanity-aware failure"
            r["verdict"] = "fail"
            return r
        if "rationale=" in article_text and "expected_to_fail" not in article_text:
            # Sanity row that should PASS
            return _all_yes()
        return _all_yes()
    return call


def _all_yes() -> dict:
    out = {f"q{i}": "Yes" for i in range(1, 7)}
    for i in range(1, 7):
        out[f"q{i}_reason"] = "ok"
    out["verdict"] = "pass"
    return out
