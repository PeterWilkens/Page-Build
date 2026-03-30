\version "2.24.0"
#(set-global-staff-size 24)
\paper {
  indent = 0\mm
  ragged-right = ##t
  top-margin = 4\mm
  bottom-margin = 4\mm
  left-margin = 2\mm
  right-margin = 2\mm
  paper-width = 90\mm
  paper-height = 50\mm
}
\score {
  \new Staff \with {
    \omit TimeSignature
  } {
    \clef treble
    c'2 d'2 e'2
    \bar "|."
  }
  \layout { }
}
