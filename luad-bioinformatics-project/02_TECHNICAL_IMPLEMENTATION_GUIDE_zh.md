# 技术实施指南：从当前状态到一区投稿

---

## 一、新增数据获取清单与方法

### 1.1 scRNA-seq 数据（最高优先级）

#### 主力数据集：GSE131907 (Kim et al., Nat Med 2020)

```bash
# GEO 下载 (raw counts)
# 地址: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE131907
# 包含: 58 samples, ~208,506 cells
# 包括: primary LUAD, metastatic, normal lung, lymph node
# 格式: 10x Genomics filtered feature-barcode matrices

# 用 GEO 提供的 supplementary files
wget -P raw_data/scRNA/ "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE131nnn/GSE131907/suppl/"

# 或使用 SRA toolkit
prefetch SRP198326
fasterq-dump SRP198326 --outdir raw_data/scRNA/GSE131907/
```

**为什么选这个**: 这是 NSCLC scRNA-seq 引用率最高的数据集之一，审稿人熟悉，有完整的 cell type annotation 可以做 benchmark。

#### 补充数据集推荐

| 数据集 | 细胞数 | 下载方式 | 优先级 |
|--------|--------|----------|--------|
| GSE131907 | ~208K | GEO suppl files | 必须 |
| GSE171145 | ~100K | GEO suppl files | 强推 |
| HLCA (Sikkema et al., Nat Med 2023) | >2M | CELLxGENE portal .h5ad | 推荐(正常参考) |

### 1.2 额外外部验证队列

```bash
# GSE72094 (Schabath et al., JCO 2016) - 442 LUAD samples with RNA-seq + clinical
# 地址: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE72094

# GSE68465 (Director's Challenge) - 443 LUAD microarray + survival
# 地址: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE68465

# GSE37745 - European NSCLC cohort
# 地址: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE37745
```

### 1.3 TCGA 多组学扩展

```bash
# 从 UCSC Xena 下载 (与你现有 TCGA 数据同源)
# DNA Methylation 450K
# https://xenabrowser.net/datapages/ → TCGA-LUAD → DNA Methylation

# Copy Number Variation (Gene-level)
# TCGA-LUAD.gistic.tsv.gz

# miRNA expression
# TCGA-LUAD.mirna.tsv.gz
```

### 1.4 CPTAC-LUAD 蛋白组

```bash
# CPTAC Lung Adenocarcinoma Discovery Study
# 地址: https://cptac-data-portal.georgetown.edu/
# 或 PDC: https://pdc.cancer.gov/
# 数据: 110 tumor + 101 normal adjacent, TMT proteomics
# 用途: 蛋白水平验证基因表达发现
```

---

## 二、新增核心分析的技术方案

### 2.1 scRNA-seq 完整分析流程

#### 环境准备

```bash
# R packages
install.packages(c("Seurat", "harmony", "SingleR", "ggplot2"))
BiocManager::install(c("scran", "scater", "infercnv", "clusterProfiler", "GSVA"))
devtools::install_github("sqjin/CellChat")
devtools::install_github("aertslab/SCENIC")

# Python packages
pip install scanpy anndata scvi-tools loompy pyscenic cellrank
```

#### 分析流程（R + Seurat 为主）

```r
# ============================================
# Step 1: 数据读入与质控
# ============================================
library(Seurat)
library(harmony)

# 读入 10x 数据
data_dirs <- list.dirs("raw_data/scRNA/GSE131907", recursive = FALSE)
seurat_list <- lapply(data_dirs, function(d) {
  Read10X(d) |> CreateSeuratObject(min.cells = 3, min.features = 200)
})

# 合并
merged <- merge(seurat_list[[1]], seurat_list[-1])

# QC metrics
merged[["percent.mt"]] <- PercentageFeatureSet(merged, pattern = "^MT-")
merged <- subset(merged,
  nFeature_RNA > 200 & nFeature_RNA < 6000 &
  percent.mt < 20 & nCount_RNA > 500)

# ============================================
# Step 2: 标准化 + 降维 + 批次校正
# ============================================
merged <- NormalizeData(merged) |>
  FindVariableFeatures(nfeatures = 3000) |>
  ScaleData() |>
  RunPCA(npcs = 50)

# Harmony 批次校正
merged <- RunHarmony(merged, group.by.vars = "orig.ident")
merged <- RunUMAP(merged, reduction = "harmony", dims = 1:30) |>
  FindNeighbors(reduction = "harmony", dims = 1:30) |>
  FindClusters(resolution = c(0.3, 0.5, 0.8, 1.0))

# ============================================
# Step 3: 细胞类型注释
# ============================================
library(SingleR)

# 自动注释 (初筛)
ref <- celldex::HumanPrimaryCellAtlasData()
pred <- SingleR(test = GetAssayData(merged), ref = ref, labels = ref$label.fine)
merged$singler_label <- pred$pruned.labels

# 手动精细注释 (基于 canonical markers)
# Epithelial: EPCAM, KRT7, KRT19
# Malignant: 通过 InferCNV 鉴定
# T cells: CD3D, CD3E, CD4, CD8A
# B cells: CD79A, MS4A1
# Myeloid: CD68, CD163, CD14
# Fibroblast: COL1A1, DCN
# Endothelial: PECAM1, VWF

# ============================================
# Step 4: InferCNV 恶性细胞鉴定
# ============================================
library(infercnv)

# 用正常肺上皮作为 reference
infercnv_obj <- CreateInfercnvObject(
  raw_counts_matrix = GetAssayData(merged, slot = "counts"),
  annotations_file = "cell_annotations.txt",
  gene_order_file = "gene_positions.txt",
  ref_group_names = c("Normal_Epithelial"))

infercnv_obj <- infercnv::run(infercnv_obj,
  cutoff = 0.1, cluster_by_groups = TRUE,
  denoise = TRUE, HMM = TRUE, num_threads = 8)

# ============================================
# Step 5: 候选基因在各细胞类型中的表达
# ============================================
# 你的 8 个 Cox model genes
candidate_genes <- c("GENE1", "GENE2", "GENE3", ...) # 替换为你的实际基因

# DotPlot
DotPlot(merged, features = candidate_genes, group.by = "cell_type") +
  RotatedAxis()

# 恶性 vs 非恶性差异表达
malignant <- subset(merged, cell_type == "Malignant")
nonmalignant <- subset(merged, cell_type != "Malignant")
deg <- FindMarkers(merged, ident.1 = "Malignant", ident.2 = "Non-Malignant",
                   features = candidate_genes)

# ============================================
# Step 6: CellChat 细胞通讯
# ============================================
library(CellChat)

cellchat <- createCellChat(object = merged, group.by = "cell_type")
cellchat@DB <- CellChatDB.human
cellchat <- subsetData(cellchat)
cellchat <- identifyOverExpressedGenes(cellchat)
cellchat <- identifyOverExpressedInteractions(cellchat)
cellchat <- computeCommunProb(cellchat)
cellchat <- computeCommunProbPathway(cellchat)
cellchat <- aggregateNet(cellchat)

# 高风险 vs 低风险组的通讯差异
# (基于你的 risk score 分组)

# ============================================
# Step 7: 发育轨迹分析
# ============================================
library(monocle3)

# 转换为 monocle3 对象
cds <- as.cell_data_set(merged)
cds <- cluster_cells(cds)
cds <- learn_graph(cds)
cds <- order_cells(cds) # 交互选择 root

# 候选基因沿轨迹的表达变化
plot_genes_in_pseudotime(cds, candidate_genes)
```

### 2.2 空间转录组深度分析（基于你已有的 E-MTAB-13530）

```python
# ============================================
# 空间 Deconvolution: cell2location
# ============================================
import scanpy as sc
import cell2location
import numpy as np

# 读入 Visium 数据 (你已有 .h5 文件)
adata_vis = sc.read_visium("path/to/visium/section/")
adata_vis.var_names_make_unique()

# 读入 scRNA-seq reference (来自 GSE131907 分析结果)
adata_ref = sc.read_h5ad("processed/scRNA_annotated.h5ad")

# cell2location reference model
from cell2location.models import RegressionModel
cell2location.models.RegressionModel.setup_anndata(adata_ref, labels_key="cell_type")
mod = RegressionModel(adata_ref)
mod.train(max_epochs=250)
adata_ref = mod.export_posterior(adata_ref)

# cell2location spatial model
inf_aver = adata_ref.varm["means_per_cluster_mu_fg"]
cell2location.models.Cell2location.setup_anndata(adata_vis)
mod_spatial = cell2location.models.Cell2location(
    adata_vis, cell_state_df=inf_aver, N_cells_per_location=15)
mod_spatial.train(max_epochs=30000)

# 提取 deconvolution 结果
adata_vis = mod_spatial.export_posterior(adata_vis)

# 可视化各细胞类型的空间分布
sc.pl.spatial(adata_vis, color=["Malignant", "T_cell", "Macrophage", "Fibroblast"],
              cmap="magma", size=1.5)

# ============================================
# 空间共定位分析
# ============================================
from scipy.stats import spearmanr

# 计算候选 axis score 与各细胞类型的空间共定位
cell_types = ["Malignant", "T_cell_CD8", "T_cell_CD4", "Macrophage_M1", "Macrophage_M2"]
for ct in cell_types:
    r, p = spearmanr(adata_vis.obs["axis_score"], adata_vis.obsm["q05_cell_abundance_w_sf"][ct])
    print(f"{ct}: rho={r:.3f}, p={p:.2e}")

# ============================================
# 肿瘤-免疫界面分析
# ============================================
# 定义 tumor-immune interface spots
# (高恶性 + 高免疫细胞共定位的区域)
tumor_score = adata_vis.obsm["q05_cell_abundance_w_sf"]["Malignant"]
immune_score = adata_vis.obsm["q05_cell_abundance_w_sf"][["T_cell_CD8", "Macrophage"]].sum(axis=1)

adata_vis.obs["interface_score"] = tumor_score * immune_score
adata_vis.obs["region"] = pd.cut(adata_vis.obs["interface_score"],
    bins=3, labels=["immune_desert", "mixed", "immune_hot"])
```

### 2.3 升级预后模型

```r
# ============================================
# Multi-algorithm ensemble survival model
# ============================================
library(glmnet)
library(randomForestSRC)
library(xgboost)
library(survival)
library(survminer)
library(timeROC)
library(rms)

# 数据准备 (使用你已有的 TCGA 数据)
# train/test split 保持不变

# --- Method 1: LASSO Cox ---
cv_lasso <- cv.glmnet(x_train, y_train, family = "cox", alpha = 1, nfolds = 10)
lasso_model <- glmnet(x_train, y_train, family = "cox", alpha = 1,
                       lambda = cv_lasso$lambda.min)
lasso_genes <- rownames(coef(lasso_model))[coef(lasso_model)[, 1] != 0]

# --- Method 2: Random Survival Forest ---
rsf_model <- rfsrc(Surv(OS.time, OS) ~ ., data = train_df,
                    ntree = 1000, importance = TRUE)
rsf_vimp <- vimp(rsf_model)$importance
rsf_genes <- names(sort(rsf_vimp, decreasing = TRUE))[1:20]

# --- Method 3: stepwise multivariate Cox ---
# 取 LASSO + RSF 交集基因做 stepwise
overlap_genes <- intersect(lasso_genes, rsf_genes)
multi_cox <- coxph(Surv(OS.time, OS) ~ ., data = train_df[, c("OS.time", "OS", overlap_genes)])
step_cox <- step(multi_cox, direction = "both")

# --- 最终模型: 基于 stepwise 结果的 Cox 模型 ---
final_genes <- names(coef(step_cox))
final_model <- coxph(Surv(OS.time, OS) ~ ., data = train_df[, c("OS.time", "OS", final_genes)])

# Risk score
risk_score <- predict(final_model, newdata = test_df, type = "risk")
test_df$risk_group <- ifelse(risk_score > median(risk_score), "High", "Low")

# C-index
concordance(final_model, newdata = test_df)

# ============================================
# Nomogram
# ============================================
library(rms)
dd <- datadist(train_df)
options(datadist = "dd")

cph_model <- cph(Surv(OS.time, OS) ~ risk_score + stage + age + sex,
                 data = train_df, surv = TRUE, x = TRUE, y = TRUE)

nom <- nomogram(cph_model, fun = list(function(x) surv(365, x),
                                        function(x) surv(1095, x),
                                        function(x) surv(1825, x)),
                fun.at = c(0.1, 0.3, 0.5, 0.7, 0.9),
                funlabel = c("1-year OS", "3-year OS", "5-year OS"))
plot(nom)

# ============================================
# Calibration curve
# ============================================
cal <- calibrate(cph_model, u = 1095, cmethod = "KM", m = 50)
plot(cal)

# ============================================
# DCA (Decision Curve Analysis)
# ============================================
library(dcurves)
dca(Surv(OS.time, OS) ~ risk_score + stage, data = test_df, time = 1095)

# ============================================
# Time-dependent ROC
# ============================================
library(timeROC)
troc <- timeROC(T = test_df$OS.time, delta = test_df$OS,
                marker = risk_score,
                times = c(365, 1095, 1825),
                cause = 1, iid = TRUE)
# 1-year AUC, 3-year AUC, 5-year AUC
print(troc$AUC)
```

### 2.4 SCENIC 转录因子调控网络

```python
# ============================================
# pySCENIC workflow
# ============================================
import loompy
from pyscenic.utils import modules_from_adjacencies
from pyscenic.prune import prune2df, df2regulons
from pyscenic.aucell import aucell
from arboreto.algo import grnboost2

# Step 1: GRN inference
adjacencies = grnboost2(expression_data, tf_names, verbose=True)

# Step 2: Regulon prediction (cisTarget)
# 需要预下载 ranking databases
# hg38__refseq-r80__500bp_up_and_100bp_down_tss.mc9nr.genes_vs_motifs.rankings.feather
# hg38__refseq-r80__10kb_up_and_down_tss.mc9nr.genes_vs_motifs.rankings.feather

modules = modules_from_adjacencies(adjacencies, expression_data)
df = prune2df(ranking_dbs, modules, motif_annotations)
regulons = df2regulons(df)

# Step 3: AUCell scoring
auc_mtx = aucell(expression_data, regulons)

# Step 4: 与风险组关联
# 高风险 vs 低风险的 regulon activity 差异
from scipy.stats import mannwhitneyu
for regulon in auc_mtx.columns:
    stat, pval = mannwhitneyu(
        auc_mtx.loc[high_risk_cells, regulon],
        auc_mtx.loc[low_risk_cells, regulon])
    if pval < 0.05:
        print(f"{regulon}: p={pval:.2e}")
```

### 2.5 免疫微环境深度表征

```r
# ============================================
# 多方法免疫浸润估计
# ============================================

# CIBERSORT
source("CIBERSORT.R")
cibersort_results <- CIBERSORT("LM22.txt", expr_matrix, perm = 1000)

# ESTIMATE
library(estimate)
estimate_scores <- estimateScore(expr_matrix)

# xCell
library(xCell)
xcell_results <- xCellAnalysis(expr_matrix)

# ssGSEA (用 GSVA 包)
library(GSVA)
immune_signatures <- getGmt("immune_gene_sets.gmt")
ssgsea_scores <- gsva(expr_matrix, immune_signatures, method = "ssgsea")

# ============================================
# TIDE 免疫逃逸预测
# ============================================
# 提交到 http://tide.dfci.harvard.edu/
# 或使用 R 包
# TIDE score 与你的 risk score 的关联

# ============================================
# 与风险组的关联分析
# ============================================
# 对每种免疫细胞: 高风险 vs 低风险 Wilcoxon test
# 绘制: boxplot + heatmap
```

---

## 三、推荐的 Python/R 环境配置

### 3.1 R 环境 (≥4.3)

```r
# 核心包
install.packages(c("Seurat", "ggplot2", "dplyr", "survival", "survminer",
                   "glmnet", "randomForestSRC", "rms", "pheatmap"))

# Bioconductor
BiocManager::install(c("clusterProfiler", "org.Hs.eg.db", "GSVA",
                        "infercnv", "SingleR", "celldex", "scran",
                        "ComplexHeatmap", "EnhancedVolcano"))

# GitHub
devtools::install_github(c("sqjin/CellChat", "aertslab/SCENIC",
                           "dviraran/xCell", "GfellerLab/EPIC"))
```

### 3.2 Python 环境 (≥3.9)

```bash
pip install scanpy anndata cell2location pyscenic scvi-tools
pip install cellrank squidpy stlearn
pip install lifelines scikit-survival xgboost
```

---

## 四、质控检查清单

完成每个分析后，对照检查：

### 模型层
- [ ] Train C-index ≥ 0.70
- [ ] Internal test C-index ≥ 0.65
- [ ] External validation ≥ 3 independent cohorts, 各 C-index ≥ 0.60
- [ ] 1/3/5-year AUC 均报告
- [ ] Nomogram + calibration curve + DCA 完成
- [ ] 与已发表 signatures 对比 benchmark

### 单细胞层
- [ ] ≥ 50,000 cells 通过 QC
- [ ] ≥ 8 主要细胞类型注释
- [ ] InferCNV 恶性细胞鉴定
- [ ] 候选基因 cell-type-specific expression
- [ ] CellChat / NicheNet 细胞通讯
- [ ] SCENIC regulon activity

### 空间层
- [ ] cell2location / CARD deconvolution
- [ ] 空间共定位 (候选 axis vs 细胞类型)
- [ ] 肿瘤-免疫界面定义
- [ ] ≥ 5 个 sections 展示

### 免疫层
- [ ] ≥ 3 种免疫浸润估计方法
- [ ] TIDE / tumor immunity analysis
- [ ] ICB cohort validation (≥ 2 cohorts)
- [ ] 风险组与 TME 的系统关联

### 论文层
- [ ] 6 main figures + ≥ 8 supplementary figures
- [ ] Clear biological narrative (不是方法罗列)
- [ ] Limitation section 明确边界
- [ ] Source data 完整
- [ ] 代码可复现
