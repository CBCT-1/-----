#!/usr/bin/env python3
"""Proper incremental prognostic assessment (addresses GPT: clinical-only model, train-fit/test-eval, CIs, LR test).
Fit clinical-only / gene-only / combined on TCGA TRAIN; evaluate on held-out TEST with bootstrap CIs."""
import numpy as np, pandas as pd
from pathlib import Path
from scipy import optimize, special, stats
P=Path("/home/user/-----/luad-bioinformatics-project/v1.1_extracted/unpacked/data discoverer/03_bioinformatics_data/processed")
OUT=Path("processed")
pred=pd.read_csv(P/"TCGA-LUAD_consensus_axis_model_predictions.csv",encoding="utf-8-sig")  # risk_score,OS,OS_time_days,split
clin=pd.read_csv(P/"TCGA-LUAD_clinical_mutation_context.csv",encoding="utf-8-sig")[["sample_id","age_at_index","gender","ajcc_pathologic_stage"]]
df=pred.merge(clin,on="sample_id",how="inner").dropna(subset=["OS","OS_time_days","risk_score"])
df=df[df["OS_time_days"]>0].copy()
smap={"Stage I":1,"Stage IA":1,"Stage IB":1,"Stage II":2,"Stage IIA":2,"Stage IIB":2,"Stage IIIA":3,"Stage IIIB":3,"Stage IV":4}
df["stage_ord"]=df["ajcc_pathologic_stage"].map(smap); df["age"]=pd.to_numeric(df["age_at_index"],errors="coerce")
df["male"]=(df["gender"].astype(str).str.lower()=="male").astype(float)
df=df.dropna(subset=["stage_ord","age"])
tr=df[df.split=="train"].copy(); te=df[df.split=="test"].copy()
# standardise using TRAIN mean/sd (freeze)
for c,src in [("risk_z","risk_score"),("age_z","age"),("stage_z","stage_ord")]:
    m,s=tr[src].mean(),tr[src].std(ddof=0); tr[c]=(tr[src]-m)/s; te[c]=(te[src]-m)/s

def coxfit(X,t,e):
    X=np.asarray(X,float)
    def f(b):
        eta=X@b; nll=0.0; g=np.zeros(X.shape[1])
        for i in np.where(e==1)[0]:
            rm=t>=t[i]; le=special.logsumexp(eta[rm]); w=np.exp(eta[rm]-le); nll-=eta[i]-le; g-=X[i]-w@X[rm]
        return nll,g
    r=optimize.minimize(f,np.zeros(X.shape[1]),jac=True,method="L-BFGS-B")
    return r.x, -f(r.x)[0]   # coef, loglik
def cidx(t,e,r):
    t=np.asarray(t);e=np.asarray(e);r=np.asarray(r);c=p=0.0
    for i in range(len(t)):
        if e[i]!=1:continue
        m=t>t[i]; p+=m.sum(); c+=(r[i]>r[m]).sum()+0.5*(r[i]==r[m]).sum()
    return c/p if p else np.nan

models={"clinical_only":["stage_z","age_z","male"],"gene_only":["risk_z"],"combined":["risk_z","stage_z","age_z","male"]}
tt,et=tr["OS_time_days"].to_numpy(float),tr["OS"].to_numpy(int)
tte,ete=te["OS_time_days"].to_numpy(float),te["OS"].to_numpy(int)
fit={}; loglik={}
for k,cols in models.items():
    b,ll=coxfit(tr[cols].to_numpy(),tt,et); fit[k]=(cols,b); loglik[k]=ll
# test-set C-index + bootstrap CI
rng=np.random.RandomState(12345)  # fixed seed
def boot_c(cols,b,B=1000):
    lp=te[cols].to_numpy()@b; cs=[]
    idx=np.arange(len(te))
    for _ in range(B):
        s=rng.choice(idx,len(idx),replace=True)
        cs.append(cidx(tte[s],ete[s],lp[s]))
    return cidx(tte,ete,lp),np.nanpercentile(cs,2.5),np.nanpercentile(cs,97.5),lp
rows=[]; lps={}
for k,(cols,b) in fit.items():
    c,lo,hi,lp=boot_c(cols,b); lps[k]=lp
    rows.append({"model":k,"test_c_index":round(c,3),"ci95_low":round(lo,3),"ci95_high":round(hi,3),"n_test":len(te),"events_test":int(ete.sum())})
res=pd.DataFrame(rows)
# delta C combined vs clinical (paired bootstrap)
idx=np.arange(len(te)); dc=[]
for _ in range(1000):
    s=rng.choice(idx,len(idx),replace=True)
    dc.append(cidx(tte[s],ete[s],lps["combined"][s])-cidx(tte[s],ete[s],lps["clinical_only"][s]))
dc=np.array(dc); dc_pt=cidx(tte,ete,lps["combined"])-cidx(tte,ete,lps["clinical_only"])
# LR test combined vs clinical (on train)
lr=2*(loglik["combined"]-loglik["clinical_only"]); lr_p=stats.chi2.sf(lr,df=1)
res.to_csv(OUT/"nomogram_proper_cindex.csv",index=False)
print("=== TRAIN-fit / TEST-eval C-index (bootstrap 95% CI) ===")
print(res.to_string(index=False))
print(f"\nΔC-index (combined − clinical-only) on test: {dc_pt:+.3f}  (95% CI {np.percentile(dc,2.5):+.3f} to {np.percentile(dc,97.5):+.3f})")
print(f"Likelihood-ratio test (adding gene score to clinical, train): chi2={lr:.2f}, p={lr_p:.2e}")
print(f"train n={len(tr)} (events {int(et.sum())}); test n={len(te)} (events {int(ete.sum())})")
# also gene-only vs clinical
print(f"\ngene-only test C={res[res.model=='gene_only'].test_c_index.values[0]}, clinical-only test C={res[res.model=='clinical_only'].test_c_index.values[0]}, combined test C={res[res.model=='combined'].test_c_index.values[0]}")
pd.DataFrame({"delta_c_combined_minus_clinical":[dc_pt],"ci_low":[np.percentile(dc,2.5)],"ci_high":[np.percentile(dc,97.5)],"LR_chi2":[lr],"LR_p":[lr_p]}).to_csv(OUT/"nomogram_incremental.csv",index=False)
print("NOMOGRAM_PROPER_DONE")
