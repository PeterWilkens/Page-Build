"""
Generate individual half-note SVGs for every chromatic pitch from F3 to D6
(treble clef with 3 ledger lines above and below the staff).

File naming convention:
  note-<natural>  e.g. note-c4, note-d5
  note-<sharp>s   e.g. note-cs4 (C#4), note-ds5 (D#5)
  (always sharp, not flat)

LilyPond absolute pitch notation used:
  octave 3 = no suffix  (f g a b)
  octave 4 = '          (c' d' ... b')
  octave 5 = ''         (c'' d'' ... b'')
  octave 6 = '''        (c''' d''' only up to D6)
"""

import subprocess
import os

LILY = "/opt/venv/lib/python3.13/site-packages/lilypond-binaries/bin/lilypond"
OUTDIR = os.path.dirname(os.path.abspath(__file__))

# (lilypond_pitch, output_file_stem)
NOTES = [
    # Octave 3  (3 ledger lines below treble: F3, and up to B3)
    ("f",       "note-f3"),
    ("fis",     "note-fs3"),
    ("g",       "note-g3"),
    ("gis",     "note-gs3"),
    ("a",       "note-a3"),
    ("ais",     "note-as3"),
    ("b",       "note-b3"),
    # Octave 4  (E4 = first line treble staff; C4 = middle C, 1 ledger below)
    ("c'",      "note-c4"),
    ("cis'",    "note-cs4"),
    ("d'",      "note-d4"),
    ("dis'",    "note-ds4"),
    ("e'",      "note-e4"),
    ("f'",      "note-f4"),
    ("fis'",    "note-fs4"),
    ("g'",      "note-g4"),
    ("gis'",    "note-gs4"),
    ("a'",      "note-a4"),
    ("ais'",    "note-as4"),
    ("b'",      "note-b4"),
    # Octave 5  (C5 = middle of treble staff; F5 = top line)
    ("c''",     "note-c5"),
    ("cis''",   "note-cs5"),
    ("d''",     "note-d5"),
    ("dis''",   "note-ds5"),
    ("e''",     "note-e5"),
    ("f''",     "note-f5"),
    ("fis''",   "note-fs5"),
    ("g''",     "note-g5"),
    ("gis''",   "note-gs5"),
    ("a''",     "note-a5"),
    ("ais''",   "note-as5"),
    ("b''",     "note-b5"),
    # Octave 6  (up to D6 = 3 ledger lines above treble staff)
    ("c'''",    "note-c6"),
    ("cis'''",  "note-cs6"),
    ("d'''",    "note-d6"),
]

TEMPLATE = r"""\version "2.24.0"
#(set-global-staff-size 24)
\paper {{
  indent = 0\mm
  ragged-right = ##t
  top-margin = 4\mm
  bottom-margin = 4\mm
  left-margin = 2\mm
  right-margin = 2\mm
  paper-width = 42\mm
  paper-height = 50\mm
}}
\score {{
  \new Staff \with {{
    \omit TimeSignature
  }} {{
    \clef treble
    {note}2
    \bar "|."
  }}
  \layout {{ }}
}}
"""

ok = 0
fail = 0

for ly_note, stem in NOTES:
    ly_path = os.path.join(OUTDIR, f"{stem}.ly")
    svg_out = os.path.join(OUTDIR, stem)   # LilyPond appends .svg

    # Write .ly source
    with open(ly_path, "w") as fh:
        fh.write(TEMPLATE.format(note=ly_note))

    # Compile to SVG
    result = subprocess.run(
        [LILY, "--svg", "-o", svg_out, ly_path],
        capture_output=True, text=True,
        cwd=OUTDIR
    )
    if result.returncode == 0:
        print(f"  OK  {stem}")
        ok += 1
    else:
        print(f"  FAIL {stem}:\n{result.stderr[:300]}")
        fail += 1

print(f"\nDone: {ok} generated, {fail} failed.")
