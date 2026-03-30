\version "2.24.0"
#(set-global-staff-size 24)
\paper {
  indent = 0\mm
  ragged-right = ##t
  top-margin = 2\mm
  bottom-margin = 2\mm
  left-margin = 2\mm
  right-margin = 2\mm
  paper-width = 42\mm
  paper-height = 36\mm
}
\score {
  \new Staff \with {
    \omit TimeSignature
  } {
    \clef treble
    <g' b' d'' g''>2 ^ \markup { \bold "G Maj" }
    \bar "|."
  }
  \layout { }
}
