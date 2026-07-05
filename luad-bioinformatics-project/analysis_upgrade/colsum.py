import numpy as np, pandas as pd, sys
from pathlib import Path
D=Path("/home/user/-----/luad-bioinformatics-project/analysis_upgrade/data/GSE131907")
cols=None; cs=None; n=0
for ch in pd.read_csv(D/"raw_UMI.txt.gz",sep="\t",index_col=0,chunksize=1500,dtype=np.int16):
    if cols is None: cols=ch.columns.to_numpy(); cs=np.zeros(len(cols),dtype=np.int64)
    cs+=ch.to_numpy().astype(np.int64).sum(axis=0); n+=len(ch)
    print(f"  {n} genes summed",flush=True)
np.save(D/"colsum.npy",cs)
pd.Series(cs,index=cols).to_csv(D/"colsum.csv")
print("COLSUM_DONE",n,"genes,",len(cols),"cells",flush=True)
