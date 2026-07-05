# 顶刊标准与最新方法综合调研报告

基于 2024-2026 年发表的高影响力 LUAD 生信论文调研

---

## 一、顶刊对预后模型的性能要求

### C-index / AUC 门槛

| 期刊级别 | 验证集 C-index 最低要求 | 备注 |
|----------|----------------------|------|
| Nature / Cell | > 0.75 | 通常需要前瞻性或大型独立队列验证 |
| Nature Communications / Genome Biology | > 0.65-0.70 | 需要 ≥3 独立外部队列 |
| J Hematol Oncol / Molecular Cancer | > 0.65 | 需要 ≥2 独立外部队列 |
| Briefings in Bioinformatics | > 0.60-0.65 | 方法学创新可弥补部分性能 |

**你目前的状态：test C-index 0.584，低于所有一区门槛。**

### 最新趋势：GNN 等方法已实现 C-index 0.82

- npj Precision Oncology (2026) 的一篇文章用 GNN 建模空间肿瘤-免疫交互，在 506 例 NSCLC 中达到 C-index 0.82
- Cox-Sage (Briefings in Bioinformatics 2025) 将 GNN 与 Cox 模型结合，兼顾可解释性和高性能
- 这意味着单纯的 LASSO/Ridge Cox 在方法学上已经不够有竞争力

---

## 二、方法学分层：标准 vs 创新 vs 前沿

### 第一层：标准方法（审稿人期望你有，但不产生新意）

| 方法 | 状态 | 说明 |
|------|------|------|
| LASSO-Cox / Ridge-Cox | 已成模板化 | 数百篇 LUAD 论文用几乎相同的流程 |
| WGCNA | 标准 | 不捕获高阶基因交互 |
| CIBERSORT / ssGSEA | 标准 | 免疫浸润估计的基本工具 |
| ESTIMATE / TIDE | 标准 | 免疫逃逸基础分析 |
| CellChat | 已从新颖变为标准 | 2024+ 已是 scRNA-seq 论文的标配 |
| Seurat / Scanpy 标准流程 | 基础设施 | 不产生差异化 |
| Kaplan-Meier + Log-rank | 基础 | 所有生存分析论文必须 |

**单独使用这些方法只能发 Frontiers / MDPI 级别期刊。**

### 第二层：新兴方法（能让论文脱颖而出）

| 方法 | 新颖度 | 适用场景 | 推荐使用 |
|------|--------|----------|----------|
| **SCENIC / SCENIC+** | 高 | 单细胞转录因子调控网络 | 强烈推荐 |
| **Graph Neural Networks (GNN/GAT)** | 很高 | 多组学生存预测 | 有余力时做 |
| **scGPT / Geneformer** | 前沿 | 单细胞基础模型 | 可选（需谨慎fine-tune） |
| **CellNEST** | 很高 | 空间细胞通讯relay网络 | Nature Methods 2025 发表 |
| **DeepSurv / Cox-nnet** | 高 | 深度学习生存分析 | 可替代LASSO-Cox |
| **NicheNet v2** | 高 | 配体-受体-靶基因三层通讯 | 比 CellChat 更深入 |

### 第三层：空间方法（当前顶刊最看重的方向）

| 方法 | 类型 | 性能排名 | 推荐度 |
|------|------|----------|--------|
| **CARD** | 空间感知参考基 deconvolution | 基准测试第一 (中位 RMSE 0.079) | **最推荐** |
| **cell2location** | 贝叶斯概率模型 | 广泛使用，性能稳定 | 推荐 |
| **BayesSpace** | 贝叶斯空间聚类 | 亚 spot 级超分辨率 | 推荐 |
| **SpatialDWLS** | 阻尼加权最小二乘 | 比 RCTD 和 SPOTlight 准确 | 可选 |
| **GraphST** | GNN + 空间转录组 | Nature Comms 2023 | 可选 |

**关键洞察：空间转录组 deconvolution + 单细胞 GRN 分析是 2024-2026 年顶刊 LUAD 论文的"甜区"。**

---

## 三、超越 TCGA/GEO 的公开数据集

### 3.1 蛋白组学

| 数据集 | 样本量 | 数据类型 | 获取方式 |
|--------|--------|----------|----------|
| **CPTAC-LUAD (2020)** | 110 tumor + 101 NAT | 蛋白/磷酸化/乙酰化/基因组/影像 | MassIVE MSV000086793; GDC; PDC |
| **CPTAC-LUAD 扩展 (2025)** | 406 tumor + 388 NAT | 多人种蛋白基因组学 | Cancer Cell 2025 |

### 3.2 单细胞图谱

| 数据集 | 细胞数 | 特点 | 获取方式 |
|--------|--------|------|----------|
| **HLCA v1.0** (Sikkema et al., Nat Med 2023) | 2.4M cells, 486 donors | 最全面的肺单细胞图谱 | EGAS00001004344; CellxGENE |
| **uniLUNG** (eBioMedicine 2025) | 9.2M cells, 1807 donors | 整合 62 个数据集，122 种细胞类型 | 2025 年最新 |
| **GSE131907** (Kim et al., Nat Comms) | 208K cells, 44 patients | LUAD scRNA-seq 引用最高 | GEO |
| **GSE171145** | ~100K cells | LUAD TME focused | GEO |
| **CRA001160** (NGDC/GSA) | ~90K cells | 中国人群 LUAD | NGDC |

### 3.3 空间转录组

| 数据集 | 样本量 | 特点 |
|--------|--------|------|
| **E-MTAB-13530** (你已有) | 22 LUAD sections, 54K spots | 已下载 |
| **E-MTAB-13062** | 8 NSCLC + 8 NAT + 2 healthy, 40 sections | 可补充 |
| **Nat Comms 2024 LUAD spatial** | 30 LUAD tumors (22 早期 + 8 浸润) | 展示 LUAD 进展中的肿瘤-免疫共变 |

### 3.4 Bulk 外部验证队列（你需要增加的）

| 数据集 | 样本量 | 平台 | 特点 |
|--------|--------|------|------|
| **GSE72094** | 442 LUAD | RNA-seq | 有 KRAS/EGFR/STK11/TP53 突变注释 + OS |
| **GSE68465** | 442 LUAD | 芯片 GPL96 | Director's Challenge 最大 GEO LUAD |
| **GSE30219** | ~293 NSCLC | 芯片 | 法国队列 |
| **GSE37745** | ~196 NSCLC | 芯片 | 瑞典队列 |

### 3.5 其他

| 数据集 | 类型 | 用途 |
|--------|------|------|
| **ICGC LUAD** | 全基因组/突变/表达/甲基化, 569 samples | 与 TCGA 互补验证 |
| **NLST** | CT 影像 + 病理 + 临床, ~54K participants | 深度学习/计算病理 |

---

## 四、近期高被引 LUAD 生信论文案例

### 案例 1: CPTAC 多人种蛋白基因组学 (Cancer Cell 2025)
- 406 个 LUAD 肿瘤的跨人种蛋白基因组整合
- 关键创新：多组学整合 + 人种多样性 + 大样本
- 发表在 Cancer Cell

### 案例 2: 空间转录组揭示 LUAD 发展关键步骤 (Nat Comms 2024)
- 30 个 LUAD 的 Visium 空间分析
- 关键创新：早期到晚期的空间进展模式 + 肿瘤-免疫共变
- 用了空间 deconvolution + scRNA-seq reference 整合

### 案例 3: GNN 空间肿瘤-免疫交互预后模型 (npj Precision Oncology 2026)
- 506 例 NSCLC 的 GNN 建模
- C-index 0.82
- 关键创新：图神经网络 + 空间交互 + 高性能预后

### 案例 4: CellNEST 空间细胞通讯 (Nature Methods 2025)
- 注意力机制建模空间转录组中的细胞-细胞中继网络
- 应用于 LUAD 识别侵袭性通讯模式
- 超越 CellChat 的配体-受体方法

### 案例 5: uniLUNG 肺元图谱 (eBioMedicine 2025)
- 整合 62 个数据集，9.2M cells
- 四层细胞注释框架，122 种细胞类型
- 发现肺癌中的过渡态细胞群

---

## 五、对你的项目的具体启示

### 5.1 你的差异化优势

1. **22 个 Visium sections** - 多数论文只有 3-8 个，你有 22 个是真正的优势
2. **系统文献支撑** - 100 篇全文解析，方法有据可依
3. **多层数据已到位** - TCGA + GEO × 2 + 空间 + DepMap + Drug + ICB

### 5.2 你必须补上的短板

1. **Raw scRNA-seq 分析** → 用 GSE131907 或 HLCA
2. **空间 deconvolution** → 用 CARD (最佳性能) 或 cell2location
3. **模型升级** → 至少 LASSO + RSF + multivariate Cox ensemble，目标 C > 0.65
4. **SCENIC 转录因子网络** → 在 scRNA-seq 恶性细胞上运行
5. **增加验证队列** → GSE72094 (442 samples, 有突变注释)

### 5.3 可选但加分的创新

- 用 CARD 替代 cell2location（2023 年基准测试排名第一）
- 用 CellNEST 做空间通讯分析（Nature Methods 2025 方法，非常新）
- 用 DeepSurv 或 Cox-Sage 做深度学习生存模型
- 用 CPTAC-LUAD 做蛋白水平验证（很少有论文同时做了转录组+蛋白组+空间）

### 5.4 你应该避免的

- 不要只用 LASSO-Cox 作为唯一建模方法（已成模板化）
- 不要把 WGCNA 放在主流程里（除非你有明确的 module 发现叙事）
- 不要尝试 scGPT/Geneformer 除非你有 GPU 资源和 fine-tuning 经验（基准测试显示未经 fine-tune 时可能不如 PCA）
- 不要过度包装 CIBERSORT 结果为"新发现"（审稿人已经看过太多了）

---

## 六、推荐的方法组合（你的论文最佳配置）

### 核心方法栈

```
┌─────────────────────────────────────────────────┐
│  Discovery: TCGA-LUAD bulk RNA-seq + mutation   │
│  ↓                                              │
│  Feature selection: LASSO + RSF + stepwise Cox  │
│  ↓                                              │
│  Validation: TCGA test + GSE31210 + GSE50081    │
│              + GSE72094 (新增)                   │
│  ↓                                              │
│  Clinical: Nomogram + Calibration + DCA + tROC  │
│  ↓                                              │
│  Single-cell: GSE131907 scRNA-seq               │
│  → Seurat + Harmony + SingleR + InferCNV        │
│  → CellChat + Monocle3 pseudotime               │
│  → pySCENIC regulon analysis                    │
│  ↓                                              │
│  Spatial: E-MTAB-13530 Visium (你已有)          │
│  → CARD / cell2location deconvolution           │
│  → Spatial co-localization                      │
│  → Tumor-immune interface                       │
│  ↓                                              │
│  TME: CIBERSORT + xCell + ESTIMATE + TIDE       │
│  ↓                                              │
│  Function: DepMap + Drug (精简) + HPA           │
│  ↓                                              │
│  ICB: 现有 3 cohorts + 扩展                     │
└─────────────────────────────────────────────────┘
```

这个方法栈覆盖了 Nature Communications 级别论文的所有要求，同时你已有的 22 个 Visium sections + CARD deconvolution 可以成为差异化亮点。
