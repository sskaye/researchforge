"""Verifier helper: normalize text and substring-search evidence quotes."""
import unicodedata
import re
import subprocess
import os

def normalize(s):
    if s is None:
        return ""
    s = unicodedata.normalize("NFKC", s)
    # Fold dashes
    for d in ["‐", "‑", "‒", "–", "—", "―", "−", "⁃"]:
        s = s.replace(d, "-")
    # Fold Cyrillic С to ASCII C
    s = s.replace("С", "C").replace("с", "c").replace("Р", "P")
    # Collapse whitespace
    s = re.sub(r"\s+", " ", s)
    return s.lower().strip()

def read_paper(folder):
    base = "/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/" + folder
    if folder.endswith(".pdf"):
        try:
            r = subprocess.run(["pdftotext", "-layout", base, "-"], capture_output=True, text=True)
            return r.stdout
        except Exception as e:
            return ""
    # Try nxml then txt then pdf
    candidates = [
        os.path.join(base, "article.nxml"),
        os.path.join(base, "article_text.txt"),
        os.path.join(base, "article.txt"),
        os.path.join(base, "article.pdf"),
    ]
    for c in candidates:
        if os.path.exists(c):
            if c.endswith(".pdf"):
                try:
                    r = subprocess.run(["pdftotext", "-layout", c, "-"], capture_output=True, text=True)
                    return r.stdout
                except:
                    continue
            else:
                with open(c, "r", encoding="utf-8", errors="ignore") as f:
                    return f.read()
    return ""

def check_quote_in_text(quote, text):
    n_quote = normalize(quote)
    n_text = normalize(text)
    return n_quote in n_text

if __name__ == "__main__":
    import sys
    folder = sys.argv[1]
    quote = sys.argv[2]
    t = read_paper(folder)
    print(check_quote_in_text(quote, t))
