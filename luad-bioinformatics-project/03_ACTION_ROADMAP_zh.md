# 行动路线图：LUAD 一区论文冲刺计划

---

## 核心判断

你目前的项目最大问题不是"做得不够多"，而是"做得太多但每个都不够深"。审稿人看到 10 个数据源但单细胞只是 aggregated query、空间只是 spot proxy、Cox C-index 只有 0.584，会直接 reject。

**核心策略：砍宽度、加深度、建叙事。**

---

## 一、必须砍掉或弱化的内容

| 当前内容 | 处理 | 理由 |
|----------|------|------|
| 100 篇文献系统总结 | 移到 Supplementary Methods S1，主文只提 "guided by systematic review of 100 recent Q1/Q2 publications" | 占篇幅但不是科学发现 |
| Ridge Cox 8-feature 模型 (C=0.584) | **删除**，替换为新模型 | 性能不达标 |
| CELLxGENE WMG aggregated query | **删除**，替换为 raw scRNA-seq | 审稿人不认可 |
| DepMap 全面展示 | 保留 top 3-5 dependency genes 的结果 | 辅助即可 |
| GDSC/CTRP/PRISM 全面展示 | 保留 top 5 compounds 的关联 | 太散 |
| HPA 全面展示 | 保留关键 IHC 图片 + prognostic 链接 | 辅助 |
| ICB 3 cohort expression | 保留但需扩展样本量 | 当前太弱 |

---

## 二、必须新增的分析（不做就不能发一区）

### TIER 0：生死线（没有这些，任何一区都不可能接收）

#### T0-1. Raw scRNA-seq 分析

**数据选择方案（二选一）：**

方案 A（推荐）：使用 **GSE131907** (Kim et al., Nat Med 2020)
- 优点：引用率最高，审稿人熟悉，有完整 annotation
- 208K cells，涵盖 primary LUAD / metastatic / normal
- 可直接从 GEO supplementary 下载 processed counts

方案 B：使用 **GSE171145** + **GSE149655** 组合
- 优点：更新，TME focused
- 缺点：需要自己做全部 annotation

**必须完成的分析：**
1. 标准 Seurat pipeline: QC → normalize → integrate (Harmony) → cluster → UMAP
2. 细胞类型注释 (SingleR + canonical markers 双验证)
3. InferCNV 恶性细胞鉴定
4. 候选基因的 cell-type-specific expression (DotPlot + VlnPlot)
5. 恶性细胞中的 DEG + pathway
6. CellChat 细胞通讯（高表达 vs 低表达组间通讯差异）

**产出：Fig 3 (single-cell atlas + candidate gene expression + cell communication)**

#### T0-2. 预后模型升级

**当前问题：** Ridge Cox C-index 0.584 = 几乎没有预测能力

**解决方案：LASSO → RSF → multivariate Cox 三步法**

1. LASSO Cox (alpha=1) 筛选 features
2. Random Survival Forest 独立筛选 (VIMP ranking)
3. 取 LASSO + RSF 交集 genes → stepwise multivariate Cox
4. 目标：validation C-index ≥ 0.65

**必须的额外展示：**
- Time-dependent ROC (1/3/5-year AUC)
- Nomogram (risk score + clinical covariates)
- Calibration curve (1/3/5-year)
- DCA (Decision Curve Analysis)
- 与已发表 signatures 的 benchmark (≥3 published signatures)

**额外验证队列（至少加一个）：**
- GSE72094 (442 LUAD, RNA-seq, 最推荐)
- GSE68465 (443 LUAD, microarray, Director's Challenge)

**产出：Fig 2 (model construction + multi-cohort validation + nomogram)**

#### T0-3. 空间转录组深度分析

你已有 E-MTAB-13530 (22 sections, 54K spots)，数据量足够。

**需要新增：**
1. cell2location 空间 deconvolution（需要 T0-1 的 scRNA-seq 作为 reference）
2. 各细胞类型的空间分布可视化
3. 候选 axis score 与细胞类型的空间共定位 (Spearman correlation per spot)
4. 肿瘤核心 vs 侵袭前沿 vs 免疫浸润区的候选基因表达差异
5. Squidpy 空间邻域分析

**产出：Fig 4 (spatial deconvolution + co-localization + tumor-immune interface)**

### TIER 1：强烈推荐（显著提升论文竞争力）

#### T1-1. SCENIC 转录因子调控网络

- 在 scRNA-seq 恶性细胞上运行 pySCENIC
- 识别驱动候选 axis 的核心 transcription factors
- Regulon activity 在高/低风险组间的差异
- 与 TCGA bulk 做交叉验证

**产出：Fig 6 一部分 (regulatory network)**

#### T1-2. 免疫微环境深度表征

- CIBERSORT + xCell + MCPcounter + ESTIMATE (至少 3 种方法)
- 22 种免疫细胞 vs risk score 的系统关联
- TIDE score 计算 (immune evasion)
- Tumor Immunity in the Microenvironment (TIME) classification

**产出：Fig 5 一部分 (TME characterization)**

#### T1-3. ICB 响应预测扩展

当前 3 个 GEO cohort 样本量太小。推荐：
- 整合你已有的 3 个 + 再找 1-2 个
- 如果能找到有 OS 的 ICB cohort，做 survival analysis
- Meta-analysis forest plot

**产出：Fig 5 一部分 (ICB response prediction)**

### TIER 2：加分但不是必须

#### T2-1. 多组学整合
- TCGA DNA methylation + expression correlation
- CNV-expression association
- 这些 TCGA 都有现成数据，工作量不大

#### T2-2. 蛋白验证
- CPTAC-LUAD 蛋白组验证基因表达
- 增加一个独立验证层

---

## 三、重构后的论文叙事线

### Before（当前）：
> "我们系统阅读了 100 篇文献，下载了 10 个数据库，做了很多分析"
> → 审稿人反应："so what?"

### After（目标）：
> "我们发现 LUAD 中存在一个 [mitotic-checkpoint / ER-stress / epithelial-plasticity] 调控程序，该程序在单细胞水平由 [TF-X] 驱动、在空间水平与免疫排斥微环境共定位、在临床水平预测不良预后和免疫治疗抵抗"
> → 审稿人反应："这是一个有生物学意义的发现"

### 具体叙事架构

**Title**: "Single-cell and spatial transcriptomics delineate a [X]-regulatory axis governing immune exclusion and prognosis in lung adenocarcinoma"

**Abstract 逻辑链**:
1. LUAD 预后异质性的分子基础尚不完全清楚
2. 我们通过整合 bulk/single-cell/spatial 多层组学，识别了一个以 [X] 为核心的转录调控轴
3. 该轴在多个独立队列中预测不良预后 (C-index=0.XX)
4. 单细胞分析揭示该轴主要在恶性上皮细胞中由 [TF] 激活
5. 空间转录组确认高轴活性区域与免疫排斥微环境共定位
6. 功能依赖性和药物敏感性分析提示潜在治疗靶点
7. 结论：该调控轴可作为 LUAD 预后分层和免疫治疗选择的候选标志物

---

## 四、Figure 规划

| Figure | 标题 | 核心内容 | Panel 数 |
|--------|------|----------|----------|
| **Fig 1** | Study overview and discovery | A: Study design schema; B: TCGA LUAD landscape (mutation+expression+clinical); C: 候选 axis identification; D: Multi-omics overview | 4-6 |
| **Fig 2** | Prognostic model and validation | A: LASSO feature selection; B: Risk score distribution (train+test); C: KM curves (TCGA train/test, GSE31210, GSE50081, GSE72094); D: Time-ROC; E: Forest plot (multivariate); F: Nomogram + calibration | 6-8 |
| **Fig 3** | Single-cell atlas | A: UMAP all cells; B: Cell type annotation; C: InferCNV; D: Candidate gene DotPlot; E: Malignant cell subgroups; F: Pseudotime trajectory | 6 |
| **Fig 4** | Spatial transcriptomics | A: H&E + spatial overview; B: cell2location deconvolution; C: Axis score spatial distribution; D: Cell type co-localization; E: Tumor-immune interface; F: Neighborhood analysis | 6 |
| **Fig 5** | Tumor immune microenvironment | A: Immune infiltration heatmap (multi-method); B: Risk group vs immune cells; C: TIDE analysis; D: ICB cohort validation; E: Immune checkpoint expression | 5-6 |
| **Fig 6** | Regulatory network and therapy | A: SCENIC top regulons; B: TF-target network; C: DepMap dependency; D: Drug sensitivity top hits; E: HPA IHC validation | 5 |
| **Suppl** | Extended data | 详细 QC、benchmark、sensitivity analysis、完整表格 | 8-12 figs |

---

## 五、具体时间表

### Week 1-2: 数据获取 + 环境
- [ ] 下载 GSE131907 scRNA-seq
- [ ] 下载 GSE72094 (额外验证队列)
- [ ] 下载 TCGA methylation + CNV (UCSC Xena)
- [ ] 安装 Seurat + Scanpy + cell2location + pySCENIC 环境
- [ ] scRNA-seq QC + 初步处理

### Week 3-4: scRNA-seq 核心分析
- [ ] Harmony integration + clustering + annotation
- [ ] InferCNV
- [ ] 候选基因 cell-type expression
- [ ] CellChat
- [ ] Pseudotime (if applicable)

### Week 5: 空间 deconvolution
- [ ] cell2location training (用 scRNA-seq 做 reference)
- [ ] 对 E-MTAB-13530 做 deconvolution
- [ ] 空间共定位 + 界面分析

### Week 6: 模型升级 + 验证
- [ ] LASSO + RSF + stepwise Cox
- [ ] 多队列验证 (TCGA + GSE31210 + GSE50081 + GSE72094)
- [ ] Nomogram + calibration + DCA + time-ROC
- [ ] Benchmark vs published signatures

### Week 7: 免疫 + 调控网络
- [ ] 多方法免疫浸润
- [ ] SCENIC
- [ ] TIDE
- [ ] ICB 扩展

### Week 8-9: 论文重写
- [ ] 全新 Results 架构
- [ ] 6 main figures
- [ ] 8+ supplementary figures
- [ ] Methods 详细描述
- [ ] Discussion 重写

### Week 10: 审计与提交准备
- [ ] 新一轮 CNS readiness audit
- [ ] Source data package
- [ ] Code repository (GitHub/Zenodo)
- [ ] Cover letter
- [ ] 目标：CNS audit ≥ 88/100

---

## 六、你现在立刻可以做的事

**今天就可以开始：**

1. 去 GEO 下载 GSE131907 的 supplementary files（processed count matrix）
2. 去 GEO 下载 GSE72094 的 expression + clinical data
3. 去 UCSC Xena 下载 TCGA-LUAD methylation 450K data
4. 安装 R 4.3+ 和 Seurat v5

**本周末前完成：**
- scRNA-seq 数据下载和 QC
- 确认 cell2location 环境可运行
- 确认你当前的 8 个 Cox genes 在 scRNA-seq 里都能 map 到

---

## 七、投稿目标建议

根据你的项目基础和可能的完成度：

| 如果你能完成... | 可投 | 概率 |
|----------------|------|------|
| T0 全部 + T1 部分 | Nature Communications / Genome Biology | 30-40% |
| T0 全部 + T1 全部 | J Hematol Oncol / Molecular Cancer | 50-60% |
| T0 全部 | Briefings in Bioinformatics / CBM | 70-80% |

最现实的策略：先冲 Nature Communications，被拒后转投 J Hematol Oncol 或 Molecular Cancer，这两个对生信数据挖掘论文接受度很高且影响因子都在一区。

---

## 八、给你的直接建议

1. **不要再加新数据源了**。你已经有足够多的数据，问题是深度不够。
2. **围绕一个 lead biological axis**。从你当前的 8 个 Cox genes 里选一个最有生物学故事的方向（mitotic checkpoint 或 ER-redox 最可能）。
3. **scRNA-seq 是生死线**。2024 年以后，没有 raw scRNA-seq 的 LUAD 计算论文不可能发一区。
4. **空间 deconvolution 是你的差异化优势**。很多论文没有真正的 Visium 数据，你有 22 个 sections，用好了是大加分。
5. **模型性能必须提上去**。C-index < 0.60 在审稿人眼里约等于 random guess。
6. **论文要讲 story，不是列清单**。每个 figure 应该服务于"一个 biological axis 被逐层验证"的叙事。
