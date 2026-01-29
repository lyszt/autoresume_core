# Makefile for building main.tex into main.pdf
# Usage:
#   make build    # build PDF (prefers latexmk, falls back to pdflatex)
#   make view     # build then open PDF (xdg-open on Linux)
#   make clean    # remove generated files

TEX ?= main.tex
PDF := $(TEX:.tex=.pdf)

.PHONY: all build clean view
all: build

build:
	@echo "Building $(TEX) -> $(PDF)"
	@if command -v latexmk >/dev/null 2>&1; then \
		echo "Using latexmk..."; \
		latexmk -pdf -interaction=nonstopmode $(TEX); \
	else \
		echo "latexmk not found, falling back to pdflatex (2 passes)..."; \
		pdflatex -interaction=nonstopmode $(TEX) || exit 1; \
		pdflatex -interaction=nonstopmode $(TEX) || exit 1; \
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
