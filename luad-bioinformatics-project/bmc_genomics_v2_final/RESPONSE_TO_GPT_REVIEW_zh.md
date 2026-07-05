# 对 GPT 审稿意见的逐条回应

日期:2026-07-04 · 结论:GPT 审稿质量高,大部分正确,我据实**接受并已修改**了绝大多数。以下逐条说明处理方式。

---

## 一、我完全接受并已用真实重分析修复的(核心)

### 1. 单细胞细胞级 P 值伪重复(GPT #9)—— 已改为样本级 pseudobulk ✅
- **接受**。原来把 32,764 vs 3,703 个**细胞**当独立观测得 P<1e-20 是伪重复。
- **已重做**:每样本上皮细胞聚合成 pseudobulk,在**样本层面**比较(36 个肿瘤来源 vs 11 个正常肺样本,Mann-Whitney)。
- **新结果**:9/9 基因仍 **FDR<0.05**(样本级)。结论不变但统计单位正确。摘要/正文/Fig6b/图注全部改。
- 新表:`sc_malignant_vs_normal_pseudobulk.csv`。

### 2. "malignant-specific"过强 + "tumour-origin"≠"malignant"(GPT #10/#11)—— 已降级 ✅
- **接受**。C1QTNF6/STEAP1 在成纤维最高,不能叫"specific"。
- **已改**:全文 "malignant-epithelial-**specific**" → "**enriched** in malignant/tumour-derived epithelium";恶性态用 Kim 的 **inferCNV 恶性标签**;明确写"compartment-biased rather than strictly specific"。

### 3. 空间解卷积循环验证(GPT #14)—— 已做 leave-programme-out ✅
- **接受**。原 64-marker signature **包含了 9 个 programme 基因**,再相关就人为放大。
- **已重做**:signature **删掉 9 个 programme 基因**(剩 55 基因)重新解卷积。
- **新结果**:仍成立但更诚实——21/22 切片、**5/5 患者**阳性,median rho 0.18。新表 `spatial_deconv_leaveout_section.csv`。

### 4. 22 切片非独立 + 空间自相关(GPT #15/#16)—— 已按患者/切片报告 ✅
- **接受**。22 切片其实只来自 **5 个患者**;spot 级 P 值不能当主推断。
- **已改**:改报 per-section 和 per-patient(5/5 患者阳性),明确写只有 5 患者、**患者级 Wilcoxon p=0.06(欠功效)**;不再强调 pooled-spot 的 P≈0。

### 5. nomogram 缺 clinical-only + 训练测试泄漏(GPT #4/#5/#6)—— 已彻底重做 ✅ **(最重要)**
- **完全接受,且你的批评改变了结论**。原来只比"gene vs gene+clinical",没比 clinical-only,且在全 557 例拟合后回测。
- **已重做**:train 拟合 / test 评价三个模型 + bootstrap CI + LR 检验。
- **新结果(诚实且关键)**:
  - clinical-only test C=**0.724**;gene-only 0.638;combined 0.730
  - **ΔC(combined−clinical)= +0.006(95% CI −0.07 ~ +0.08)——几乎零增量**
  - LR 检验 p=9.5e-09(独立相关但**不改善判别**)
- **已把全文"nomogram 提到 0.75 / clinical utility"改写为**:"score 是独立预后因子但相比临床分期**不提供增量判别**"。Fig8 标题 → "Incremental prognostic assessment"。这反而更符合本文诚实定位。新表 `nomogram_proper_cindex.csv`、`nomogram_incremental.csv`。

---

## 二、我接受并已修改(表述/一致性,GPT 第七节等)

### 6. 新旧版本矛盾(GPT 第七节)—— 全部已同步 ✅
- 图数 "5 main figures" → **8 main + 2 supplementary**(图例表头、正文均改)。
- Limitations 删掉"single-cell 是聚合的""spatial 是 proxy 非 deconvolution"(与新工作矛盾)。
- Future work 删掉"补单细胞和 deconvolution"(已做)。
- 数据角色表**新增 GSE131907 行**,更新 CELLxGENE/Visium 角色描述。
- **引用 [22] 标错**已改:E-MTAB-13530 解卷积句改引 **[13,14]**(数据),scanpy [22] 仅作方法引用。

### 7. 其它降级(GPT #12/#17/#18/#20)—— 已改 ✅
- **#20 Fig1"两个最强候选"**:ERO1A 其实第 4(DKK1/KCNF1 在前)→ 改"two biologically prioritised lead candidates"。
- **#12 MKI67 不算新发现**:score 本含细胞周期基因 → 明确写"proliferation link is expected...captures a proliferative state rather than a novel programme"。
- **#17 GSE37745"查明机制"过强**:改"post-hoc gene-level inspection suggested...exploratory rather than pre-specified mechanism"。
- **#18 GSE37745"mixed-histology" vs "n=106 adeno"矛盾**:统一为"adenocarcinoma subset of a mixed-histology cohort"。
- **未核验 meta HR 1.346**(GPT 建议删):已从正文删除,仅留一句"descriptive supplementary, not primary evidence"。

---

## 三、原"留给后续"的三条,本轮也已补做 ✅

### 8. GEO 外部验证信息泄漏(GPT #1)—— 已重训无泄漏冻结模型 ✅
- **已做**:候选池 = **12 个纯 TCGA 全基因组 FDR<0.05 基因(完全不含 GEO)**,TCGA train 拟合多变量 Cox、冻结系数,再把 5 个 GEO 当**真外部**评价。
- **结果(强)**:leak-free 模型复现了原模型的模式——完全独立的 **GSE30219 C=0.700(HR 1.53)、GSE68465 C=0.608(HR 1.27)** 验证成功;GSE37745 仍 0.525(与之前一致);TCGA test 0.649。
- **结论**:**外部信号不是特征选择泄漏造成的**。已把这一 rebuttal 写进正文 Results,并在 Limitations 注明。新表 `frozen_model_external_validation.csv`、`frozen_model_coefficients.csv`。

### 9. 自写 Cox 可重复性(GPT #2)—— 已用 scikit-survival 核验 ✅
- **已做**:装上 scikit-survival,把我的手写 Cox/concordance 与之比对。
- **结果**:**完全一致**(train 0.6656 vs 0.6656;test 0.6494 vs 0.6496,三位小数一致)。已写进 Methods。新表 `cox_implementation_crosscheck.csv`。
- 未做:Schoenfeld 比例风险检验仍建议你本地用 R survival 补(lifelines 本环境编译失败)。

### 10. TCGA 样本溯源(GPT #3)—— 已给完整 sample-flow + 稳健性 ✅
- **已做**:589 行 = **517 患者**(528 primary-tumour、59 normal-tissue、2 metastatic 条码)→ 576 有正随访(211 事件)→ 557 有 stage/age(nomogram 集)。
- **暴露并处理了真问题**:含 59 个正常组织条码 + 66 个多样本患者。
- **稳健性**:清洗到 primary-tumour-only + 患者去重(**503 患者**)后 test C=**0.749**(比含噪版更高)→ 结果不由正常条码/重复样本驱动。已写进 Methods。新表 `tcga_sample_flow.csv`。

### 11. HPA 候选池(GPT #21)—— 已解释 ✅
- **已做**:HPA 评价的是 **35 基因候选池**(top-survival + pathway 候选的并集,含 9 个 programme 基因 + KIF18A/PFKP/ERO1B 等)。已在正文 Fig3 段注明。

### 仍受硬件/数据限制未做(如实标注)
- 全 pySCENIC(无 GPU)、IPCW time-ROC、前瞻验证、湿实验 —— 文中均标为未完成边界。
- Schoenfeld PH 检验 —— 建议你本地 R survival 补。

## 四、关于期刊定位

**接受 GPT 的判断**:上一轮报告说"可冲 J Hem Onc / Molecular Cancer 之下一档"过于乐观。以当前公共数据性质、无湿实验、以及"score 无增量判别"的诚实结论,**现实定位仍是 BMC Genomics 或同级组学/生信期刊**。完成第三节的深层修复(重训冻结模型、R survival、sample-flow)后,送审基础会更稳。

---

## 五、修改后的净变化

- 3 张图(Fig6/7/8)按修正分析重做 + 无泄漏冻结模型/Cox核验/样本流程三项补做;主稿、图例、Word 附图、BMC 分文件包全部同步。
- 关键数字更新:单细胞→样本级 FDR<0.05;空间→leave-out 5/5 患者;nomogram→ΔC +0.006(独立但无增量)。
- 残留过强表述检查 = 0。
- **本轮把"疑似夸大"的三处(单细胞 P 值、nomogram 0.75、空间 confirmed)全部改为经得起审的诚实版本**——这正是本文"透明证据层级"定位应有的样子。GPT 的审稿实质性提高了稿件质量。
