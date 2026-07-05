# 对 GPT 第二轮审稿的逐条回应(R2)

日期:2026-07-04 · 结论:GPT 抓住的核心问题(主 TCGA 分析集不合格、患者级泄漏)**完全正确**,我已把主分析**彻底重做**。这轮修改改变了论文的核心结论,以下如实说明。

---

## ★ 决定性重做:清洗患者级主分析(GPT 第一、二节)—— 已完成,且结论显著减弱

**做了什么**:严格按 GPT 要求重建——
```
仅 Primary Tumor → TCGA patient barcode → 每患者仅一个样本 → 503 独立患者
→ 按患者分组、事件分层 70/30 拆分(train 352/ev127, test 151/ev55,无患者跨集)
→ 全基因组 median-split log-rank 筛选【只在训练集】→ BH FDR
→ 冻结系数 → test 只评一次 → GEO 真外部
```

**诚实结果(核心变化)**:
- **训练集全基因组筛选:0 个基因通过 FDR<0.05**。原来的"12 FDR 基因"是用**全部 TCGA(含测试集)**算的——GPT #2 完全正确。
- 用 nominal top-gene 建模:**held-out test C=0.62(95% CI 0.53–0.72)**,CI 触及 0.5。
- 外部转移**弱且不一致**:GSE30219 0.63、GSE37745 0.57、GSE68465 0.56,CI 都触及 0.5。
- **原来报的 ~0.64 是乐观的**(特征选择用了全队列);清洗后更弱。

**影响**:全文已把这个 score **降级为 exploratory prognostic signal(非 validated signature)**。摘要、模型段、Figure 2、Limitations、Discussion 全部改写。**Figure 2 已重做**成"0 基因过全基因组 FDR + test 0.62 宽 CI + 弱外部转移"。

这是本轮最重要的诚实修正:严格做统计后,预后信号比之前呈现的弱得多。

---

## 一、单细胞:改为患者级配对(GPT 第四节)✅
- **接受**:36 vs 11"样本"仍有患者嵌套(58 样本来自 ~44 患者)。
- **已重做**:对 **10 个有配对正常肺+肿瘤上皮的患者**做**配对 Wilcoxon**(患者为单位)。
- **结果**:**7/9 基因 FDR<0.05**(PLK1/ERO1A/TK1/DKK1/C1QTNF6/STEAP1/ECT2;KNL1、DEPDC1B 不显著)。Figure 6b 已改患者配对,Figure 6d 删掉"P≈0"、标注为 descriptive cell-level。新表 `sc_paired_patient_tumour_vs_normal.csv`。

## 二、空间(GPT 第五节)✅
- 摘要/正文"supported"→"**descriptively consistent with** epithelial co-localisation";已明确 5 患者、患者级 p=0.06 欠功效;已按 section/patient 报告(不再强调 pooled-spot)。

## 三、Methods 与结果同步(GPT 第三节)✅
- 单细胞方法改为**患者级配对 Wilcoxon**、写清聚合方式、FDR 项数、inferCNV 恶性标签。
- 空间 signature 明确 **64→删9→55 基因**、NNLS 比例归一化、per-section/patient。
- **删除 time-dependent AUC**(未做 IPCW,不再声称);删除 nomogram-Breslow 校准表述。
- C-index 数字来源统一:现在主结果只有清洗患者级一套(train 0.67 / test 0.62),并说明 scikit-survival 核验一致。

## 四、临床联合模型(GPT 第六节)✅(结论本就正确,措辞收紧)
- LR p=9.5e-9 已明确标注为**训练集内关联,非独立验证统计**。
- stage 编码写明(ordinal 1–4)、age 标准化、sex 二元、complete-case;**PH 假设未正式检验**已如实写入 limitation。

## 五、GEO 泄漏(GPT 第七节)◑ 已如实降级
- 正文"The external signal is therefore not created by feature-selection leakage" → 降为"**A separately derived TCGA-only model showed a similar cross-cohort pattern, suggesting the signal was not solely attributable to GEO-informed feature selection**",并明确"neither model constitutes validated external performance"。
- 清洗模型的 GEO 转移已带 **CI 和 n/events**(新表 `clean_model_geo_external.csv`);Figure 2 明确标注哪两个队列参与了选择(灰色)vs 独立(蓝色)。

## 六、概念降级 programme→signature(GPT 第八节)✅
- **标题**改为"…a PLK1-associated **mitotic and ER-redox signature** in lung adenocarcinoma";摘要、Discussion 同步。Discussion 明确写:证据本身反对"coordinated programme"(mitotic 核心稳定、ERO1A 单独 context、remodelling 基因偏 stromal 且在一个队列反转)→ 定性为 **composite prognostic signature**。

## 七、删除项(GPT 第十、十二节)✅
- **免疫治疗段删除**,只留一句"Treatment-response prediction was not evaluated as a primary endpoint…non-use boundary"。
- **未核验 meta-analysis** 的"requires final human verification"**已删除**,改为纯 descriptive supplementary。
- 图数已是 8 主图(图例表头已更新)。

## 八、图件(GPT 第十一节)部分完成
- ✅ Figure 2 重做(清洗模型)、Figure 6 改患者配对、Fig4 在图件计划中移为 Supplementary。
- ⏳ 仍待做(下轮/你本地):Fig 6b 加每患者散点+CI、Fig 7a 改 per-section 分布图、Fig 8 "clinical covariates"命名、把图内大标题移到 legend、Fig 5b 加细胞系分布。

---

## 仍需你/本地完成(如实标注,我无法在此环境做)
1. **nested CV / 重复拆分 / bootstrap optimism**(GPT 反复强调)——单次 70/30 在这个事件数下不稳,已写入 limitation;建议你本地补。
2. **Schoenfeld PH 检验**(R survival / lifelines,本环境装不上)。
3. **真实文献综述深化**(GPT 第九节):Background 需补 PLK1-LUAD、ERO1A-ER stress、既有 LUAD signature、PLK 抑制剂临床前的真实引用,并写明检索方法。我可以下一轮补 5–8 篇真实文献。
4. 作者信息、仓库 DOI、查重。

---

## 诚实的总判断
GPT 是对的:**在解决主分析集问题之前,其它数字都不算最终结果**。现在这个问题已解决,代价是——**预后信号被证明是弱的、nominal 的、未通过全基因组校正的**。这不是坏事:它把稿件从"声称有预后 signature"诚实地变成了"透明证据层级 + 一个 exploratory 信号 + 一组清晰的 negative boundaries"。这个定位对 BMC Genomics 仍可行,但创新性有限,期刊定位维持 BMC Genomics 或同级。
