all:
	pdflatex *.tex
	bibtex *.aux
	pdflatex *.tex
	pdflatex *.tex
	pdflatex *.tex

clean:
	-rm *.aux 2>/dev/null
	-rm *.log 2>/dev/null
	-rm *.toc 2>/dev/null
	-rm *.out 2>/dev/null
	-rm *.synctex.gz 2>/dev/null
	-rm *.fdb_latexmk 2>/dev/null
	-rm *.bbl 2>/dev/null
	-rm *.blg 2>/dev/null