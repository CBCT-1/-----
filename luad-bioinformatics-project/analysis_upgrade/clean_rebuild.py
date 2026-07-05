#!/usr/bin/env python3
"""DECISIVE rebuild on clean patient-level set (GPT #1/#2): primary-tumour-only, patient-deduplicated,
patient-grouped split, genome-wide screen + model fit on TRAIN ONLY, test evaluated once."""
import numpy as np, pandas as pd, warnings, math
warnings.filterwarnings("ignore")
from pathlib import Path
from scipy import stats
from sksurv.linear_model import CoxPHSurvivalAnalysis
from sksurv.util import Surv
from sksurv.metrics import concordance_index_censored
A=Path("/home/user/-----/luad-bioinformatics-project/v1.1_extracted/unpacked/data discoverer/03_bioinformatics_data")
OUT=Path("processed"); FULL=A/"raw/TCGA-LUAD.star_tpm.tsv.gz"
split=pd.read_csv(OUT/"tcga_clean_patient_split.csv")   # sample_id,patient,OS,OS_time_days,split
tr=split[split.split=="train"]; te=split[split.split=="test"]
tr_s=tr.sample_id.tolist(); te_s=te.sample_id.tolist()
sy=pd.read_csv(A/"manifests/gencode.v36.annotation.gtf.gene.probemap",sep="\t").set_index("id")["gene"].to_dict() if (A/"manifests/gencode.v36.annotation.gtf.gene.probemap").exists() else {}

def logrank_p(t,e,g):
    t=np.asarray(t,float);e=np.asarray(e,int);g=np.asarray(g,int);ome=v=0.0
    for tt in np.unique(t[e==1]):
        a1=np.sum((g==1)&(t>=tt));a0=np.sum((g==0)&(t>=tt));d1=np.sum((g==1)&(t==tt)&(e==1));d0=np.sum((g==0)&(t==tt)&(e==1))
        n=a1+a0;d=d1+d0
        if n<=1 or d==0: continue
        ome+=d1-d*a1/n; v+=(a1*a0*d*(n-d))/(n**2*(n-1))
    return float(stats.chi2.sf(ome**2/v,1)) if v>0 else np.nan

print("loading TRAIN submatrix (genome-wide, train patients only)...",flush=True)
tr_expr=pd.read_csv(FULL,sep="\t",index_col=0,usecols=["Ensembl_ID"]+tr_s).astype(np.float32)
tr_expr=tr_expr[tr_s]
tt=tr.set_index("sample_id").loc[tr_s,"OS_time_days"].to_numpy(float); et=tr.set_index("sample_id").loc[tr_s,"OS"].to_numpy(int)
mean=tr_expr.mean(1); var=tr_expr.var(1)
expressed=mean[mean>0.5].index
top=var.loc[expressed].sort_values(ascending=False).head(8000).index
print(f"train {tr_expr.shape[1]} patients; expressed {len(expressed)}; screening top {len(top)} variance genes on TRAIN ONLY",flush=True)
rows=[]
for i,g in enumerate(top):
    v=tr_expr.loc[g].to_numpy(float); med=np.median(v); grp=(v>=med).astype(int)
    if grp.sum()<10 or (1-grp).sum()<10: continue
    p=logrank_p(tt,et,grp); rows.append((g,p))
scr=pd.DataFrame(rows,columns=["Ensembl_ID","logrank_p"]).dropna()
scr["fdr"]=stats.false_discovery_control(scr["logrank_p"]) if hasattr(stats,"false_discovery_control") else scr["logrank_p"]*len(scr)/stats.rankdata(scr["logrank_p"])
scr["gene"]=[sy.get(g,g) for g in scr.Ensembl_ID]
sel=scr[scr.fdr<0.05].sort_values("fdr")
print(f"train-only genome-wide FDR<0.05: {len(sel)} genes",flush=True)
print(sel.head(20)[["gene","logrank_p","fdr"]].to_string(index=False))
scr.to_csv(OUT/"clean_trainonly_screen.csv",index=False)
selg=sel.Ensembl_ID.tolist()
if len(selg)<3:
    selg=scr.sort_values("logrank_p").head(10).Ensembl_ID.tolist()
    print("fewer than 3 FDR genes; using top-10 by p as candidate set",flush=True)

# fit Cox on TRAIN selected genes; evaluate once on TEST
tr_X=tr_expr.loc[selg].T
mu=tr_X.mean(); sd=tr_X.std(ddof=0).replace(0,1); Ztr=(tr_X-mu)/sd
cox=CoxPHSurvivalAnalysis(alpha=1e-4).fit(Ztr,Surv.from_arrays(et.astype(bool),tt))
coef=pd.Series(cox.coef_,index=selg)
te_expr=pd.read_csv(FULL,sep="\t",index_col=0,usecols=["Ensembl_ID"]+te_s).astype(np.float32)[te_s]
te_X=te_expr.loc[selg].T; Zte=(te_X-mu)/sd
tte=te.set_index("sample_id").loc[te_s,"OS_time_days"].to_numpy(float); ete=te.set_index("sample_id").loc[te_s,"OS"].to_numpy(int)
risk_te=cox.predict(Zte); risk_tr=cox.predict(Ztr)
def cidx(y_e,y_t,r): return concordance_index_censored(y_e.astype(bool),y_t,r)[0]
rng=np.random.RandomState(7)
def bootci(t,e,r,B=1000):
    idx=np.arange(len(t)); cs=[cidx(e[s],t[s],r[s]) for s in (rng.choice(idx,len(idx),True) for _ in range(B))]
    return np.percentile(cs,2.5),np.percentile(cs,97.5)
c_tr=cidx(et,tt,risk_tr); c_te=cidx(ete,tte,risk_te); lo,hi=bootci(tte,ete,risk_te)
print(f"\n=== CLEAN patient-level model ===\ntrain C={c_tr:.3f} (n={len(tr)},ev={int(et.sum())}) | TEST C={c_te:.3f} 95%CI {lo:.3f}-{hi:.3f} (n={len(te)},ev={int(ete.sum())})",flush=True)
pd.DataFrame({"gene":[sy.get(g,g) for g in selg],"Ensembl_ID":selg,"coef":coef.values}).to_csv(OUT/"clean_model_coefficients.csv",index=False)

# GEO external transfer of the clean frozen model
ENS_base={g.split('.')[0]:g for g in selg}
RB=A/"raw"
geo=[("GSE31210",RB/"refinebio_GSE31210/extracted/GSE31210/GSE31210.tsv","GEO_consensus_axis_external_predictions.csv","GSE31210_eligible","OS_time_days",1),
     ("GSE50081",RB/"refinebio_GSE50081/extracted/GSE50081/GSE50081.tsv","GEO_consensus_axis_external_predictions.csv","GSE50081_adenocarcinoma_like","OS_time_years",365.25),
     ("GSE30219",RB/"refinebio_GSE30219/extracted/GSE30219/GSE30219.tsv","GSE30219_GSE37745_unused_full_consensus_axis_scores.csv","GSE30219_ADC","OS_time_years",365.25),
     ("GSE37745",RB/"refinebio_GSE37745/extracted/GSE37745/GSE37745.tsv","GSE30219_GSE37745_unused_full_consensus_axis_scores.csv","GSE37745_adeno","OS_time_years",365.25),
     ("GSE68465",RB/"refinebio_GSE68465/extracted/GSE68465/GSE68465.tsv","GSE68465_partial_consensus_axis_scores.csv",None,"OS_time_months",30.4375)]
grows=[]
for name,exprp,survp,coh,tcol,mult in geo:
    ex=pd.read_csv(exprp,sep="\t",index_col=0); ex.index=[str(i).split(".")[0] for i in ex.index]
    avail=[b for b in ENS_base if b in ex.index]
    if len(avail)<3: grows.append({"cohort":name,"note":"coverage<3"}); continue
    Z=((ex.loc[avail].T-ex.loc[avail].T.mean())/ex.loc[avail].T.std(ddof=0))
    sc=(Z*pd.Series({b:coef[ENS_base[b]] for b in avail})).sum(1)
    sdf=pd.read_csv(A/"processed"/survp,encoding="utf-8-sig")
    if coh and "cohort" in sdf: sdf=sdf[sdf.cohort==coh]
    if name=="GSE31210": sdf=sdf[sdf.get("eligible_for_prognosis",True)==True]
    sdf["time"]=pd.to_numeric(sdf[tcol],errors="coerce")*mult; sdf["event"]=pd.to_numeric(sdf["OS_event"],errors="coerce")
    m=sdf[["sample_id","time","event"]].dropna().merge(sc.rename("s"),left_on="sample_id",right_index=True).dropna()
    m=m[m.time>0]
    if len(m)<20: grows.append({"cohort":name,"n":len(m),"note":"small"}); continue
    z=(m.s-m.s.mean())/m.s.std(ddof=0); c=cidx(m.event.values,m.time.values,z.values)
    b=CoxPHSurvivalAnalysis(alpha=1e-4).fit(z.values.reshape(-1,1),Surv.from_arrays(m.event.astype(bool),m.time))
    lo2,hi2=bootci(m.time.values,m.event.values,z.values,500)
    grows.append({"cohort":name,"n_genes":len(avail),"n":len(m),"events":int(m.event.sum()),"c_index":round(c,3),"c_lo":round(lo2,3),"c_hi":round(hi2,3),"HR_per_SD":round(float(np.exp(b.coef_[0])),3),"independent":name in("GSE30219","GSE37745","GSE68465")})
gres=pd.DataFrame(grows); gres.to_csv(OUT/"clean_model_geo_external.csv",index=False)
print("\n=== CLEAN model GEO external transfer ===\n"+gres.to_string(index=False),flush=True)
print("CLEAN_REBUILD_DONE",flush=True)
