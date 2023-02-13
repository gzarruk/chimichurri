import pandas as pd
import numpy as np


def vma(series: pd.Series, periods: int = 38) -> pd.Series:
    """Variable Moving Average.

    This moving average is designed to become flat (constant value) when the data
    within the lookup window does not vary significantly. It can also be state detector. The calculation is based on
    the variability of the signal in a lookup window.

    Args:
        series (pandas.Series): Time series.
        periods (int, optional): Lookup window.
            Window length in data points used to estimate the variability of the signal.

    Returns:
        pandas.Series: Moving average.
        If the results has the same value as the previous moving average result, the signal can be considered to
        be on steady state.
    """
    k = 1.0 / periods
    N = len(series)

    # Estimate iS:
    diff = np.diff(series)
    iS = _estimate_iS(diff, k, N)

    # Estimate hhv, llv, vI:
    iS_df = (
        pd.Series(iS, index=series.index)
        .rolling(periods, min_periods=1)
        .aggregate(["min", "max"])
        .fillna(0)
    )
    hhv, llv = iS_df["max"], iS_df["min"]
    vI = (iS - llv) / (hhv - llv)

    # Finally, estimate variable moving average:
    return pd.Series(_estimate_vma(vI.values, series.values, k, N), index=series.index)


def _estimate_iS(diff, k, N):
    # Estimate pdm and mdm:
    pdm, mdm = np.zeros(N), np.zeros(N)
    pdm[1:] = np.maximum(diff, 0)
    mdm[1:] = np.maximum(-diff, 0)
    # Estimate pdmS, mdmS:
    pdmS, mdmS = np.zeros(N), np.zeros(N)
    for i in range(1, N):
        pdmS[i] = (1 - k) * pdmS[i - 1] + k * pdm[i]
        mdmS[i] = (1 - k) * mdmS[i - 1] + k * mdm[i]
    pdi, mdi = np.zeros(N), np.zeros(N)
    s = mdmS + pdmS
    pdi[1:] = pdmS[1:] / s[1:]
    mdi[1:] = mdmS[1:] / s[1:]
    # Estimate pdiS, mdiS, d, s1:
    pdiS, mdiS = np.zeros(N), np.zeros(N)
    for i in range(1, N):
        pdiS[i] = (1 - k) * pdiS[i - 1] + k * pdi[i]
        mdiS[i] = (1 - k) * mdiS[i - 1] + k * mdi[i]
    d = np.abs(pdiS - mdiS)
    s1 = pdiS + mdiS
    # Estimate iS:
    iS = np.zeros(N)
    for i in range(1, N):
        iS[i] = (1 - k) * iS[i - 1] + k * d[i] / s1[i]
    return iS


def _estimate_vma(vI, arr, k, N):
    vma = np.zeros(N)
    for i in range(1, N):
        vma[i] = (1 - k * vI[i]) * vma[i - 1] + k * vI[i] * arr[i]
    return vma
