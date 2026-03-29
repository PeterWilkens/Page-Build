\version "2.24.0"
#(set-global-staff-size 16)
\paper {
  indent = 0\mm
  ragged-right = ##t
  top-margin = 3\mm
  bottom-margin = 3\mm
  left-margin = 3\mm
  right-margin = 3\mm
  paper-width = 70\mm
  paper-height = 30\mm
}
\score {
  \new Staff \with {
    \omit TimeSignature
  } {
    \clef treble
    <c' e' g'>2
    \bar "|."
  }
  \layout { }
}
