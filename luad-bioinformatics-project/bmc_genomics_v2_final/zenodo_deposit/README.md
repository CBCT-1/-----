# LUAD PLK1/ERO1A public-data evidence hierarchy — code & source data

This repository accompanies the manuscript "A literature-guided public-data evidence hierarchy
prioritises a PLK1-centred mitotic/redox programme in lung adenocarcinoma" (target: BMC Genomics).

## Contents to deposit
- `code/` — all analysis scripts (Python; numpy/scipy/pandas/matplotlib/seaborn) and figure code.
- `source_data/` — machine-readable source-data tables for every figure panel (project Tables 1–42).
- `figures/` — main + supplementary figures (PDF vector + PNG).
- `manuscript/` — final manuscript and figure legends.

## Data sources (all public; not re-distributed here beyond derived tables)
- TCGA-LUAD via UCSC Xena (GDC hub)
- GEO/refine.bio: GSE31210, GSE50081, GSE30219, GSE37745, GSE68465
- BioStudies/ArrayExpress: E-MTAB-13530 (10x Visium)
- DepMap Public 26Q1; Harmonized DrugScreens 25Q2
- iLINCS / L1000; CZ CELLxGENE Discover; Human Protein Atlas

## Environment
Python 3 with numpy, scipy, pandas, matplotlib, seaborn, python-docx. Cox proportional-hazards,
log-rank and Harrell C-index are implemented directly against these libraries.

## Reproduce figures
`python make_figures.py` regenerates all 7 figures from the source tables.

## Licence
- Code: TODO_AUTHOR_CHOOSE (template: MIT — see LICENSE-CODE-MIT.txt)
- Derived data: TODO_AUTHOR_CHOOSE (template: CC BY 4.0 — see LICENSE-DATA-CC-BY-4.0.txt)

## Cite
TODO_AUTHOR_METADATA: authors, year, title, repository DOI (minted on deposit).
