# BMC Genomics 定稿说明 + 人工清单(v2 final)

日期:2026-07-04
适用:LUAD PLK1/ERO1A programme,BMC Genomics(Research article)投稿

---

## 一、这轮我做了什么(把散乱素材塌缩成一份可投稿)

你的投稿包里同时存在三份互相矛盾的草稿(v1.9 primary / v1.9 structured / v1.10 optimized)。
我以**质量最高的 v1.10 为基底**,合并成**唯一一份定稿** `manuscript_bmc_genomics_final.md`,并做了以下修正:

| # | 改动 | 原因 |
|---|------|------|
| 1 | 统一为**一个标题、一份结构化摘要**(Background/Results/Conclusions,<350 词) | v1.9/v1.10 标题与摘要不一致;BMC 要求结构化摘要 |
| 2 | **图件全篇统一为 5 主图 + 2 补充(Additional file 1/2)+ 1 补充表包** | 旧图例是 7 主图 + 2 "Extended Data",与正文矛盾,且 "Extended Data" 不是 BMC 术语 |
| 3 | **插入 in-text 引用编号 [1]–[20] 并附完整 Vancouver 参考文献表** | v1.10 正文完全没有引用,参考文献只是占位符 |
| 4 | **修掉过度精度 p 值**(如 `p=0.7298811809825891` → `p = 0.73`) | 审稿人会认为是机器直出、不专业 |
| 5 | **GSE37745 失败具名化**:正文+讨论明确写 C=0.529、HR=1.04、p=0.71 未复制,作为诚实外部边界 | 原稿只含糊说"null stress-test",藏着反而危险;主动披露更可信 |
| 6 | **统一 9 基因 vs 8 基因**:主用 9 基因 programme score,8 基因 TCGA-only locked 明确说明是防泄漏敏感性复算(丢 KNL1),两者迁移几乎一致且都在 GSE37745 为 null | 原素材两个 axis 定义并存、未解释,会让审稿人困惑 |
| 7 | **空间矛盾处理**:marker-basis 与 CZI-reference 在 epithelial compartment 符号相反,只报道跨方法稳健的 tumour-context 富集,compartment 级标注降级为 proxy | 两张表自相矛盾是审稿人会抓的内部一致性问题 |
| 8 | **扩充 Methods**:数据集版本/accession、各队列样本量与基因覆盖、软件栈(Python numpy/scipy/pandas/matplotlib/seaborn,手写 Cox/log-rank/C-index)、标准化、endpoint 定义、多重性(BH-FDR) | BMC 要求 Methods 含 design/materials/processes/statistics/software;原稿太薄 |
| 9 | **补全 Data Availability**:列出全部 11 类公开库 accession + 仓库 DOI 占位 | BMC 要求可持续标识符 |
| 10 | **删除所有自我编辑批注和内部术语**("lead story should…"、"WP3"、"Fig.33"、"Route C" 等) | 这些是过程痕迹,绝不能进投稿稿 |

**产出的三份文件:**
1. `manuscript_bmc_genomics_final.md` — 唯一定稿(正文 + 结构化摘要 + Methods + Declarations + 20 条参考文献)
2. `main_figure_legends_final_5main_2supp.md` — 与正文完全对齐的 5+2 图例
3. `REVISION_NOTES_and_HUMAN_CHECKLIST_zh.md` — 本文件

---

## 二、审稿人仍可能提的诚实弱点 + 建议答辩措辞

这篇稿件的定位是"透明的公共数据证据层级研究",不是临床 biomarker,也不是机制论文。以下弱点**不必假装解决**,而是用诚实措辞守住边界:

| 弱点 | 审稿人可能说 | 建议回应 |
|------|-------------|----------|
| 单细胞仍是聚合查询(非 raw scRNA-seq) | "为什么不做真正的单细胞?" | 明确本层定位为 aggregate localisation / tissue-context,不声称 malignant-cell specificity;raw 单细胞列为 future work。**不要**把 CELLxGENE 结果写成差异表达。 |
| C-index 0.640 中等 | "预测力不够临床用" | 全稿已把 score 定位为 public-data prioritisation tool,非 patient-level risk model;这是**设计选择**不是缺陷。 |
| GSE37745 失败 | "外部验证不稳" | 主动披露 + 解释:紧凑转录组 score 的跨平台迁移对 histology/platform 敏感,报告 null 比只挑支持性队列更严谨。 |
| 空间是 proxy 非 deconvolution | "不是真正的 deconvolution" | 已明确 marker-basis / CZI-NNLS 是 composition proxy,不是 reference-based deconvolution;只保留跨方法稳健信号。 |
| 校准是 apparent(样本内) | "没有真外部校准" | 已在正文标注 apparent calibration,并说明 IPCW timeROC / 外部绝对风险校准 / 前瞻验证是临床用语的前提。 |
| PLK1 泛必需、无治疗窗口 | "PLK1 不是 LUAD 特异靶点" | 这本来就是你**主动做出的 negative boundary**(Fig 5 + S2),是稿件严谨性的体现,不是漏洞。 |

---

## 三、只有你(作者)能完成的清单——投稿前必须逐项关闭

我无法代填以下任何一项(涉及真实身份、机构决策、外部账号):

### A. 作者与声明(填进 `manuscript_bmc_genomics_final.md` 里所有 `TODO_AUTHOR_METADATA`)
- [ ] 作者姓名、顺序、精确拼写
- [ ] 各作者单位/科室/机构地址
- [ ] 每位作者 ORCID
- [ ] 通讯作者 + 邮箱
- [ ] 是否有 equal-contribution 说明
- [ ] CRediT 作者贡献分工
- [ ] Funding(资助号/资助方角色;若无写 "no external funding")
- [ ] Competing interests(利益冲突;若无写 "none")
- [ ] Ethics approval 措辞(公开去标识数据的标准表述,按你单位政策定稿)
- [ ] AI 使用声明签字确认(草稿已备,需你确认属实)

### B. 仓库与标识符
- [ ] 把 Source Data + 代码打包上传到 **Zenodo / Figshare / OSF**,获取 **DOI**
- [ ] 用真实 DOI 替换全稿中的 `TODO_REPOSITORY_DOI_OR_ACCESSION`
- [ ] 生成 reviewer 私有访问链接(投稿系统/仓库支持时)
- [ ] 选定 **code licence**(如 MIT/BSD)与 **data licence**(如 CC BY 4.0)

### C. 期刊核验与查重
- [ ] 用你机构的 **JCR / 中科院分区** 权限,核实 BMC Genomics(ISSN 1471-2164)当前分区,确认符合你的 Q2 目标
- [ ] 完成 **NLM 期刊缩写** 最终核验(参考 `bmc_genomics_nlm_journal_abbreviation_review_queue_v1.9.csv`)
- [ ] 逐句 **citation-context** 人工核验(引用是否真的支持该句)
- [ ] 跑 **iThenticate / Turnitin** 查重

### D. 数字复核(强烈建议)
- [ ] 复核摘要/正文里未验证的 **fixed-effect HR 1.346**(endpoint 独立性 + 异质性假设)——目前已在稿中标注"待人工核验",若不核验就**从正文降级或删除**

---

## 四、Cover letter 骨架(投稿时用)

```
Dear Editor,

我们提交题为 "A literature-guided public-data evidence hierarchy prioritises a
PLK1-centred mitotic/redox programme in lung adenocarcinoma" 的 Research article,
供 BMC Genomics 考虑。

【1 段:问题】公共 LUAD 生信研究常把 discovery / validation / context / functional
混在一起,不区分推断强度,导致过度解读。

【2 段:我们做了什么】我们构建了一个文献引导的公共数据证据层级,把 TCGA 发现、5 个 GEO
队列的回顾性迁移、HPA/CELLxGENE/Visium 组织背景、DepMap/药物/iLINCS 功能层分层组织,
围绕一个 PLK1 为核心的 mitotic/redox programme,并明确标注每层能与不能支持的结论。

【3 段:主要发现 + 诚实边界】紧凑 9 基因 score 在 held-out TCGA(C=0.640)和 4/5 外部队列
显著迁移(GSE37745 为透明的 null 边界);功能层把 PLK1 提名为实验后续靶点,但主动排除了
LUAD 特异性、治疗窗口、药物响应和临床部署等未被数据支持的声称。

【4 段:契合度】本文是一个透明、可复现、以证据层级为核心的公共数据转录组研究,契合 BMC
Genomics 的范围;所有图件配有机读 source data,代码与数据已存入 [DOI]。

【5 段:声明】本研究仅用公开去标识数据;无利益冲突[或列出];AI 使用已在 Methods 声明;
未一稿多投。

建议审稿人:[3–5 位,姓名/单位/邮箱];回避:[如有]。

通讯作者敬上
```

---

## 五、这份稿件适合投哪里(现实判断)

- **首选**:BMC Genomics(你已定的稳妥 Q2 路线)——稿件当前状态**契合**,补完上面清单即可投。
- **同级备选**(若 BMC 拒或想换):Frontiers in Genetics、PeerJ、Scientific Reports、BMC Cancer。
- **暂不适合**:Molecular Cancer / JHO / Nature 子刊——除非补真单细胞+deconvolution(选项3)或湿实验(选项4)。

---

## 六、下一步

补完第三节的作者清单和仓库 DOI 后,这篇就可以投了。如果你愿意,我可以:
1. 帮你把 Source Data + 代码整理成一个干净的 Zenodo 上传包(含 README、licence 模板、DataCite metadata);
2. 或者根据你提供的作者信息,把 `TODO_AUTHOR_METADATA` 占位全部替换成终稿;
3. 或者把定稿转成 BMC 投稿系统需要的具体格式(分文件的 manuscript / figures / additional files)。
