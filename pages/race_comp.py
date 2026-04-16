import os
import math
import streamlit as st
import pandas as pd
import numpy as np
from custom import top_menu, bottom_head
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

top_menu()


# Folder that contains the CSV files. Change if needed.
DATA_DIR = "Data/WorldChamp/M"

YEARS = list(range(2003, 2026))          # 2003 – 2025
DISCIPLINE_COLORS = {
    "Swim":  "#38bdf8",   # sky blue
    "T1":    "#a78bfa",   # violet
    "Bike":  "#34d399",   # emerald
    "T2":    "#fb923c",   # orange
    "Run":   "#f87171",   # red
}
ATHLETE_PALETTE = ["#10b981", "#3b82f6", "#f97316", "#a855f7"]


##############
    #FUNCTIONS

def parse_time(t) -> float:
    """HH:MM:SS → seconds. Returns NaN for zeros / invalid / DNF."""
    s = str(t).strip() if not pd.isna(t) else ""
    if s in ("", "00:0:0", "0:0:0", "nan"):
        return np.nan
    try:
        parts = s.split(":")
        if len(parts) == 3:
            total = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        elif len(parts) == 2:
            total = int(parts[0]) * 60 + int(parts[1])
        else:
            return np.nan
        return float(total) if total > 0 else np.nan
    except Exception:
        return np.nan


def hms(seconds) -> str:
    """seconds → H:MM:SS"""
    if pd.isna(seconds):
        return "N/A"
    seconds = int(round(seconds))
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h}:{m:02d}:{s:02d}"


def hm(seconds) -> str:
    """seconds → H:MM"""
    if pd.isna(seconds):
        return "N/A"
    seconds = int(round(seconds))
    h = seconds // 3600
    m = (seconds % 3600) // 60
    return f"{h}:{m:02d}"


def pace_per_km(seconds, km) -> str:
    """seconds for a leg → MM:SS/km pace string"""
    if pd.isna(seconds) or km == 0:
        return "N/A"
    pace = seconds / km
    m = int(pace // 60)
    s = int(round(pace % 60))
    return f"{m}:{s:02d}/km"


def speed_kmh(seconds, km) -> str:
    if pd.isna(seconds) or seconds == 0:
        return "N/A"
    return f"{(km / seconds * 3600):.1f} km/h"


def percentile_rank(value, series) -> float:
    """Percentile of 'value' within 'series' (lower time → higher percentile)."""
    valid = series.dropna()
    if len(valid) == 0:
        return 50.0
    return round(float((valid > value).sum() / len(valid) * 100), 1)

# ─── Data Loading ─────────────────────────────────────────────────────────────

@st.cache_data(show_spinner="Loading race data …")
def load_data() -> pd.DataFrame:
    frames = []
    for year in YEARS:
        for code in ("M", "F"):
            path = os.path.join(DATA_DIR, f"IM{year}_{code}.csv")
            if not os.path.exists(path):
                continue
            try:
                df = pd.read_csv(path, low_memory=False)
                df["Year"] = year
                df["FileGender"] = code
                frames.append(df)
            except Exception as e:
                st.warning(f"Could not read {path}: {e}")

    if not frames:
        st.error(
            "No CSV files found. Place IM2003_F.csv … IM2026_M.csv "
            f"in: {DATA_DIR}"
        )
        st.stop()

    raw = pd.concat(frames, ignore_index=True)

    # ── Parse times to seconds ──────────────────────────────────────────────
    time_map = {
        "Overall Time":       "Overall_sec",
        "Swim Time":          "Swim_sec",
        "Bike Time":          "Bike_sec",
        "Run Time":           "Run_sec",
        "Transition 1 Time":  "T1_sec",
        "Transition 2 Time":  "T2_sec",
    }
    for col, sec_col in time_map.items():
        if col in raw.columns:
            raw[sec_col] = raw[col].apply(parse_time)

    # ── Keep finishers with valid overall time ───────────────────────────────
    raw = raw[raw["Finish"] == "FIN"].copy()
    raw = raw[raw["Overall_sec"].notna() & (raw["Overall_sec"] > 0)].copy()

    # ── Derive gender from Division prefix (more reliable than Gender col) ───
    def div_gender(div):
        d = str(div).upper()
        if d.startswith("F"):
            return "Female"
        if d.startswith("M"):
            return "Male"
        return "Unknown"

    raw["Gender_clean"] = raw["Division"].apply(div_gender)

    # ── Normalise age-group labels  ──────────────────────────────────────────
    def clean_div(div):
        d = str(div).strip()
        if d in ("MPRO", "FPRO"):
            return "PRO"
        return d.replace("M", "").replace("F", "").strip() if d not in ("Male", "Female") else d

    raw["AgeGroup"] = raw["Division"].apply(clean_div)

    # ── Derived numeric columns ──────────────────────────────────────────────
    raw["Total_min"] = raw["Overall_sec"] / 60
    raw["Total_hr"]  = raw["Overall_sec"] / 3600

    # ── Percentile within year × gender × age-group ─────────────────────────
    # (computed lazily per query to avoid huge upfront cost)

    raw.reset_index(drop=True, inplace=True)
    return raw


df_all = load_data()
df = df_all
##########



st.header("Race Intelligence Dashboard")

if df.empty:
    st.warning("No data matches the current filters.")
else:
    # ── KPI Cards ────────────────────────────────────────────────────────
    n_fin     = len(df)
    avg_total = df["Overall_sec"].mean()
    best_time = df["Overall_sec"].min()
    worst_time= df["Overall_sec"].max()
    avg_swim  = df["Swim_sec"].dropna().mean()
    avg_bike  = df["Bike_sec"].dropna().mean()
    avg_run   = df["Run_sec"].dropna().mean()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Finishers",  f"{n_fin:,}")
    c2.metric("Average Finish",   hms(avg_total))
    c3.metric("Course Record",    hms(best_time))
    c4.metric("Slowest Finisher", hms(worst_time))
    st.markdown("---")
    # ── Average split composition ─────────────────────────────────────
    st.subheader("Average Split Composition")
    splits = {
        "Swim": avg_swim,
        "T1":   df["T1_sec"].dropna().mean(),
        "Bike": avg_bike,
        "T2":   df["T2_sec"].dropna().mean(),
        "Run":  avg_run,
    }
    total_split = sum(v for v in splits.values() if not np.isnan(v))
    split_pct = {k: (v / total_split * 100 if not np.isnan(v) else 0) for k, v in splits.items()}
    fig_split = go.Figure()
    x_pos = 0
    for seg, pct in split_pct.items():
        fig_split.add_trace(go.Bar(
            name=seg,
            x=[pct],
            y=["Avg Finisher"],
            orientation="h",
            marker_color=DISCIPLINE_COLORS[seg],
            text=f"{seg}<br>{hms(splits[seg])}<br>({pct:.1f}%)",
            textposition="inside",
            insidetextanchor="middle",
            hovertemplate=f"<b>{seg}</b><br>Avg: {hms(splits[seg])}<br>{pct:.1f}% of race<extra></extra>",
        ))
    fig_split.update_layout(
        barmode="stack",
        height=100,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False),
    )
    st.plotly_chart(fig_split, width="stretch")
    st.markdown("---")
    col_hist, col_bench = st.columns([3, 2])
    # ── Finish-Time Histogram ────────────────────────────────────────────
    with col_hist:
        st.subheader("Finish Time Distribution")
        bins = st.slider("Histogram bins", 20, 80, 40, key="hist_bins")
        fig_hist = px.histogram(
            df,
            x="Total_hr",
            nbins=bins,
            labels={"Total_hr": "Finish Time (hours)"},
            color_discrete_sequence=["#10b981"],
        )
        fig_hist.update_traces(
            hovertemplate="Time: %{x:.2f} hrs<br>Count: %{y}<extra></extra>"
        )
        fig_hist.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(17,24,39,0.6)",
            font_color="#9ca3af",
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(gridcolor="#374151"),
            yaxis=dict(title="Athletes", gridcolor="#374151"),
        )
        st.plotly_chart(fig_hist, width="stretch")
    # ── Age Group Benchmarks ─────────────────────────────────────────────
    with col_bench:
        st.subheader("Age Group Benchmarks")
        ag_stats = (
            df.groupby("AgeGroup")["Overall_sec"]
            .agg(["mean", "median", "min", "count"])
            .reset_index()
            .rename(columns={"mean": "Avg", "median": "Median",
                              "min": "Best", "count": "N"})
            .sort_values("Avg")
        )
        ag_stats = ag_stats[ag_stats["N"] >= 5]  # At least 5 finishers
        fig_ag = go.Figure()
        fig_ag.add_trace(go.Bar(
            y=ag_stats["AgeGroup"],
            x=ag_stats["Avg"] / 3600,
            orientation="h",
            name="Average",
            marker_color="#10b981",
            text=[hm(v) for v in ag_stats["Avg"]],
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Avg: %{text}<br>N=%{customdata}<extra></extra>",
            customdata=ag_stats["N"],
        ))
        fig_ag.add_trace(go.Scatter(
            y=ag_stats["AgeGroup"],
            x=ag_stats["Best"] / 3600,
            mode="markers",
            name="Best",
            marker=dict(color="#fbbf24", size=8, symbol="diamond"),
            hovertemplate="<b>%{y}</b> Best: %{text}<extra></extra>",
            text=[hm(v) for v in ag_stats["Best"]],
        ))
        fig_ag.update_layout(
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(17,24,39,0.6)",
            font_color="#9ca3af",
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(title="Hours", gridcolor="#374151"),
            yaxis=dict(gridcolor="#374151"),
            legend=dict(orientation="h", y=1.05),
        )
        st.plotly_chart(fig_ag, width="stretch")
    st.markdown("---")
    # ── Year-over-Year Trends ────────────────────────────────────────────
    st.subheader("Year-over-Year Performance Trends")
    yearly = (
        df.groupby("Year")
        .agg(
            Avg_Total=("Overall_sec", "mean"),
            Avg_Swim=("Swim_sec", "mean"),
            Avg_Bike=("Bike_sec", "mean"),
            Avg_Run=("Run_sec", "mean"),
            Finishers=("Overall_sec", "count"),
        )
        .reset_index()
    )
    col_trend_l, col_trend_r = st.columns([3, 1])
    with col_trend_l:
        fig_trend = go.Figure()
        for seg, col_key in [("Swim", "Avg_Swim"), ("Bike", "Avg_Bike"), ("Run", "Avg_Run")]:
            fig_trend.add_trace(go.Scatter(
                x=yearly["Year"],
                y=yearly[col_key] / 3600,
                mode="lines+markers",
                name=seg,
                line=dict(color=DISCIPLINE_COLORS[seg], width=2),
                hovertemplate=f"<b>{seg}</b> %{{x}}: %{{text}}<extra></extra>",
                text=[hm(v) for v in yearly[col_key]],
            ))
        fig_trend.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(17,24,39,0.6)",
            font_color="#9ca3af",
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(title="Year", dtick=1, gridcolor="#374151"),
            yaxis=dict(title="Hours (avg)", gridcolor="#374151"),
            legend=dict(orientation="h", y=1.05),
        )
        st.plotly_chart(fig_trend, width="stretch")
    with col_trend_r:
        st.markdown("#### Field Size")
        for _, row in yearly.iterrows():
            st.metric(str(int(row["Year"])), f"{int(row['Finishers']):,} finishers")






bottom_head()


