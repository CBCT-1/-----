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

The workflow assigned TCGA-LUAD to discovery and score construction, five public GEO cohorts to retrospective transfer and stress testing, and HPA, CELLxGENE, Visium, DepMap, pharmacogenomic and iLINCS resources to biological, tissue and functional context. TCGA-LUAD nominated mitotic and ER-redox candidates, and a compact nine-gene programme score showed moderate held-out separation (C-index 0.640; log-rank p = 8.7e-04). The score transferred with significant hazard ratios in four of five external cohorts (GSE31210, GSE50081, GSE30219 and the partial-coverage GSE68465) but did not replicate in GSE37745 (OS C-index 0.529; p = 0.71), which we retain as a transparent external boundary. Biological-context analyses linked the programme to mitotic-checkpoint, chromosome-segregation and ER-redox processes, and Visium analyses placed candidate signals in tumour-section-enriched tissue context. Functional screens prioritised PLK1 as an experimental dependency node but did not support LUAD-selective PLK1 vulnerability, ERO1A-stratified PLK-inhibitor response, normal-lung safety or clinical deployment.

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
| BioStudies E-MTAB-13530 | 10x Visium spatial transcriptomics | 22 sections (12 tumour, 10 adjacent-normal) | Tissue-context localisation | Spatial proxy; not cell-type-resolved malignant specificity |
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

### Evidence argument audit

Each central statement was assigned an allowed inference, a prohibited inference and a required action. This audit downgraded unsupported claims into limitations or non-use boundaries. Mechanistic, therapeutic-window, treatment-response and clinical-deployment claims were excluded unless a local source table supported the exact inference.

### Statistical software and reproducibility

All survival and association statistics were computed in Python 3 with numpy, scipy, pandas, matplotlib and seaborn; Cox proportional-hazards fitting, log-rank testing and the Harrell concordance index were implemented directly against these libraries and cross-checked against the frozen source tables. Multiple testing used Benjamini-Hochberg FDR for the full-transcriptome discovery screen and for drug-association testing; exploratory context layers report nominal p values with disclosed endpoint multiplicity (see the statistical endpoint/multiplicity boundary table in the source-data package). All figure-linked analyses are paired with machine-readable source data. Final submission requires repository DOI or accession assignment, author metadata, declarations, final citation checking and journal-format conversion.

## Results

### Literature-guided evidence hierarchy and TCGA-LUAD nomination

Figure 1 presents the literature-derived evidence hierarchy and TCGA-LUAD discovery layer.

The literature survey [1] motivated a tiered analysis rather than a single uninterrupted pipeline. TCGA-LUAD was used to nominate candidate biology, whereas GEO, tissue-context and functional resources were reserved for distinct inferential roles. This design prevented TCGA discovery signals from being presented as external validation or clinical deployment evidence.

The TCGA-LUAD discovery layer identified a mitotic/redox candidate programme anchored by PLK1 and ERO1A, the two strongest-ranked candidates in the full-transcriptome survival screen. PLK1 contributed mitotic-checkpoint and proliferation context, while ERO1A contributed ER-redox and protein-folding stress context. The initial broader modelling layer was retained as discovery scaffolding, and inferential emphasis was shifted to a compact biologically constrained programme.

### Compact PLK1-centred score and retrospective transfer

Figure 2 consolidates the compact score, held-out TCGA evidence, retrospective GEO transfer and supplementary public GEO synthesis.

The compact nine-gene score produced moderate held-out separation in TCGA-LUAD (C-index 0.640; log-rank p = 8.7e-04), improving substantially on the earlier ridge scaffold, whose held-out separation was not significant. This supports retrospective prognostic prioritisation, but the magnitude does not justify clinical model language. We therefore describe the score as a public-data prioritisation tool rather than a patient-level risk model.

Retrospective transfer across public GEO cohorts supported marker-level consistency while preserving boundary evidence. The score was a significant predictor in four of five external cohorts: GSE31210 (OS hazard ratio [HR] per z 1.52, C-index 0.685, p = 4.3e-03), GSE50081 (OS HR 1.54, C-index 0.619; DFS HR 1.69, C-index 0.635), GSE30219 (OS HR 1.40, C-index 0.665) and the partial-coverage GSE68465 (OS HR 1.30, C-index 0.626, p = 5.8e-04). It did not replicate in GSE37745, a mixed-histology cohort in which the score was essentially non-discriminating (OS C-index 0.529, HR 1.04, p = 0.71; RFS C-index 0.507). We retain GSE37745 as a transparent external non-replication rather than excluding it. The supplementary public GEO synthesis summarised the transfer layer across cohorts and recorded a fixed-effect hazard ratio of 1.346 (95% CI 1.249-1.450; p = 5.5e-15; I2 = 43.1%). Because endpoint independence and heterogeneity handling require final human verification, this summary is treated as supplementary retrospective public-cohort evidence rather than primary validation.

### Biological and tissue-context coherence

Figure 3 summarises pathway and Human Protein Atlas biological-context evidence.

Pathway and annotation layers supported biological coherence for the candidate programme. Enrichment results connected the programme with mitotic spindle, chromosome segregation, checkpoint and protein-folding/oxidoreductase processes. HPA annotations supplied tissue and pathology context for candidate genes but were not treated as evidence of causal mechanism.

Figure 4 summarises CELLxGENE, Visium and spatial-proxy tissue-context evidence.

Single-cell aggregate and Visium analyses placed candidate genes into lung tumour tissue context. The E-MTAB-13530 analysis showed higher tumour-section than adjacent-normal section module signals for mitotic, ER-redox and HPA-supported candidate groups, and tumour-context enrichment was the signal that remained directionally consistent across independent spatial proxy methods (marker-basis and CZI-reference composition). We note that the compartment-level labels of the two proxy methods diverge (for example, the epithelial-compartment sign is not consistent between methods), so we report only the cross-method-robust tumour-context enrichment and treat compartment-resolved assignments as proxy-level. These analyses remain below the threshold for malignant-cell-specific localisation or pathologist-annotated spatial mechanism.

### Functional prioritisation and therapeutic-boundary evidence

Figure 5 integrates PLK1 dependency, pharmacogenomic boundaries and negative ERO1A-modulation evidence.

DepMap Public 26Q1 prioritised PLK1 as a perturbation node: PLK1 dependency was strong across LUAD models, with a LUAD dependency fraction of 1.0 below the common dependency threshold. However, the LUAD versus non-lung comparison did not support lineage selectivity (Mann-Whitney p = 0.73). PLK1 is therefore a strong experimental follow-up target, not a LUAD-selective therapeutic-window claim.

Drug-response and expression-modulation analyses blocked stronger therapeutic interpretation. ERO1A expression was not supported as a PLK-inhibitor response stratifier (0 of 12 expression-drug associations passed Benjamini-Hochberg FDR < 0.05), and non-cancer model coverage did not establish normal-lung safety. Supplementary Figure S1 retains the iLINCS perturbation-convergence stress test, in which PLK1 and ERO1A knockdown signatures converged in HCC515 (Spearman rho 0.38) but not in A549 (rho 0.05) — context-dependent transcriptomic overlap, not molecular interaction, epistasis or drug synergy. Supplementary Figure S2 retains the normal-lung and non-cancer coverage audit as a boundary against safety overclaiming; no non-cancerous lung model had PLK1 CRISPR or PLK-inhibitor coverage.

### Clinical-response and model-readiness boundaries

The immunotherapy-response and model-readiness analyses were retained as non-use safeguards. In three public NSCLC immunotherapy cohorts (n = 64; 22 responders, 42 non-responders), a generic immune-panel score separated responders from non-responders in a fixed/random-effects meta-analysis (Hedges' g = 1.21; 95% CI 0.64-1.77; p = 3.1e-05; I2 = 0%), consistent with expected immune-response biology; however, the PLK1/ERO1A survival programme itself did not separate responders (transfer-score g = -0.36; p = 0.39) and does not support a treatment-response biomarker claim. Apparent (in-sample) calibration and decision-curve outputs remain useful diagnostics (held-out TCGA 3-year AUC 0.678), but formal inverse-probability-of-censoring-weighted (IPCW) time-dependent ROC, external absolute-risk calibration and prospective testing are required before clinical-use language would be appropriate.

## Discussion

This study prioritises a PLK1-centred mitotic/redox LUAD programme through a transparent public-data evidence hierarchy. Its main contribution is not the isolated rediscovery of PLK1 or ERO1A, both of which have plausible biological roles, but the organisation of prognosis, tissue context, dependency and negative therapeutic evidence into separate claim layers.

The results support a narrow but useful inference. TCGA-LUAD nominates a mitotic/redox programme; public GEO cohorts provide retrospective transfer and stress testing; pathway, HPA, single-cell and Visium data provide biological and tissue-context coherence; DepMap nominates PLK1 as an experimental dependency node; and pharmacogenomic, perturbation and non-cancer analyses define the claims that remain unsupported.

This evidence hierarchy also explains why negative results are central to the manuscript. The data do not establish a direct PLK1-ERO1A molecular mechanism. They do not show that PLK1 dependency is LUAD-selective. They do not support ERO1A as a PLK-inhibitor stratifier, normal-lung safety, immunotherapy-response prediction or clinical deployment. These boundaries make the public-data claim more credible because the most tempting overinterpretations are explicitly excluded. The GSE37745 non-replication is reported in the same spirit: retrospective transfer of a compact transcriptomic score is platform- and cohort-sensitive, and disclosing a null cohort is more informative than selecting only supportive cohorts.

The study has several limitations. All patient-cohort analyses are retrospective and public-data based. The held-out TCGA performance is moderate, and one external cohort (GSE37745) did not replicate. Some external cohorts differ by platform, endpoint definition and gene coverage. Single-cell evidence is aggregate rather than raw-cell, and spatial analyses rely on aggregate and proxy-level composition rather than full malignant-cell segmentation or reference-based deconvolution. DepMap dependency reflects cell-line perturbation and common-essentiality constraints. Calibration is apparent rather than externally validated, and the fixed-effect GEO synthesis requires final verification of endpoint independence and heterogeneity handling before it is emphasised in the final abstract.

Future work should test PLK1 perturbation in matched LUAD and non-transformed lung models, evaluate whether ER-redox state modifies response under controlled conditions, add raw single-cell and reference-based spatial deconvolution, and validate programme localisation with stronger spatial annotation. These experiments would directly address the mechanistic and therapeutic-window claims that public data cannot resolve.

## Conclusions

A literature-guided public-data evidence hierarchy prioritises a PLK1-centred mitotic/redox programme in LUAD and nominates PLK1 for experimental follow-up. ERO1A is best retained as ER-redox context within the programme. The evidence supports retrospective public-data prioritisation, not direct mechanism, LUAD-selective therapeutic window, inhibitor-response prediction, prospective validation or clinical deployment.

## Figure and additional-file plan

- Figure 1. Literature-guided evidence hierarchy and TCGA-LUAD discovery.
- Figure 2. Compact nine-gene score, held-out TCGA separation, retrospective GEO transfer and supplementary GEO synthesis (including the GSE37745 null boundary).
- Figure 3. Pathway enrichment and Human Protein Atlas biological-context coherence.
- Figure 4. CELLxGENE aggregate and E-MTAB-13530 Visium/spatial-proxy tissue context.
- Figure 5. DepMap PLK1 dependency, pharmacogenomic boundaries and negative ERO1A-modulation/lineage-selectivity evidence.
- Additional file 1 (Supplementary Figure S1). iLINCS/L1000 PLK1-ERO1A perturbation-convergence stress test.
- Additional file 2 (Supplementary Figure S2). Normal-lung and non-cancer PLK1 therapeutic-window boundary audit.
- Additional file 3. Supplementary tables (full model, cohort coverage, calibration/DCA/horizon, ICB meta-analysis, iLINCS and therapeutic-window detail) and the statistical endpoint/multiplicity boundary table.

## Declarations

### Ethics approval and consent to participate

This study analyses public, de-identified datasets and does not add direct human-subject recruitment, intervention or specimen collection. Original data-generating studies obtained their own ethics approvals as described in their primary publications and repositories. Final wording requires author review against institutional policy before submission.

### Consent for publication

Not applicable for public, de-identified datasets; final author confirmation is required before submission.

### Availability of data and materials

All datasets analysed are publicly available: TCGA-LUAD via UCSC Xena (GDC hub); GEO cohorts GSE31210, GSE50081, GSE30219, GSE37745 and GSE68465 via GEO/refine.bio; E-MTAB-13530 via BioStudies/ArrayExpress; DepMap Public 26Q1 and Harmonized DrugScreens 25Q2 via the DepMap portal; iLINCS/L1000 signatures via iLINCS; aggregated single-cell summaries via CZ CELLxGENE Discover; and protein/tissue annotations via the Human Protein Atlas. All source data and analysis code should be deposited in a DOI- or accession-issuing repository before submission. Replace TODO_REPOSITORY_DOI_OR_ACCESSION with the final repository identifier and reviewer-access link.

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

*Dataset accessions (TCGA-LUAD, GSE31210, GSE50081, GSE30219, GSE37745, GSE68465, E-MTAB-13530, DepMap Public 26Q1, Harmonized DrugScreens 25Q2) are cited in the Availability of data and materials statement with access dates; per BMC Genomics Vancouver style, confirm whether the target journal requires each accession as a numbered reference or as a Data Availability entry, and complete NLM journal-title abbreviation verification before submission.*
