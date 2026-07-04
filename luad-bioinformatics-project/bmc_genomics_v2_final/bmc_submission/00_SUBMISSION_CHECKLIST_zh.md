# BMC Genomics 分文件投稿包 — 使用说明与清单

## 目录结构(按 BMC 在线投稿系统的文件类型分好)

- `01_manuscript/` — 主稿(`.docx` 用于上传;`.md` 为源）。含标题页、结构化摘要、Background/Methods/Results/Discussion/Conclusions/Declarations/References。
- `02_main_figures/` — 5 张主图,每张 PDF(矢量,首选上传)+ PNG(预览)。BMC 要求每图单独文件、按 Figure 1..5 命名。
- `03_additional_files/` — 补充材料:
  - `Additional_file_1_Figure_S1.pdf`(iLINCS 扰动)
  - `Additional_file_2_Figure_S2.pdf`(PLK1 治疗窗口边界)
  - `supplementary_tables/` — 14 张关键源数据表(consensus 模型、外部验证、ICB meta、空间 deconvolution、iLINCS、治疗窗口、统计多重性)。上传时可合并为一个 Additional file 3(zip 或 xlsx)。
- `04_cover_letter/` — cover letter(填作者信息后转 PDF/贴入系统)。

## 上传顺序(BMC 系统)
1. Cover letter
2. Manuscript(`.docx`)
3. Figures 1–5(逐个 PDF)
4. Additional files 1–3

## 投稿前必须由作者关闭(我无法代填)
- [ ] 主稿与 cover letter 中所有 `TODO_AUTHOR_METADATA`(作者/单位/ORCID/通讯/CRediT/funding/COI/ethics 措辞)
- [ ] 用真实仓库 DOI 替换所有 `TODO_REPOSITORY_DOI_OR_ACCESSION`(见 `../zenodo_deposit/`)
- [ ] 机构核验 BMC Genomics(ISSN 1471-2164)当前 JCR/中科院分区
- [ ] 逐句 citation-context 核查 + 查重(iThenticate/Turnitin)
- [ ] 复核摘要外的 fixed-effect HR 1.346(endpoint 独立性/异质性)
- [ ] 选定 code / data licence(模板见 zenodo_deposit）

## 图件说明
- 图用验证过的色盲友好色板生成,PLK1/ERO1A 全程高亮,负面/边界结果如实呈现(Fig 5、S1、S2)。
- 矢量 PDF 可直接编辑;如期刊要 TIFF/EPS,用 `figures/*.pdf` 转换即可(勿从 PNG 转,会失真)。
