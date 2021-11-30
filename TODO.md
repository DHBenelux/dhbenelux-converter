# Todos regarding conversion and styling

* Do we want abstracts on the articles or not? This should be part of the author guidelines.

* See references in Kemman et al. (issue 1). Bibliography is generated at the end of document, not between end of text and appendices. No idea why.

* Pandoc bibliography conversion is case sensitive (Overleaf's is apparently not), thus `@article{Svensson2011,` in `.bib` does result in `???` in HTML if the `.tex` has `\citep{svensson2011}`.

* We have various citation systems (footnotes vs. author/date). And We have 'clashing' parentheses both in PDF and HTML for in text citations, but in different ways:

  * HTML: "writers ((Bruni 1978), (Bruni 1984)), scholars"
  * PDF: "writers (Bruni (1978), Bruni (1984)), scholars"
