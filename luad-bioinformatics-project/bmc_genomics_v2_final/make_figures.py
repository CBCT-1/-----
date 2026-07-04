#!/usr/bin/env python3
"""Publication figures for the BMC Genomics LUAD PLK1/ERO1A manuscript.
5 main + 2 supplementary, from frozen source tables. CVD-safe palette, 400 dpi PNG + PDF."""
from __future__ import annotations
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

TBL = Path("/home/user/-----/luad-bioinformatics-project/v1.1_extracted/unpacked/"
           "data discoverer/06_bmc_genomics_submission_packet_v1.9/"
           "02_figures_tables/tables/all_project_tables")
OUT = Path("/home/user/-----/luad-bioinformatics-project/bmc_genomics_v2_final/figures")
OUT.mkdir(parents=True, exist_ok=True)
def load(name): return pd.read_csv(TBL/f"{name}.csv", encoding="utf-8-sig")

BLUE="#2a78d6"; AQUA="#1baf7a"; VIOLET="#4a3aa7"; ORANGE="#eb6834"
GOOD="#0ca30c"; WARN="#fab219"; CRIT="#d03b3b"
INK="#0b0b0b"; INK2="#52514e"; MUTED="#898781"; GRID="#e1e0d9"; AXIS="#c3c2b7"; SURF="#ffffff"
ACCENT=BLUE; ACCENT2=ORANGE
mpl.rcParams.update({"figure.dpi":150,"savefig.dpi":400,"figure.facecolor":SURF,"axes.facecolor":SURF,
 "savefig.facecolor":SURF,"font.family":"DejaVu Sans","font.size":8.2,"axes.edgecolor":AXIS,"axes.linewidth":0.8,
 "axes.titlesize":9,"axes.titleweight":"bold","axes.titlelocation":"left","axes.titlepad":5,"axes.labelcolor":INK2,
 "axes.labelsize":8,"xtick.color":MUTED,"ytick.color":MUTED,"xtick.labelsize":7.4,"ytick.labelsize":7.4,"text.color":INK,
 "axes.spines.top":False,"axes.spines.right":False,"xtick.major.width":0.8,"ytick.major.width":0.8,"legend.frameon":False,"legend.fontsize":7.3})
def plabel(ax,s,dx=-0.02,dy=1.06): ax.text(dx,dy,s,transform=ax.transAxes,fontsize=11,fontweight="bold",va="top",ha="right",color=INK)
def hgrid(ax): ax.grid(axis="x",color=GRID,lw=0.6,zorder=0); ax.set_axisbelow(True)
def vgrid(ax): ax.grid(axis="y",color=GRID,lw=0.6,zorder=0); ax.set_axisbelow(True)
def tidy(ax):
    for s in ("left","bottom"): ax.spines[s].set_color(AXIS)
def save(fig,stem):
    fig.savefig(OUT/f"{stem}.png",bbox_inches="tight",pad_inches=0.06)
    fig.savefig(OUT/f"{stem}.pdf",bbox_inches="tight",pad_inches=0.06)
    plt.close(fig); print("wrote",stem)
G9=["PLK1","ERO1A","KNL1","DEPDC1B","TK1","DKK1","C1QTNF6","STEAP1","ECT2"]
def gc(g): return ACCENT if g=="PLK1" else ACCENT2 if g=="ERO1A" else "#c8d6e8"

def figure1():
    fig=plt.figure(figsize=(7.2,3.0)); gs=fig.add_gridspec(1,2,width_ratios=[1.05,1.25],wspace=0.42)
    ax=fig.add_subplot(gs[0,0])
    t2=load("Table2_LUAD_top_survival_genes").dropna(subset=["logrank_p"]).sort_values("logrank_p").head(15).copy()
    t2["nlp"]=-np.log10(t2["logrank_p"]); t2=t2.iloc[::-1]; y=np.arange(len(t2))
    ax.barh(y,t2["nlp"],color=[gc(g) for g in t2["gene_symbol"]],height=0.72,zorder=3,edgecolor=SURF,linewidth=0.6)
    ax.set_yticks(y); ax.set_yticklabels(t2["gene_symbol"],fontsize=6.8)
    for lbl,g in zip(ax.get_yticklabels(),t2["gene_symbol"]):
        if g in("PLK1","ERO1A"): lbl.set_fontweight("bold"); lbl.set_color(INK)
    ax.set_xlabel("Survival screen  -log10 P"); ax.set_title("LUAD survival screen"); hgrid(ax); tidy(ax); plabel(ax,"a",dx=-0.34)
    ax=fig.add_subplot(gs[0,1])
    t22=load("Table22_LUAD_consensus_axis_prognostic_model").set_index("gene_symbol").loc[G9]
    lc=["tcga_fdr_significant","internal_train_supported","gse31210_supported","gse50081_supported","depmap_dependency_supported","spatial_supported"]
    ll=["TCGA FDR","TCGA train","GSE31210","GSE50081","DepMap","Spatial"]; M=t22[lc].astype(float).values
    ax.imshow(M,aspect="auto",cmap=mpl.colors.ListedColormap(["#eef0f2",AQUA]),vmin=0,vmax=1)
    ax.set_xticks(range(len(ll))); ax.set_xticklabels(ll,rotation=38,ha="right",fontsize=6.8)
    ax.set_yticks(range(len(G9))); ax.set_yticklabels(G9,fontsize=6.8)
    for lbl,g in zip(ax.get_yticklabels(),G9):
        if g in("PLK1","ERO1A"): lbl.set_fontweight("bold"); lbl.set_color(INK)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if M[i,j]>0.5: ax.text(j,i,"X",ha="center",va="center",color="white",fontsize=6.5,fontweight="bold")
    ax.set_xticks(np.arange(-.5,len(ll),1),minor=True); ax.set_yticks(np.arange(-.5,len(G9),1),minor=True)
    ax.grid(which="minor",color=SURF,lw=1.4); ax.tick_params(which="minor",length=0)
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_title("Cross-layer evidence support")
    ns=t22["cross_layer_support_count"].astype(int).values; ax2=ax.twinx(); ax2.set_ylim(ax.get_ylim()); ax2.set_yticks(range(len(G9)))
    ax2.set_yticklabels([f"{n}/6" for n in ns],fontsize=6.4); ax2.tick_params(length=0)
    for s in ax2.spines.values(): s.set_visible(False)
    plabel(ax,"b",dx=-0.24)
    fig.suptitle("Figure 1  Literature-guided TCGA discovery of a PLK1-centred mitotic/redox programme",x=0.012,ha="left",fontsize=9.2,fontweight="bold",y=1.05)
    save(fig,"Figure1")

def figure2():
    fig=plt.figure(figsize=(7.4,5.6)); gs=fig.add_gridspec(2,2,height_ratios=[1,1.05],width_ratios=[1,1.15],hspace=0.5,wspace=0.42)
    ax=fig.add_subplot(gs[0,0])
    t22=load("Table22_LUAD_consensus_axis_prognostic_model").set_index("gene_symbol").loc[G9]
    coef=t22["coefficient"].astype(float).sort_values(); y=np.arange(len(coef))
    ax.barh(y,coef.values,color=[CRIT if c>0 else BLUE for c in coef],height=0.72,zorder=3,edgecolor=SURF,linewidth=0.6); ax.axvline(0,color=AXIS,lw=0.9)
    ax.set_yticks(y); ax.set_yticklabels(coef.index,fontsize=6.9)
    for lbl,g in zip(ax.get_yticklabels(),coef.index):
        if g in("PLK1","ERO1A"): lbl.set_fontweight("bold"); lbl.set_color(INK)
    ax.set_xlabel("Cox coefficient (frozen, TCGA train)"); ax.set_title("Nine-gene programme score"); hgrid(ax); tidy(ax)
    ax.legend(handles=[Rectangle((0,0),1,1,color=CRIT),Rectangle((0,0),1,1,color=BLUE)],labels=["risk-increasing","protective"],loc="lower right",fontsize=6.6,handlelength=1.0,handleheight=1.0,borderpad=0.3)
    plabel(ax,"a",dx=-0.30)
    ax=fig.add_subplot(gs[0,1])
    vals=[0.584,0.660,0.640]; x=np.arange(3)
    ax.bar(x,vals,color=[MUTED,"#9ec5f4",ACCENT],width=0.62,zorder=3,edgecolor=SURF,linewidth=0.8)
    ax.axhline(0.5,color=CRIT,lw=1.0,ls=(0,(4,3))); ax.text(-0.45,0.503,"random 0.5",color=CRIT,fontsize=6.2,va="bottom",ha="left")
    for xi,v in zip(x,vals): ax.text(xi,v+0.006,f"{v:.3f}",ha="center",va="bottom",fontsize=7.6,fontweight="bold",color=INK)
    ax.set_xticks(x); ax.set_xticklabels(["Prior ridge\n(held-out)","Consensus\ntrain","Consensus\nheld-out"],fontsize=6.9)
    ax.set_ylim(0.5,0.70); ax.set_ylabel("Harrell C-index"); ax.set_title("Discrimination improved over prior model"); vgrid(ax); tidy(ax); plabel(ax,"b",dx=-0.22)
    ax=fig.add_subplot(gs[1,0:2])
    _t=[load("Table23_LUAD_consensus_axis_external_validation"),load("Table31_GSE68465_partial_consensus_axis_validation"),load("Table32_GSE30219_GSE37745_unused_full_consensus_axis_validation")]
    t23=pd.concat(_t,ignore_index=True); t23=t23[t23["model"]=="risk_univariable"].copy()
    rows=[]
    for base in ["GSE31210","GSE50081","GSE30219","GSE68465","GSE37745"]:
        cand=[c for c in t23["cohort"].unique() if str(c).startswith(base)]; r=None
        for c in cand:
            rr=t23[(t23["cohort"]==c)&(t23["outcome"]=="OS")]
            if len(rr): r=rr.iloc[0]; break
        if r is None:
            for c in cand:
                rr=t23[t23["cohort"]==c]
                if len(rr): r=rr.iloc[0]; break
        if r is not None: rows.append((base,r))
    labels=[]; hr=[]; lo=[]; hi=[]; pv=[]; ci=[]
    for base,r in rows:
        nm="GSE68465 (7/9)" if base=="GSE68465" else base
        labels.append(f"{nm}  {r['outcome']}"); hr.append(float(r["hazard_ratio"])); lo.append(float(r["ci95_low"]))
        hi.append(float(r["ci95_high"])); pv.append(float(r["p_value"])); ci.append(float(r["c_index"]))
    y=np.arange(len(labels))[::-1]
    for yi,l,h,hh,p in zip(y,lo,hr,hi,pv):
        col=ACCENT if p<0.05 else WARN
        ax.plot([l,hh],[yi,yi],color=col,lw=2.0,solid_capstyle="round",zorder=3)
        ax.scatter([h],[yi],s=34,color=col,zorder=4,edgecolor=SURF,linewidth=0.8)
    ax.axvline(1.0,color=AXIS,lw=1.0); ax.set_yticks(y); ax.set_yticklabels(labels,fontsize=7.2)
    for lbl,p in zip(ax.get_yticklabels(),pv):
        if p>=0.05: lbl.set_color(CRIT)
    ax.set_xlim(0.7,2.6); ax.set_xlabel("Hazard ratio per 1-SD score (95% CI)")
    ax.set_title("External transfer: significant in 4/5 cohorts; GSE37745 is a transparent null"); hgrid(ax); tidy(ax)
    for yi,p,c in zip(y,pv,ci):
        ax.text(2.56,yi,f"C={c:.3f}  P={p:.2g} {'*' if p<0.05 else 'n.s.'}",fontsize=6.3,va="center",ha="right",color=INK2)
    ax.legend(handles=[Line2D([0],[0],color=ACCENT,lw=2,marker="o",markersize=5,markeredgecolor=SURF),Line2D([0],[0],color=WARN,lw=2,marker="o",markersize=5,markeredgecolor=SURF)],labels=["significant (P<0.05)","non-replication"],loc="lower left",fontsize=6.6,handlelength=1.4)
    plabel(ax,"c",dx=-0.14,dy=1.08)
    fig.suptitle("Figure 2  A nine-gene score: construction, held-out separation and multi-cohort transfer",x=0.012,ha="left",fontsize=9.2,fontweight="bold",y=0.98)
    save(fig,"Figure2")

def figure3():
    fig=plt.figure(figsize=(7.2,3.1)); gs=fig.add_gridspec(1,2,width_ratios=[1.35,1.0],wspace=0.45)
    ax=fig.add_subplot(gs[0,0])
    t11=load("Table11_LUAD_pathway_enrichment").sort_values("minus_log10_p",ascending=False).drop_duplicates("term_name").head(10).iloc[::-1]
    def th(r):
        s=(str(r["term_name"])+str(r["native_id"])).lower()
        return ORANGE if any(k in s for k in["thiol","oxid","redox","folding","endoplasmic","disulf","ero"]) else BLUE
    y=np.arange(len(t11)); ax.barh(y,t11["minus_log10_p"],color=[th(r) for _,r in t11.iterrows()],height=0.72,zorder=3,edgecolor=SURF,linewidth=0.6)
    ax.set_yticks(y); ax.set_yticklabels([t[:34] for t in t11["term_name"]],fontsize=6.3)
    ax.set_xlabel("Enrichment  -log10 adjusted P (g:SCS)"); ax.set_title("Pathway coherence"); hgrid(ax); tidy(ax)
    ax.legend(handles=[Rectangle((0,0),1,1,color=BLUE),Rectangle((0,0),1,1,color=ORANGE)],labels=["mitotic / checkpoint","ER-redox / folding"],loc="lower right",fontsize=6.5,handlelength=1.0,handleheight=1.0,borderpad=0.3)
    plabel(ax,"a",dx=-0.55)
    ax=fig.add_subplot(gs[0,1])
    t14=load("Table14_HPA_LUAD_tissue_validation"); present=t14[t14["hpa_present"]==True] if "hpa_present" in t14 else t14
    def cls(row):
        m=row.get("hpa_tcga_direction_match")
        return "concordant" if m in(True,"True") else "discordant" if m in(False,"False") else "unannotated"
    counts=present.apply(cls,axis=1).value_counts().reindex(["concordant","unannotated","discordant"]).fillna(0)
    x=np.arange(3); ax.bar(x,counts.values,color=[GOOD,MUTED,CRIT],width=0.62,zorder=3,edgecolor=SURF,linewidth=0.8)
    for xi,v in zip(x,counts.values): ax.text(xi,v+0.15,int(v),ha="center",va="bottom",fontsize=8,fontweight="bold",color=INK)
    ax.set_xticks(x); ax.set_xticklabels(["concordant","unannot.","discordant"],fontsize=7)
    ax.set_ylabel("HPA-evaluated candidate genes"); ax.set_title("HPA pathology direction"); vgrid(ax); tidy(ax); plabel(ax,"b",dx=-0.26)
    fig.suptitle("Figure 3  Pathway and Human Protein Atlas biological-context coherence",x=0.012,ha="left",fontsize=9.2,fontweight="bold",y=1.04)
    save(fig,"Figure3")

def figure4():
    fig=plt.figure(figsize=(7.2,3.2)); gs=fig.add_gridspec(1,2,width_ratios=[1.15,1.1],wspace=0.42)
    ax=fig.add_subplot(gs[0,0])
    t15=load("Table15_E-MTAB13530_LUAD_spatial_candidate_expression").sort_values("tumor_minus_adjacent_mean_log1p_cp10k")
    d=t15["tumor_minus_adjacent_mean_log1p_cp10k"].astype(float)
    cols=[ACCENT if g=="PLK1" else ACCENT2 if g=="ERO1A" else("#c8d6e8" if v>=0 else "#f0c9c9") for g,v in zip(t15["gene_symbol"],d)]
    y=np.arange(len(t15)); ax.barh(y,d,color=cols,height=0.72,zorder=3,edgecolor=SURF,linewidth=0.5); ax.axvline(0,color=AXIS,lw=0.9)
    ax.set_yticks(y); ax.set_yticklabels(t15["gene_symbol"],fontsize=6.2)
    for lbl,g in zip(ax.get_yticklabels(),t15["gene_symbol"]):
        if g in("PLK1","ERO1A"): lbl.set_fontweight("bold"); lbl.set_color(INK)
    ax.set_xlabel("Visium tumour - adjacent  dlog1p(CP10K)"); ax.set_title("Visium tumour enrichment"); hgrid(ax); tidy(ax); plabel(ax,"a",dx=-0.34)
    ax=fig.add_subplot(gs[0,1])
    vals=[0.288,0.253,0.311]; ax.bar(np.arange(3),vals,color=[ORANGE,BLUE,VIOLET],width=0.6,zorder=3,edgecolor=SURF,linewidth=0.8)
    for xi,v in zip(range(3),vals): ax.text(xi,v+0.005,f"{v:.2f}",ha="center",va="bottom",fontsize=7.4,fontweight="bold",color=INK)
    ax.set_xticks(range(3)); ax.set_xticklabels(["ER-redox","Mitotic-\ncheckpoint","Strong-HPA"],fontsize=6.9)
    ax.set_ylabel("Spot rho vs tumour-like state"); ax.set_ylim(0,0.38); ax.set_title("Axis co-localises with tumour context"); vgrid(ax); tidy(ax)
    ax.text(0.98,0.96,"positive in 12/12 sections",transform=ax.transAxes,ha="right",va="top",fontsize=6.3,color=INK2,style="italic"); plabel(ax,"b",dx=-0.24)
    fig.suptitle("Figure 4  Single-cell aggregate and Visium tissue-context evidence",x=0.012,ha="left",fontsize=9.2,fontweight="bold",y=1.04)
    save(fig,"Figure4")

def figure5():
    fig=plt.figure(figsize=(7.4,3.2)); gs=fig.add_gridspec(1,3,width_ratios=[1.1,0.9,0.95],wspace=0.5)
    ax=fig.add_subplot(gs[0,0])
    t16=load("Table16_DepMap26Q1_LUAD_CRISPR_dependency").dropna(subset=["luad_mean_gene_effect"]).sort_values("luad_mean_gene_effect").head(12).iloc[::-1]
    d=t16["luad_mean_gene_effect"].astype(float); y=np.arange(len(t16))
    ax.barh(y,d,color=[gc(g) for g in t16["gene_symbol"]],height=0.72,zorder=3,edgecolor=SURF,linewidth=0.5)
    ax.axvline(-0.5,color=CRIT,lw=1.0,ls=(0,(4,3))); ax.text(-0.5,len(t16)-0.3,"dependency\nthreshold",color=CRIT,fontsize=5.9,ha="center",va="top")
    ax.set_yticks(y); ax.set_yticklabels(t16["gene_symbol"],fontsize=6.3)
    for lbl,g in zip(ax.get_yticklabels(),t16["gene_symbol"]):
        if g in("PLK1","ERO1A"): lbl.set_fontweight("bold"); lbl.set_color(INK)
    ax.set_xlabel("Mean LUAD CRISPR effect"); ax.set_title("Dependency ranking"); hgrid(ax); tidy(ax); plabel(ax,"a",dx=-0.42)
    ax=fig.add_subplot(gs[0,1])
    row=load("Table16_DepMap26Q1_LUAD_CRISPR_dependency"); row=row[row["gene_symbol"]=="PLK1"].iloc[0]
    vals=[float(row["luad_mean_gene_effect"]),float(row["other_lung_mean_gene_effect"]),float(row["non_lung_mean_gene_effect"])]
    labs=[f"LUAD\n(n={int(row['n_luad_models'])})",f"Other lung\n(n={int(row['n_other_lung_models'])})",f"Non-lung\n(n={int(row['n_non_lung_models'])})"]
    x=np.arange(3); ax.bar(x,vals,color=[ACCENT,"#9ec5f4","#c8d6e8"],width=0.62,zorder=3,edgecolor=SURF,linewidth=0.8); ax.axhline(-0.5,color=CRIT,lw=1.0,ls=(0,(4,3)))
    for xi,v in zip(x,vals): ax.text(xi,v+0.10,f"{v:.2f}",ha="center",va="bottom",fontsize=7.4,fontweight="bold",color="white")
    ax.set_xticks(x); ax.set_xticklabels(labs,fontsize=6.6); ax.set_ylabel("PLK1 mean CRISPR effect"); ax.set_title("Lineage (P=0.73)"); vgrid(ax); tidy(ax); plabel(ax,"b",dx=-0.30)
    ax=fig.add_subplot(gs[0,2])
    t40=load("Table40_DepMap_PLK1_ERO1A_selectivity_modulation")
    drug=t40[t40["evidence_layer"].astype(str).str.contains("expression_drug",na=False)].dropna(subset=["fdr"]).copy()
    drug["nlfdr"]=-np.log10(drug["fdr"].astype(float))
    for gene,col in [("PLK1",BLUE),("ERO1A",ORANGE)]:
        sub=drug[drug["expression_gene"]==gene]
        ax.scatter(sub["effect_or_correlation"],sub["nlfdr"],color=col,s=36,edgecolor=SURF,linewidth=0.7,label=gene,zorder=4)
    thr=-np.log10(0.05); ax.axhline(thr,color=CRIT,lw=1.0,ls=(0,(4,3)),zorder=2); ax.axvline(0,color=AXIS,lw=0.8)
    ax.text(0.0,thr+0.03,"FDR 0.05",color=CRIT,fontsize=6.2,ha="center",va="bottom")
    ax.set_ylim(0,thr+0.35); ax.set_xlim(-0.6,0.6)
    ax.set_xlabel("Spearman r (expr vs AUC)"); ax.set_ylabel("-log10 FDR"); ax.set_title("Drug: 0/12 FDR")
    vgrid(ax); tidy(ax); ax.legend(loc="upper right",fontsize=6.6,handletextpad=0.2)
    ax.text(0.5,0.04,"no ERO1A/PLK1 drug stratifier",transform=ax.transAxes,ha="center",va="bottom",fontsize=6.2,color=CRIT,style="italic")
    plabel(ax,"c",dx=-0.28)
    fig.suptitle("Figure 5  Functional prioritisation of PLK1 with explicit therapeutic boundaries",x=0.012,ha="left",fontsize=9.2,fontweight="bold",y=1.04)
    save(fig,"Figure5")

def figureS1():
    fig=plt.figure(figsize=(7.2,3.1)); gs=fig.add_gridspec(1,2,width_ratios=[1.0,1.15],wspace=0.5)
    ax=fig.add_subplot(gs[0,0])
    bars=[("HCC515","0.38",0.379,AQUA),("A549","0.05",0.053,MUTED),("PLK1-KD","-0.10",-0.095,CRIT),("ERO1A-KD","0.28",0.279,BLUE)]
    x=np.arange(len(bars)); vv=[b[2] for b in bars]; ax.bar(x,vv,color=[b[3] for b in bars],width=0.62,zorder=3,edgecolor=SURF,linewidth=0.8); ax.axhline(0,color=AXIS,lw=0.9)
    ax.set_ylim(-0.17,0.45)
    for xi,b in zip(x,bars): ax.text(xi,b[2]+(0.015 if b[2]>=0 else -0.015),b[1],ha="center",va="bottom" if b[2]>=0 else "top",fontsize=7,fontweight="bold",color=INK)
    ax.set_xticks(x); ax.set_xticklabels([b[0] for b in bars],fontsize=6.6)
    ax.set_ylabel("Signature Spearman rho (978 L1000 genes)"); ax.set_title("Context-dependent convergence"); vgrid(ax); tidy(ax); plabel(ax,"a",dx=-0.24)
    ax=fig.add_subplot(gs[0,1]); ax.axis("off"); ax.text(0.06,1.02,"Interpretation boundary",transform=ax.transAxes,fontsize=9,fontweight="bold",va="bottom")
    lines=[("Convergence only in HCC515","PLK1-KD and ERO1A-KD signatures overlap in HCC515 (rho=0.38) but not A549 (rho=0.05).",ORANGE),
           ("PLK1-KD not reproducible","The PLK1 knockdown signature does not reproduce across the two cell lines (rho=-0.10).",CRIT),
           ("Not a molecular interaction","Signature overlap is not interaction, epistasis, pathway ordering or drug synergy.",INK2)]
    yy=0.86
    for head,body,c in lines:
        ax.add_patch(Rectangle((0.0,yy-0.02),0.028,0.02,transform=ax.transAxes,color=c,clip_on=False))
        ax.text(0.06,yy,head,transform=ax.transAxes,fontsize=7.6,fontweight="bold",va="center",color=INK)
        ax.text(0.06,yy-0.10,body,transform=ax.transAxes,fontsize=6.7,va="top",color=INK2); yy-=0.32
    plabel(ax,"b",dx=-0.02)
    fig.suptitle("Additional file 1 (Supplementary Figure S1)  iLINCS/L1000 PLK1-ERO1A perturbation convergence",x=0.012,ha="left",fontsize=8.8,fontweight="bold",y=1.03)
    save(fig,"FigureS1")

def figureS2():
    fig=plt.figure(figsize=(7.2,3.1)); gs=fig.add_gridspec(1,2,width_ratios=[1.0,1.05],wspace=0.5)
    ax=fig.add_subplot(gs[0,0])
    bars=[("LUAD\nmodels",1.00,ACCENT),("Non-cancer\nmodels",1.00,"#c8d6e8")]; x=np.arange(2)
    ax.bar(x,[b[1] for b in bars],color=[b[2] for b in bars],width=0.56,zorder=3,edgecolor=SURF,linewidth=0.8)
    for xi,b in zip(x,bars): ax.text(xi,b[1]+0.01,f"{b[1]:.2f}",ha="center",va="bottom",fontsize=8,fontweight="bold",color=INK)
    ax.set_xticks(x); ax.set_xticklabels([b[0] for b in bars],fontsize=7); ax.set_ylim(0,1.15); ax.set_ylabel("PLK1 dependency fraction (effect < -0.5)"); ax.set_title("Pan-essential in both groups"); vgrid(ax); tidy(ax); plabel(ax,"a",dx=-0.26)
    ax=fig.add_subplot(gs[0,1]); ax.axis("off"); ax.text(0.06,1.02,"Normal-lung safety is untested",transform=ax.transAxes,fontsize=9,fontweight="bold",va="bottom")
    tiles=[("0","non-cancerous lung models with PLK1 CRISPR coverage",CRIT),("0","normal-lung models with PLK-inhibitor AUC coverage",CRIT),("n.s.","LUAD vs non-cancer PLK1 / ERO1A expression difference",MUTED)]
    yy=0.82
    for big,label,c in tiles:
        ax.text(0.04,yy,big,transform=ax.transAxes,fontsize=20,fontweight="bold",color=c,va="center")
        ax.text(0.28,yy,label,transform=ax.transAxes,fontsize=7.0,color=INK2,va="center"); yy-=0.30
    _=0; ax.text(0.04,0.03,"No therapeutic-window or normal-tissue safety claim is supported.",transform=ax.transAxes,fontsize=6.8,color=CRIT,style="italic"); plabel(ax,"b",dx=-0.02)
    fig.suptitle("Additional file 2 (Supplementary Figure S2)  PLK1 lacks a demonstrated LUAD-selective therapeutic window",x=0.012,ha="left",fontsize=8.6,fontweight="bold",y=1.03)
    save(fig,"FigureS2")

if __name__=="__main__":
    figure1(); figure2(); figure3(); figure4(); figure5(); figureS1(); figureS2(); print("ALL FIGURES DONE")
