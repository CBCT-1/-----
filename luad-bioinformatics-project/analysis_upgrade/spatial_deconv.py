#!/usr/bin/env python3
"""Weakness 2: reference-based marker deconvolution of E-MTAB-13530 Visium using a REAL
GSE131907 single-cell reference (replaces the aggregated-CZI proxy). NNLS per spot."""
import numpy as np, pandas as pd, glob, warnings, re
warnings.filterwarnings("ignore")
from pathlib import Path
from scipy.optimize import nnls
from scipy import stats
import scanpy as sc
D=Path("/home/user/-----/luad-bioinformatics-project/analysis_upgrade/data/GSE131907")
SP=Path("/home/user/-----/luad-bioinformatics-project/v1.1_extracted/unpacked/data discoverer/03_bioinformatics_data/raw/E-MTAB-13530")
OUT=Path("/home/user/-----/luad-bioinformatics-project/analysis_upgrade/processed"); OUT.mkdir(parents=True,exist_ok=True)
ALIAS={"CASC5":"KNL1"}; PROG=["PLK1","ERO1A","KNL1","DEPDC1B","TK1","DKK1","C1QTNF6","STEAP1","ECT2"]

# ---- build single-cell cell-type signature from marker rows ----
mk=pd.read_csv(D/"markers_rows.tsv",sep="\t",index_col=0); mk.index=[ALIAS.get(g,g) for g in mk.index]
cells=mk.columns.to_numpy()
lib=pd.read_csv(D/"colsum.tsv",sep="\t",header=None,index_col=0).iloc[:,0].reindex(cells).to_numpy().astype(float); lib[lib<=0]=1
norm=np.log1p(mk.to_numpy()/lib*1e4)                       # genes x cells
X=pd.DataFrame(norm.T,index=cells,columns=mk.index)
ann=pd.read_csv(D/"cell_annotation.txt.gz",sep="\t").set_index("Index")
common=X.index.intersection(ann.index); X=X.loc[common]; ct=ann.loc[common,"Cell_type.refined"].values
X["ct"]=ct
sig=X.groupby("ct").mean().T                               # genes x cell_types  (signature)
sig=sig[[c for c in sig.columns]]
sig_genes=sig.index.tolist()
print("signature:",sig.shape,"cell types:",list(sig.columns))
sig.to_csv(OUT/"sc_celltype_signature.csv")

# ---- deconvolve each Visium section ----
S=sig.to_numpy()   # genes x K
K=S.shape[1]; ctypes=list(sig.columns)
files=sorted(glob.glob(str(SP/"*filtered_feature_bc_matrix.h5")))
all_spot=[]
for f in files:
    name=Path(f).stem.replace("-filtered_feature_bc_matrix","")
    is_tumor = ("_T" in name)
    a=sc.read_10x_h5(f); a.var_names_make_unique()
    sc.pp.normalize_total(a,target_sum=1e4); sc.pp.log1p(a)
    present=[g for g in sig_genes if g in a.var_names]
    sub=a[:,present].X
    sub=np.asarray(sub.todense()) if hasattr(sub,"todense") else np.asarray(sub)
    Ssub=sig.loc[present].to_numpy()
    props=np.zeros((sub.shape[0],K))
    for i in range(sub.shape[0]):
        w,_=nnls(Ssub,sub[i]); s=w.sum(); props[i]=w/s if s>0 else w
    pr=pd.DataFrame(props,columns=ctypes)
    # programme score per spot = mean log1p CP10K of programme genes present
    pg=[g for g in PROG if g in a.var_names]
    pv=a[:,pg].X; pv=np.asarray(pv.todense()) if hasattr(pv,"todense") else np.asarray(pv)
    pr["programme_score"]=pv.mean(axis=1)
    pr["section"]=name; pr["is_tumor"]=is_tumor
    all_spot.append(pr)
    print(f"  {name}: {sub.shape[0]} spots, {len(present)}/{len(sig_genes)} sig genes")
spots=pd.concat(all_spot,ignore_index=True)
spots.to_csv(OUT/"spatial_deconv_spots.csv.gz",index=False,compression="gzip")

# ---- correlate programme score with cell-type proportions (co-localisation) ----
epi_col=[c for c in ctypes if "Epithel" in c][0]
rows=[]
for ctp in ctypes:
    rho,p=stats.spearmanr(spots["programme_score"],spots[ctp])
    rows.append({"cell_type":ctp,"spearman_rho":float(rho),"p_value":float(p)})
corr=pd.DataFrame(rows).sort_values("spearman_rho",ascending=False)
corr.to_csv(OUT/"spatial_deconv_programme_colocalisation.csv",index=False)
# per-section consistency for epithelial (malignant proxy)
sec=[]
for s,sub in spots.groupby("section"):
    rho,p=stats.spearmanr(sub["programme_score"],sub[epi_col])
    sec.append({"section":s,"is_tumor":sub["is_tumor"].iloc[0],"rho_programme_vs_epithelial":float(rho),"n_spots":len(sub)})
secdf=pd.DataFrame(sec); secdf.to_csv(OUT/"spatial_deconv_section_consistency.csv",index=False)
print("\n=== programme score vs cell-type proportion (all spots) ===")
print(corr.to_string(index=False))
print(f"\nepithelial co-localisation positive in {int((secdf.rho_programme_vs_epithelial>0).sum())}/{len(secdf)} sections")
print("mean epithelial rho:",round(secdf.rho_programme_vs_epithelial.mean(),3))
print("SPATIAL_DECONV_DONE")
