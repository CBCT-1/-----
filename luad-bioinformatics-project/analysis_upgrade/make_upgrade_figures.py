#!/usr/bin/env python3
"""New figures for the 5-weakness upgrade: single-cell, spatial deconvolution, nomogram."""
import numpy as np, pandas as pd, matplotlib as mpl
mpl.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from pathlib import Path
P=Path("/home/user/-----/luad-bioinformatics-project/analysis_upgrade/processed")
OUT=Path("/home/user/-----/luad-bioinformatics-project/bmc_genomics_v2_final/figures"); OUT.mkdir(parents=True,exist_ok=True)
BLUE="#2a78d6"; AQUA="#1baf7a"; VIOLET="#4a3aa7"; ORANGE="#eb6834"; GOOD="#0ca30c"; WARN="#fab219"; CRIT="#d03b3b"
INK="#0b0b0b"; INK2="#52514e"; MUTED="#898781"; GRID="#e1e0d9"; AXIS="#c3c2b7"; SURF="#ffffff"; ACCENT=BLUE; ACCENT2=ORANGE
mpl.rcParams.update({"figure.dpi":150,"savefig.dpi":400,"figure.facecolor":SURF,"axes.facecolor":SURF,"savefig.facecolor":SURF,
 "font.family":"DejaVu Sans","font.size":8.2,"axes.edgecolor":AXIS,"axes.linewidth":0.8,"axes.titlesize":9,"axes.titleweight":"bold",
 "axes.titlelocation":"left","axes.titlepad":5,"axes.labelcolor":INK2,"axes.labelsize":8,"xtick.color":MUTED,"ytick.color":MUTED,
 "xtick.labelsize":7.2,"ytick.labelsize":7.2,"text.color":INK,"axes.spines.top":False,"axes.spines.right":False,
 "xtick.major.width":0.8,"ytick.major.width":0.8,"legend.frameon":False,"legend.fontsize":7})
def plabel(ax,s,dx=-0.02,dy=1.07): ax.text(dx,dy,s,transform=ax.transAxes,fontsize=11,fontweight="bold",va="top",ha="right",color=INK)
def hgrid(ax): ax.grid(axis="x",color=GRID,lw=0.6,zorder=0); ax.set_axisbelow(True)
def vgrid(ax): ax.grid(axis="y",color=GRID,lw=0.6,zorder=0); ax.set_axisbelow(True)
def tidy(ax):
    for s in ("left","bottom"): ax.spines[s].set_color(AXIS)
def save(fig,stem):
    fig.savefig(OUT/f"{stem}.png",bbox_inches="tight",pad_inches=0.06); fig.savefig(OUT/f"{stem}.pdf",bbox_inches="tight",pad_inches=0.06)
    plt.close(fig); print("wrote",stem)
PROG=["PLK1","ERO1A","KNL1","DEPDC1B","TK1","DKK1","C1QTNF6","STEAP1","ECT2"]
def gc(g): return ACCENT if g=="PLK1" else ACCENT2 if g=="ERO1A" else "#c8d6e8"

# ================= Figure 6: single-cell =================
def fig_sc():
    de=pd.read_csv(P/"sc_malignant_vs_normal_pseudobulk.csv"); ct=pd.read_csv(P/"sc_celltype_expression.csv")
    sub=pd.read_csv(P/"sc_programme_by_epithelial_subtype.csv")
    fig=plt.figure(figsize=(7.4,5.7)); gs=fig.add_gridspec(2,2,height_ratios=[1.15,1],width_ratios=[1.25,1],hspace=0.55,wspace=0.5)
    # (a) DotPlot cell type x programme gene
    ax=fig.add_subplot(gs[0,0])
    cts=["Epithelial cells","T/NK cells","B lymphocytes","Myeloid cells","Fibroblasts","Endothelial cells","MAST cells"]
    ctp=ct[ct.gene.isin(PROG)].pivot(index="cell_type",columns="gene",values="mean_expr").reindex(cts)[PROG]
    ctpct=ct[ct.gene.isin(PROG)].pivot(index="cell_type",columns="gene",values="pct_expressing").reindex(cts)[PROG]
    vmax=np.nanmax(ctp.to_numpy())
    for i,cty in enumerate(cts):
        for j,g in enumerate(PROG):
            m=ctp.loc[cty,g]; pc=ctpct.loc[cty,g]
            ax.scatter(j,i,s=6+pc*3.2,c=[[*plt.cm.Blues(0.25+0.75*m/vmax)[:3]]],edgecolor="#00000022",linewidth=0.3,zorder=3)
    ax.set_xticks(range(len(PROG))); ax.set_xticklabels(PROG,rotation=45,ha="right",fontsize=6.6)
    ax.set_yticks(range(len(cts))); ax.set_yticklabels([c.replace(" cells","").replace(" lymphocytes","") for c in cts],fontsize=6.8)
    ax.set_title("Programme expression across cell types"); ax.set_xlim(-0.6,len(PROG)-0.4); ax.set_ylim(-0.6,len(cts)-0.4)
    ax.invert_yaxis(); ax.tick_params(length=0)
    for s in ax.spines.values(): s.set_visible(False)
    ax.legend(handles=[plt.scatter([],[],s=6+p*3.2,color=MUTED) for p in [10,30,50]],labels=["10%","30%","50%"],
              title="% expr",loc="upper right",bbox_to_anchor=(1.28,1.0),fontsize=6,title_fontsize=6,labelspacing=0.9)
    plabel(ax,"a",dx=-0.36)
    # (b) malignant vs normal epithelial diff
    ax=fig.add_subplot(gs[0,1]); de=de.set_index("gene").reindex(PROG).reset_index()
    de["diff"]=de["sample_level_diff"]
    y=np.arange(len(de))[::-1]
    ax.barh(y,de["diff"],color=[gc(g) for g in de.gene],height=0.7,zorder=3,edgecolor=SURF,linewidth=0.5)
    ax.set_yticks(y); ax.set_yticklabels(de.gene,fontsize=6.8)
    for lbl,g in zip(ax.get_yticklabels(),de.gene):
        if g in("PLK1","ERO1A"): lbl.set_fontweight("bold"); lbl.set_color(INK)
    ax.set_xlabel("tumour − normal-lung sample\nΔ mean expr (pseudobulk)"); ax.set_title("Malignant-epithelial enrichment")
    hgrid(ax); tidy(ax)
    ax.text(0.97,0.03,"9/9 genes FDR<0.05\n(36 vs 11 samples)",transform=ax.transAxes,ha="right",va="bottom",fontsize=6.0,color=GOOD,style="italic")
    plabel(ax,"b",dx=-0.30)
    # (c) programme by epithelial subtype
    ax=fig.add_subplot(gs[1,0]); sub=sub.rename(columns={sub.columns[0]:"subtype"})
    sub=sub.sort_values("prog",ascending=True)
    cols=[CRIT if s=="Malignant cells" else WARN if str(s).startswith("tS") else "#c8d6e8" for s in sub.subtype]
    y=np.arange(len(sub)); ax.barh(y,sub["prog"],color=cols,height=0.7,zorder=3,edgecolor=SURF,linewidth=0.5)
    ax.set_yticks(y); ax.set_yticklabels(sub.subtype,fontsize=6.6)
    ax.set_xlabel("mean programme score"); ax.set_title("Programme peaks in malignant states"); hgrid(ax); tidy(ax)
    ax.legend(handles=[Rectangle((0,0),1,1,color=CRIT),Rectangle((0,0),1,1,color=WARN),Rectangle((0,0),1,1,color="#c8d6e8")],
              labels=["malignant","tumour-transitional","normal epithelial"],loc="lower right",fontsize=6,handlelength=1,handleheight=1)
    plabel(ax,"c",dx=-0.42)
    # (d) programme vs proliferation
    ax=fig.add_subplot(gs[1,1])
    bars=[("PLK1 vs MKI67",0.471,ACCENT),("Programme\nvs MKI67",0.268,BLUE)]
    x=np.arange(len(bars)); ax.bar(x,[b[1] for b in bars],color=[b[2] for b in bars],width=0.55,zorder=3,edgecolor=SURF,linewidth=0.8)
    for xi,b in zip(x,bars): ax.text(xi,b[1]+0.008,f"{b[1]:.2f}",ha="center",va="bottom",fontsize=7.6,fontweight="bold",color=INK)
    ax.set_xticks(x); ax.set_xticklabels([b[0] for b in bars],fontsize=6.8); ax.set_ylim(0,0.55)
    ax.set_ylabel("Spearman ρ (epithelial cells)"); ax.set_title("Linked to proliferation"); vgrid(ax); tidy(ax)
    ax.text(0.97,0.96,"all P≈0",transform=ax.transAxes,ha="right",va="top",fontsize=6.2,color=INK2,style="italic")
    plabel(ax,"d",dx=-0.30)
    fig.suptitle("Figure 6  Single-cell (GSE131907, 208,506 cells): the programme is enriched in malignant epithelial cells",
                 x=0.012,ha="left",fontsize=9.0,fontweight="bold",y=0.99)
    save(fig,"Figure6_singlecell")

# ================= Figure 7: spatial deconvolution =================
def fig_deconv():
    co=pd.read_csv(P/"spatial_deconv_programme_colocalisation.csv"); sec=pd.read_csv(P/"spatial_deconv_leaveout_section.csv").rename(columns={"rho_leaveout":"rho_programme_vs_epithelial"})
    fig=plt.figure(figsize=(7.2,3.1)); gs=fig.add_gridspec(1,2,width_ratios=[1.1,1.05],wspace=0.5)
    ax=fig.add_subplot(gs[0,0]); co=co.sort_values("spearman_rho")
    cols=[ACCENT if "Epithel" in c else (AQUA if r>0 else CRIT) for c,r in zip(co.cell_type,co.spearman_rho)]
    y=np.arange(len(co)); ax.barh(y,co.spearman_rho,color=cols,height=0.7,zorder=3,edgecolor=SURF,linewidth=0.5); ax.axvline(0,color=AXIS,lw=0.9)
    ax.set_yticks(y); ax.set_yticklabels([c.replace(" cells","").replace(" lymphocytes","") for c in co.cell_type],fontsize=6.8)
    for lbl,c in zip(ax.get_yticklabels(),co.cell_type):
        if "Epithel" in c: lbl.set_fontweight("bold"); lbl.set_color(INK)
    ax.set_xlabel("Spearman ρ  (programme score vs cell-type abundance)"); ax.set_title("Programme co-localises with epithelium"); hgrid(ax); tidy(ax)
    plabel(ax,"a",dx=-0.40)
    ax=fig.add_subplot(gs[0,1]); sec=sec.sort_values("rho_programme_vs_epithelial")
    cols=[ACCENT if t else "#9ec5f4" for t in sec.is_tumor]
    ax.barh(np.arange(len(sec)),sec.rho_programme_vs_epithelial,color=cols,height=0.8,zorder=3,edgecolor=SURF,linewidth=0.4); ax.axvline(0,color=AXIS,lw=0.9)
    ax.set_yticks([]); ax.set_xlabel("per-section ρ (programme vs epithelial)")
    ax.set_title("Leave-programme-out: 21/22 sections, 5/5 patients"); hgrid(ax); tidy(ax)
    ax.legend(handles=[Rectangle((0,0),1,1,color=ACCENT),Rectangle((0,0),1,1,color="#9ec5f4")],labels=["tumour section","adjacent section"],
              loc="upper left",fontsize=6.4,handlelength=1,handleheight=1)
    ax.text(0.97,0.05,f"median ρ={sec.rho_programme_vs_epithelial.median():.2f}\n5/5 patients positive",transform=ax.transAxes,ha="right",va="bottom",fontsize=6.2,color=INK2)
    plabel(ax,"b",dx=-0.06)
    fig.suptitle("Figure 7  Reference-based Visium deconvolution (22 sections from 5 patients; programme genes excluded from signature)",
                 x=0.012,ha="left",fontsize=9.0,fontweight="bold",y=1.03)
    save(fig,"Figure7_spatial_deconv")

# ================= Figure 8: nomogram =================
def fig_nomo():
    ci=pd.read_csv(P/"nomogram_proper_cindex.csv"); inc=pd.read_csv(P/"nomogram_incremental.csv"); cal=pd.read_csv(P/"nomogram_calibration_3yr.csv")
    order=["clinical_only","gene_only","combined"]; lab={"clinical_only":"clinical\n(stage+age+sex)","gene_only":"gene\nscore","combined":"combined"}
    ci=ci.set_index("model").reindex(order).reset_index()
    fig=plt.figure(figsize=(7.4,3.1)); gs=fig.add_gridspec(1,3,width_ratios=[1.15,1,1],wspace=0.55)
    # (a) 3 models test C-index with 95% CI
    ax=fig.add_subplot(gs[0,0]); x=np.arange(3)
    cols=[MUTED,"#9ec5f4",ACCENT]
    ax.bar(x,ci.test_c_index,color=cols,width=0.6,zorder=3,edgecolor=SURF,linewidth=0.8)
    ax.errorbar(x,ci.test_c_index,yerr=[ci.test_c_index-ci.ci95_low,ci.ci95_high-ci.test_c_index],fmt="none",ecolor=INK2,elinewidth=1.1,capsize=3,zorder=4)
    for xi,v in zip(x,ci.test_c_index): ax.text(xi,v+0.02,f"{v:.2f}",ha="center",va="bottom",fontsize=7,fontweight="bold",color=INK)
    ax.axhline(0.5,color=CRIT,lw=0.9,ls=(0,(3,3)))
    ax.set_xticks(x); ax.set_xticklabels([lab[m] for m in order],fontsize=6.4); ax.set_ylim(0.5,0.85); ax.set_ylabel("held-out test C-index")
    ax.set_title("Discrimination by model"); vgrid(ax); tidy(ax); plabel(ax,"a",dx=-0.34)
    # (b) incremental value
    ax=fig.add_subplot(gs[0,1])
    d=float(inc.delta_c_combined_minus_clinical[0]); lo=float(inc.ci_low[0]); hi=float(inc.ci_high[0])
    ax.axhline(0,color=CRIT,lw=1.0,ls=(0,(4,3)))
    ax.errorbar([0],[d],yerr=[[d-lo],[hi-d]],fmt="o",color=ACCENT,markersize=9,markeredgecolor=SURF,elinewidth=1.6,capsize=5,zorder=4)
    ax.text(0,hi+0.006,f"ΔC = {d:+.3f}",ha="center",va="bottom",fontsize=8,fontweight="bold",color=INK)
    ax.set_xlim(-0.6,0.6); ax.set_xticks([]); ax.set_ylim(min(-0.12,lo-0.02),max(0.12,hi+0.04))
    ax.set_ylabel("ΔC-index (combined − clinical)")
    ax.set_title("No incremental discrimination"); vgrid(ax); tidy(ax)
    ax.text(0.5,0.03,f"95% CI crosses 0\nbut LR p={float(inc.LR_p[0]):.0e} (independent)",transform=ax.transAxes,ha="center",va="bottom",fontsize=6.0,color=INK2,style="italic")
    plabel(ax,"b",dx=-0.34)
    # (c) calibration (honest: over-prediction)
    ax=fig.add_subplot(gs[0,2])
    ax.plot([0,0.7],[0,0.7],color=MUTED,lw=1,ls=(0,(3,3)),zorder=2)
    ax.plot(cal.mean_predicted_3yr_risk,cal.observed_3yr_event_rate,"-o",color=ACCENT,lw=1.8,markersize=7,markeredgecolor=SURF,zorder=4)
    for _,r in cal.iterrows(): ax.annotate(r.risk_tertile,(r.mean_predicted_3yr_risk,r.observed_3yr_event_rate),textcoords="offset points",xytext=(6,-7),fontsize=6,color=INK2)
    ax.set_xlim(0,0.7); ax.set_ylim(0,0.7); ax.set_xlabel("predicted 3-yr risk"); ax.set_ylabel("observed 3-yr rate")
    ax.set_title("Calibration (over-predicts)"); ax.grid(color=GRID,lw=0.6); ax.set_axisbelow(True); tidy(ax); plabel(ax,"c",dx=-0.34)
    fig.suptitle("Figure 8  Incremental prognostic assessment: the score is independent but does not improve discrimination over clinical staging (TCGA-LUAD)",
                 x=0.012,ha="left",fontsize=8.2,fontweight="bold",y=1.03)
    save(fig,"Figure8_nomogram")

fig_sc(); fig_deconv(); fig_nomo(); print("UPGRADE_FIGURES_DONE")
