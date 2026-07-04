# Zenodo/Figshare 上传清单(Task 1)

## 上传步骤
1. 新建 Zenodo(或 Figshare/OSF)记录 → 选 "Dataset" 或 "Software"。
2. 打包上传:
   - `code/`：项目 `scripts/` 全部脚本 + 本包 `make_figures.py`、`build_figures_docx.py`
   - `source_data/`：项目 `06_..._packet/02_figures_tables/tables/all_project_tables/` 全部 CSV
   - `figures/`：本包 `figures/` 下 PDF+PNG
   - `manuscript/`：`manuscript_bmc_genomics_final.docx/.md` + 图例
3. 填 `metadata_zenodo.json` 里的作者/ORCID/licence,替换所有 `TODO_`。
4. 选 licence(code=MIT 模板,data=CC BY 4.0 模板;需你机构确认)。
5. Publish → 获得 **DOI**。
6. 回到主稿和 cover letter,把所有 `TODO_REPOSITORY_DOI_OR_ACCESSION` 替换成该 DOI;需要时生成 reviewer 私有链接。

## 只有你能决定
- 作者身份与顺序、ORCID
- code/data 的最终 licence
- 是否在投稿前公开(可先 restricted + reviewer link,接收后转 open)
