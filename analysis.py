import numpy as np
import pandas as pd
from database import SUBJECTS

# Database stores lowercase column names; SUBJECTS holds display names.
SUBJ_LIST  = [s.lower() for s in SUBJECTS]
SUBJ_LABEL = {s.lower(): s for s in SUBJECTS}


def to_df(records: list) -> pd.DataFrame:
    if not records:
        return pd.DataFrame()
    df = pd.DataFrame(records)
    marks = df[SUBJ_LIST].to_numpy(dtype=float)
    df["total"]      = marks.sum(axis=1)
    df["percentage"] = np.round(marks.sum(axis=1) / len(SUBJ_LIST), 2)
    df["result"]     = np.where(df["percentage"] >= 40, "Pass", "Fail")
    df["grade"]      = np.select(
        [df["percentage"] >= 90, df["percentage"] >= 75,
         df["percentage"] >= 60, df["percentage"] >= 40],
        ["A+", "A", "B", "C"], default="F")
    df["rank"]       = df["total"].rank(method="min", ascending=False).astype(int)
    return df


def stats(df: pd.DataFrame) -> dict:
    if df.empty:
        return {"students": 0, "avg": 0, "high": 0, "low": 0,
                "pass_rate": 0,
                "subject_avg": {SUBJ_LABEL[s]: 0 for s in SUBJ_LIST},
                "top": None}
    marks = df[SUBJ_LIST].to_numpy(dtype=float)
    top = df.loc[df["total"].idxmax()].to_dict()
    return {
        "students":    int(len(df)),
        "avg":         round(float(np.mean(df["percentage"])), 2),
        "high":        round(float(np.max(df["percentage"])), 2),
        "low":         round(float(np.min(df["percentage"])), 2),
        "pass_rate":   round(float((df["result"] == "Pass").mean() * 100), 2),
        "subject_avg": {SUBJ_LABEL[s]: round(float(np.mean(marks[:, i])), 2)
                        for i, s in enumerate(SUBJ_LIST)},
        "subject_high": {SUBJ_LABEL[s]: float(np.max(marks[:, i]))
                        for i, s in enumerate(SUBJ_LIST)},
        "subject_low":  {SUBJ_LABEL[s]: float(np.min(marks[:, i]))
                        for i, s in enumerate(SUBJ_LIST)},
        "top":         top,
    }


def export_csv(df: pd.DataFrame, path: str):
    df.to_csv(path, index=False)


def class_wise_summary(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    return (df.groupby("klass")
              .agg(students=("id", "count"),
                   avg_pct=("percentage", "mean"),
                   avg_total=("total", "mean"),
                   pass_rate=("result", lambda s: (s == "Pass").mean() * 100))
              .round(2)
              .reset_index())