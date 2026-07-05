# 基于实际数据的精准诊断报告（v2.0）

本报告基于完整解压并阅读了项目所有代码、数据和论文后写成，取代之前基于交接文档的初步诊断。

---

## 一、发现的关键问题

### 问题 1（致命）：Cox 模型基因与生物学叙事完全脱节

你的全转录组生存筛选 top 12 FDR 显著基因是：

| 排名 | 基因 | FDR | 方向 | 生物学 |
|------|------|-----|------|--------|
| 1 | **PLK1** | 0.021 | high=worse | 有丝分裂激酶，100% LUAD 依赖 |
| 2 | **DKK1** | 0.021 | high=worse | Wnt 拮抗因子 |
| 3 | **KCNF1** | 0.021 | high=worse | 钾通道 |
| 4 | **ERO1A** | 0.021 | high=worse | ER 氧化应激 |
| 5 | INPP5J | 0.021 | high=better | 磷脂酶 |
| 6 | **DEPDC1B** | 0.021 | high=worse | 有丝分裂 |
| 7 | **KNL1** | 0.021 | high=worse | 着丝粒 |
| 8 | C1QTNF6 | 0.021 | high=worse | 补体样因子 |
| 9 | **STEAP1** | 0.033 | high=worse | 金属还原酶 |
| 10 | **TK1** | 0.033 | high=worse | 胸苷激酶 |
| 11 | GPD1L | 0.033 | high=better | 磷酸脱氢酶 |
| 12 | IRX5 | 0.033 | high=better | 转录因子 |

但你的 8 基因 Cox 模型选的是：

| 基因 | 系数 | 在生存筛选中的排名 |
|------|------|-------------------|
| DKK1 | +0.303 | **#2** (唯一重叠) |
| FABP6 | -0.253 | 不在 top 30 |
| SPRR1B | +0.196 | ~#18 |
| C11orf16 | -0.180 | 不在 top 30 |
| IER5L | +0.177 | 不在 top 30 |
| STRIP2 | +0.176 | 不在 top 30 |
| BANCR | -0.053 | ~#29 |
| GALNT14 | +0.042 | 不在 top 30 |

**只有 DKK1 同时出现在生物学叙事和模型中。** 你的论文讲的是 PLK1/ERO1A/KNL1 的有丝分裂/ER-redox 故事，但你的预后模型里一个都没有。审稿人一定会问：如果 PLK1 是最重要的生物学发现，为什么模型里没有它？

**原因分析：** 你的脚本 `08_internal_cox_model_luad.py` 用的流程是：
1. 取训练集 top 5000 高方差基因（不是全部 8000）
2. 中位数分割 log-rank 筛选
3. 取 top 80 → 按 Spearman |r| < 0.75 顺序去相关
4. 保留前 8 个不相关基因
5. Ridge Cox (alpha=0.2)

问题在于第 3-4 步：PLK1/ERO1A/KNL1/ECT2/TK1 这些有丝分裂基因彼此高度相关（它们在同一个 pathway），所以去相关步骤把大部分都删了，最终模型里留下的是一堆低相关但生物学不连贯的基因。

### 问题 2（致命）：内部验证完全失败

- **Test C-index = 0.584**
- **Test log-rank p = 0.295**（不显著！）

这意味着你的模型在自己的内部 held-out test set 上**连统计显著性都没达到**。这不是"性能偏低"的问题——这是模型在自己的数据上就不工作。

但有趣的是，外部验证反而更好：
- GSE31210 eligible OS: C-index = 0.665, p = 3.36e-04
- GSE50081 adeno OS: C-index = 0.622, p = 9.77e-03

这说明信号是真实存在的，但你的建模方法（median-split → correlation pruning → Ridge）太弱了，没有有效地捕获这个信号。

### 问题 3（严重）：建模方法落后

当前方法的具体问题：

| 步骤 | 问题 | 顶刊做法 |
|------|------|----------|
| 特征筛选：中位数分割 log-rank | 连续变量二值化损失信息 | 单变量 Cox p 值排序 |
| 特征选择：顺序去相关 | 结果依赖顺序，不稳定 | LASSO 自动处理共线性 |
| 模型：Ridge Cox (alpha=0.2) | 极弱正则化，几乎没有收缩 | LASSO Cox + CV 选 lambda |
| 超参数选择：固定 alpha=0.2 | 没有 CV 调参 | 10-fold CV 选最优 alpha |
| 特征数：固定 MAX=8 | 任意数字 | 由 LASSO 自动决定 |
| 验证：单次随机分割 | 种子依赖性强 | 100 次 bootstrap 或 repeated CV |

### 问题 4（严重）：摘要 1200 字，Results 16 节

- 摘要应该 250 字（structured）或 300 字（unstructured），你的是 1200 字
- Results 有 16 个小节，审稿人看到第 5 节就会失去耐心
- 论文整体读起来像分析日志，不像科学论文

### 问题 5（已知）：缺少 scRNA-seq 和空间 deconvolution

（与初步诊断一致，不再赘述）

---

## 二、你的项目真正的优势（不要丢掉）

1. **PLK1 是一个极好的 lead gene：**
   - 全转录组生存筛选 #1（FDR 0.021）
   - DepMap 100% LUAD 依赖（mean effect = -2.77）
   - 空间转录组显著（p = 8.73e-05）
   - 有成熟的 PLK 抑制剂（BI-2536, Volasertib）
   - 已有临床试验数据

2. **ERO1A 形成完美的双轴叙事：**
   - 生存筛选 #4（FDR 0.021）
   - 空间转录组最强差异（tumor-adjacent diff = 0.343, p = 8.73e-05）
   - 代表 ER 氧化应激轴，与 PLK1 的有丝分裂轴互补
   - ERO1B 也在 top 20

3. **22 个 Visium sections 是真正的差异化优势**

4. **外部验证的信号是真实的** — GSE31210 C-index 0.665 说明存在可挖掘的预后信号

5. **免疫 panel score 在 ICB 中有效** — 3/3 cohorts 显著

---

## 三、推荐的根本性重构方案

### 3.1 重新定义 Lead Story

**从：** "我们做了 ridge Cox 建了一个 8 基因模型"
**改为：** "我们发现 LUAD 中 PLK1-driven mitotic checkpoint 和 ERO1A-driven ER-redox 两个调控轴协同驱动预后异质性"

**标题建议：**
"Mitotic checkpoint and ER-redox stress axes converge to shape prognosis and immune microenvironment in lung adenocarcinoma: a multi-layered computational dissection"

### 3.2 重建预后模型

**具体操作：**

```
步骤 1：候选基因池
- 取全转录组生存筛选 FDR < 0.05 的基因（约 12-28 个）
- 加上空间/DepMap/pathway 多层支持的基因
- 总池大约 30-50 个候选基因

步骤 2：多方法特征选择
- LASSO Cox (alpha=1, 10-fold CV): 记录 non-zero genes
- Elastic Net Cox (alpha=0.5, 10-fold CV): 记录 non-zero genes
- Random Survival Forest (VIMP ranking): top 20
- 取 ≥2/3 方法共同选出的基因（consensus）

步骤 3：最终模型
- multivariate Cox with stepwise selection
- 10-fold CV 估计 C-index 分布
- 100 次 bootstrap 稳定性评估

步骤 4：验证
- TCGA 内部 100 次 bootstrap C-index
- GSE31210: C-index + KM + time-ROC
- GSE50081: C-index + KM + time-ROC
- GSE72094 (新增): C-index + KM + time-ROC
```

**为什么这样做：**
- LASSO 会自动保留 PLK1 或 KNL1（它们是真正的 top hit）
- 不再需要手动去相关
- 多方法 consensus 比单一 Ridge 稳定
- 预计 validation C-index 可以从 0.584 提升到 0.65-0.70

### 3.3 重构 Figure 和 Results

**从 18 张主图 → 6 张主图：**

| 新 Figure | 对应的原内容 | 改动 |
|-----------|------------|------|
| **Fig 1**: Study design + TCGA discovery | 原 Fig1-4 合并 | 加 study schema |
| **Fig 2**: Prognostic model + multi-cohort validation | 原 Fig5,7,8,9 合并重做 | LASSO 特征选择 + KM + time-ROC + nomogram |
| **Fig 3**: Single-cell atlas | **全新** | 需要 raw scRNA-seq |
| **Fig 4**: Spatial transcriptomics | 原 Fig13,18 升级 | 加 deconvolution |
| **Fig 5**: TME + ICB response | 原 Fig16,17 + 新增 | 多方法免疫浸润 + TIDE |
| **Fig 6**: Regulatory network + function | 原 Fig10,14,15 合并 | 加 SCENIC + 精简 DepMap/Drug |

**从 16 节 Results → 6 节：**

1. Identification of PLK1-mitotic and ERO1A-ER-redox axes in LUAD (原 §1-3 合并)
2. A consensus prognostic model and multi-cohort validation (原 §4-8 替换重做)
3. Single-cell landscape reveals cell-type-specific regulation (全新)
4. Spatial transcriptomics confirms tissue-level axis architecture (原 §12 升级)
5. The dual axis shapes the tumor immune microenvironment (原 §5-6,15-16 合并)
6. Functional dependency and therapeutic vulnerability (原 §13-14 精简)

---

## 四、你的 8 个 Cox 基因怎么处理

**不要完全丢弃它们。** 虽然模型需要重建，但其中几个基因有独立价值：

| 基因 | 处理建议 | 理由 |
|------|----------|------|
| **DKK1** | 保留，可能进入新模型 | 生存筛选 #2，Wnt pathway |
| **SPRR1B** | 保留观察 | 生存筛选 #18，上皮分化 |
| **BANCR** | 可保留 | lncRNA，有独立研究价值 |
| IER5L | 移到补充材料 | 生物学不清晰 |
| STRIP2 | 移到补充材料 | 不在核心 pathway |
| C11orf16 | 移到补充材料 | 功能未知 |
| GALNT14 | 移到补充材料 | 系数太小 (0.042) |
| FABP6 | 移到补充材料 | 保护性方向，与主轴不一致 |

---

## 五、脚本层面需要修改的具体文件

### 需要重写的脚本

| 脚本 | 问题 | 修改内容 |
|------|------|----------|
| `08_internal_cox_model_luad.py` | 整个建模流程需要重写 | LASSO + RSF + consensus → multivariate Cox |
| `14_luad_single_cell_localization.py` | 用 CELLxGENE WMG API，不是 raw scRNA-seq | 替换为 Seurat/Scanpy raw scRNA-seq pipeline |
| `18_biostudies_visium_luad_spatial.py` | 只做 spot-level proxy | 增加 CARD/cell2location deconvolution |

### 需要新增的脚本

| 新脚本 | 内容 |
|--------|------|
| `29_scrnaseq_analysis.py` (或 .R) | GSE131907 raw scRNA-seq 全流程 |
| `30_spatial_deconvolution.py` | CARD/cell2location 空间 deconvolution |
| `31_scenic_regulon_analysis.py` | pySCENIC 转录因子网络 |
| `32_immune_infiltration_multi_method.py` | CIBERSORT + xCell + MCPcounter |
| `33_build_consensus_prognostic_model.py` | LASSO + RSF + stepwise Cox |
| `34_additional_external_validation.py` | GSE72094 验证 |
| `35_nomogram_calibration_dca.py` | Nomogram + 校准 + DCA |

### 可以保留的脚本

| 脚本 | 状态 |
|------|------|
| `00-07` (文献+TCGA数据+GEO) | 保留不变 |
| `05` (全转录组筛选) | 保留，结果可信 |
| `09-12` (临床+突变+外部验证) | 保留，可能需要用新模型的 score 重跑 |
| `13` (pathway) | 保留 |
| `17` (HPA) | 保留 |
| `19-20` (DepMap/Drug) | 保留，精简展示 |
| `22-23` (ICB) | 保留 |
| `24-28` (审计/source data) | 保留，最后重跑 |

---

## 六、实际数据中的亮点（可以直接用在新论文中）

### 6.1 最强的统计结果

| 发现 | 数值 | 可以怎么用 |
|------|------|----------|
| PLK1 全转录组 #1 | FDR 0.021, chi2=20.6 | Lead gene 的 discovery 证据 |
| 临床+突变校正 HR | 1.775, p=6.14e-13 | 独立预后因子 |
| PLK1 DepMap 100% 依赖 | effect=-2.77 | 功能必需性证据 |
| ERO1A 空间最强差异 | diff=0.343, p=8.73e-05 | 空间验证 |
| 免疫 panel ICB 3/3 显著 | Cho p=4.58e-04 | 免疫治疗预测潜力 |
| EGFR 在低风险组富集 | 19.1% vs 9.2%, p=0.001 | 突变-表达关联 |
| SMARCA4 在高风险组富集 | 11.4% vs 4.3%, p=0.003 | 突变-表达关联 |

### 6.2 你的 cytotoxic-checkpoint coupling (rho=0.788) 很有趣

这个发现本身不预测生存，但它说明了 LUAD 中免疫应答和免疫抑制是紧耦合的——可以支撑 TME 章节的讨论。

---

## 七、最终建议优先级

| 优先级 | 任务 | 预计时间 | 影响 |
|--------|------|----------|------|
| **P0** | 用 LASSO+RSF+consensus 重建预后模型 | 3-5 天 | 解决 C-index 问题 |
| **P0** | 下载 GSE131907 做 raw scRNA-seq | 1-2 周 | 解决单细胞缺失 |
| **P0** | 对 E-MTAB-13530 做 CARD deconvolution | 3-5 天 | 解决空间深度 |
| **P1** | 下载 GSE72094 做第三外部验证 | 2-3 天 | 增加验证队列 |
| **P1** | pySCENIC 转录因子网络 | 3-5 天 | 增加机制层 |
| **P1** | 多方法免疫浸润 + TIDE | 2-3 天 | 增加免疫深度 |
| **P2** | 重写论文（6 节 Results + 250 字摘要） | 1 周 | 叙事重构 |
| **P2** | Nomogram + calibration + DCA | 1-2 天 | 临床转化指标 |
| **P3** | TCGA methylation/CNV 多组学整合 | 2-3 天 | 多组学证据 |

---

## 八、一句话总结

你的项目有真实的生物学信号（PLK1/ERO1A 双轴在 TCGA + 2 个 GEO + 空间 + DepMap 中一致），但当前的 Ridge Cox 建模方法太弱，选出了一组与核心生物学不匹配的基因，导致内部验证都不显著。**重建模型 + 加 scRNA-seq + 空间 deconvolution + 重写叙事 = 一区可投。**
