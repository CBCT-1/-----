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

## 三、部分接受 / 已诚实标注但受环境限制未能完全重做

### 8. GEO 外部验证信息泄漏(GPT #1)—— 已如实重贴标签,但未重训模型 ◑
- **接受问题真实存在**:GSE31210/GSE50081 通过 cross-layer support 参与了选基因,不能算完全独立外部验证。
- **已做**:摘要/正文把"four of five **external** cohorts"改为"four of five **retrospective transfer** cohorts";明确写只有 GSE30219/GSE37745/GSE68465 完全独立;Limitations 和 Future work 都点明。
- **未做(留给你)**:GPT 的方案 A(只用文献+TCGA 冻结选基因、所有 GEO 才算外部)需要**重新推导整个 9 基因集并重训**,这是更深的重跑,已在 Future work 写明为下一步。当前用诚实措辞守住,不再声称完全独立。

### 9. 自写 Cox 可重复性 / R survival 重算(GPT #2)◑
- **部分接受**。lifelines 在本环境编译失败,未能用成熟软件平行复算。
- **已做**:train/test 用固定 split 与随机种子(seed 20260610,70/30 分层)、报告 train/test 事件数、bootstrap CI。
- **未做**:R survival/scikit-survival 逐病例交叉核验、Schoenfeld 比例风险检验 —— 留给你在本地补(建议采纳)。

### 10. TCGA 样本溯源审计(GPT #3)◑
- **部分**:已报告 n=557 建模(train 388/test 169,事件 144/62)。
- **未做**:589→576→557 的逐步样本流程图、aliquot 去重、Primary Tumor 筛选说明 —— 需要你补一张 sample-flow 图(建议采纳)。

### 11. 全 SCENIC / IPCW timeROC / 前瞻验证 —— 环境或数据不允许 ✗
- 无 GPU / 无湿实验 / 无前瞻队列,已在文中如实标注为未完成边界(与上一轮一致)。

---

## 四、关于期刊定位

**接受 GPT 的判断**:上一轮报告说"可冲 J Hem Onc / Molecular Cancer 之下一档"过于乐观。以当前公共数据性质、无湿实验、以及"score 无增量判别"的诚实结论,**现实定位仍是 BMC Genomics 或同级组学/生信期刊**。完成第三节的深层修复(重训冻结模型、R survival、sample-flow)后,送审基础会更稳。

---

## 五、修改后的净变化

- 3 张图(Fig6/7/8)按修正分析重做;主稿、图例、Word 附图、BMC 分文件包全部同步。
- 关键数字更新:单细胞→样本级 FDR<0.05;空间→leave-out 5/5 患者;nomogram→ΔC +0.006(独立但无增量)。
- 残留过强表述检查 = 0。
- **本轮把"疑似夸大"的三处(单细胞 P 值、nomogram 0.75、空间 confirmed)全部改为经得起审的诚实版本**——这正是本文"透明证据层级"定位应有的样子。GPT 的审稿实质性提高了稿件质量。
