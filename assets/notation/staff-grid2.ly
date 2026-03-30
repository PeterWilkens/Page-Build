\version "2.24.0"
#(set-global-staff-size 36)
\paper {
  indent = 0\mm
    ragged-right = ##f
    line-width = 14\mm
        top-margin = 4\mm
        bottom-margin = 4\mm
  left-margin = 2\mm
  right-margin = 2\mm
    paper-width = 60\mm
    paper-height = 50\mm
}
\header {
    tagline = ##f
}
\score {
  \new Staff \with {
    \omit TimeSignature
  } {
    \clef treble
        \time 2/4
    <c' e' g' bes'>2
        \bar "|."
  }
  \layout { }
}
