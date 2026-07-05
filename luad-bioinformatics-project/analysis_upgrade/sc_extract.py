#!/usr/bin/env python3
"""Memory-light single pass over GSE131907 raw UMI (genes x cells dense TSV):
accumulate per-cell library size + extract programme/marker gene rows,
then compute cell-type-specific CP10K-log1p expression using Kim et al. annotation."""
import numpy as np, pandas as pd
from pathlib import Path
from scipy import stats
D=Path("/home/user/-----/luad-bioinformatics-project/analysis_upgrade/data/GSE131907")
OUT=Path("/home/user/-----/luad-bioinformatics-project/analysis_upgrade/processed"); OUT.mkdir(parents=True,exist_ok=True)

PROG=["PLK1","ERO1A","KNL1","DEPDC1B","TK1","DKK1","C1QTNF6","STEAP1","ECT2"]
MARK=["EPCAM","KRT19","KRT18","SFTPC","NAPSA","CD3D","CD3E","CD8A","CD4","NKG7","GNLY",
      "CD79A","MS4A1","MZB1","LYZ","CD68","CD14","FCGR3A","MARCO","COL1A1","DCN","PECAM1",
      "VWF","CLDN5","PTPRC","MKI67","TOP2A"]
KEEP=set(PROG+MARK)

ann=pd.read_csv(D/"cell_annotation.txt.gz",sep="\t").set_index("Index")
cells_order=None; colsum=None; kept={}
print("streaming raw UMI...",flush=True)
reader=pd.read_csv(D/"raw_UMI.txt.gz",sep="\t",chunksize=800,index_col=0)
nrows=0
for ci,chunk in enumerate(reader):
    if cells_order is None:
        cells_order=chunk.columns.to_numpy(); colsum=np.zeros(len(cells_order),dtype=np.float64)
    vals=chunk.to_numpy(dtype=np.float32); colsum+=vals.sum(axis=0)
    for g in chunk.index:
        if g in KEEP: kept[g]=chunk.loc[g].to_numpy(dtype=np.float32)
    nrows+=len(chunk)
    if ci%10==0: print(f"  {nrows} genes, found {len(kept)}/{len(KEEP)}",flush=True)
print(f"done: {nrows} genes x {len(cells_order)} cells; keep {len(kept)}",flush=True)

lib=colsum.copy(); lib[lib==0]=1
expr=pd.DataFrame({g:np.log1p(kept[g]/lib*1e4) for g in kept}, index=cells_order); expr.index.name="Index"
common=expr.index.intersection(ann.index); expr=expr.loc[common]; a=ann.loc[common]
expr["Cell_type"]=a["Cell_type.refined"].values; expr["Sample_Origin"]=a["Sample_Origin"].values; expr["Cell_subtype"]=a["Cell_subtype"].values
expr.to_parquet(OUT/"sc_keepgene_expr.parquet"); print("saved parquet",expr.shape,flush=True)

genes=[g for g in PROG+MARK if g in kept]; rows=[]
for ct,sub in expr.groupby("Cell_type"):
    for g in genes:
        v=sub[g].to_numpy()
        rows.append({"cell_type":ct,"gene":g,"n_cells":len(v),"mean_log1p_cp10k":float(v.mean()),"pct_expressing":float((v>0).mean()*100)})
pd.DataFrame(rows).to_csv(OUT/"sc_celltype_expression.csv",index=False); print("saved sc_celltype_expression.csv",flush=True)

epi=expr[expr["Cell_type"].astype(str).str.contains("Epithelial",case=False,na=False)].copy()
so=epi["Sample_Origin"].astype(str)
epi["grp"]=np.where(so.str.startswith("t")|so.str.contains("Brain|PE|mLN",case=False,na=False),"tumor_epi","normal_epi")
mrows=[]
for g in PROG:
    if g not in kept: continue
    t=epi.loc[epi["grp"]=="tumor_epi",g].to_numpy(); n=epi.loc[epi["grp"]=="normal_epi",g].to_numpy()
    if len(t)>5 and len(n)>5:
        U,p=stats.mannwhitneyu(t,n,alternative="two-sided")
        mrows.append({"gene":g,"tumor_epi_mean":float(t.mean()),"normal_epi_mean":float(n.mean()),"diff":float(t.mean()-n.mean()),"n_tumor":len(t),"n_normal":len(n),"mannwhitney_p":float(p)})
pd.DataFrame(mrows).to_csv(OUT/"sc_malignant_vs_normal_epi.csv",index=False); print("saved sc_malignant_vs_normal_epi.csv",flush=True)
print("celltypes:",expr["Cell_type"].value_counts().to_dict(),flush=True)
print("origins:",expr["Sample_Origin"].value_counts().to_dict(),flush=True)
print("SC_EXTRACT_DONE",flush=True)
