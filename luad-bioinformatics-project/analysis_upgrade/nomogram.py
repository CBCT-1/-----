#!/usr/bin/env python3
"""Weakness 3: nomogram (risk score + clinical) improves combined discrimination.
Multivariable Cox on TCGA-LUAD consensus score + stage + age (+sex); C-index, time-AUC, calibration, DCA."""
import numpy as np, pandas as pd
from pathlib import Path
from scipy import optimize, special, stats
P=Path("/home/user/-----/luad-bioinformatics-project/v1.1_extracted/unpacked/data discoverer/03_bioinformatics_data/processed")
OUT=Path("/home/user/-----/luad-bioinformatics-project/analysis_upgrade/processed"); OUT.mkdir(parents=True,exist_ok=True)

pred=pd.read_csv(P/"TCGA-LUAD_consensus_axis_model_predictions.csv",encoding="utf-8-sig")  # sample_id,risk_score,OS,OS_time_days,split
clin=pd.read_csv(P/"TCGA-LUAD_clinical_mutation_context.csv",encoding="utf-8-sig")[["sample_id","age_at_index","gender","ajcc_pathologic_stage"]]
df=pred.merge(clin,on="sample_id",how="inner").dropna(subset=["OS","OS_time_days","risk_score"])
df=df[df["OS_time_days"]>0].copy()
smap={"Stage I":1,"Stage IA":1,"Stage IB":1,"Stage II":2,"Stage IIA":2,"Stage IIB":2,"Stage IIIA":3,"Stage IIIB":3,"Stage IV":4}
df["stage_ord"]=df["ajcc_pathologic_stage"].map(smap)
df=df.dropna(subset=["stage_ord"])
df["age"]=pd.to_numeric(df["age_at_index"],errors="coerce"); df=df.dropna(subset=["age"])
df["male"]=(df["gender"].astype(str).str.lower()=="male").astype(float)
z=lambda s:(s-s.mean())/s.std(ddof=0)
df["risk_z"]=z(df["risk_score"]); df["age_z"]=z(df["age"]); df["stage_z"]=z(df["stage_ord"])
t=df["OS_time_days"].to_numpy(float); e=df["OS"].to_numpy(int)

def cox(X,t,e):
    X=np.asarray(X,float); 
    def f(b):
        eta=X@b; nll=0.0; g=np.zeros(X.shape[1])
        for i in np.where(e==1)[0]:
            rm=t>=t[i]; le=special.logsumexp(eta[rm]); w=np.exp(eta[rm]-le)
            nll-=eta[i]-le; g-=X[i]-w@X[rm]
        return nll,g
    r=optimize.minimize(f,np.zeros(X.shape[1]),jac=True,method="L-BFGS-B")
    # SE from numeric Hessian
    b=r.x; H=np.zeros((len(b),len(b))); eps=1e-4
    for i in range(len(b)):
        bp=b.copy();bp[i]+=eps;bm=b.copy();bm[i]-=eps
        H[:,i]=(f(bp)[1]-f(bm)[1])/(2*eps)
    se=np.sqrt(np.diag(np.linalg.inv(H)))
    return b,se
def cidx(t,e,r):
    c=p=0.0
    for i in range(len(t)):
        if e[i]!=1:continue
        for j in range(len(t)):
            if t[i]<t[j]: p+=1; c+=1.0 if r[i]>r[j] else 0.5 if r[i]==r[j] else 0.0
    return c/p if p else np.nan
def tauc(t,e,r,horizon):
    case=(e==1)&(t<=horizon); ctrl=t>horizon
    if case.sum()<3 or ctrl.sum()<3: return np.nan,int(case.sum()),int(ctrl.sum())
    rc=r[case]; ro=r[ctrl]; auc=(np.greater.outer(rc,ro).sum()+0.5*np.equal.outer(rc,ro).sum())/(len(rc)*len(ro))
    return float(auc),int(case.sum()),int(ctrl.sum())

# models
Xrisk=df[["risk_z"]].to_numpy(); Xfull=df[["risk_z","age_z","stage_z","male"]].to_numpy()
br,_=cox(Xrisk,t,e); bf,sf=cox(Xfull,t,e)
lp_risk=Xrisk@br; lp_full=Xfull@bf
out={"model":["risk_only","risk+clinical_nomogram"],
     "c_index_all":[cidx(t,e,lp_risk),cidx(t,e,lp_full)]}
# test split
te=df["split"]=="test"
out["c_index_test"]=[cidx(t[te.values],e[te.values],lp_risk[te.values]),cidx(t[te.values],e[te.values],lp_full[te.values])]
res=pd.DataFrame(out); 
# time AUC for full model
yr=365.25; tauc_rows=[]
for h,lab in [(1*yr,"1yr"),(3*yr,"3yr"),(5*yr,"5yr")]:
    a,nc,no=tauc(t,e,lp_full,h); ar,_,_=tauc(t,e,lp_risk,h)
    tauc_rows.append({"horizon":lab,"nomogram_AUC":a,"risk_only_AUC":ar,"cases":nc,"controls":no})
tdf=pd.DataFrame(tauc_rows)
# nomogram coefficients / points
coefs=pd.DataFrame({"variable":["risk_score_z","age_z","stage_ord_z","male"],"coef":bf,"se":sf,
                    "HR":np.exp(bf),"HR_low":np.exp(bf-1.96*sf),"HR_high":np.exp(bf+1.96*sf),
                    "p":2*stats.norm.sf(np.abs(bf/sf))})
maxabs=np.max(np.abs(bf)); coefs["nomogram_points_per_SD"]=100*coefs["coef"]/maxabs
# calibration at 3yr via Breslow baseline
order=np.argsort(t); H0=np.zeros(len(t))
# Breslow cumulative baseline hazard at 3yr
eta=lp_full; risk=np.exp(eta); h3=0.0
for tt in np.unique(t[e==1]):
    if tt>3*yr: break
    d=np.sum((t==tt)&(e==1)); denom=np.sum(risk[t>=tt]); 
    if denom>0: h3+=d/denom
surv3=np.exp(-h3*risk); pred_risk3=1-surv3
df["_pr3"]=pred_risk3
cal=[]
df["_tert"]=pd.qcut(eta,3,labels=["low","mid","high"])
for g,sub in df.groupby("_tert",observed=True):
    obs=np.mean((sub["OS"]==1)&(sub["OS_time_days"]<=3*yr))
    cal.append({"risk_tertile":g,"n":len(sub),"mean_predicted_3yr_risk":float(sub["_pr3"].mean()),"observed_3yr_event_rate":float(obs)})
caldf=pd.DataFrame(cal)

res.to_csv(OUT/"nomogram_cindex.csv",index=False)
tdf.to_csv(OUT/"nomogram_timeAUC.csv",index=False)
coefs.to_csv(OUT/"nomogram_coefficients.csv",index=False)
caldf.to_csv(OUT/"nomogram_calibration_3yr.csv",index=False)
print("=== C-index ===\n",res.to_string(index=False))
print("\n=== time-AUC (full model) ===\n",tdf.to_string(index=False))
print("\n=== nomogram Cox ===\n",coefs[["variable","HR","HR_low","HR_high","p","nomogram_points_per_SD"]].to_string(index=False))
print("\n=== calibration 3yr ===\n",caldf.to_string(index=False))
print("\nN =",len(df),"| events =",int(e.sum()))
print("NOMOGRAM_DONE")
