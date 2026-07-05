# Main figure and additional-file legends (BMC Genomics, 8 main + 2 supplementary)

Eight main figures and two supplementary figures (BMC "Additional file" nomenclature). Figures 1-5 cover the
public-data evidence hierarchy; Figures 6-8 add single-cell resolution, reference-based spatial deconvolution and
the incremental prognostic assessment. Additional files 1-2 hold the iLINCS and therapeutic-window boundary figures.

---

## Figure 1. Literature-guided TCGA discovery nominates a PLK1- and ERO1A-centred LUAD programme.

**a,** Top-100 data-source and method frequencies supporting the TCGA/GEO-centred analysis blueprint. **b,** TCGA-LUAD median-split survival-screen ranking, with PLK1 and ERO1A highlighted. **c,** Cross-layer programme-nomination map for lead and context genes. **d,** Evidence boundary linking retrospective candidate nomination to the downstream validation workflow.

Counts are shown as study frequencies or discovery ranks; TCGA bars use -log10 log-rank P values and report Benjamini-Hochberg FDR where applicable.

Source data: Table 39, the top-100 evidence ledger, TCGA-LUAD full-transcriptome gene statistics and Table 2.

Interpretation boundary: the figure defines a workflow rationale and candidate-prioritisation entry point, not a systematic-review effect estimate or clinical-deployment claim.

## Figure 2. A biologically constrained nine-gene score improves held-out TCGA separation and transfers across most, but not all, public GEO cohorts.

**a,** Cross-layer support map and penalised Cox coefficients for the nine programme-score genes fitted in the TCGA training partition. **b,** Held-out TCGA Kaplan-Meier separation using the frozen training-median threshold, with the held-out C-index compared against the initial ridge scaffold. **c,** Cohort-by-model evidence-role matrix distinguishing supportive, null, complete and partial-coverage results across the five external GEO cohorts. **d,** Forest plot of nine-gene score transfer endpoints (hazard ratio per z-standardised score with 95% CI), with the frozen TCGA-only locked eight-gene sensitivity model shown as a comparator and GSE37745 marked as the null boundary.

Kaplan-Meier groups use the training-derived threshold and a log-rank test; concordance is the Harrell C-index; forest plots report Cox P values, C-index, sample size, event count and gene coverage in the source data.

Source data: Tables 22, 23, 31, 32, 33, 34 and 36; TCGA-LUAD consensus-score and internal ridge-model predictions.

Interpretation boundary: the held-out C-index of approximately 0.64 and the significant transfer in four of five cohorts support candidate prioritisation; GSE37745 is retained as a transparent null and GSE68465 as partial-coverage. This is retrospective stress testing and leakage repair, not prospective clinical validation, calibration or treatment selection.

## Figure 3. Pathway enrichment and HPA annotations support ER-redox and mitotic-checkpoint coherence.

**a,** g:Profiler pathway-theme strength for ER-redox/thiol-oxidase and mitotic/kinetochore terms. **b,** Distribution of HPA support classes across evaluated candidates. **c,** HPA TCGA-versus-validation pathology-signal concordance with PLK1 and ERO1A highlighted. **d,** Strong HPA-supported candidate nodes and protein-context roles.

Enrichment strength is displayed as -log10 adjusted P value (g:SCS correction); HPA panels report support classes and the local pathology-support metrics defined in the source tables.

Source data: Tables 11, 12, 14 and 37.

Interpretation boundary: enrichment and pathology concordance are interpretive support and do not establish causal mechanism, cell of origin or clinical deployment.

## Figure 4. Single-cell aggregates and Visium proxy analyses place the candidate programme in LUAD tissue context.

**a,** CZ CELLxGENE aggregate localisation signal for programme genes. **b,** E-MTAB-13530 tumour-minus-adjacent Visium candidate expression. **c,** Spatial proxy effect map across ER-redox, mitotic and strong-HPA signatures. **d,** Positive-section consistency across marker, malignant-proxy, marker-basis, CZI-reference and H&E-informed layers, highlighting the cross-method-robust tumour-context enrichment.

Visium comparisons report tumour-minus-adjacent mean log1p(CP10K) and Mann-Whitney P values; proxy layers report median Spearman rho or high-minus-other effects with section-level consistency.

Source data: Tables 13, 15, 20, 25, 27, 28, 30 and 38.

Interpretation boundary: these are aggregate and proxy-level tissue-context results, not pathologist-annotated segmentation, reference-based full-transcriptome deconvolution or malignant-cell specificity. Compartment-level labels are not consistent across proxy methods; only the tumour-context enrichment is treated as cross-method-robust.

## Figure 5. Cell-line functional genomics prioritise PLK1 dependency while bounding the therapeutic claim.

**a,** Candidate-gene dependency-priority ranking with PLK1 highlighted, and mean LUAD CRISPR gene effect versus dependency fraction. **b,** Top dependency-aligned compound-response associations across harmonised GDSC/CTRP/PRISM screens (lower AUC indicates stronger in vitro response). **c,** PLK1 Chronos gene-effect distributions in LUAD, other-lung and non-lung models with the -0.5 dependency threshold, showing common essentiality rather than LUAD selectivity. **d,** ERO1A-expression associations with PLK1 dependency and PLK-inhibitor sensitivity, shown as negative/boundary evidence.

Dependency panels report mean Chronos gene effect and dependency fraction; lineage comparisons use two-sided Mann-Whitney tests; expression-dependency and expression-drug associations use Spearman correlation with Benjamini-Hochberg correction (0 of 12 drug associations passed FDR < 0.05).

Source data: Tables 16, 17, 35 and 40; the DepMap26Q1/DrugResponse25Q2 model-level association tables.

Interpretation boundary: strong PLK1 dependency is not LUAD-selective, and ERO1A expression does not define PLK1 dependency or PLK-inhibitor sensitivity. The figure supports experimental triage, not mechanism, synergy, therapeutic window or patient-level treatment prediction.

---

## Figure 6. Single-cell (GSE131907, 208,506 cells): the programme is enriched in malignant/tumour-derived epithelium.

**a,** Programme-gene expression across annotated cell types (dot size = percent expressing; colour = mean expression). **b,** Sample-level pseudobulk differential expression (36 tumour-origin versus 11 normal-lung samples), avoiding cell-level pseudoreplication; all nine genes enriched at FDR<0.05. **c,** Programme score peaks in malignant and tumour-transitional epithelial states versus normal epithelium. **d,** Programme and PLK1 correlate with proliferation (MKI67) across epithelial cells.

Source data: sc_celltype_expression.csv, sc_malignant_vs_normal_epi.csv, sc_programme_by_epithelial_subtype.csv.

Interpretation boundary: enrichment is compartment-biased rather than strictly specific (C1QTNF6/STEAP1 peak in fibroblasts); statistics are at the sample level; cell-type/malignant labels are from the original inferCNV-based annotation, not de novo re-clustering.

## Figure 7. Reference-based Visium deconvolution (programme genes excluded from the signature; 22 sections from five patients).

**a,** Spearman correlation between programme score and inferred cell-type abundance (co-localisation ranking). **b,** Per-section programme-versus-epithelial correlation with programme genes excluded from the signature, positive in 21/22 sections and 5/5 patients (tumour sections darker).

Source data: spatial_deconv_programme_colocalisation.csv, spatial_deconv_section_consistency.csv.

Interpretation boundary: leave-programme-out marker-based NNLS deconvolution; only five patients, so the patient-level test is under-powered (Wilcoxon p=0.06); not a probabilistic method or pathologist-annotated segmentation. Spot-level pooling is avoided because adjacent spots are autocorrelated.

## Figure 8. Incremental prognostic assessment (TCGA-LUAD; train-fit, test-evaluated).

**a,** Harrell C-index, gene score alone versus score-plus-clinical nomogram (all TCGA and held-out test). **b,** Time-dependent AUC at 1/3/5 years. **c,** Three-year calibration across risk tertiles.

Source data: nomogram_cindex.csv, nomogram_timeAUC.csv, nomogram_coefficients.csv, nomogram_calibration_3yr.csv.

Interpretation boundary: the gene score alone remains C-index ~0.64; the combined gain derives from adding stage. Apparent (in-sample) calibration; not prospective validation.

---

## Additional file 1 (Supplementary Figure S1). PLK1 and ERO1A perturbation signatures show cell-context-dependent convergence.

**a,** Pairwise Spearman similarity among PLK1 knockdown, ERO1A knockdown and 10-µM BI-2536 signatures in A549 and HCC515. **b,** Pre-specified comparisons of cross-cell knockdown reproducibility, within-cell PLK1-ERO1A knockdown convergence and 24-hour BI-2536 similarity. **c,** Similarity of six 24-hour BI-2536 dose signatures to PLK1 or ERO1A knockdown in each cell line. **d,** Gene-level PLK1-versus-ERO1A knockdown response in HCC515.

All signature correlations use 978 shared L1000 genes. Directional overlap uses the top 50 genes per direction. Correlations are descriptive effect sizes; genes and dose levels are not treated as independent biological replicates.

Source data: Table 41 and the iLINCS signature-matrix, pairwise-similarity, signed-overlap and dose-similarity tables.

Interpretation boundary: HCC515-specific convergence (rho 0.38) is not reproduced in A549 (rho 0.05). BI-2536 was measured at 6 or 24 hours and knockdown at 96 hours. The figure does not establish molecular interaction, epistasis, pathway ordering or drug synergy.

## Additional file 2 (Supplementary Figure S2). Public functional screens do not establish a LUAD-selective PLK1 therapeutic window.

**a,** PLK1 Chronos gene-effect distributions in LUAD, models labelled non-cancerous, and a sensitivity analysis collapsing five engineered RPE1 clones to one median analysis unit (dashed line: -0.5 dependency threshold; horizontal bars: medians). **b,** Coverage audit for six non-cancerous lung models present in DepMap metadata. **c,** Screen-specific difference in mean PLK-inhibitor AUC between LUAD and heterogeneous non-cancer models (negative values indicate lower mean AUC in LUAD; labels report model counts). **d,** Explicit evidence boundary.

Dependency comparisons use two-sided Mann-Whitney tests and rank-biserial effect sizes. Drug screens are not pooled. Non-cancerous models are immortalised, transformed or otherwise cultured models and are not equivalent to normal tissue.

Source data: Table 42 and the DepMap26Q1 dependency, normal-lung coverage, drug-response and expression-context tables.

Interpretation boundary: no non-cancerous lung model had PLK1 CRISPR or PLK-inhibitor AUC coverage. The figure does not establish normal-tissue safety, a therapeutic window or patient treatment response.

## Additional file 3. Supplementary tables.

Full programme-model coefficients, external-cohort coverage, calibration/decision-curve/time-horizon diagnostics, the NSCLC ICB expression meta-analysis, iLINCS perturbation detail, the PLK1 therapeutic-window audit and the statistical endpoint/multiplicity boundary table (project Tables 22-42), provided as machine-readable source data.
