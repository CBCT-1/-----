#!/usr/bin/env python3
"""GEO-leakage-free frozen-feature model (GPT #1) + standard-software Cox cross-check (GPT #2).
Candidate pool = 12 genome-wide FDR<0.05 genes from TCGA ONLY (no GEO in selection).
Fit multivariable Cox on TCGA TRAIN, freeze, evaluate on all 5 GEO cohorts as truly external."""
import numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
from pathlib import Path
from scipy import optimize, special, stats
from sksurv.linear_model import CoxPHSurvivalAnalysis, CoxnetSurvivalAnalysis
from sksurv.util import Surv
from sksurv.metrics import concordance_index_censored
A=Path("/home/user/-----/luad-bioinformatics-project/v1.1_extracted/unpacked/data discoverer/03_bioinformatics_data")
OUT=Path("processed")
ENS2SYM={"ENSG00000035499":"DEPDC1B","ENSG00000107984":"DKK1","ENSG00000133466":"C1QTNF6","ENSG00000137812":"KNL1",
"ENSG00000162975":"KCNF1","ENSG00000166851":"PLK1","ENSG00000185133":"INPP5J","ENSG00000197930":"ERO1A",
"ENSG00000164647":"STEAP1","ENSG00000152642":"GPD1L","ENSG00000176842":"IRX5","ENSG00000167900":"TK1"}
GENES=list(ENS2SYM.values())

# ---- TCGA ----
tpm=pd.read_csv("tcga_candidate_tpm.tsv",sep="\t",index_col=0)
tpm.index=[str(i).split(".")[0] for i in tpm.index]; tpm=tpm.rename(index=ENS2SYM)
X_tcga=tpm.loc[GENES].T  # samples x genes (log2 TPM)
surv=pd.read_csv(A/"processed/TCGA-LUAD_consensus_axis_model_predictions.csv",encoding="utf-8-sig")[["sample_id","OS","OS_time_days","split"]]
df=surv.merge(X_tcga,left_on="sample_id",right_index=True).dropna()
df=df[df["OS_time_days"]>0]
tr=df[df.split=="train"].copy(); te=df[df.split=="test"].copy()
mu=tr[GENES].mean(); sd=tr[GENES].std(ddof=0)                # FREEZE train z-scaling
Ztr=(tr[GENES]-mu)/sd; Zte=(te[GENES]-mu)/sd
ytr=Surv.from_arrays(tr["OS"].astype(bool),tr["OS_time_days"]); yte=Surv.from_arrays(te["OS"].astype(bool),te["OS_time_days"])

# primary: standard multivariable Cox (sksurv) on 12 FDR genes
cox=CoxPHSurvivalAnalysis(alpha=1e-4).fit(Ztr,ytr)
coef=pd.Series(cox.coef_,index=GENES)
# LASSO sensitivity
try:
    net=CoxnetSurvivalAnalysis(l1_ratio=1.0,alpha_min_ratio=0.01,max_iter=100000).fit(Ztr.values,ytr)
    a_mid=net.alphas_[len(net.alphas_)//2]; net2=CoxnetSurvivalAnalysis(l1_ratio=1.0,alphas=[a_mid],fit_baseline_model=False).fit(Ztr.values,ytr)
    lasso_nz=[g for g,c in zip(GENES,net2.coef_.ravel()) if abs(c)>1e-6]
except Exception as e:
    lasso_nz=["(coxnet failed: %s)"%e]

def cidx_sksurv(y,risk): return concordance_index_censored(y["event"],y["time"],risk)[0]
# hand-coded Cox C-index cross-check
def cidx_manual(t,e,r):
    t=np.asarray(t);e=np.asarray(e);r=np.asarray(r);c=p=0.0
    for i in range(len(t)):
        if e[i]!=1:continue
        m=t>t[i]; p+=m.sum(); c+=(r[i]>r[m]).sum()+0.5*(r[i]==r[m]).sum()
    return c/p if p else np.nan
risk_tr=cox.predict(Ztr); risk_te=cox.predict(Zte)
xcheck=pd.DataFrame({"split":["train","test"],
   "sksurv_cindex":[cidx_sksurv(ytr,risk_tr),cidx_sksurv(yte,risk_te)],
   "manual_cindex":[cidx_manual(tr.OS_time_days,tr.OS,risk_tr),cidx_manual(te.OS_time_days,te.OS,risk_te)]})

# ---- score a GEO cohort with frozen model ----
def score_geo(expr_path, surv_df, gene_ids_present):
    ex=pd.read_csv(expr_path,sep="\t",index_col=0); ex.index=[str(i).split(".")[0] for i in ex.index]
    sym=ex.rename(index={k:v for k,v in ENS2SYM.items()})
    avail=[g for g in GENES if g in sym.index]
    Z=((sym.loc[avail].T - sym.loc[avail].T.mean())/sym.loc[avail].T.std(ddof=0))  # within-cohort z
    score=(Z*coef[avail]).sum(axis=1)
    return score, avail

RB=A/"raw"
geo=[("GSE31210",RB/"refinebio_GSE31210/extracted/GSE31210/GSE31210.tsv","processed/GEO_consensus_axis_external_predictions.csv","GSE31210_eligible","OS_time_days","OS_event",1),
     ("GSE50081",RB/"refinebio_GSE50081/extracted/GSE50081/GSE50081.tsv","processed/GEO_consensus_axis_external_predictions.csv","GSE50081_adenocarcinoma_like","OS_time_years","OS_event",365.25),
     ("GSE30219",RB/"refinebio_GSE30219/extracted/GSE30219/GSE30219.tsv","processed/GSE30219_GSE37745_unused_full_consensus_axis_scores.csv","GSE30219_ADC","OS_time_years","OS_event",365.25),
     ("GSE37745",RB/"refinebio_GSE37745/extracted/GSE37745/GSE37745.tsv","processed/GSE30219_GSE37745_unused_full_consensus_axis_scores.csv","GSE37745_adeno","OS_time_years","OS_event",365.25),
     ("GSE68465",RB/"refinebio_GSE68465/extracted/GSE68465/GSE68465.tsv","processed/GSE68465_partial_consensus_axis_scores.csv",None,"OS_time_months","OS_event",30.4375)]
rows=[]
for name,exprp,survp,coh,tcol,ecol,mult in geo:
    sdf=pd.read_csv(A/survp,encoding="utf-8-sig")
    if coh and "cohort" in sdf: sdf=sdf[sdf["cohort"]==coh]
    if name=="GSE31210": sdf=sdf[sdf.get("eligible_for_prognosis",True)==True]
    sdf=sdf[["sample_id",tcol,ecol]].dropna(); sdf["time"]=pd.to_numeric(sdf[tcol],errors="coerce")*mult; sdf["event"]=pd.to_numeric(sdf[ecol],errors="coerce")
    sdf=sdf.dropna(subset=["time","event"]); sdf=sdf[sdf.time>0]
    score,avail=score_geo(exprp,sdf,GENES)
    m=sdf.merge(score.rename("score"),left_on="sample_id",right_index=True).dropna(subset=["score"])
    if len(m)<20: rows.append({"cohort":name,"n":len(m),"note":"too small/unmatched"}); continue
    zc=(m["score"]-m["score"].mean())/m["score"].std(ddof=0)
    c=cidx_manual(m.time,m.event,zc.values)
    # univariable Cox HR (sksurv)
    y=Surv.from_arrays(m.event.astype(bool),m.time)
    b=CoxPHSurvivalAnalysis(alpha=1e-4).fit(zc.values.reshape(-1,1),y)
    hr=float(np.exp(b.coef_[0]))
    # p via wald from partial-lik curvature (approx) -> use score test through logrank on median split
    grp=(zc>=zc.median()).astype(int)
    from math import isnan
    rows.append({"cohort":name,"n_genes_used":len(avail),"n":len(m),"events":int(m.event.sum()),"c_index":round(c,3),"HR_per_SD":round(hr,3),"fully_independent":name in("GSE30219","GSE37745","GSE68465")})
res=pd.DataFrame(rows)
# TCGA test
res_tcga=pd.DataFrame([{"cohort":"TCGA_test","n":len(te),"events":int(te.OS.sum()),"c_index":round(cidx_sksurv(yte,risk_te),3),"fully_independent":"internal"}])
allres=pd.concat([res_tcga,res],ignore_index=True)
allres.to_csv(OUT/"frozen_model_external_validation.csv",index=False)
coefout=pd.DataFrame({"gene":GENES,"frozen_coef":coef.values}); coefout.to_csv(OUT/"frozen_model_coefficients.csv",index=False)
xcheck.to_csv(OUT/"cox_implementation_crosscheck.csv",index=False)

print("=== FROZEN MODEL: 12 TCGA-FDR genes, fit on TCGA train only (no GEO in selection) ===")
print("frozen coefficients (standard sksurv Cox):"); print(coef.round(3).to_string())
print("\nLASSO sensitivity kept:",lasso_nz)
print("\n=== Cox implementation cross-check (my hand-code vs sksurv) ===")
print(xcheck.round(4).to_string(index=False))
print("\n=== External validation of the LEAK-FREE model ===")
print(allres.to_string(index=False))
ind=res[res.fully_independent==True]
print(f"\nfully-independent cohorts (never in selection): {(ind.c_index>0.55).sum()}/{len(ind)} with C>0.55")
print("FROZEN_MODEL_DONE")
