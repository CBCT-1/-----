import numpy as np, pandas as pd, matplotlib as mpl
mpl.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from pathlib import Path
P=Path("processed"); OUT=Path("/home/user/-----/luad-bioinformatics-project/bmc_genomics_v2_final/figures")
BLUE="#2a78d6"; ACCENT=BLUE; WARN="#fab219"; CRIT="#d03b3b"; MUTED="#898781"; INK="#0b0b0b"; INK2="#52514e"; GRID="#e1e0d9"; AXIS="#c3c2b7"; SURF="#ffffff"
mpl.rcParams.update({"savefig.dpi":400,"figure.facecolor":SURF,"axes.facecolor":SURF,"savefig.facecolor":SURF,"font.family":"DejaVu Sans","font.size":8.2,
 "axes.edgecolor":AXIS,"axes.linewidth":0.8,"axes.titlesize":9,"axes.titleweight":"bold","axes.titlelocation":"left","axes.labelcolor":INK2,"axes.labelsize":8,
 "xtick.color":MUTED,"ytick.color":MUTED,"xtick.labelsize":7.2,"ytick.labelsize":7.2,"axes.spines.top":False,"axes.spines.right":False,"legend.frameon":False,"legend.fontsize":7})
def plabel(ax,s,dx=-0.02,dy=1.07): ax.text(dx,dy,s,transform=ax.transAxes,fontsize=11,fontweight="bold",va="top",ha="right",color=INK)
def tidy(ax):
    for sp in ("left","bottom"): ax.spines[sp].set_color(AXIS)
geo=pd.read_csv(P/"clean_model_geo_external.csv")
fig=plt.figure(figsize=(7.3,3.2)); gs=fig.add_gridspec(1,2,width_ratios=[0.85,1.25],wspace=0.42)
# (a) internal train/test
ax=fig.add_subplot(gs[0,0]); x=np.arange(2); vals=[0.672,0.623]; lo=[np.nan,0.529]; hi=[np.nan,0.717]
ax.bar(x,vals,color=["#9ec5f4",ACCENT],width=0.6,zorder=3,edgecolor=SURF,linewidth=0.8)
ax.errorbar([1],[0.623],yerr=[[0.623-0.529],[0.717-0.623]],fmt="none",ecolor=INK2,elinewidth=1.2,capsize=4,zorder=4)
ax.axhline(0.5,color=CRIT,lw=0.9,ls=(0,(3,3)))
for xi,v in zip(x,vals): ax.text(xi,v+0.012,f"{v:.2f}",ha="center",va="bottom",fontsize=8,fontweight="bold",color=INK)
ax.set_xticks(x); ax.set_xticklabels(["train\n(n=352)","held-out test\n(n=151)"],fontsize=6.9); ax.set_ylim(0.5,0.82); ax.set_ylabel("Harrell C-index")
ax.set_title("Patient-level model"); ax.grid(axis="y",color=GRID,lw=0.6); ax.set_axisbelow(True); tidy(ax)
ax.text(0.5,0.03,"0 genes pass genome-wide\nFDR (train-only screen)",transform=ax.transAxes,ha="center",va="bottom",fontsize=6.2,color=CRIT,style="italic")
plabel(ax,"a",dx=-0.30)
# (b) external transfer with CI
ax=fig.add_subplot(gs[0,1])
g=geo.dropna(subset=["c_index"]).copy()
order=["GSE31210","GSE50081","GSE30219","GSE68465","GSE37745"]; g=g.set_index("cohort").reindex([c for c in order if c in g.cohort.values]).reset_index()
y=np.arange(len(g))[::-1]
for yi,(_,r) in zip(y,g.iterrows()):
    col=ACCENT if r["independent"] else MUTED
    ax.plot([r.c_lo,r.c_hi],[yi,yi],color=col,lw=2,solid_capstyle="round",zorder=3)
    ax.scatter([r.c_index],[yi],s=32,color=col,zorder=4,edgecolor=SURF,linewidth=0.7)
ax.axvline(0.5,color=CRIT,lw=1.0,zorder=2)
labs=[f"{r.cohort}{' *' if r['independent'] else ''}  (n={int(r.n)})" for _,r in g.iterrows()]
ax.set_yticks(y); ax.set_yticklabels(labs,fontsize=7)
ax.set_xlim(0.45,0.8); ax.set_xlabel("External transfer C-index (95% CI)")
ax.set_title("Weak, inconsistent external transfer"); ax.grid(axis="x",color=GRID,lw=0.6); ax.set_axisbelow(True); tidy(ax)
for yi,(_,r) in zip(y,g.iterrows()): ax.text(0.79,yi,f"C={r.c_index:.2f}",fontsize=6.3,va="center",ha="right",color=INK2)
ax.legend(handles=[Line2D([0],[0],color=ACCENT,lw=2,marker="o",markersize=5,markeredgecolor=SURF),Line2D([0],[0],color=MUTED,lw=2,marker="o",markersize=5,markeredgecolor=SURF)],
          labels=["independent of selection","informed selection"],loc="lower right",fontsize=6.3)
plabel(ax,"b",dx=-0.16)
fig.suptitle("Figure 2  Patient-level rebuild: no genome-wide-significant gene; a nominal signature transfers weakly",x=0.012,ha="left",fontsize=8.8,fontweight="bold",y=1.02)
fig.savefig(OUT/"Figure2.png",bbox_inches="tight",pad_inches=0.06); fig.savefig(OUT/"Figure2.pdf",bbox_inches="tight",pad_inches=0.06)
print("wrote clean Figure2")
