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
    de=pd.read_csv(P/"sc_malignant_vs_normal_epi.csv"); ct=pd.read_csv(P/"sc_celltype_expression.csv")
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
    y=np.arange(len(de))[::-1]
    ax.barh(y,de["diff"],color=[gc(g) for g in de.gene],height=0.7,zorder=3,edgecolor=SURF,linewidth=0.5)
    ax.set_yticks(y); ax.set_yticklabels(de.gene,fontsize=6.8)
    for lbl,g in zip(ax.get_yticklabels(),de.gene):
        if g in("PLK1","ERO1A"): lbl.set_fontweight("bold"); lbl.set_color(INK)
    ax.set_xlabel("malignant − normal epithelial\nΔ mean expr"); ax.set_title("Malignant-cell enrichment")
    hgrid(ax); tidy(ax)
    ax.text(0.97,0.03,"all 9 genes P<1e-20",transform=ax.transAxes,ha="right",va="bottom",fontsize=6.2,color=GOOD,style="italic")
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
    fig.suptitle("Figure 6  Single-cell (GSE131907, 208,506 cells): the programme is malignant-epithelial-specific",
                 x=0.012,ha="left",fontsize=9.0,fontweight="bold",y=0.99)
    save(fig,"Figure6_singlecell")

# ================= Figure 7: spatial deconvolution =================
def fig_deconv():
    co=pd.read_csv(P/"spatial_deconv_programme_colocalisation.csv"); sec=pd.read_csv(P/"spatial_deconv_section_consistency.csv")
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
    ax.set_title("Positive in 22/22 sections"); hgrid(ax); tidy(ax)
    ax.legend(handles=[Rectangle((0,0),1,1,color=ACCENT),Rectangle((0,0),1,1,color="#9ec5f4")],labels=["tumour section","adjacent section"],
              loc="upper left",fontsize=6.4,handlelength=1,handleheight=1)
    ax.text(0.97,0.05,f"mean ρ={sec.rho_programme_vs_epithelial.mean():.2f}",transform=ax.transAxes,ha="right",va="bottom",fontsize=6.4,color=INK2)
    plabel(ax,"b",dx=-0.06)
    fig.suptitle("Figure 7  Reference-based Visium deconvolution (real GSE131907 single-cell reference, 22 sections)",
                 x=0.012,ha="left",fontsize=9.0,fontweight="bold",y=1.03)
    save(fig,"Figure7_spatial_deconv")

# ================= Figure 8: nomogram =================
def fig_nomo():
    ci=pd.read_csv(P/"nomogram_cindex.csv"); ta=pd.read_csv(P/"nomogram_timeAUC.csv"); cal=pd.read_csv(P/"nomogram_calibration_3yr.csv")
    fig=plt.figure(figsize=(7.4,3.1)); gs=fig.add_gridspec(1,3,width_ratios=[1,1.05,1],wspace=0.55)
    # (a) C-index
    ax=fig.add_subplot(gs[0,0]); x=np.arange(2); w=0.36
    ax.bar(x-w/2,ci.c_index_all,w,color="#9ec5f4",zorder=3,edgecolor=SURF,linewidth=0.7,label="all TCGA")
    ax.bar(x+w/2,ci.c_index_test,w,color=ACCENT,zorder=3,edgecolor=SURF,linewidth=0.7,label="held-out test")
    ax.axhline(0.70,color=GOOD,lw=1.0,ls=(0,(4,3))); ax.text(1.4,0.705,"0.70",color=GOOD,fontsize=6,va="bottom",ha="right")
    for xi,va,vt in zip(x,ci.c_index_all,ci.c_index_test):
        ax.text(xi-w/2,va+0.006,f"{va:.2f}",ha="center",va="bottom",fontsize=6.4,color=INK2)
        ax.text(xi+w/2,vt+0.006,f"{vt:.2f}",ha="center",va="bottom",fontsize=6.4,fontweight="bold",color=INK)
    ax.set_xticks(x); ax.set_xticklabels(["gene\nscore","+clinical\nnomogram"],fontsize=6.8); ax.set_ylim(0.5,0.80); ax.set_ylabel("Harrell C-index")
    ax.set_title("Nomogram lifts C-index"); vgrid(ax); tidy(ax); ax.legend(loc="upper left",fontsize=6)
    plabel(ax,"a",dx=-0.34)
    # (b) time-AUC
    ax=fig.add_subplot(gs[0,1]); x=np.arange(3)
    ax.plot(x,ta.nomogram_AUC,"-o",color=ACCENT,lw=2,markersize=6,markeredgecolor=SURF,label="nomogram",zorder=4)
    ax.plot(x,ta.risk_only_AUC,"-o",color=MUTED,lw=2,markersize=6,markeredgecolor=SURF,label="gene score",zorder=3)
    for xi,v in zip(x,ta.nomogram_AUC): ax.text(xi,v+0.012,f"{v:.2f}",ha="center",va="bottom",fontsize=6.4,fontweight="bold",color=ACCENT)
    ax.set_xticks(x); ax.set_xticklabels(ta.horizon,fontsize=7); ax.set_ylim(0.6,0.82); ax.set_ylabel("time-dependent AUC")
    ax.set_title("Discrimination over time"); vgrid(ax); tidy(ax); ax.legend(loc="lower left",fontsize=6.3)
    plabel(ax,"b",dx=-0.28)
    # (c) calibration
    ax=fig.add_subplot(gs[0,2])
    ax.plot([0,0.7],[0,0.7],color=MUTED,lw=1,ls=(0,(3,3)),zorder=2)
    ax.plot(cal.mean_predicted_3yr_risk,cal.observed_3yr_event_rate,"-o",color=ACCENT,lw=1.8,markersize=7,markeredgecolor=SURF,zorder=4)
    for _,r in cal.iterrows(): ax.annotate(r.risk_tertile,(r.mean_predicted_3yr_risk,r.observed_3yr_event_rate),
        textcoords="offset points",xytext=(6,-7),fontsize=6,color=INK2)
    ax.set_xlim(0,0.7); ax.set_ylim(0,0.7); ax.set_xlabel("predicted 3-yr event risk"); ax.set_ylabel("observed 3-yr event rate")
    ax.set_title("Calibration (3-year)"); ax.grid(color=GRID,lw=0.6); ax.set_axisbelow(True); tidy(ax)
    plabel(ax,"c",dx=-0.32)
    fig.suptitle("Figure 8  Clinical utility: a risk-score + clinical nomogram (TCGA-LUAD, n=557)",
                 x=0.012,ha="left",fontsize=9.0,fontweight="bold",y=1.03)
    save(fig,"Figure8_nomogram")

fig_sc(); fig_deconv(); fig_nomo(); print("UPGRADE_FIGURES_DONE")
