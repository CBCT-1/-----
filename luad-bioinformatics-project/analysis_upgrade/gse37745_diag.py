#!/usr/bin/env python3
"""Diagnose GSE37745 null: is the mitotic/proliferation score early-stage-specific?
Stage-stratified re-test of the frozen 9-gene consensus score in GSE37745 adenocarcinoma."""
import numpy as np, pandas as pd
from pathlib import Path
from scipy import optimize, special, stats
R=Path("/home/user/-----/luad-bioinformatics-project/v1.1_extracted/unpacked/data discoverer/03_bioinformatics_data/raw/refinebio_GSE37745/extracted/GSE37745")
OUT=Path("/home/user/-----/luad-bioinformatics-project/analysis_upgrade/processed"); OUT.mkdir(parents=True,exist_ok=True)

COEF={"ENSG00000166851":0.171225,"ENSG00000197930":0.162351,"ENSG00000137812":-0.086769,
      "ENSG00000035499":-0.090715,"ENSG00000167900":0.096549,"ENSG00000107984":0.343455,
      "ENSG00000133466":0.024320,"ENSG00000164647":-0.100102,"ENSG00000114346":0.042283}

def cox_univar(x,t,e):
    x=np.asarray(x,float); t=np.asarray(t,float); e=np.asarray(e,int)
    def nll(b):
        eta=x*b[0]; tot=0.0; g=0.0
        for i in np.where(e==1)[0]:
            rm=t>=t[i]; le=special.logsumexp(eta[rm]); w=np.exp(eta[rm]-le)
            tot-=eta[i]-le; g-=x[i]-np.sum(w*x[rm])
        return tot,np.array([g])
    r=optimize.minimize(lambda b:nll(b),[0.0],jac=True,method="L-BFGS-B")
    b=r.x[0]
    # SE via observed information (numeric 2nd deriv)
    eps=1e-4; f0,_=nll([b]); fp,_=nll([b+eps]); fm,_=nll([b-eps])
    H=(fp-2*f0+fm)/eps**2; se=1/np.sqrt(H) if H>0 else np.nan
    z=b/se if se==se else np.nan; p=2*stats.norm.sf(abs(z)) if z==z else np.nan
    return b,se,p

def cindex(t,e,risk):
    t=np.asarray(t,float); e=np.asarray(e,int); r=np.asarray(risk,float); c=p=0.0
    for i in range(len(t)):
        if e[i]!=1: continue
        for j in range(len(t)):
            if t[i]<t[j]:
                p+=1; c+= 1.0 if r[i]>r[j] else 0.5 if r[i]==r[j] else 0.0
    return c/p if p else np.nan

def logrank(t,e,grp):
    t=np.asarray(t,float); e=np.asarray(e,int); grp=np.asarray(grp,int); ome=v=0.0
    for tt in np.unique(t[e==1]):
        a1=np.sum((grp==1)&(t>=tt)); a0=np.sum((grp==0)&(t>=tt)); d1=np.sum((grp==1)&(t==tt)&(e==1)); d0=np.sum((grp==0)&(t==tt)&(e==1))
        n=a1+a0; d=d1+d0
        if n<=1 or d==0: continue
        ome+=d1-d*a1/n; v+=(a1*a0*d*(n-d))/(n**2*(n-1))
    return 2*stats.norm.sf(abs(ome/np.sqrt(v))) if v>0 else np.nan

expr=pd.read_csv(R/"GSE37745.tsv",sep="\t",index_col=0)
expr.index=[str(i).split(".")[0] for i in expr.index]
meta=pd.read_csv(R/"metadata_GSE37745.tsv",sep="\t")
key="refinebio_accession_code"
meta=meta.set_index(key)
meta=meta.loc[meta.index.intersection(expr.columns)]
adeno=meta[meta["characteristics_ch1_histology"]=="adeno"].copy()
# survival
adeno["event"]=(adeno["characteristics_ch1_dead"].astype(str).str.lower()=="yes").astype(int)
adeno["time"]=pd.to_numeric(adeno["characteristics_ch1_days to determined death status"],errors="coerce")
adeno=adeno.dropna(subset=["time"]); adeno=adeno[adeno["time"]>0]
# stage
st=adeno["characteristics_ch1_tumor stage"].astype(str).str.lower()
adeno["stage_group"]=np.where(st.str.startswith("1"),"stageI","stageII+")
# score
sub=expr[[g for g in adeno.index]]
zrows=[]; 
for ens,co in COEF.items():
    if ens in sub.index:
        v=sub.loc[ens].astype(float); z=(v-v.mean())/v.std(ddof=0); zrows.append(z*co)
score=pd.concat(zrows,axis=1).sum(axis=1)
adeno["score_z"]=((score-score.mean())/score.std(ddof=0)).reindex(adeno.index).values

res=[]
for label,df in [("all_adeno",adeno),("stageI",adeno[adeno.stage_group=="stageI"]),("stageII+",adeno[adeno.stage_group=="stageII+"])]:
    if len(df)<15: 
        res.append({"subset":label,"n":len(df),"events":int(df.event.sum()),"note":"too small"}); continue
    b,se,p=cox_univar(df.score_z,df.time,df.event); c=cindex(df.time,df.event,df.score_z)
    med=df.score_z.median(); lr=logrank(df.time,df.event,(df.score_z>=med).astype(int))
    res.append({"subset":label,"n":len(df),"events":int(df.event.sum()),"HR":float(np.exp(b)),
                "cox_p":float(p),"c_index":float(c),"logrank_p":float(lr)})
rd=pd.DataFrame(res); rd.to_csv(OUT/"gse37745_stage_stratified.csv",index=False)
print(rd.to_string()); 
print("\nStage distribution (adeno):",adeno.stage_group.value_counts().to_dict())
print("Median age:",pd.to_numeric(adeno['characteristics_ch1_age'],errors='coerce').median(),
      "| event rate:",round(adeno.event.mean(),3))
print("GSE37745_DIAG_DONE")
