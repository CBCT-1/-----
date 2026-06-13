# LUAD 生信数据挖掘项目诊断与一区投稿路线图

生成日期：2026-06-12

---

## 一、当前项目总体评估

### 1.1 已完成工作盘点

| 层级 | 内容 | 状态 | 质量评价 |
|------|------|------|----------|
| 文献 | 100 篇 Q1/Q2 全文解析 + 方法矩阵 | 完成 | 优秀，超过多数同类论文 |
| 发现队列 | TCGA-LUAD bulk RNA-seq + survival + mutation | 完成 | 标准 |
| 内部模型 | Ridge Cox, 8 features, train C=0.697 | 完成 | **不足** |
| 外部验证 | GSE31210 + GSE50081 | 完成 | 基本可用 |
| Pathway | g:Profiler enrichment | 完成 | 标准但浅 |
| 单细胞 | CELLxGENE WMG aggregated query | 完成 | **严重不足** |
| HPA | 蛋白图谱验证 | 完成 | 辅助支持 |
| 空间 | E-MTAB-13530 Visium, 22 sections | 完成 | **有数据但分析浅** |
| DepMap | CRISPR dependency | 完成 | 辅助支持 |
| 药物 | GDSC/CTRP/PRISM | 完成 | 探索性 |
| ICB | 3 个 GEO cohort expression | 完成 | **样本量不足** |
| 论文 | v1.0 草稿, CNS audit 78.6/100 | 完成 | 需要大幅重构 |

### 1.2 核心问题诊断（为什么现在不能投一区）

**问题 1：模型性能不达标**
- 内部 test C-index 0.584 在一区期刊基本不可发表
- 对比标准：Nature Communications / Genome Biology 级别论文通常要求 validation C-index > 0.65，最好 > 0.70
- Ridge Cox 8 features 在方法学上没有新意

**问题 2：单细胞分析几乎缺失**
- CELLxGENE WMG 只是 aggregated summary，不是真正的 scRNA-seq 分析
- 2024-2026 年顶刊生信论文，没有 raw single-cell analysis 几乎不可能发一区
- 缺少：细胞类型注释、差异表达、细胞通讯、轨迹分析、转录因子调控

**问题 3：空间转录组有数据没深度**
- 22 个 Visium section 的数据量其实很好
- 但只做了 spot-level marker module proxy，没有做：
  - 空间 deconvolution (cell2location / CARD / BayesSpace)
  - 空间细胞通讯 (CellChat / COMMOT)
  - 空间异质性分析
  - 与单细胞的 reference-based integration

**问题 4：分析太散，没有 lead story**
- 做了 10+ 个数据源但每个都浅尝辄止
- 一区论文需要一个清晰的 biological narrative，不是 "我们做了很多分析"
- 当前像是 "方法展示" 而不是 "科学发现"

**问题 5：缺乏机制层面的计算验证**
- 没有转录因子调控网络 (SCENIC / SCENIC+)
- 没有基因调控网络推断
- 没有突变-表达关联分析 (如 driver mutation 对 signature 的影响)
- 没有拷贝数变异整合

---

## 二、与 CNS 级别论文的差距分析

### 2.1 近年一区生信数据挖掘论文的标准配置

| 模块 | 一区标准 | 你目前的状态 | 差距 |
|------|----------|-------------|------|
| 发现队列 | TCGA + ≥2 独立外部队列 | TCGA + 2 GEO | 基本达标 |
| 模型方法 | ML ensemble 或深度学习 + 传统 Cox 对比 | 仅 Ridge Cox | **大幅落后** |
| 模型性能 | 验证 C-index ≥ 0.65 | 0.584 | **不达标** |
| 单细胞 | Raw scRNA-seq 分析 (≥3 数据集) | 仅 aggregated query | **缺失** |
| 空间 | Deconvolution + spatial co-localization | 仅 spot module proxy | **不足** |
| 免疫 | 多方法免疫浸润 + TME 表征 | 有相关性但不深入 | **不足** |
| 机制 | 转录因子网络 / 基因调控 / 通路交互 | 仅 g:Profiler enrichment | **缺失** |
| 药物 | 药物敏感性 + 分子对接 / IC50 预测 | 仅 cell-line AUC 相关 | 基本 |
| 临床转化 | Nomogram + 校准曲线 + DCA | 无 | **缺失** |
| 验证层级 | ≥3 层独立验证 | 2 层 (GEO) | 不足 |

### 2.2 一区论文的叙事结构（你需要对标的模板）

典型的 Nature Communications 级别 LUAD 生信论文结构：

1. **Opening**: 用多组学数据识别一个新的 biological axis / molecular subtype / regulatory program
2. **Discovery**: 在 TCGA 中用 bulk + mutation + CNV 建立发现
3. **Single-cell resolution**: 用 scRNA-seq 揭示细胞类型来源和调控机制
4. **Spatial validation**: 用空间转录组确认组织空间分布
5. **Functional implication**: DepMap + drug + 转录因子网络暗示功能
6. **Clinical translation**: 多队列验证的预后模型 + nomogram
7. **Immunotherapy relevance**: TME 表征 + ICB 响应预测

---

## 三、推荐的重构方案

### 3.1 核心策略：从 "方法展示" 转向 "生物学发现"

**推荐 lead story**: 围绕 mitotic-checkpoint / ER-redox / epithelial remodeling axis 中的一个，建立一个 "LUAD 中的 [X] regulatory program 驱动预后异质性和免疫微环境重塑" 的叙事。

### 3.2 建议删除/弱化的内容

| 内容 | 处理建议 | 理由 |
|------|----------|------|
| 100 篇文献系统总结 | 移到补充材料 | 创新但偏离生物学主线 |
| Ridge Cox 8-feature 模型 | 替换为更强的模型 | 性能不够 |
| CELLxGENE WMG query | 替换为 raw scRNA-seq | 不被审稿人认可 |
| DepMap 全面展示 | 保留关键基因结果 | 辅助即可 |
| GDSC/CTRP/PRISM 全面展示 | 精简到 top candidates | 太散 |

### 3.3 必须新增的分析（按优先级排序）

#### P0 - 必须做，否则不可能一区

**1. Raw scRNA-seq 分析**
- 数据源推荐：
  - **HLCA (Human Lung Cell Atlas)**: 最全面的肺单细胞图谱
  - **GSE131907**: NSCLC scRNA-seq (Kim et al., Nature Medicine 2020), 208,506 cells
  - **GSE149655**: LUAD scRNA-seq with treatment info
  - **GSE171145**: LUAD tumor microenvironment scRNA-seq
  - **CRA001160 (NGDC/GSA)**: 中国人群 LUAD scRNA-seq
- 分析内容：
  - 细胞类型注释 (Seurat/Scanpy)
  - 候选基因的细胞类型特异表达
  - 恶性细胞 vs 非恶性细胞差异表达
  - InferCNV 恶性细胞鉴定
  - 细胞通讯分析 (CellChat)
  - 发育轨迹 (Monocle3 / scVelo)

**2. 空间转录组深度分析**
- 你已有 E-MTAB-13530 的 22 个 section，这是很好的资源
- 需要新增：
  - cell2location / CARD / BayesSpace 空间 deconvolution
  - 与 scRNA-seq reference 的整合
  - 空间共定位分析
  - 空间异质性评分
  - 肿瘤-免疫界面分析

**3. 升级预后模型**
- 替换 Ridge Cox 为：
  - LASSO Cox + RSF (Random Survival Forest) + XGBoost survival + CoxBoost 的 ensemble
  - 或 deep learning survival model (DeepSurv / Cox-nnet)
- 目标：validation C-index ≥ 0.65
- 增加：Nomogram + 校准曲线 + DCA (Decision Curve Analysis) + 时间依赖 ROC

#### P1 - 强烈推荐，显著提升论文质量

**4. 转录因子调控网络**
- 方法：SCENIC / SCENIC+ / pySCENIC
- 在单细胞数据上推断调控网络
- 找到驱动候选 axis 的核心转录因子
- 与 bulk TCGA 做交叉验证

**5. 免疫微环境深度表征**
- 多方法估计：CIBERSORT / xCell / MCPcounter / ESTIMATE / TIMER / EPIC
- 免疫评分与风险模型的关联
- 免疫逃逸分析 (TIDE)
- Tumor Immunity Dysfunction and Exclusion

**6. 扩展 ICB 验证**
- 更多 ICB cohort:
  - **IMvigor210** (Mariathasan et al.) - 虽然是膀胱癌但可做 pan-cancer 参考
  - **GSE78220** (melanoma anti-PD1)
  - **NSCLC-specific**: 寻找 ORIENT-11, KEYNOTE-024/189 的公开表达数据
  - **POPLAR / OAK trials**: 如果有公开部分

#### P2 - 加分项，增强创新性

**7. 多组学整合**
- TCGA-LUAD 的 DNA methylation (450K) + 表达整合
- 拷贝数变异 (CNV) 与表达关联
- miRNA-mRNA 调控网络
- 突变谱与表达 signature 的关联

**8. 分子对接 / 药物预测**
- 对 drug sensitivity 关联结果做分子对接验证
- AutoDock Vina / MOE
- 增强药物转化叙事

---

## 四、推荐的新数据源

### 4.1 必须获取的数据

| 数据集 | 类型 | 用途 | 获取方式 |
|--------|------|------|----------|
| GSE131907 | scRNA-seq | 单细胞主分析 | GEO 直接下载 |
| HLCA | scRNA-seq atlas | 正常肺参考 | CELLxGENE portal |
| CPTAC-LUAD | 蛋白质组 | 蛋白验证 | CPTAC portal |
| TCGA-LUAD methylation | DNA 甲基化 | 多组学整合 | UCSC Xena |
| TCGA-LUAD CNV | 拷贝数 | 多组学整合 | UCSC Xena |
| TCGA-LUAD miRNA | miRNA-seq | 调控网络 | UCSC Xena |

### 4.2 推荐获取的数据

| 数据集 | 类型 | 用途 |
|--------|------|------|
| GSE72094 | Bulk + clinical | 第三外部验证队列 |
| GSE68465 | Bulk + clinical | 第四外部验证队列 (Director's Challenge) |
| GSE37745 | Bulk + clinical | 欧洲队列验证 |
| MSKCC cBioPortal | 突变 + clinical | 突变验证 |

### 4.3 单细胞数据详细推荐

| 数据集 | 细胞数 | 特点 |
|--------|--------|------|
| GSE131907 | ~208K | 最常引用的 NSCLC scRNA-seq |
| GSE171145 | ~100K | LUAD TME focused |
| GSE149655 | ~60K | Treatment context |
| CRA001160 | ~90K | 中国人群 |

---

## 五、重构后的论文框架建议

### 标题模板
"Single-cell and spatial transcriptomics reveal a [X]-regulatory program driving prognostic heterogeneity and immune microenvironment remodeling in lung adenocarcinoma"

### 重构后的 Results 架构

1. **Identification of a [X]-associated transcriptomic axis in LUAD**
   - TCGA-LUAD 全转录组筛选
   - 与临床特征和突变的关联
   - 多组学整合支持

2. **Construction and multi-cohort validation of a prognostic model**
   - 升级后的 ML ensemble 模型
   - TCGA internal + GSE31210 + GSE50081 + GSE72094 验证
   - Nomogram + DCA

3. **Single-cell landscape reveals cell-type-specific expression and regulatory networks**
   - scRNA-seq 分析
   - SCENIC 转录因子网络
   - 细胞通讯

4. **Spatial transcriptomics confirms tissue-level organization of the [X] axis**
   - 空间 deconvolution
   - 空间共定位
   - 肿瘤-免疫界面

5. **The [X] axis shapes the tumor immune microenvironment**
   - 多方法免疫浸润估计
   - TIDE 免疫逃逸
   - ICB 响应关联

6. **Functional dependency and therapeutic vulnerability**
   - DepMap CRISPR
   - Drug sensitivity
   - HPA 蛋白验证

### 重构后的 Figure 规划

| Figure | 内容 | 数据源 |
|--------|------|--------|
| Fig 1 | Study design + TCGA discovery + multi-omics landscape | TCGA |
| Fig 2 | Prognostic model construction + multi-cohort validation | TCGA + GEO × 3-4 |
| Fig 3 | Single-cell atlas: cell-type expression + InferCNV + trajectory | scRNA-seq |
| Fig 4 | Spatial transcriptomics: deconvolution + co-localization | E-MTAB-13530 |
| Fig 5 | TME characterization + immune infiltration + ICB response | TCGA + ICB cohorts |
| Fig 6 | Regulatory network + functional dependency + drug sensitivity | SCENIC + DepMap + Drug |
| Suppl | 详细方法、扩展验证、附加分析 | All |

---

## 六、技术实施路线图

### Phase 1 (Week 1-2): 数据获取与环境搭建
- [ ] 下载 scRNA-seq 数据 (GSE131907 优先)
- [ ] 下载额外验证队列 (GSE72094, GSE68465)
- [ ] 下载 TCGA methylation + CNV + miRNA
- [ ] 下载 CPTAC-LUAD 蛋白组
- [ ] 搭建 R/Python 分析环境 (Seurat, Scanpy, cell2location, SCENIC)

### Phase 2 (Week 3-5): 核心新分析
- [ ] scRNA-seq 全流程分析
- [ ] 空间 deconvolution + integration
- [ ] 模型升级 + 多队列验证
- [ ] SCENIC 转录因子网络

### Phase 3 (Week 6-7): 整合与补充分析
- [ ] 免疫微环境深度表征
- [ ] 多组学整合
- [ ] ICB 扩展验证
- [ ] 分子对接 (optional)

### Phase 4 (Week 8-10): 论文重写
- [ ] 重构 Results
- [ ] 重做所有 Figure
- [ ] 更新 Source Data
- [ ] 新一轮 CNS readiness audit

---

## 七、投稿策略建议

### 目标期刊梯队

| 梯队 | 期刊 | IF (2025) | 建议 |
|------|------|-----------|------|
| 冲刺 | Nature Communications | ~17 | 需要所有 P0+P1 完成 |
| 冲刺 | Genome Biology | ~13 | 方法学创新要求高 |
| 稳妥一区 | Journal of Hematology & Oncology | ~28 | 临床转化叙事强 |
| 稳妥一区 | Molecular Cancer | ~37 | 机制+数据挖掘结合 |
| 保底一区 | Briefings in Bioinformatics | ~9 | 方法导向 |
| 保底一区 | Computers in Biology and Medicine | ~7 | 计算方法导向 |

### 关键审稿人可能的问题

1. "为什么不做真正的单细胞分析？" → 必须解决
2. "C-index 太低" → 必须提升
3. "缺乏机制层面支持" → SCENIC + spatial 解决
4. "只有回顾性验证" → 增加队列数量 + nomogram
5. "与现有 LUAD signatures 的比较？" → 需要 benchmark

---

## 八、总结

你的项目有一个很好的基础：全面的文献调研、完整的 TCGA 发现流程、真实的 Visium 空间数据。但距离一区投稿，核心差距在于：

1. **缺少 raw scRNA-seq 分析**（这是 2024-2026 生信论文的标配）
2. **预后模型性能偏低**（C-index 0.584 不够）
3. **空间分析深度不足**（有数据但没做 deconvolution）
4. **缺乏清晰的 biological narrative**

建议的核心动作：
- 获取 GSE131907 scRNA-seq 数据，做完整单细胞分析
- 对 E-MTAB-13530 做 cell2location 空间 deconvolution
- 升级预后模型并增加验证队列
- 围绕一个 lead biological axis 重写论文

预计需要 8-10 周完成所有新增分析和论文重写。
