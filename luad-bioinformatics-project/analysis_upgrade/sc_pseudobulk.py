#!/usr/bin/env python3
"""Patient/sample-level pseudobulk single-cell DE (addresses cell-level pseudoreplication).
Aggregate each sample's epithelial cells, compare tumour-origin vs normal-lung samples at SAMPLE level."""
import numpy as np, pandas as pd
from pathlib import Path
from scipy import stats
D=Path("data/GSE131907"); OUT=Path("processed")
ALIAS={"CASC5":"KNL1"}; PROG=["PLK1","ERO1A","KNL1","DEPDC1B","TK1","DKK1","C1QTNF6","STEAP1","ECT2"]
keep=pd.read_csv(D/"keep_rows.tsv",sep="\t",index_col=0); keep.index=[ALIAS.get(g,g) for g in keep.index]
cells=keep.columns.to_numpy()
lib=pd.read_csv(D/"colsum.tsv",sep="\t",header=None,index_col=0).iloc[:,0].reindex(cells).to_numpy().astype(float); lib[lib<=0]=1
norm=np.log1p(keep.loc[PROG].to_numpy()/lib*1e4)
X=pd.DataFrame(norm.T,index=cells,columns=PROG)
ann=pd.read_csv(D/"cell_annotation.txt.gz",sep="\t").set_index("Index")
common=X.index.intersection(ann.index); X=X.loc[common]; a=ann.loc[common]
X["ct"]=a["Cell_type.refined"].values; X["subtype"]=a["Cell_subtype"].values; X["sample"]=a["Sample"].values; X["origin"]=a["Sample_Origin"].values
epi=X[X["ct"].astype(str).str.contains("Epithel",na=False)].copy()
# sample-level pseudobulk: mean per programme gene within each sample's epithelial cells
pb=epi.groupby(["sample","origin"])[PROG].mean().reset_index()
pb["n_epi_cells"]=epi.groupby(["sample","origin"]).size().values
pb["group"]=np.where(pb["origin"].astype(str).str.startswith("t")|pb["origin"].astype(str).str.contains("Brain|PE|mLN",case=False,na=False),"tumour_origin","normal_lung")
pb=pb[pb["n_epi_cells"]>=20]   # require >=20 epithelial cells per sample for a stable pseudobulk
pb.to_csv(OUT/"sc_pseudobulk_sample_means.csv",index=False)
nt=(pb.group=="tumour_origin").sum(); nn=(pb.group=="normal_lung").sum()
print(f"pseudobulk samples: tumour-origin={nt}, normal-lung={nn}")
rows=[]
from statistics import median
pvals=[]
for g in PROG:
    t=pb.loc[pb.group=="tumour_origin",g].to_numpy(); n=pb.loc[pb.group=="normal_lung",g].to_numpy()
    U,p=stats.mannwhitneyu(t,n,alternative="two-sided")
    rows.append({"gene":g,"tumour_sample_mean":float(np.mean(t)),"normal_sample_mean":float(np.mean(n)),
                 "sample_level_diff":float(np.mean(t)-np.mean(n)),"n_tumour_samples":int(nt),"n_normal_samples":int(nn),
                 "mannwhitney_p_sample_level":float(p)})
    pvals.append(p)
# BH FDR
order=np.argsort(pvals); rk=np.empty(len(pvals)); rk[order]=np.arange(1,len(pvals)+1)
fdr=np.minimum(1,np.array(pvals)*len(pvals)/rk)
for r,f in zip(rows,fdr): r["fdr_sample_level"]=float(f)
res=pd.DataFrame(rows); res.to_csv(OUT/"sc_malignant_vs_normal_pseudobulk.csv",index=False)
print(res[["gene","tumour_sample_mean","normal_sample_mean","sample_level_diff","mannwhitney_p_sample_level","fdr_sample_level"]].round(4).to_string(index=False))
sig=(res.fdr_sample_level<0.05).sum()
print(f"\nsample-level FDR<0.05: {sig}/9 genes (vs cell-level pseudoreplicated P<1e-20)")
print("SC_PSEUDOBULK_DONE")
