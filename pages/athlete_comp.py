import streamlit as st
from custom import top_menu, bottom_head

import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go

top_menu()


# Folder that contains the CSV files. Change if needed.
DATA_DIR = "Data/WorldChamp/M"

YEARS = list(range(2003, 2026))          # 2003 – 2025
DISCIPLINE_COLORS = {
    "Swim":  "#18A3DD",   # swim blue
    "T1":    "#a78bfa",   # violet
    "Bike":  "#05A435",   # bike green
    "T2":    "#fb923c",   # orange
    "Run":   "#E8E812",   # run yellow
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

##########

# ─── Sidebar – Global Filters ─────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## ⚙️ Global Filters")
    sel_years = st.multiselect(
        "Year(s)",
        options=YEARS,
        default=YEARS,
    )
    sel_gender = st.selectbox(
        "Gender",
        ["All", "Male", "Female"],
        index=0,
    )
    all_ag = sorted(df_all["AgeGroup"].dropna().unique().tolist())
    sel_ag = st.multiselect(
        "Age Group(s)",
        options=all_ag,
        default=[],
        placeholder="All age groups",
    )
    st.markdown("---")
    st.caption("Ironman World Championship • 2003 – 2025")

# Apply global filters
def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if sel_years:
        out = out[out["Year"].isin(sel_years)]
    if sel_gender != "All":
        out = out[out["Gender_clean"] == sel_gender]
    if sel_ag:
        out = out[out["AgeGroup"].isin(sel_ag)]
    return out

df = apply_filters(df_all)

############










st.header("Athlete Performance Comparator")

# Athlete search
all_names = sorted(df["Name"].dropna().unique().tolist())
sel_athletes = st.multiselect(
    "Search and select up to 4 athletes",
    options=all_names,
    max_selections=4,
    placeholder="Type a name …",
)
if not sel_athletes:
    st.info("Select at least one athlete from the list above to begin comparison.")
else:
    athlete_df = df[df["Name"].isin(sel_athletes)].copy()
    # If an athlete raced multiple years, show latest
    athlete_rows = (
        athlete_df
        .sort_values("Year", ascending=False)
        .groupby("Name", as_index=False)
        .first()
    )
    # ── Summary cards ──────────────────────────────────────────────────
    cols = st.columns(len(athlete_rows))
    for i, (_, row) in enumerate(athlete_rows.iterrows()):
        with cols[i]:
            color = ATHLETE_PALETTE[i % len(ATHLETE_PALETTE)]
            st.markdown(
                f"<div style='border:1px solid {color};border-radius:8px;"
                f"padding:12px;background:rgba(0,0,0,0.3)'>"
                f"<b style='color:{color}'>{row['Name']}</b><br>"
                f"<span style='font-size:0.8em;color:#9ca3af'>"
                f"{row.get('Division','?')} · {int(row['Year'])} · {row.get('Country','?')}</span><br>"
                f"<span style='font-size:1.4em;color:#e5e7eb'>{hms(row['Overall_sec'])}</span><br>"
                f"<span style='font-size:0.75em;color:#6b7280'>"
                f"Rank #{int(row['Overall Rank']) if not pd.isna(row.get('Overall Rank')) else '?'}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )
    st.markdown("---")
    # ── Score normalisation for radar  ─────────────────────────────────
    # Score each discipline 0–100: 100 = fastest finisher, 0 = slowest
    def score_discipline(val, col_ref):
        valid = df[col_ref].dropna()
        if valid.empty or pd.isna(val):
            return 50.0
        worst = valid.quantile(0.95)
        best  = valid.quantile(0.05)
        if worst == best:
            return 50.0
        return float(np.clip((worst - val) / (worst - best) * 100, 0, 100))
    radar_cats = ["Swim", "Bike", "Run", "T1 Eff.", "T2 Eff."]
    col_map    = ["Swim_sec", "Bike_sec", "Run_sec", "T1_sec", "T2_sec"]
    fig_radar = go.Figure()
    for i, (_, row) in enumerate(athlete_rows.iterrows()):
        scores = [
            score_discipline(row["Swim_sec"], "Swim_sec"),
            score_discipline(row["Bike_sec"], "Bike_sec"),
            score_discipline(row["Run_sec"],  "Run_sec"),
            # Transitions: lower is better, score inverted
            score_discipline(row["T1_sec"],   "T1_sec"),
            score_discipline(row["T2_sec"],   "T2_sec"),
        ]
        # Prendiamo il colore base dell'atleta
    base_color = ATHLETE_PALETTE[i % len(ATHLETE_PALETTE)]
    
    # Convertiamo l'esadecimale (es. #10b981) in formato rgba(R, G, B, 0.15)
    h = base_color.lstrip('#')
    r, g, b = tuple(int(h[j:j+2], 16) for j in (0, 2, 4))
    fill_rgba = f"rgba({r}, {g}, {b}, 0.15)"
    fig_radar.add_trace(go.Scatterpolar(
        r=scores + [scores[0]],
        theta=radar_cats + [radar_cats[0]],
        fill="toself",
        name=row["Name"],
        line_color=base_color,
        fillcolor=fill_rgba,
        opacity=0.85,
    ))
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(range=[0, 100], showticklabels=True, gridcolor="#374151"),
            angularaxis=dict(gridcolor="#374151"),
            bgcolor="rgba(17,24,39,0.6)",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#9ca3af",
        showlegend=True,
        height=420,
        legend=dict(orientation="h", y=-0.1),
    )
    # ── Split comparison bars ────────────────────────────────────────────
    bar_segs = [
        ("Swim", "Swim_sec"),
        ("T1",   "T1_sec"),
        ("Bike", "Bike_sec"),
        ("T2",   "T2_sec"),
        ("Run",  "Run_sec"),
    ]
    fig_bar = go.Figure()
    for seg, sec_col in bar_segs:
        fig_bar.add_trace(go.Bar(
            name=seg,
            x=[r["Name"] for _, r in athlete_rows.iterrows()],
            y=[r[sec_col] / 60 if not pd.isna(r[sec_col]) else 0
               for _, r in athlete_rows.iterrows()],
            marker_color=DISCIPLINE_COLORS[seg],
            text=[hm(r[sec_col]) for _, r in athlete_rows.iterrows()],
            textposition="inside",
            hovertemplate=f"<b>{seg}</b><br>%{{x}}: %{{text}}<extra></extra>",
        ))
    fig_bar.update_layout(
        barmode="stack",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(17,24,39,0.6)",
        font_color="#9ca3af",
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(gridcolor="#374151"),
        yaxis=dict(title="Minutes", gridcolor="#374151"),
        legend=dict(orientation="h", y=1.05),
        height=350,
    )
    col_r, col_b = st.columns(2)
    with col_r:
        st.subheader("Performance Radar")
        st.plotly_chart(fig_radar, width="stretch")
    with col_b:
        st.subheader("Split Breakdown")
        st.plotly_chart(fig_bar, width="stretch")
    # ── Detail table ────────────────────────────────────────────────────
    st.subheader("Split Details")
    detail_rows = []
    for _, row in athlete_rows.iterrows():
        detail_rows.append({
            "Athlete":      row["Name"],
            "Year":         int(row["Year"]),
            "Division":     row.get("Division", "?"),
            "Country":      row.get("Country", "?"),
            "Finish Time":  hms(row["Overall_sec"]),
            "Overall Rank": int(row["Overall Rank"]) if not pd.isna(row.get("Overall Rank")) else "?",
            "Swim":         hms(row["Swim_sec"]),
            "T1":           hms(row["T1_sec"]),
            "Bike":         hms(row["Bike_sec"]),
            "T2":           hms(row["T2_sec"]),
            "Run":          hms(row["Run_sec"]),
        })
    st.dataframe(
        pd.DataFrame(detail_rows),
        width="stretch",
        hide_index=True,
    )

bottom_head()

