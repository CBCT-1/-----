#!/usr/bin/env python3
"""Single-cell cell-type-specific expression of the programme genes from GSE131907 RAW UMI.
Uses grep-extracted keep_rows.tsv (36 genes x 208k cells) + colsum library size + Kim annotation."""
import numpy as np, pandas as pd
from pathlib import Path
from scipy import stats
D=Path("/home/user/-----/luad-bioinformatics-project/analysis_upgrade/data/GSE131907")
OUT=Path("/home/user/-----/luad-bioinformatics-project/analysis_upgrade/processed"); OUT.mkdir(parents=True,exist_ok=True)
PROG=["PLK1","ERO1A","KNL1","DEPDC1B","TK1","DKK1","C1QTNF6","STEAP1","ECT2"]
ALIAS={"CASC5":"KNL1"}

keep=pd.read_csv(D/"keep_rows.tsv",sep="\t",index_col=0)          # genes x cells (raw UMI)
keep.index=[ALIAS.get(g,g) for g in keep.index]
cells=keep.columns.to_numpy()
lib=pd.read_csv(D/"colsum.tsv",sep="\t",header=None,index_col=0).iloc[:,0]  # per-cell total UMI
lib=lib.reindex(cells).to_numpy().astype(float); lib[lib<=0]=1
# CP10K + log1p
norm=np.log1p(keep.to_numpy()/lib*1e4)                            # genes x cells
X=pd.DataFrame(norm.T,index=cells,columns=keep.index)             # cells x genes
ann=pd.read_csv(D/"cell_annotation.txt.gz",sep="\t").set_index("Index")
common=X.index.intersection(ann.index); X=X.loc[common]; a=ann.loc[common]
X["cell_type"]=a["Cell_type.refined"].values; X["origin"]=a["Sample_Origin"].values; X["subtype"]=a["Cell_subtype"].values
genes=[g for g in keep.index]
# per cell type dotplot data
rows=[]
for ct,sub in X.groupby("cell_type"):
    for g in genes:
        v=sub[g].to_numpy(); rows.append({"cell_type":ct,"gene":g,"n_cells":len(v),
            "mean_expr":float(v.mean()),"pct_expressing":float((v>0).mean()*100)})
pd.DataFrame(rows).to_csv(OUT/"sc_celltype_expression.csv",index=False)
# malignant (tumour-origin epithelial) vs normal-lung epithelial
epi=X[X["cell_type"].astype(str).str.contains("Epithelial",case=False,na=False)].copy()
so=epi["origin"].astype(str)
epi["grp"]=np.where(so.str.startswith("t")|so.str.contains("Brain|PE|mLN",case=False,na=False),"malignant_epi","normal_epi")
mr=[]
for g in PROG:
    t=epi.loc[epi.grp=="malignant_epi",g].to_numpy(); n=epi.loc[epi.grp=="normal_epi",g].to_numpy()
    if len(t)>5 and len(n)>5:
        U,p=stats.mannwhitneyu(t,n,alternative="two-sided")
        mr.append({"gene":g,"malignant_mean":float(t.mean()),"normal_mean":float(n.mean()),
                   "log2fc":float(np.log2((t.mean()+1e-6)/(n.mean()+1e-6))),"diff":float(t.mean()-n.mean()),
                   "n_malignant":len(t),"n_normal":len(n),"mannwhitney_p":float(p)})
pd.DataFrame(mr).to_csv(OUT/"sc_malignant_vs_normal_epi.csv",index=False)
# summary
print("cell types:",X["cell_type"].value_counts().to_dict())
print("epi groups:",epi["grp"].value_counts().to_dict())
print(pd.DataFrame(mr)[["gene","malignant_mean","normal_mean","diff","mannwhitney_p"]].to_string())
# which cell type has highest programme expression (dominant compartment per gene)
dp=pd.DataFrame(rows)
for g in PROG:
    top=dp[dp.gene==g].sort_values("mean_expr",ascending=False).head(1)
    print(f"{g}: top cell type = {top['cell_type'].values[0]} (mean {top['mean_expr'].values[0]:.2f}, {top['pct_expressing'].values[0]:.0f}% expr)")
print("SC_ANALYZE_DONE")
