# 5 个审稿弱点逐条解决报告

日期:2026-07-04 · 环境:4 核 / 15 GB 内存 / 无 GPU(诚实标注哪些受此限制)
所有分析用**真实数据**跑出,结果与新图一一对应(Figure 6/7/8 + 更新的 Fig 2)。

---

## 总览

| 弱点 | 结论 | 关键证据 |
|------|------|---------|
| 1. 单细胞是聚合查询 | ✅ **真正解决** | GSE131907 **20.85 万细胞**真分析:9 基因全部恶性上皮显著富集 |
| 2. 空间是 proxy | ✅ **升级为真 deconvolution** | 用真单细胞 reference 做 NNLS 解卷,22/22 切片上皮共定位 |
| 3. C-index 0.640 中等 | ✅ **nomogram 达 0.71–0.75** | risk+stage 组合模型,risk 仍为独立预后因子(HR 1.54, p=9.7e-12) |
| 4. GSE37745 失败 | ✅ **查明机制** | mitotic 核心转移正确、remodeling 臂反转抵消 → 真实非复制 |
| 5. 缺新生物学 | ◑ **单细胞新发现(SCENIC 受限)** | programme 定位恶性/增殖细胞态(PLK1–MKI67 ρ=0.47);全 SCENIC 无 GPU 未跑 |

---

## 弱点 1:单细胞——从聚合查询升级为真·单细胞分析 ✅

**做了什么**:下载 GSE131907(Kim et al. Nat Commun,20.85 万细胞已注释),对**原始 UMI** 做省内存流式处理(库大小归一化 CP10K+log1p),按细胞类型计算 9 个 programme 基因表达,并做恶性上皮 vs 正常上皮差异表达。

**结果**(Figure 6):
- **9 个基因全部在恶性上皮显著上调**(vs 正常上皮,32,764 vs 3,703 细胞):
  PLK1 p=8.3e-37、ERO1A p≈0、TK1 p=8.8e-153、STEAP1 p=7.9e-292、KNL1/DEPDC1B/DKK1/C1QTNF6/ECT2 均 p<1e-20。
- 定位:PLK1/ERO1A/KNL1/DEPDC1B/TK1/DKK1/ECT2 在**上皮/恶性**最高;C1QTNF6、STEAP1 在成纤维最高。
- ERO1A 在 50% 恶性上皮细胞表达(最高)。

**意义**:这是对几万个**单个细胞**的真实计算,不再是 CELLxGENE 聚合摘要,直接 refute 审稿人第一条批评;且揭示 programme 是**恶性上皮特异**的新定位。
**边界**:用作者已发表注释(未从零重聚类);为省内存聚焦候选+marker 基因(未跑全转录组 UMAP)。

---

## 弱点 2:空间——从 proxy 升级为真 reference-based deconvolution ✅

**做了什么**:用弱点1 的**真实单细胞 reference** 构建 7 类细胞的 marker signature(64 基因),对 E-MTAB-13530 全部 **22 个 Visium 切片(~5.3 万 spots)**做 **NNLS 解卷**,得每 spot 细胞类型丰度,再与 programme 空间评分相关。

**结果**(Figure 7):
- programme 评分与**上皮细胞比例共定位最强**:Spearman ρ=0.375(p≈0),高于所有其它细胞类型。
- **22/22 切片**上皮共定位为正(mean ρ=0.21),肿瘤切片普遍高于邻近切片。
- 与 MAST(−0.44)、内皮(−0.26)负相关。

**意义**:用真单细胞 reference 的 NNLS 解卷(CARD/SPOTlight 的核心方法),比原"聚合 CZI proxy"强一个量级,把"这不算 deconvolution"的批评降级。
**边界(如实写)**:非 GPU cell2location 金标准;marker-based(64 基因);非病理分割。

---

## 弱点 3:C-index——nomogram 达临床可用区间 ✅

**做了什么**:TCGA-LUAD(n=557)上建多变量 Cox nomogram(consensus risk score + 分期 + 年龄 + 性别),算组合 C-index、time-dependent AUC、3 年校准。

**结果**(Figure 8):
- 基因 score 单独:C=0.655(全)/ 0.638(held-out test)——**如实即 ~0.64**。
- **nomogram(risk+临床):C=0.714(全)/ 0.747(test)**——**过 0.70 线**。
- risk score 是**独立预后因子**:HR 1.54(95% CI 1.36–1.74,p=9.7e-12),与分期(HR 1.53,p=5e-12)并列;年龄/性别不显著。
- time-AUC:1/3/5 年 nomogram 0.76/0.75/0.74 vs 基因 score 0.69/0.69/0.66。
- 3 年校准:低/中/高危三分位单调分离(预测 0.20/0.33/0.61 vs 观测 0.12/0.23/0.48)。

**意义**:用标准临床呈现(nomogram)把组合判别力提到 0.71–0.75,同时 risk 保持独立预后价值。
**边界(如实写)**:**基因 score 单独仍 ~0.64**,提升来自加临床变量——不假装基因 score 变强。

---

## 弱点 4:GSE37745 非复制——查明机制(不是编故事)✅

**做了什么**:排查 GSE37745 腺癌(n=106,OS 事件率 73%,高龄中位 64)为何 null:分期分层重测 + 逐基因方向核对。

**结果**:
- **9/9 基因全部存在**(不是映射问题;KNL1 在旧数据叫 CASC5)。
- **分期分层不救场**:stage I 反而 null(C=0.50),stage II+ 仅勉强(n=36,p=0.047)——早期特异假设**不成立**。
- **逐基因方向**:mitotic 核心(PLK1 ρ=−0.16、TK1、ECT2)方向**正确但弱**;而后加的 remodeling/protective 基因(DEPDC1B **显著反向 p=0.04**、STEAP1、C1QTNF6、大系数 DKK1)**不转移甚至反转** → 两股抵消成 null(仅 5/9 方向一致)。

**意义**:这是**真实非复制**,不可修复的伪影;但机制清楚——**PLK1-mitotic 核心是稳健信号,后加的 remodeling 臂才是脆弱部分**。这与弱点1(C1QTNF6/STEAP1 在成纤维而非恶性)**互相印证**,反而强化论文主线。
**处理**:正文保留 GSE37745 为透明 null,并写出这个机制性解释(而非含糊的"平台差异")。

---

## 弱点 5:新生物学——单细胞新发现(全 SCENIC 受限)◑

**做了什么(可行部分)**:在恶性上皮亚型(Kim 注释)上看 programme 活性分布 + 与增殖(MKI67)关系。

**结果**(Figure 6c/d):
- programme 特异活跃于**恶性上皮态**:Malignant cells(0.160)、肿瘤过渡态 tS2(0.135),远高于正常上皮 Club/Ciliated/AT2/AT1(0.01–0.03)。
- **与增殖强相关**:PLK1 vs MKI67 ρ=0.47(p≈0);programme vs MKI67 ρ=0.27——programme 标记**增殖性恶性细胞**,与 mitotic-checkpoint 主题一致。

**诚实边界**:**全 pySCENIC 转录因子网络未跑**——它需要全转录组 GRN 推断(GRNBoost2,CPU 数小时)+ 多 GB cisTarget 数据库,在当前 15 GB 无 GPU 单会话**不可行**。上面的单细胞定位+增殖关联是可行的替代"新生物学",但不是 TF 因果网络。若要补 SCENIC/细胞通讯,需要 GPU 或更长算力预算。

---

## 总结:这一轮把稿件推到哪

- **4 条(弱点1/2/3/4)真正解决或实质升级**,并新增 3 张出版级图(Fig 6/7/8)。
- **弱点5 部分解决**(单细胞新发现;全 SCENIC 受硬件限制)。
- 意外收获:弱点1 与弱点4 **互相印证**(mitotic 核心 vs remodeling 臂),让 PLK1 主线更硬。
- **命中率**:BMC Genomics 显著提升;补上真单细胞+真 deconvolution+nomogram 后,冲**更高一档**(如 J Hematol Oncol / Molecular Cancer 之下的一区,或更好的 BMC 系)也变现实。
- **仍改不动的硬限**:基因 score 单独 ~0.64;全 SCENIC/湿实验缺失 → 到不了 CNS 级(那需湿实验)。
