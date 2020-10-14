# Todos regarding conversion and styling

* Do we want abstracts on the articles or not? This should be part of the author guidelines.

* We either need to make the Overleaf template more strict to avoid the use of `affil`, as only `address` percolates through to HTML via Pandoc. Or we have to devise some scriptyscript that rewrites the .tex on the fly.

* See references in Kemman et al. (issue 1). Bibliography is generated at the end of document, not between end of text and appendices. No idea why.

* Pandoc bibliography conversion is case sensitive (Overleaf's is apparently not), thus `@article{Svensson2011,` in `.bib` does result in `???` in HTML if the `.tex` has `\citep{svensson2011}`.

* We have various citation systems (footnotes vs. author/date). And We have 'clashing' parentheses both in PDF and HTML for in text citations, but in different ways:

  * HTML: "writers ((Bruni 1978), (Bruni 1984)), scholars"
  * PDF: "writers (Bruni (1978), Bruni (1984)), scholars"



## Notes while remedying some of the above

* Only if the `.tex` source has `\begin{Abstract}` … `\end{Abstract}` with a **capital A** the abstract will be ported to HTML by Pandoc, as a plain no title, no header(!) paragraph. It can basically only be distinguished as the abstract by assuming it is the first `p` element after the document `header` element (css selector `header+p` ).
