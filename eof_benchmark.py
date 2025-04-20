# eof_benchmark.py
# ---------------------------------------------------------------
# Minimal downstream application: EOF-based hindcast skill test
# Works with any decomposition   A ≈ U @ np.diag(S) @ VT
# ---------------------------------------------------------------
import time
import numpy as np
import xarray as xr
from scipy.stats import pearsonr

# ---- user‑set parameters --------------------------------------
P       = 10          # number of EOF modes to retain
TRAIN_YEARS = slice("1980-01-01", "2010-12-31")
TEST_YEARS  = slice("2011-01-01", "2022-12-31")
region = dict(lat=slice(10, -10), lon=slice(90, 130))

# ---------------------------------------------------------------

def target_slp(ds_slp, region):
    box = ds_slp.sel(**region)
    clim = box.groupby("time.dayofyear").mean("time")
    anom = box.groupby("time.dayofyear") - clim
    return anom.mean(("lat", "lon")).to_dataframe()["msl"]


def eof_hindcast(U, S, VT, times, target_series, p=P):
    """
    Compute EOF PCs from (U,S,VT), train linear mapping on TRAIN_YEARS,
    predict on TEST_YEARS, and return correlation skill.
    """
    # 1. build PCs  (p × n_time)
    PCs = (np.diag(S[:p]) @ VT[:p, :])          # shape (p, n)
    # 2. split train/test
    idx_train = (times >= TRAIN_YEARS.start) & (times <= TRAIN_YEARS.stop)
    idx_test  = (times >= TEST_YEARS.start)  & (times <= TEST_YEARS.stop)
    X_train, y_train = PCs[:, idx_train].T, target_series[idx_train]
    X_test,  y_test  = PCs[:, idx_test ].T, target_series[idx_test ]
    # 3. ordinary least‑squares fit   y ≈ X β
    beta, *_ = np.linalg.lstsq(X_train, y_train, rcond=None)
    y_pred   = X_test @ beta
    # 4. skill metric
    skill, _ = pearsonr(y_test, y_pred)
    return skill

def run_eof_benchmark(U, S, VT, ds_slp):
    """
    Wrapper that measures wall‑clock time for EOF analysis
    and returns (skill, elapsed_seconds).
    """
    tic = time.time()
    series = target_slp(ds_slp, region)
    skill = eof_hindcast(U, S, VT,
                         ds_slp["time"].values.astype("datetime64[D]"),
                         nino_series.values)
    return skill, time.time() - tic
