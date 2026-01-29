# Makefile for building main.tex into main.pdf
# Usage:
#   make build    # build PDF (prefers latexmk, falls back to pdflatex)
#   make view     # build then open PDF (xdg-open on Linux)
#   make clean    # remove generated files

SRCTEX := main.tex
PDF := $(SRCTEX:.tex=.pdf)

.PHONY: all build clean view
all: build

build:
	@echo "Building $(SRCTEX) -> $(PDF)"
	@if [ ! -f "$(SRCTEX)" ]; then \
		echo "Source file '$(SRCTEX)' not found. Please create it or adjust SRCTEX in the Makefile."; \
		exit 1; \
	fi
	@if command -v latexmk >/dev/null 2>&1; then \
		echo "Using latexmk..."; \
		latexmk -pdf -interaction=nonstopmode $(SRCTEX); \
	elif command -v pdflatex >/dev/null 2>&1; then \
		echo "latexmk not found, falling back to pdflatex (2 passes)..."; \
		pdflatex -interaction=nonstopmode $(SRCTEX) || exit 1; \
		pdflatex -interaction=nonstopmode $(SRCTEX) || exit 1; \
	else \
		echo "Error: neither 'latexmk' nor 'pdflatex' were found in PATH. Please install a TeX distribution (e.g., TeX Live) and try again."; \
		exit 1; \
	fi

view: build
	@echo "Opening $(PDF)"
	@if command -v xdg-open >/dev/null 2>&1; then \
		xdg-open $(PDF) >/dev/null 2>&1 & \
	else \
		echo "Please open $(PDF) manually (xdg-open not found)"; \
	fi

clean:
	@echo "Cleaning generated files"
	@rm -f $(PDF) *.aux *.log *.out *.toc *.fls *.fdb_latexmk *.synctex.gz *.nav *.snm *.vrb
