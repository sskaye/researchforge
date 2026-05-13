"""Unit tests for scripts/ingest_article.py.

Per § 12.1 of merged_skill_proposal.md.
"""
import os
import sys
import tempfile
import textwrap

# Make scripts/ importable
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts"))

from ingest_article import (
    ingest_article, _parse_nxml, _scan_pdf_text_for_doi, _normalize_text,
    diagnostic_dump,
)


# Use the real test corpus for integration-style unit tests
DEV_ROOT = "/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/mp_bp_dev_set"


def find_paper(prefix: str) -> str:
    """Helper: find the full directory name for a paper given its prefix."""
    for d in os.listdir(DEV_ROOT):
        if d.startswith(prefix):
            return os.path.join(DEV_ROOT, d)
    raise FileNotFoundError(f"No paper with prefix {prefix}")


# ---------- Test 1: parse a known-good NXML ----------

def test_pmc_nxml_parses_correctly():
    art = ingest_article(find_paper("026_PMC8332001"))
    assert art.source_kind == "pmc_nxml"
    assert "nxml" in art.available_sources
    assert len(art.sections) > 0
    assert len(art.tables) == 3  # paper 026 has 3 NXML tables
    # Table 1 has 3 data rows (compounds 4, 8, 9) — NOT 4 (header was dedup'd)
    table_1 = art.tables[0]
    assert table_1.label == "Table 1"
    assert len(table_1.rows) == 3, f"expected 3 data rows, got {len(table_1.rows)}"
    # Headers correctly populated
    assert "M.P °C" in table_1.headers
    # First data row is compound 4 with mp 68
    first_row_texts = [c.text for c in table_1.rows[0]]
    assert "4" in first_row_texts
    assert "68" in first_row_texts


def test_pmc_nxml_dense_prose():
    """Paper 011 has many sections and many tables. Make sure the parser
    handles dense structure."""
    art = ingest_article(find_paper("011_PMC12943719"))
    assert art.source_kind == "pmc_nxml"
    assert len(art.sections) > 50, \
        f"expected many sections, got {len(art.sections)}"
    assert len(art.tables) >= 10
    # full_text should be substantial
    assert len(art.full_text) > 100_000


# ---------- Test 2: malformed NXML fails gracefully ----------

def test_malformed_nxml_fails_gracefully():
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "article.nxml"), "w") as f:
            f.write("<this is < not > valid XML")
        art = ingest_article(tmpdir, article_id="malformed_test")
        # Should NOT raise; should record the error in warnings
        assert any("nxml_parse_error" in w for w in art.warnings)
        # Sections and tables should be empty
        assert art.sections == []
        assert art.tables == []


# ---------- Test 3: DOI candidates from each source ----------

def test_doi_from_nxml_front_matter():
    art = ingest_article(find_paper("026_PMC8332001"))
    sources = {c.source for c in art.doi_candidates}
    assert "nxml_front_matter" in sources
    nxml_dois = [c.doi for c in art.doi_candidates if c.source == "nxml_front_matter"]
    assert "10.1007/s13738-021-02358-x" in nxml_dois


def test_doi_from_pdf_text():
    """Loose PDFs should yield DOI via pdf_text_first_2_pages."""
    art = ingest_article(find_paper("2014_Schmittel"))
    sources = {c.source for c in art.doi_candidates}
    assert "pdf_text_first_2_pages" in sources
    pdf_dois = [c.doi for c in art.doi_candidates if c.source == "pdf_text_first_2_pages"]
    assert "10.3762/bjoc.10.317" in pdf_dois


def test_doi_user_metadata_override():
    """A user-provided DOI should appear as a separate candidate."""
    art = ingest_article(find_paper("2014_Schmittel"), user_doi="10.test/override")
    sources = [c.source for c in art.doi_candidates]
    assert "user_metadata" in sources


# ---------- Test 4: loose PDF (no NXML) is handled ----------

def test_loose_pdf_no_nxml():
    art = ingest_article(find_paper("2014_Schmittel"))
    assert art.source_kind == "loose_pdf"
    assert "nxml" not in art.available_sources
    assert "pdf" in art.available_sources
    # Sections and tables are empty (no NXML to parse them from)
    assert len(art.sections) == 0
    assert len(art.tables) == 0
    # Full text is populated from pdftotext
    assert len(art.full_text) > 1000


# ---------- Test 5: scan_pdf_text_for_doi ----------

def test_scan_pdf_text_for_doi_basic():
    txt = "Some content with 10.1234/test.doi and another 10.5555/x.y.z here"
    found = _scan_pdf_text_for_doi(txt)
    assert "10.1234/test.doi" in found
    assert "10.5555/x.y.z" in found


def test_scan_pdf_text_for_doi_strips_trailing_punct():
    txt = "See doi:10.1234/abc.def. End of sentence."
    found = _scan_pdf_text_for_doi(txt)
    # Trailing period should be stripped
    assert "10.1234/abc.def" in found


def test_scan_pdf_text_for_doi_dedups():
    txt = "10.1234/repeat appears here and 10.1234/repeat appears here"
    found = _scan_pdf_text_for_doi(txt)
    assert found.count("10.1234/repeat") == 1


# ---------- Test 6: missing file graceful exit ----------

def test_missing_directory_raises_filenotfound():
    try:
        ingest_article("/nonexistent/path/that/does/not/exist")
    except FileNotFoundError:
        return  # expected
    raise AssertionError("Expected FileNotFoundError")


# ---------- Test 7: extraction never modifies article files ----------

def test_no_files_modified():
    """Read mtimes before and after ingestion; confirm unchanged."""
    paper_dir = find_paper("026_PMC8332001")
    files = [os.path.join(paper_dir, f) for f in os.listdir(paper_dir)
             if os.path.isfile(os.path.join(paper_dir, f))]
    mtimes_before = {f: os.path.getmtime(f) for f in files}
    _ = ingest_article(paper_dir)
    mtimes_after = {f: os.path.getmtime(f) for f in files}
    for f, t in mtimes_before.items():
        assert mtimes_after[f] == t, f"File modified: {f}"


# ---------- Test 8: diagnostic_dump structure ----------

def test_diagnostic_dump_has_required_keys():
    art = ingest_article(find_paper("026_PMC8332001"))
    diag = diagnostic_dump(art)
    required = {"article_id", "source_kind", "available_sources",
                "section_count", "table_count", "doi_candidate_count",
                "full_text_length", "warnings"}
    assert required.issubset(set(diag.keys()))


# ---------- Test 9: normalize_text NFC ----------

def test_normalize_text_nfc():
    # Combining char form (NFD) of é = e + combining acute
    nfd = "café"  # already NFC
    # ́ is combining acute. Let's build an NFD-like string
    nfd_built = "café"
    assert _normalize_text(nfd_built) == "café"


# ---------- Test 10: PDF rowspan/colspan handled minimally ----------

def test_table_with_rowspan():
    """Synthesize a small NXML with rowspan and confirm it expands."""
    nxml = textwrap.dedent("""\
        <article>
        <front><article-meta>
        <article-id pub-id-type="doi">10.test/rs</article-id>
        </article-meta></front>
        <body><sec><title>X</title><p>p1</p>
        <table-wrap id="t1"><label>Table 1</label>
        <caption><p>cap</p></caption>
        <table>
          <thead><tr><th>A</th><th>B</th></tr></thead>
          <tbody>
            <tr><td rowspan="2">spanA</td><td>1</td></tr>
            <tr><td>2</td></tr>
          </tbody>
        </table>
        </table-wrap></sec></body></article>""")
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "article.nxml"), "w") as f:
            f.write(nxml)
        art = ingest_article(tmpdir, article_id="rs_test")
    assert len(art.tables) == 1
    t = art.tables[0]
    assert t.headers == ["A", "B"]
    assert len(t.rows) == 2
    # Both rows should have "spanA" in column 0
    assert t.rows[0][0].text == "spanA"
    assert t.rows[1][0].text == "spanA"
    # And the data values 1 and 2 in column 1
    assert t.rows[0][1].text == "1"
    assert t.rows[1][1].text == "2"


if __name__ == "__main__":
    # Simple runner — find every test_ function and call it
    import inspect
    here = sys.modules[__name__]
    failures = []
    passed = 0
    for name, fn in inspect.getmembers(here, inspect.isfunction):
        if not name.startswith("test_"):
            continue
        try:
            fn()
            passed += 1
            print(f"PASS  {name}")
        except AssertionError as e:
            failures.append((name, str(e)))
            print(f"FAIL  {name}: {e}")
        except Exception as e:
            failures.append((name, f"{type(e).__name__}: {e}"))
            print(f"ERROR {name}: {type(e).__name__}: {e}")
    print(f"\n{passed} passed, {len(failures)} failed")
    if failures:
        sys.exit(1)
