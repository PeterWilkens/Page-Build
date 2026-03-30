#!/usr/bin/env python3
"""
update-notation.py
------------------
Run from the project root after editing ch-four-chord-grids.ptx:

    python3 update-notation.py

Reads every \\gn{col}{row}{label}{1} selection in each of the 4 chord
grids, maps the coordinates to LilyPond note names, rewrites the matching
.ly file, recompiles it with LilyPond, copies the SVG/PDF to the web
output folder, then runs `pretext build web`.
"""

import re
import subprocess
import shutil
from pathlib import Path

# ── paths ────────────────────────────────────────────────────────────────────
PROJECT  = Path(__file__).parent
PTX_FILE = PROJECT / "source" / "ch-four-chord-grids.ptx"
NOTE_DIR = PROJECT / "assets" / "notation"
WEB_OUT  = PROJECT / "output" / "web" / "external" / "notation"

# prefer system LilyPond, fallback to python package if available
LILY = shutil.which("lilypond")
if not LILY:
    try:
        import lilypond as _lp
        LILY = _lp.executable()
    except Exception:
        LILY = None

# ── grid position → LilyPond note name ───────────────────────────────────────
# Derived from the 30 nodes defined in \drawgridandnotes in docinfo.ptx
NOTE_MAP = {
    (5, 1.5): "c'",    (4, 2.0): "cis'",  (3, 2.5): "d'",
    (2, 3.0): "ees'",  (1, 3.5): "e'",
    (5, 2.5): "ees'",  (4, 3.0): "e'",   (3, 3.5): "f'",
    (2, 4.0): "fis'",  (1, 4.5): "g'",
    (5, 3.5): "fis'",  (4, 4.0): "g'",   (3, 4.5): "aes'",
    (2, 5.0): "a'",    (1, 5.5): "bes'",
    (5, 4.5): "a'",    (4, 5.0): "bes'",  (3, 5.5): "b'",
    (2, 6.0): "c''",   (1, 6.5): "cis''",
    (5, 5.5): "c''",   (4, 6.0): "cis''", (3, 6.5): "d''",
    (2, 7.0): "ees''", (1, 7.5): "e''",
    (5, 6.5): "ees''", (4, 7.0): "e''",   (3, 7.5): "f''",
    (2, 8.0): "fis''", (1, 8.5): "g''",
}

# ascending pitch order for sorting selected notes
_PITCH_NAMES = [
    "c'", "cis'", "d'", "ees'", "e'", "f'", "fis'", "g'", "aes'", "a'", "bes'", "b'",
    "c''", "cis''", "d''", "ees''", "e''", "f''", "fis''", "g''",
]
PITCH_ORDER = {n: i for i, n in enumerate(_PITCH_NAMES)}

# ── grid → staff-grid stem ──────────────────────────────────────────────────
GRIDS = {
    "img-grid-c-major": "staff-grid1",
    "img-grid-g-major": "staff-grid2",
    "img-grid-f-major": "staff-grid3",
    "img-grid-a-minor": "staff-grid4",
}

# ── LilyPond file template ────────────────────────────────────────────────────
LY_TEMPLATE = r"""\version "2.24.0"
#(set-global-staff-size 36)
\paper {{
  indent = 0\mm
    ragged-right = ##f
    line-width = 14\mm
        top-margin = 4\mm
        bottom-margin = 4\mm
  left-margin = 2\mm
  right-margin = 2\mm
    paper-width = 60\mm
    paper-height = 50\mm
}}
\header {{
    tagline = ##f
}}
\score {{
  \new Staff \with {{
    \omit TimeSignature
  }} {{
    \clef treble
        {time_cmd}
    {body}
        \bar "|."
  }}
  \layout {{ }}
}}
"""

# ── helpers ───────────────────────────────────────────────────────────────────

def get_selected_notes(ptx_text: str, xml_id: str) -> list[str]:
    """Return sorted, deduplicated LilyPond notes for \\gn entries flagged {1}."""
    # grab the tikzpicture block belonging to this image xml:id
    pat = rf'xml:id="{re.escape(xml_id)}".*?\\end\{{tikzpicture\}}'
    m = re.search(pat, ptx_text, re.DOTALL)
    if not m:
        print(f"  WARNING: could not find block for {xml_id}")
        return []
    block = m.group(0)
    notes = []
    for gm in re.finditer(r'\\gn\{(\d+)\}\{([\d.]+)\}\{[^}]*\}\{1\}', block):
        key = (int(gm.group(1)), float(gm.group(2)))
        note = NOTE_MAP.get(key)
        if note:
            notes.append(note)
        else:
            print(f"  WARNING: no note mapping for position {key}")
    # deduplicate and sort ascending by pitch
    return sorted(set(notes), key=lambda n: PITCH_ORDER.get(n, 99))


def make_body(notes: list[str]) -> str:
    """Build LilyPond note expression (or rest)."""
    if not notes:
        note_expr = "r2"
    elif len(notes) == 1:
        note_expr = notes[0] + "2"
    else:
        note_expr = "<" + " ".join(notes) + ">2"

    return note_expr


def write_ly(stem: str, body: str) -> None:
    path = NOTE_DIR / f"{stem}.ly"
    path.write_text(LY_TEMPLATE.format(body=body, time_cmd="\\time 2/4"))
    print(f"  Wrote {path.name}  →  {body[:60]}")


def expand_svg_viewbox(stem: str, min_width: float = 40.0) -> None:
    """Ensure SVG viewBox is wide enough and size matches the actual content."""
    svg = NOTE_DIR / f"{stem}.svg"
    if not svg.exists():
        return
    text = svg.read_text()
    m = re.search(r'viewBox="([\d.+-]+) ([\d.+-]+) ([\d.+-]+) ([\d.+-]+)"', text)
    if not m:
        return
    x0, y0, w, h = (float(m.group(i)) for i in range(1, 5))
    new_width = max(w, min_width)
    new_viewbox = f'viewBox="{x0:.4f} {y0:.4f} {new_width:.4f} {h:.4f}"'
    text = text[:m.start()] + new_viewbox + text[m.end():]

    width_match = re.search(r'width="[\d.+-]+mm"', text)
    if width_match:
        text = text[:width_match.start()] + f'width="{new_width:.2f}mm"' + text[width_match.end():]

    height_match = re.search(r'height="[\d.+-]+mm"', text)
    if height_match:
        text = text[:height_match.start()] + f'height="{h:.2f}mm"' + text[height_match.end():]

    svg.write_text(text)
    print(f"  Adjusted {stem}.svg dimensions to {new_width:.1f} × {h:.1f}")


def compile_ly(stem: str) -> bool:
    if not LILY:
        print("  ERROR: could not find LilyPond executable.")
        return False
    ly  = NOTE_DIR / f"{stem}.ly"
    out = NOTE_DIR / stem
    r = subprocess.run(
        [str(LILY), "--svg", "-o", str(out), str(ly)],
        capture_output=True, text=True,
    )
    if r.returncode == 0:
        print(f"  Compiled {stem}.svg  OK")
        expand_svg_viewbox(stem)
        return True
    else:
        print(f"  ERROR compiling {stem}:")
        print(r.stderr[-500:])
        return False


def copy_to_web(stem: str) -> None:
    WEB_OUT.mkdir(parents=True, exist_ok=True)
    for ext in ("svg", "pdf"):
        src = NOTE_DIR / f"{stem}.{ext}"
        if src.exists():
            shutil.copy2(src, WEB_OUT / src.name)
    print(f"  Copied {stem} → web output")


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    ptx = PTX_FILE.read_text()

    for xml_id, stem in GRIDS.items():
        print(f"\n[{xml_id}]")
        notes = get_selected_notes(ptx, xml_id)
        print(f"  Selected: {notes or '(none — rest will be shown)'}")
        body = make_body(notes)
        write_ly(stem, body)
        if compile_ly(stem):
            copy_to_web(stem)

    print("\nRunning pretext build web …")
    r = subprocess.run(
        ["pretext", "build", "web"],
        cwd=PROJECT, capture_output=True, text=True,
    )
    if r.returncode == 0:
        print("Build succeeded.  Run `pretext view web` to see results.")
    else:
        print("BUILD ERROR:")
        print(r.stderr[-600:])


if __name__ == "__main__":
    main()
