# 执行清单：从当前状态到一区投稿

每完成一项打勾，按顺序执行。

---

## Phase 1: 数据获取（第 1-2 周）

### 单细胞数据
- [ ] 下载 GSE131907 processed count matrix (GEO supplementary)
- [ ] 下载 GSE131907 metadata / cell annotations
- [ ] (可选) 下载 GSE171145 作为第二 scRNA-seq 数据集
- [ ] 确认候选 8 genes 在 scRNA-seq 数据中可 map

### 额外验证队列
- [ ] 下载 GSE72094 expression + clinical (442 LUAD, 最推荐)
- [ ] 下载 GSE68465 expression + clinical (442 LUAD, Director's Challenge)
- [ ] 验证 Cox coefficients 在新队列中的可转移性

### TCGA 多组学扩展
- [ ] 从 UCSC Xena 下载 TCGA-LUAD DNA methylation 450K
- [ ] 从 UCSC Xena 下载 TCGA-LUAD gene-level CNV (GISTIC2)
- [ ] (可选) 下载 TCGA-LUAD miRNA expression

### 蛋白组（可选但强烈推荐）
- [ ] 从 PDC/CPTAC portal 下载 CPTAC-LUAD 蛋白组数据
- [ ] 提取候选基因的蛋白表达水平

### 环境搭建
- [ ] R ≥ 4.3 + Seurat v5 + Harmony + SingleR + infercnv
- [ ] Python ≥ 3.9 + scanpy + cell2location (或 CARD)
- [ ] pySCENIC + cisTarget ranking databases (hg38)
- [ ] lifelines + scikit-survival + xgboost (Python survival)

---

## Phase 2: 单细胞分析（第 3-4 周）

### 基础流程
- [ ] QC: nFeature 200-6000, MT% < 20%, nCount > 500
- [ ] Normalize → FindVariableFeatures(3000) → ScaleData → PCA(50)
- [ ] Harmony 批次校正 (group.by = sample/patient)
- [ ] UMAP + Clustering (resolution 0.3-1.0)
- [ ] 细胞类型注释: SingleR 自动 + canonical markers 手动校正

### 恶性细胞鉴定
- [ ] InferCNV: 用正常上皮做 reference
- [ ] 标记恶性 vs 非恶性细胞

### 候选基因分析
- [ ] DotPlot: 8 genes × all cell types
- [ ] VlnPlot: 恶性 vs 非恶性表达差异
- [ ] FindMarkers: 高表达 vs 低表达恶性细胞的 DEG

### 细胞通讯
- [ ] CellChat: 全细胞通讯网络
- [ ] 高风险 vs 低风险组间通讯差异
- [ ] 关键配体-受体对识别

### 发育轨迹（如适用）
- [ ] Monocle3 或 scVelo 轨迹分析
- [ ] 候选基因沿 pseudotime 的表达变化

### SCENIC 转录因子网络
- [ ] pySCENIC: GRN inference → regulon prediction → AUCell scoring
- [ ] 识别驱动候选 axis 的核心 TFs
- [ ] 高/低风险组的 regulon activity 差异
- [ ] 与 TCGA bulk GSVA 交叉验证

---

## Phase 3: 空间 deconvolution（第 5 周）

### 数据准备
- [ ] 从已有 E-MTAB-13530 .h5 文件读入 Visium 数据
- [ ] 确认候选基因在 spatial 数据中有表达

### CARD deconvolution（推荐，基准测试第一名）
- [ ] 用 scRNA-seq (Phase 2 结果) 构建 reference
- [ ] 对 ≥5 个 representative sections 做 CARD deconvolution
- [ ] 可视化各细胞类型的空间分布

### 或 cell2location（备选）
- [ ] 训练 reference model
- [ ] 训练 spatial model (30K epochs)
- [ ] 提取 cell abundance estimates

### 空间关联分析
- [ ] 候选 axis score 与各细胞类型的 spot-level Spearman 相关
- [ ] 肿瘤核心 vs 侵袭前沿 vs 基质区 的基因表达差异
- [ ] 免疫 hot vs cold 区域的候选基因表达
- [ ] Squidpy 邻域分析

---

## Phase 4: 模型升级与多队列验证（第 6 周）

### Feature 重新筛选
- [ ] LASSO Cox (alpha=1, 10-fold CV): 记录 lambda.min genes
- [ ] Random Survival Forest (ntree=1000): VIMP ranking top 20
- [ ] 取 LASSO ∩ RSF 交集基因
- [ ] Stepwise multivariate Cox (direction="both")

### 最终模型
- [ ] 基于 stepwise 结果构建 final Cox model
- [ ] 记录最终基因 list + coefficients
- [ ] Train C-index ≥ 0.70

### 多队列验证
- [ ] TCGA held-out test: C-index ≥ 0.65
- [ ] GSE31210 external: C-index + KM curve
- [ ] GSE50081 external: C-index + KM curve
- [ ] GSE72094 external: C-index + KM curve
- [ ] (可选) GSE68465 external

### 临床转化指标
- [ ] Time-dependent ROC: 1/3/5-year AUC
- [ ] Nomogram: risk score + stage + age + sex
- [ ] Calibration curve: 1/3/5-year 校准
- [ ] DCA: net benefit 对比 treat-all / treat-none
- [ ] Multivariate Forest plot: 独立预后因子检验

### Benchmark
- [ ] 与 ≥3 个已发表 LUAD signatures 对比 C-index
- [ ] Time-ROC 对比曲线

---

## Phase 5: 免疫 + ICB 扩展（第 7 周）

### 免疫浸润
- [ ] CIBERSORT: 22 cell types
- [ ] xCell: 64 cell types
- [ ] MCPcounter / ESTIMATE
- [ ] 风险组 × 免疫细胞热图
- [ ] 关键免疫 checkpoint 基因表达比较

### TIDE 分析
- [ ] TIDE score 计算
- [ ] 高/低风险组 TIDE score 差异
- [ ] 免疫逃逸机制分析

### ICB 扩展
- [ ] 保留现有 3 GEO ICB cohorts
- [ ] 寻找更多 NSCLC ICB 公开数据
- [ ] Meta-analysis forest plot (如 ≥3 cohorts)

---

## Phase 6: 多组学整合（第 7 周，可与 Phase 5 并行）

### DNA 甲基化
- [ ] 候选基因 promoter 甲基化 vs 表达相关
- [ ] 甲基化驱动的表达沉默识别
- [ ] 甲基化与预后的关联

### 拷贝数变异
- [ ] 候选基因 CNV 频率 (GISTIC2)
- [ ] CNV 与表达的关联
- [ ] 扩增/缺失与预后

### (可选) 蛋白组
- [ ] CPTAC-LUAD 候选基因蛋白表达
- [ ] mRNA-protein 一致性验证

---

## Phase 7: 论文重写（第 8-9 周）

### Results 重构
- [ ] 重写 Result 1: Discovery + multi-omics landscape
- [ ] 重写 Result 2: Model + multi-cohort validation
- [ ] 新写 Result 3: Single-cell atlas
- [ ] 新写 Result 4: Spatial transcriptomics
- [ ] 重写 Result 5: TME + ICB
- [ ] 重写 Result 6: Regulatory network + function + therapy

### Figure 制作
- [ ] Fig 1: Study design + discovery (4-6 panels)
- [ ] Fig 2: Model + validation (6-8 panels)
- [ ] Fig 3: Single-cell (6 panels)
- [ ] Fig 4: Spatial (6 panels)
- [ ] Fig 5: TME + ICB (5-6 panels)
- [ ] Fig 6: Network + function (5 panels)
- [ ] Suppl Figs: ≥8 figures

### 其他部分
- [ ] 重写 Abstract (250 words, narrative 而非 inventory)
- [ ] 重写 Introduction (聚焦一个 biological question)
- [ ] 重写 Discussion (讲 story + limitation + future)
- [ ] 更新 Methods (完整描述所有新分析)
- [ ] 更新 Data Availability (真实 accession numbers)

---

## Phase 8: 审计与提交（第 10 周）

### 内部质控
- [ ] 新一轮 CNS readiness audit (目标 ≥ 88/100)
- [ ] Claim-to-citation audit
- [ ] Statistical multiplicity ledger 更新
- [ ] 所有 p-value 的多重检验校正检查

### 外部准备
- [ ] Source Data package 更新
- [ ] Analysis code 整理到 GitHub repo
- [ ] 代码 + 数据存档到 Zenodo (获取 DOI)
- [ ] Cover letter 撰写
- [ ] Suggested reviewers list (5-8 人)

### 投稿
- [ ] 首选：Nature Communications
- [ ] 备选 1：J Hematol Oncol
- [ ] 备选 2：Molecular Cancer
- [ ] 保底：Briefings in Bioinformatics

---

## 关键里程碑

| 里程碑 | 判断标准 | 目标周 |
|--------|----------|--------|
| scRNA-seq 分析完成 | UMAP + annotation + candidate expression 图件完成 | Week 4 |
| 空间 deconvolution 完成 | ≥5 sections 的细胞类型空间分布图 | Week 5 |
| 模型 C-index 达标 | 任一外部验证 C-index ≥ 0.65 | Week 6 |
| 所有新分析完成 | Phase 1-6 全部打勾 | Week 7 |
| 论文初稿完成 | 6 main figs + full text | Week 9 |
| 可提交状态 | CNS audit ≥ 88/100 | Week 10 |
