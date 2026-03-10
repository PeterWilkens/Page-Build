var ptx_lunr_search_style = "textbook";
var ptx_lunr_docs = [
{
  "id": "front-colophon",
  "level": "1",
  "url": "front-colophon.html",
  "type": "Colophon",
  "number": "",
  "title": "Colophon",
  "body": "  "
},
{
  "id": "sec-section-name",
  "level": "1",
  "url": "sec-section-name.html",
  "type": "Section",
  "number": "1.1",
  "title": "Section Title",
  "body": " Section Title  Text of section.  "
},
{
  "id": "sec-intervals-c-major-scale",
  "level": "1",
  "url": "sec-intervals-c-major-scale.html",
  "type": "Section",
  "number": "2.1",
  "title": "Example of intervals. C Major Scale",
  "body": " Example of intervals. C Major Scale  In a C major scale the intervals remain the same ascending and descending.  All Major scales have the same pattern of intervals, so any Major scale can be built by using the same pattern of intervals.   Examples of intervals with notation and semitone counts (C Major Scale).      "
},
{
  "id": "fig-intervals-c-major-scale-table",
  "level": "2",
  "url": "sec-intervals-c-major-scale.html#fig-intervals-c-major-scale-table",
  "type": "Figure",
  "number": "2.1.1",
  "title": "",
  "body": " Examples of intervals with notation and semitone counts (C Major Scale).     "
},
{
  "id": "sec-intervals-c-harmonic-minor-ascending",
  "level": "1",
  "url": "sec-intervals-c-harmonic-minor-ascending.html",
  "type": "Section",
  "number": "2.2",
  "title": "Example of intervals, with count and notation in an ascending C Melodic Minor scale",
  "body": " Example of intervals, with count and notation in an ascending C Melodic Minor scale  In the Melodic Minor Scale the sixth and seventh notes of the Natural Minor scale are raised by a half step when ascending and the descending scale is as the Natural Minor scale.   Examples of intervals with notation and semitone counts (ascending C melodic minor).      "
},
{
  "id": "fig-intervals-c-harmonic-minor-ascending-table",
  "level": "2",
  "url": "sec-intervals-c-harmonic-minor-ascending.html#fig-intervals-c-harmonic-minor-ascending-table",
  "type": "Figure",
  "number": "2.2.1",
  "title": "",
  "body": " Examples of intervals with notation and semitone counts (ascending C melodic minor).     "
},
{
  "id": "sec-intervals",
  "level": "1",
  "url": "sec-intervals.html",
  "type": "Section",
  "number": "2.3",
  "title": "Example of intervals,with count and notation in a descending C Melodic Minor Scale",
  "body": " Example of intervals,with count and notation in a descending C Melodic Minor Scale  Intervals of the descending Melodic Minor scale are the same as a descending Natural Minor Scale.   Examples of intervals with notation and semitone counts.      "
},
{
  "id": "fig-intervals-table",
  "level": "2",
  "url": "sec-intervals.html#fig-intervals-table",
  "type": "Figure",
  "number": "2.3.1",
  "title": "",
  "body": " Examples of intervals with notation and semitone counts.     "
},
{
  "id": "backmatter-2",
  "level": "1",
  "url": "backmatter-2.html",
  "type": "Colophon",
  "number": "",
  "title": "Colophon",
  "body": " This book was authored in PreTeXt .  "
}
]

var ptx_lunr_idx = lunr(function () {
  this.ref('id')
  this.field('title')
  this.field('body')
  this.metadataWhitelist = ['position']

  ptx_lunr_docs.forEach(function (doc) {
    this.add(doc)
  }, this)
})
