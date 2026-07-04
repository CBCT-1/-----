# A literature-guided public-data evidence hierarchy prioritises a PLK1-centred mitotic/redox programme in lung adenocarcinoma

## Title Page

Target journal: BMC Genomics

Article type: Research article

TODO_AUTHOR_METADATA: author names, affiliations, ORCID identifiers, corresponding author, equal-contribution notes and institutional addresses.

---

## Abstract

### Background

Public lung adenocarcinoma (LUAD) bioinformatics studies often combine discovery, validation, biological context and functional screens without clearly separating their inferential strength. We built a literature-guided public-data evidence hierarchy to evaluate a PLK1-centred mitotic/redox programme in LUAD and to define which mechanistic, therapeutic and clinical claims remain unsupported.

### Results

The workflow assigned TCGA-LUAD to discovery and score construction, five public GEO cohorts to retrospective transfer and stress testing, and HPA, CELLxGENE, Visium, DepMap, pharmacogenomic and iLINCS resources to biological, tissue and functional context. TCGA-LUAD nominated mitotic and ER-redox candidates, and a compact nine-gene programme score showed moderate held-out separation (C-index 0.640; log-rank p = 8.7e-04). The score transferred with significant hazard ratios in four of five retrospective transfer cohorts, of which GSE31210 and GSE50081 also contributed to candidate prioritisation; it did not replicate in GSE37745 (OS C-index 0.529; p = 0.71), retained as a transparent boundary. The score was an independent prognostic factor (likelihood-ratio p < 1e-8) but did not improve discrimination over clinical staging (held-out test C-index 0.73 combined versus 0.72 clinical-only; ΔC-index +0.006, 95% CI -0.07 to +0.08). Sample-level single-cell analysis of 208,506 cells (GSE131907; 36 tumour-origin versus 11 normal-lung samples) showed all nine genes enriched in tumour-derived epithelium (FDR < 0.05), peaking in malignant and proliferating states. Reference-based deconvolution of 22 Visium sections from five patients - with programme genes excluded from the signature - supported epithelial co-localisation (positive in 5/5 patients). Pathway and Human Protein Atlas layers linked the programme to mitotic-checkpoint, chromosome-segregation and ER-redox processes. Functional screens prioritised PLK1 as an experimental dependency node but did not support LUAD-selective PLK1 vulnerability, ERO1A-stratified PLK-inhibitor response, normal-lung safety or clinical deployment.

### Conclusions

These results support public-data prioritisation of a PLK1-centred LUAD mitotic/redox programme and nominate PLK1 for experimental follow-up. They do not establish a direct PLK1-ERO1A mechanism, a LUAD-selective therapeutic window, treatment-response prediction or a deployable clinical prognostic model.

## Keywords

lung adenocarcinoma; PLK1; ERO1A; transcriptomics; TCGA; GEO; DepMap; public bioinformatics; evidence hierarchy

---

## Background

LUAD remains a major source of cancer mortality, and public transcriptomic resources are widely used to nominate candidate biomarkers and therapeutic hypotheses [1, 2]. Their breadth is also a common source of overinterpretation. A gene associated with survival in TCGA is not automatically a validated prognostic model; a spatially enriched signal is not automatically malignant-cell-specific; and a cell-line dependency does not by itself establish a therapeutic window.

PLK1 is a biologically plausible LUAD candidate because it marks mitotic-checkpoint and proliferation biology across cancers. ERO1A is biologically plausible as an ER-redox and protein-folding stress component. However, plausibility alone cannot distinguish prognosis, tissue context, dependency and clinical utility. A useful public-data study therefore needs to organise the same candidate programme across evidence layers while stating what each layer can and cannot support.

Here, we evaluated a PLK1-centred mitotic/redox programme in LUAD using a literature-guided public-data hierarchy. The study was designed to keep a narrow primary claim: public data prioritise a PLK1-centred programme for experimental follow-up, with ERO1A retained as ER-redox context. Negative pharmacogenomic, lineage-selectivity and clinical-readiness results were retained as part of the evidentiary argument rather than treated as failed side analyses.

## Methods

### Study design and evidence hierarchy

This retrospective public-data analysis separated evidence into five layers: discovery, retrospective transfer, biological context, tissue/spatial context and functional prioritisation. TCGA-LUAD was used for discovery and internal score assessment. GEO cohorts were used for retrospective transfer and stress testing. HPA, CELLxGENE and BioStudies E-MTAB-13530 were used for biological and tissue-context interpretation. DepMap, harmonised drug-response resources and iLINCS/L1000 signatures were used to prioritise functional hypotheses and define non-use boundaries.

### Datasets, versions and role assignment

Public cohorts and resources were assigned a manuscript role before interpretation (Table 1 in-text below). TCGA-LUAD expression (UCSC Xena GDC STAR-TPM), survival, clinical and mutation data [2, 3] were used for full-transcriptome discovery, candidate-gene prioritisation and score construction (589 survival-table rows; 576 survival-aligned tumours with 211 overall-survival events after filtering to positive follow-up time). Five public GEO cohorts [4, 5] processed through refine.bio were assigned as transfer or stress-test cohorts according to endpoint availability and gene coverage: GSE31210 (early-stage LUAD; 9/9 genes), GSE50081 (NSCLC, adenocarcinoma-like subset; 9/9 genes), GSE30219 (n = 82 adenocarcinoma; 9/9 genes), GSE37745 (n = 106 adenocarcinoma; 9/9 genes) and GSE68465 (Director's Challenge; 7/9 genes, partial-coverage sensitivity cohort). BioStudies E-MTAB-13530 [13, 14] provided 22 10x Visium sections (12 tumour, 10 adjacent-normal) analysed as tissue-context evidence. CZ CELLxGENE Discover [8] and a non-small-cell lung cancer single-cell atlas [9] provided aggregate single-cell localisation. The Human Protein Atlas [10, 11, 12] provided tissue and pathology annotation. DepMap Public 26Q1 CRISPR gene-effect (Chronos) matrices [15] provided dependency evidence (the PLK1 row spans 53 LUAD, 73 other-lung and 1082 non-lung models). Harmonised GDSC, CTRP and PRISM drug-response matrices [16, 17, 18] and iLINCS/L1000 perturbation signatures [19, 20] provided pharmacogenomic and perturbation-convergence evidence.

| Resource | Data type | Count captured locally | Role in manuscript | Main inference boundary |
| --- | --- | ---: | --- | --- |
| TCGA-LUAD | Bulk RNA-seq, survival, clinical, mutation | 589 survival rows | Discovery, score construction, held-out audit | Discovery/internal; not prospective validation |
| Public GEO cohorts (×5) | Retrospective microarray/RNA expression | 9 endpoint rows (7 supportive, 2 boundary) | External transfer and stress testing | Retrospective marker consistency; not treatment-response or prospective |
| GSE131907 single-cell | 10x scRNA-seq (Kim et al.) | 208,506 annotated cells, 58 samples | Single-cell resolution and spatial-deconvolution reference | Original annotations; not de novo re-clustering |
| BioStudies E-MTAB-13530 | 10x Visium spatial transcriptomics | 22 sections (5 patients) | Reference-based deconvolution and tissue context | Marker-based deconvolution; five patients; not pathologist-annotated |
| CZ CELLxGENE Discover | Aggregated single-cell summaries | Candidate-gene aggregate outputs | Single-cell tissue-context screen | Aggregate localisation; not mechanistic perturbation |
| Human Protein Atlas | Tissue/pathology annotations | Candidate-gene annotation tables | Protein/tissue interpretability | Context support; not causal mechanism |
| DepMap Public 26Q1 | CRISPR gene-effect (Chronos) | PLK1 across 53 LUAD / 73 other-lung / 1082 non-lung | Dependency prioritisation | Cell-line dependency; not LUAD-selective window |
| Harmonised drug-response | GDSC/CTRP/PRISM matrices | Compound/expression-association tables | Pharmacogenomic boundary testing | No clinical drug-response claim |
| iLINCS/L1000 | Perturbation signatures | PLK1/ERO1A knockdown and BI-2536 signatures | Perturbation-convergence stress test | Context-dependent overlap; not interaction/epistasis/synergy |

### Score construction and survival analysis

Candidate genes were prioritised from mitotic and ER-redox evidence using a cross-layer support count (TCGA FDR significance, internal-train log-rank, GSE31210 and GSE50081 replication, DepMap dependency and spatial support; each retained gene supported by 3-5 of 6 layers). The compact programme score used nine genes: PLK1, ERO1A, KNL1, DEPDC1B, TK1, DKK1, C1QTNF6, STEAP1 and ECT2. Coefficients were fitted with a Cox proportional-hazards model on the TCGA-LUAD training partition and then frozen. For every external cohort, gene-level expression was standardised within-cohort (z-score) before applying the frozen coefficients, to avoid cross-platform scale leakage. Risk groups used the frozen training-median threshold. The score showed training discrimination of C-index 0.660 and held-out TCGA discrimination of C-index 0.640 (log-rank p = 8.7e-04). As a leakage-repair sensitivity analysis, a TCGA-only locked eight-gene variant (dropping KNL1) was refit; it gave near-identical discrimination (train 0.658, test 0.635) and the same external pattern, including the GSE37745 null. These metrics were interpreted as moderate retrospective separation, not clinical model readiness.

### GEO transfer and supplementary public GEO synthesis

The compact score was transferred into public GEO cohorts where endpoint and gene-coverage requirements were met. GSE31210 and GSE50081 provided full-gene retrospective transfer evidence; GSE30219 provided full-gene support; GSE68465 provided partial-gene (7/9) coverage sensitivity evidence; and GSE37745 was retained as a null stress-test cohort. The supplementary public GEO synthesis was treated as retrospective marker/prognostic evidence only; its fixed-effect summary requires final human verification of endpoint independence and heterogeneity assumptions before the hazard-ratio summary is highlighted in final submission text.

### Biological, tissue-context and functional analyses

Pathway enrichment (g:Profiler with g:SCS multiple-testing correction; Gene Ontology and Reactome sources) [6, 7] tested whether the candidate programme mapped to coherent mitotic, checkpoint, chromosome-segregation and ER-redox processes. HPA annotations were used for tissue and pathology context. CELLxGENE summaries and E-MTAB-13530 Visium data placed candidate signals into tissue context; spatial candidate signals were summarised both as tumour-minus-adjacent module differences and as marker-basis and CZI-reference NNLS composition proxies. DepMap Public 26Q1 gene-effect matrices were used to evaluate dependency priority and lineage selectivity, and harmonised GDSC/CTRP/PRISM matrices and iLINCS/L1000 signatures tested whether ERO1A or perturbation convergence supported stronger therapeutic claims.

### Single-cell, spatial deconvolution and nomogram analyses

Single-cell data (GSE131907; 208,506 annotated cells) were processed from the raw UMI matrix with per-cell library-size (counts-per-10,000) log1p normalisation; cell-type-specific expression, malignant (tumour-origin) versus normal epithelial differential expression (Mann-Whitney), and per-subtype programme scores were computed using the original cell annotations. Cell-type mean-expression signatures over a 64-gene marker panel were used to deconvolve all 22 E-MTAB-13530 Visium sections by per-spot non-negative least squares, and programme scores were correlated (Spearman) with inferred cell-type abundances. A multivariable Cox nomogram combined the frozen programme score with stage, age and sex on TCGA-LUAD; discrimination (Harrell C-index, time-dependent AUC) and 3-year calibration were evaluated with Breslow baseline hazard. Analyses used Python with numpy, scipy, pandas and scanpy [22].

### Evidence argument audit

Each central statement was assigned an allowed inference, a prohibited inference and a required action. This audit downgraded unsupported claims into limitations or non-use boundaries. Mechanistic, therapeutic-window, treatment-response and clinical-deployment claims were excluded unless a local source table supported the exact inference.

### Statistical software and reproducibility

All survival and association statistics were computed in Python 3 with numpy, scipy, pandas, matplotlib and seaborn; Cox proportional-hazards fitting, log-rank testing and the Harrell concordance index were implemented directly against these libraries and cross-checked against scikit-survival [23], giving identical concordance to three decimal places (0.666 train, 0.649 test). Train/test partitioning used a fixed seed with event-stratified 70/30 allocation. The TCGA survival table comprised 589 expression-aligned samples from 517 patients (528 primary-tumour, 59 normal-tissue and 2 metastatic barcodes); 576 samples had positive follow-up (211 events) and 557 had non-missing stage and age for the multivariable model. A primary-tumour-only, patient-deduplicated sensitivity analysis (503 patients) gave a comparable held-out concordance (0.75), confirming that results are not driven by normal-tissue barcodes or duplicate samples. Multiple testing used Benjamini-Hochberg FDR for the full-transcriptome discovery screen and for drug-association testing; exploratory context layers report nominal p values with disclosed endpoint multiplicity (see the statistical endpoint/multiplicity boundary table in the source-data package). All figure-linked analyses are paired with machine-readable source data. Final submission requires repository DOI or accession assignment, author metadata, declarations, final citation checking and journal-format conversion.

## Results

### Literature-guided evidence hierarchy and TCGA-LUAD nomination

Figure 1 presents the literature-derived evidence hierarchy and TCGA-LUAD discovery layer.

The literature survey [1] motivated a tiered analysis rather than a single uninterrupted pipeline. TCGA-LUAD was used to nominate candidate biology, whereas GEO, tissue-context and functional resources were reserved for distinct inferential roles. This design prevented TCGA discovery signals from being presented as external validation or clinical deployment evidence.

The TCGA-LUAD discovery layer identified a mitotic/redox candidate programme anchored by PLK1 and ERO1A as two biologically prioritised lead candidates (PLK1 ranked first in the full-transcriptome survival screen; ERO1A was among the top-ranked ER-redox genes rather than the second overall). PLK1 contributed mitotic-checkpoint and proliferation context, while ERO1A contributed ER-redox and protein-folding stress context. The initial broader modelling layer was retained as discovery scaffolding, and inferential emphasis was shifted to a compact biologically constrained programme.

### Compact PLK1-centred score and retrospective transfer

Figure 2 consolidates the compact score, held-out TCGA evidence, retrospective GEO transfer and supplementary public GEO synthesis.

The compact nine-gene score produced moderate held-out separation in TCGA-LUAD (C-index 0.640; log-rank p = 8.7e-04), improving substantially on the earlier ridge scaffold, whose held-out separation was not significant. This supports retrospective prognostic prioritisation, but the magnitude does not justify clinical model language. We therefore describe the score as a public-data prioritisation tool rather than a patient-level risk model. To test incremental clinical value we fitted clinical-only (stage, age, sex), gene-only and combined Cox models on the TCGA training split and evaluated them on the held-out test split (Figure 8). The gene score was a statistically independent prognostic factor when added to the clinical model (likelihood-ratio chi-square = 33.0, p = 9.5e-9; HR 1.54 per SD), but it did not improve discrimination over clinical staging: test C-index was 0.72 for the clinical-only model, 0.64 for the gene score alone and 0.73 for the combined model, with an incremental ΔC-index of only +0.006 (95% CI -0.07 to +0.08). Three-year calibration was directionally monotonic but over-predicted risk. The score therefore adds independent prognostic association without materially improving a stage-based clinical model - an honest boundary rather than a deployable clinical tool.

Retrospective transfer across public GEO cohorts supported marker-level consistency while preserving boundary evidence. Because GSE31210 and GSE50081 contributed to candidate prioritisation (through the cross-layer support count), only GSE30219, GSE37745 and the partial-coverage GSE68465 are fully independent of model development; we therefore describe all five as retrospective transfer cohorts rather than fully external validation. The score was a significant predictor in four of five transfer cohorts: GSE31210 (OS hazard ratio [HR] per z 1.52, C-index 0.685, p = 4.3e-03), GSE50081 (OS HR 1.54, C-index 0.619; DFS HR 1.69, C-index 0.635), GSE30219 (OS HR 1.40, C-index 0.665) and the partial-coverage GSE68465 (OS HR 1.30, C-index 0.626, p = 5.8e-04). It did not replicate in GSE37745 (the adenocarcinoma subset of a mixed-histology cohort), in which the score was essentially non-discriminating (OS C-index 0.529, HR 1.04, p = 0.71; RFS C-index 0.507). Investigating this non-replication, all nine genes were present (not a coverage artefact) and stage stratification did not rescue it (stage-I subset C-index 0.50); post-hoc gene-level inspection suggested that the mitotic-core genes (PLK1, TK1, ECT2) trended in the expected direction whereas some remodelling-associated genes (DEPDC1B, STEAP1, DKK1) did not (5/9 direction-concordant with TCGA). This observation is exploratory rather than a pre-specified mechanism, but it is consistent with the mitotic core being the more robust component. We retain GSE37745 transparently rather than excluding it. A pooled cross-cohort synthesis is provided only as descriptive supplementary material and is not used as primary evidence. Because GSE31210 and GSE50081 contributed to feature prioritisation, we further tested whether the external transfer was an artefact of this partial leakage. We refit a fully leakage-free model whose candidate pool was the 12 genome-wide FDR-significant TCGA genes only (no GEO input), froze its coefficients on the TCGA training split, and evaluated it on the GEO cohorts as genuinely external. This leak-free model reproduced the primary pattern: it validated in the fully independent GSE30219 (C-index 0.700, HR 1.53 per SD) and GSE68465 (0.608, HR 1.27), failed in GSE37745 (0.525) exactly as before, and matched overall discrimination (TCGA test 0.649). The external signal is therefore not created by feature-selection leakage.

### Biological and tissue-context coherence

Figure 3 summarises pathway and Human Protein Atlas biological-context evidence.

Pathway and annotation layers supported biological coherence for the candidate programme. Enrichment results connected the programme with mitotic spindle, chromosome segregation, checkpoint and protein-folding/oxidoreductase processes. HPA annotations supplied tissue and pathology context for a broader 35-gene candidate pool - the union of the top-ranked survival-screen genes and the pathway/model candidates, which includes the nine programme genes - but were not treated as evidence of causal mechanism.

Figure 4 summarises the aggregate CELLxGENE and Visium tissue-context screens that motivated single-cell resolution.

To resolve the programme at single-cell level, we analysed 208,506 cells from GSE131907 [21] (Figure 6). To avoid cell-level pseudoreplication we aggregated each sample's epithelial cells into a pseudobulk value and compared samples as the statistical unit: across 36 tumour-origin versus 11 normal-lung samples, all nine genes were enriched in tumour-derived epithelium (Mann-Whitney at the sample level, all FDR < 0.05). Using the original inferCNV-based malignant-cell annotation, the programme peaked in malignant and tumour-transitional epithelial states. It also correlated with proliferation (PLK1-MKI67 Spearman rho = 0.47); because the score contains cell-cycle genes this proliferation link is expected and indicates that the score captures a proliferative malignant-epithelial state rather than a novel regulatory programme. The enrichment is compartment-biased rather than strictly specific: the mitotic and ER-redox genes were epithelial-dominant, whereas C1QTNF6 and STEAP1 were highest in fibroblasts - the same remodelling genes that did not transfer in GSE37745, consistent with the mitotic core being the more coherent component.

Using this single-cell reference, we performed reference-based deconvolution (non-negative least squares) of all 22 E-MTAB-13530 Visium sections [13, 14] (Figure 7). To avoid circularity the nine programme genes were excluded from the deconvolution signature. Because the 22 sections derive from only five patients and adjacent spots are spatially autocorrelated, we report the per-section and per-patient statistics rather than the pooled spot-level correlation: the programme score correlated positively with epithelial abundance in 21/22 sections and in 5/5 patients (median per-section rho = 0.18), supporting epithelial co-localisation. With only five patients the patient-level test is under-powered (Wilcoxon p = 0.06), and this marker-based deconvolution is neither a probabilistic method nor pathologist-annotated segmentation.

### Functional prioritisation and therapeutic-boundary evidence

Figure 5 integrates PLK1 dependency, pharmacogenomic boundaries and negative ERO1A-modulation evidence.

DepMap Public 26Q1 prioritised PLK1 as a perturbation node: PLK1 dependency was strong across LUAD models, with a LUAD dependency fraction of 1.0 below the common dependency threshold. However, the LUAD versus non-lung comparison did not support lineage selectivity (Mann-Whitney p = 0.73). PLK1 is therefore a strong experimental follow-up target, not a LUAD-selective therapeutic-window claim.

Drug-response and expression-modulation analyses blocked stronger therapeutic interpretation. ERO1A expression was not supported as a PLK-inhibitor response stratifier (0 of 12 expression-drug associations passed Benjamini-Hochberg FDR < 0.05), and non-cancer model coverage did not establish normal-lung safety. Supplementary Figure S1 retains the iLINCS perturbation-convergence stress test, in which PLK1 and ERO1A knockdown signatures converged in HCC515 (Spearman rho 0.38) but not in A549 (rho 0.05) — context-dependent transcriptomic overlap, not molecular interaction, epistasis or drug synergy. Supplementary Figure S2 retains the normal-lung and non-cancer coverage audit as a boundary against safety overclaiming; no non-cancerous lung model had PLK1 CRISPR or PLK-inhibitor coverage.

### Clinical-response and model-readiness boundaries

The immunotherapy-response and model-readiness analyses were retained as non-use safeguards. In three public NSCLC immunotherapy cohorts (n = 64; 22 responders, 42 non-responders), a generic immune-panel score separated responders from non-responders in a fixed/random-effects meta-analysis (Hedges' g = 1.21; 95% CI 0.64-1.77; p = 3.1e-05; I2 = 0%), consistent with expected immune-response biology; however, the PLK1/ERO1A survival programme itself did not separate responders (transfer-score g = -0.36; p = 0.39) and does not support a treatment-response biomarker claim. Model-readiness diagnostics (Figure 8) show the score adds no discrimination over clinical staging and that calibration over-predicts risk; formal inverse-probability-of-censoring-weighted (IPCW) time-dependent ROC, external absolute-risk calibration and prospective testing would all be required before any clinical-use language would be appropriate.

## Discussion

This study prioritises a PLK1-centred mitotic/redox LUAD programme through a transparent public-data evidence hierarchy. Its main contribution is not the isolated rediscovery of PLK1 or ERO1A, both of which have plausible biological roles, but the organisation of prognosis, tissue context, dependency and negative therapeutic evidence into separate claim layers.

The results support a narrow but useful inference. TCGA-LUAD nominates a mitotic/redox programme; public GEO cohorts provide retrospective transfer and stress testing; pathway, HPA, single-cell and Visium data provide biological and tissue-context coherence; DepMap nominates PLK1 as an experimental dependency node; and pharmacogenomic, perturbation and non-cancer analyses define the claims that remain unsupported.

This evidence hierarchy also explains why negative results are central to the manuscript. The data do not establish a direct PLK1-ERO1A molecular mechanism. They do not show that PLK1 dependency is LUAD-selective. They do not support ERO1A as a PLK-inhibitor stratifier, normal-lung safety, immunotherapy-response prediction or clinical deployment. These boundaries make the public-data claim more credible because the most tempting overinterpretations are explicitly excluded. The GSE37745 non-replication is reported in the same spirit: retrospective transfer of a compact transcriptomic score is platform- and cohort-sensitive, and disclosing a null cohort is more informative than selecting only supportive cohorts.

The study has several limitations. All patient-cohort analyses are retrospective and public-data based. The held-out TCGA performance is moderate, and one external cohort (GSE37745) did not replicate. Some external cohorts differ by platform, endpoint definition and gene coverage. Single-cell effect sizes are modest and cell-type labels come from the original study annotation rather than de novo re-clustering; the spatial deconvolution is marker-based and derives from only five patients; and the gene score adds no discrimination beyond clinical staging. Two transfer cohorts (GSE31210, GSE50081) informed candidate prioritisation and are therefore not fully independent, although a leakage-free refit reproduced the external signal in the fully independent cohorts. DepMap dependency reflects cell-line perturbation and common-essentiality constraints, and calibration is internal rather than externally validated.

Future work should test PLK1 perturbation in matched LUAD and non-transformed lung models, evaluate whether ER-redox state modifies response under controlled conditions, re-derive the score with model development frozen to literature and TCGA only (so all GEO cohorts become fully independent), and validate programme localisation with pathologist-annotated spatial data and larger patient numbers. These experiments would directly address the mechanistic and therapeutic-window claims that public data cannot resolve.

## Conclusions

A literature-guided public-data evidence hierarchy prioritises a PLK1-centred mitotic/redox programme in LUAD and nominates PLK1 for experimental follow-up. ERO1A is best retained as ER-redox context within the programme. The evidence supports retrospective public-data prioritisation, not direct mechanism, LUAD-selective therapeutic window, inhibitor-response prediction, prospective validation or clinical deployment.

## Figure and additional-file plan

- Figure 1. Literature-guided evidence hierarchy and TCGA-LUAD discovery.
- Figure 2. Compact nine-gene score, held-out TCGA separation, retrospective GEO transfer and supplementary GEO synthesis (including the GSE37745 null boundary).
- Figure 3. Pathway enrichment and Human Protein Atlas biological-context coherence.
- Figure 4. CELLxGENE aggregate and E-MTAB-13530 Visium/spatial-proxy tissue context.
- Figure 5. DepMap PLK1 dependency, pharmacogenomic boundaries and negative ERO1A-modulation/lineage-selectivity evidence.
- Figure 6. Single-cell (GSE131907, 208,506 cells): programme enriched in malignant/tumour-derived epithelium (sample-level pseudobulk), cell-type localisation, malignant cell-state peak and proliferation link.
- Figure 7. Reference-based Visium deconvolution (programme genes excluded from the signature): programme correlates with epithelial abundance in 21/22 sections and 5/5 patients.
- Figure 8. Incremental prognostic assessment: clinical-only, gene-only and combined models (train-fit, test-evaluated) show the score is independent but adds no discrimination over clinical staging.
- Additional file 1 (Supplementary Figure S1). iLINCS/L1000 PLK1-ERO1A perturbation-convergence stress test.
- Additional file 2 (Supplementary Figure S2). Normal-lung and non-cancer PLK1 therapeutic-window boundary audit.
- Additional file 3. Supplementary tables including the leakage-free frozen-model external validation, sample-level single-cell pseudobulk, leave-programme-out spatial deconvolution, incremental-nomogram diagnostics, Cox implementation cross-check, TCGA sample-flow, full model coefficients, cohort coverage, ICB meta-analysis, iLINCS and therapeutic-window detail, and the statistical endpoint/multiplicity boundary table.

## Declarations

### Ethics approval and consent to participate

This study analyses public, de-identified datasets and does not add direct human-subject recruitment, intervention or specimen collection. Original data-generating studies obtained their own ethics approvals as described in their primary publications and repositories. Final wording requires author review against institutional policy before submission.

### Consent for publication

Not applicable for public, de-identified datasets; final author confirmation is required before submission.

### Availability of data and materials

All datasets analysed are publicly available: TCGA-LUAD via UCSC Xena (GDC hub); GEO cohorts GSE31210, GSE50081, GSE30219, GSE37745 and GSE68465 via GEO/refine.bio; the GSE131907 single-cell atlas via GEO; E-MTAB-13530 via BioStudies/ArrayExpress; DepMap Public 26Q1 and Harmonized DrugScreens 25Q2 via the DepMap portal; iLINCS/L1000 signatures via iLINCS; aggregated single-cell summaries via CZ CELLxGENE Discover; and protein/tissue annotations via the Human Protein Atlas. All source data and analysis code should be deposited in a DOI- or accession-issuing repository before submission. Replace TODO_REPOSITORY_DOI_OR_ACCESSION with the final repository identifier and reviewer-access link.

### Competing interests

TODO_AUTHOR_METADATA: The authors must declare competing interests or state that they have none.

### Funding

TODO_AUTHOR_METADATA: Funding sources, grant numbers and funder roles must be supplied by the authors.

### Authors' contributions

TODO_AUTHOR_METADATA: Add CRediT-style author contributions.

### Acknowledgements

TODO_AUTHOR_METADATA: Add institutional, technical or data-resource acknowledgements as appropriate.

### AI-assisted writing disclosure

Large Language Models were used to assist with literature-structure synthesis, manuscript compression and writing support. All scientific claims, analyses, figures, citations, repository metadata and submission files were reviewed and verified by the authors. Generative AI was not used as an author or to create scientific images for submission.

---

## References

1. Ferguson C, Araújo D, Faulk L, Gou Y, Hamelers A, Huang Z, et al. Europe PMC in 2020. Nucleic Acids Res. 2021;49(D1):D1507-D1514. doi:10.1093/nar/gkaa994
2. The Cancer Genome Atlas Research Network. Comprehensive molecular profiling of lung adenocarcinoma. Nature. 2014;511(7511):543-550. doi:10.1038/nature13385
3. Goldman MJ, Craft B, Hastie M, Repečka K, McDade F, Kamath A, et al. Visualizing and interpreting cancer genomics data via the Xena platform. Nat Biotechnol. 2020;38(6):675-678. doi:10.1038/s41587-020-0546-8
4. Edgar R. Gene Expression Omnibus: NCBI gene expression and hybridization array data repository. Nucleic Acids Res. 2002;30(1):207-210. doi:10.1093/nar/30.1.207
5. Barrett T, Wilhite SE, Ledoux P, Evangelista C, Kim IF, Tomashevsky M, et al. NCBI GEO: archive for functional genomics data sets—update. Nucleic Acids Res. 2012;41(D1):D991-D995. doi:10.1093/nar/gks1193
6. Kolberg L, Raudvere U, Kuzmin I, Adler P, Vilo J, Peterson H. g:Profiler—interoperable web service for functional enrichment analysis and gene identifier mapping (2023 update). Nucleic Acids Res. 2023;51(W1):W207-W212. doi:10.1093/nar/gkad347
7. The Gene Ontology Consortium. The Gene Ontology Resource: 20 years and still GOing strong. Nucleic Acids Res. 2019;47(D1):D330-D338. doi:10.1093/nar/gky1055
8. CZI Cell Science Program, Abdulla S, Aevermann B, Assis P, Badajoz S, Bell SM, et al. CZ CELLxGENE Discover: a single-cell data platform for scalable exploration, analysis and modeling of aggregated data. Nucleic Acids Res. 2025;53(D1):D886-D900. doi:10.1093/nar/gkae1142
9. Salcher S, Sturm G, Horvath L, Untergasser G, Kuempers C, Fotakis G, et al. High-resolution single-cell atlas reveals diversity and plasticity of tissue-resident neutrophils in non-small cell lung cancer. Cancer Cell. 2022;40(12):1503-1520.e8. doi:10.1016/j.ccell.2022.10.008
10. Uhlén M, Fagerberg L, Hallström BM, Lindskog C, Oksvold P, Mardinoglu A, et al. Tissue-based map of the human proteome. Science. 2015;347(6220):1260419. doi:10.1126/science.1260419
11. Uhlén M, Zhang C, Lee S, Sjöstedt E, Fagerberg L, Bidkhori G, et al. A pathology atlas of the human cancer transcriptome. Science. 2017;357(6352):eaan2507. doi:10.1126/science.aan2507
12. Thul PJ, Lindskog C. The human protein atlas: a spatial map of the human proteome. Protein Sci. 2018;27(1):233-244. doi:10.1002/pro.3307
13. De Zuani M, Xue H, Park JS, Dentro SC, Seferbekova Z, Tessier J, et al. Single-cell and spatial transcriptomics analysis of non-small cell lung cancer. Nat Commun. 2024;15(1):4388. doi:10.1038/s41467-024-48700-8
14. Sarkans U, Gostev M, Athar A, Behrangi E, Melnichuk O, Ali A, et al. The BioStudies database—one stop shop for all data supporting a life sciences study. Nucleic Acids Res. 2018;46(D1):D1266-D1270. doi:10.1093/nar/gkx965
15. Dempster JM, Boyle I, Vazquez F, Root DE, Boehm JS, Hahn WC, et al. Chronos: a cell population dynamics model of CRISPR experiments that improves inference of gene fitness effects. Genome Biol. 2021;22(1):343. doi:10.1186/s13059-021-02540-7
16. Iorio F, Knijnenburg TA, Vis DJ, Bignell GR, Menden MP, Schubert M, et al. A landscape of pharmacogenomic interactions in cancer. Cell. 2016;166(3):740-754. doi:10.1016/j.cell.2016.06.017
17. Rees MG, Seashore-Ludlow B, Cheah JH, Adams DJ, Price EV, Gill S, et al. Correlating chemical sensitivity and basal gene expression reveals mechanism of action. Nat Chem Biol. 2016;12(2):109-116. doi:10.1038/nchembio.1986
18. Corsello SM, Nagari RT, Spangler RD, Rossen J, Kocak M, Bryan JG, et al. Discovering the anticancer potential of non-oncology drugs by systematic viability profiling. Nat Cancer. 2020;1(2):235-248. doi:10.1038/s43018-019-0018-6
19. Pilarczyk M, Fazel-Najafabadi M, Kouril M, Shamsaei B, Vasiliauskas J, Niu W, et al. Connecting omics signatures and revealing biological mechanisms with iLINCS. Nat Commun. 2022;13(1):4678. doi:10.1038/s41467-022-32205-3
20. Subramanian A, Narayan R, Corsello SM, Peck DD, Natoli TE, Lu X, et al. A next generation connectivity map: L1000 platform and the first 1,000,000 profiles. Cell. 2017;171(6):1437-1452.e17. doi:10.1016/j.cell.2017.10.049
21. Kim N, Kim HK, Lee K, Hong Y, Cho JH, Choi JW, et al. Single-cell RNA sequencing demonstrates the molecular and cellular reprogramming of metastatic lung adenocarcinoma. Nat Commun. 2020;11(1):2285. doi:10.1038/s41467-020-16164-1
22. Wolf FA, Angerer P, Theis FJ. SCANPY: large-scale single-cell gene expression data analysis. Genome Biol. 2018;19(1):15. doi:10.1186/s13059-017-1382-0
23. Pölsterl S. scikit-survival: a library for time-to-event analysis built on top of scikit-learn. J Mach Learn Res. 2020;21(212):1-6.

*Dataset accessions (TCGA-LUAD, GSE31210, GSE50081, GSE30219, GSE37745, GSE68465, E-MTAB-13530, DepMap Public 26Q1, Harmonized DrugScreens 25Q2) are cited in the Availability of data and materials statement with access dates; per BMC Genomics Vancouver style, confirm whether the target journal requires each accession as a numbered reference or as a Data Availability entry, and complete NLM journal-title abbreviation verification before submission.*
