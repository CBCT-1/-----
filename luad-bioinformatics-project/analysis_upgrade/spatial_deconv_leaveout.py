#!/usr/bin/env python3
"""Leave-programme-genes-out deconvolution (addresses circularity): rebuild the cell-type
signature WITHOUT the 9 programme genes, re-deconvolve, re-correlate programme score with epithelial abundance."""
import numpy as np, pandas as pd, glob, warnings, re
warnings.filterwarnings("ignore")
from pathlib import Path
from scipy.optimize import nnls
from scipy import stats
import scanpy as sc
D=Path("data/GSE131907")
SP=Path("/home/user/-----/luad-bioinformatics-project/v1.1_extracted/unpacked/data discoverer/03_bioinformatics_data/raw/E-MTAB-13530")
OUT=Path("processed")
ALIAS={"CASC5":"KNL1"}; PROG=set(["PLK1","ERO1A","KNL1","DEPDC1B","TK1","DKK1","C1QTNF6","STEAP1","ECT2"])
mk=pd.read_csv(D/"markers_rows.tsv",sep="\t",index_col=0); mk.index=[ALIAS.get(g,g) for g in mk.index]
mk=mk.loc[[g for g in mk.index if g not in PROG]]           # DROP programme genes from signature
cells=mk.columns.to_numpy()
lib=pd.read_csv(D/"colsum.tsv",sep="\t",header=None,index_col=0).iloc[:,0].reindex(cells).to_numpy().astype(float); lib[lib<=0]=1
norm=np.log1p(mk.to_numpy()/lib*1e4)
X=pd.DataFrame(norm.T,index=cells,columns=mk.index)
ann=pd.read_csv(D/"cell_annotation.txt.gz",sep="\t").set_index("Index")
common=X.index.intersection(ann.index); X=X.loc[common]; X["ct"]=ann.loc[common,"Cell_type.refined"].values
sig=X.groupby("ct").mean().T; sig_genes=sig.index.tolist(); ctypes=list(sig.columns)
print(f"leave-out signature: {sig.shape[0]} genes (programme genes removed), {len(ctypes)} cell types")
files=sorted(glob.glob(str(SP/"*filtered_feature_bc_matrix.h5")))
patients=sorted(set(Path(f).stem.split("_")[0] for f in files))
print(f"22 sections from {len(patients)} patients: {patients}")
sec=[]
for f in files:
    name=Path(f).stem.replace("-filtered_feature_bc_matrix",""); pat=name.split("_")[0]; is_tumor=("_T" in name)
    a=sc.read_10x_h5(f); a.var_names_make_unique(); sc.pp.normalize_total(a,target_sum=1e4); sc.pp.log1p(a)
    present=[g for g in sig_genes if g in a.var_names]
    sub=a[:,present].X; sub=np.asarray(sub.todense()) if hasattr(sub,"todense") else np.asarray(sub)
    Ssub=sig.loc[present].to_numpy(); props=np.zeros((sub.shape[0],len(ctypes)))
    for i in range(sub.shape[0]):
        w,_=nnls(Ssub,sub[i]); s=w.sum(); props[i]=w/s if s>0 else w
    pr=pd.DataFrame(props,columns=ctypes)
    pg=[g for g in PROG if g in a.var_names]; pv=a[:,pg].X; pv=np.asarray(pv.todense()) if hasattr(pv,"todense") else np.asarray(pv)
    prog=pv.mean(axis=1)
    epi_col=[c for c in ctypes if "Epithel" in c][0]
    rho,p=stats.spearmanr(prog,pr[epi_col])
    sec.append({"section":name,"patient":pat,"is_tumor":is_tumor,"rho_leaveout":float(rho),"n_spots":len(pr)})
secdf=pd.DataFrame(sec); secdf.to_csv(OUT/"spatial_deconv_leaveout_section.csv",index=False)
# patient-level aggregation (mean rho per patient)
patrho=secdf.groupby("patient")["rho_leaveout"].mean()
print("\n=== leave-programme-out: programme vs epithelial (per section) ===")
print(f"positive in {(secdf.rho_leaveout>0).sum()}/{len(secdf)} sections; median rho={secdf.rho_leaveout.median():.3f} (IQR {secdf.rho_leaveout.quantile(.25):.3f}-{secdf.rho_leaveout.quantile(.75):.3f})")
print(f"patient-level: positive in {(patrho>0).sum()}/{len(patrho)} patients; mean of patient means={patrho.mean():.3f}")
print("per-patient mean rho:",{k:round(v,3) for k,v in patrho.items()})
# Wilcoxon signed-rank on patient means vs 0
w,pw=stats.wilcoxon(patrho.to_numpy())
print(f"patient-level Wilcoxon vs 0: p={pw:.4f}")
print("SPATIAL_LEAVEOUT_DONE")
