#!/bin/bash
#
# verify_zip_rebuild.sh — clean-room rebuild validation for a submission ZIP.
#
# Usage:
#   scripts/verify_zip_rebuild.sh <path-to-submission.zip>
#
# The script extracts the ZIP into a temporary directory, runs the standard
# pdflatex → bibtex → pdflatex → pdflatex sequence on paper/main.tex, and
# reports the resulting page count. Exit code 0 on success; non-zero on
# missing paper/main.pdf or an unexpected page count (not 35).
#
# The intent is to catch path-sensitive bugs that only surface when the
# repository is extracted in isolation from the development tree — e.g.,
# LaTeX \graphicspath entries pointing to symlinks that exist only in the
# working copy.

set -e

ZIP="$1"
if [ -z "$ZIP" ]; then
    echo "Usage: $0 <path-to-submission.zip>" >&2
    exit 2
fi
if [ ! -f "$ZIP" ]; then
    echo "ERROR: ZIP file not found: $ZIP" >&2
    exit 2
fi

ZIP_ABS=$(cd "$(dirname "$ZIP")" && pwd)/$(basename "$ZIP")
EXPECTED_PAGES=35

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

cd "$TMPDIR"
unzip -q "$ZIP_ABS"

PAPER_DIR=$(find . -type d -name paper -maxdepth 3 | head -1)
if [ -z "$PAPER_DIR" ]; then
    echo "Clean-room rebuild: FAIL (paper/ directory not found in ZIP)"
    exit 1
fi

cd "$PAPER_DIR"
pdflatex -interaction=nonstopmode main.tex > build1.log 2>&1 || true
bibtex main > build_bib.log 2>&1 || true
pdflatex -interaction=nonstopmode main.tex > build2.log 2>&1 || true
pdflatex -interaction=nonstopmode main.tex > build3.log 2>&1 || true

if [ ! -f main.pdf ]; then
    echo "Clean-room rebuild: FAIL (main.pdf not produced)"
    echo "--- tail of final build log ---"
    tail -40 build3.log
    exit 1
fi

# Prefer pdfinfo if available; otherwise parse the pdflatex log line
# "Output written on main.pdf (NN pages, NNNN bytes)."
if command -v pdfinfo > /dev/null 2>&1; then
    PAGES=$(pdfinfo main.pdf 2>/dev/null | awk '/^Pages:/ {print $2}')
else
    PAGES=$(awk '/Output written on main\.pdf/ {for (i=1;i<=NF;i++) if ($i ~ /^\(/) {gsub(/[()]/, "", $i); print $i; exit}}' build3.log)
fi
# grep -c always prints a count, so use `|| true` to absorb its non-zero
# exit on no-matches rather than `|| echo 0` (which would append an extra line).
UNDEF_REFS=$(grep -c "undefined references" build3.log 2>/dev/null || true)
UNDEF_CITES=$(grep -c "Citation .* undefined" build3.log 2>/dev/null || true)
ERRORS=$(grep -c "^! " build3.log 2>/dev/null || true)

if [ "$PAGES" = "$EXPECTED_PAGES" ] && [ "$ERRORS" = "0" ] && [ "$UNDEF_REFS" = "0" ] && [ "$UNDEF_CITES" = "0" ]; then
    echo "Clean-room rebuild: PASS ($PAGES pages)"
    exit 0
else
    echo "Clean-room rebuild: FAIL"
    echo "  pages=$PAGES (expected $EXPECTED_PAGES)"
    echo "  errors=$ERRORS, undef_refs=$UNDEF_REFS, undef_cites=$UNDEF_CITES"
    echo "--- tail of final build log ---"
    tail -40 build3.log
    exit 1
fi
