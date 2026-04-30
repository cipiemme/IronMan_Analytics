import streamlit as st
from custom import top_menu, bottom_head, hms, hm, load_data, gen_sel, DISCIPLINE_COLORS, ATHLETE_PALETTE, gr_gridcol, gr_fontcol

import pandas as pd
import numpy as np
import plotly.graph_objects as go

top_menu()

DATA_DIR = gen_sel()

# 2003 – 2025
YEARS = list(range(2003, 2026))

# ─── Data Loading ─────────────────────────────────────────────────────────────

df_all = load_data(DATA_DIR, YEARS)

st.header("Athlete Performance Comparator")

colL, colR = st.columns([.5, .5])

with colL.expander("Year filters"):
    sel_years = st.slider("Years", min_value= 2003, max_value= 2026, step= 1, value= (2003, 2026))

with colR.expander("Age group"):
    all_ag = sorted(df_all["AgeGroup"].dropna().unique().tolist())
    sel_ag = st.multiselect( "Age Group(s)", options=all_ag, default=[], placeholder="All age groups")

# Apply filters
if sel_years:
    df = df_all[df_all["Year"].isin(sel_years)]

if sel_ag:
    df = df_all[df_all["AgeGroup"].isin(sel_ag)]

# Athlete search
all_names = sorted(df["Name"].dropna().unique().tolist())

sel_athletes = st.multiselect( "Search and select up to 4 athletes", options=all_names,
                              max_selections=4, placeholder="Type a name …")

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
            radialaxis=dict(range=[0, 100], showticklabels=True, gridcolor= gr_gridcol),
            angularaxis=dict(gridcolor= gr_gridcol),
            bgcolor="rgba(17,24,39,0.6)",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font_color= gr_fontcol,
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
        barmode = "stack",
        paper_bgcolor = "rgba(0,0,0,0)",
        plot_bgcolor = "rgba(17,24,39,0.6)",
        font_color = gr_fontcol,
        margin = dict(l=10, r=10, t=10, b=10),
        xaxis = dict(gridcolor = gr_gridcol),
        yaxis = dict(title = "Minutes", gridcolor = gr_gridcol),
        legend = dict(orientation = "h", y = 1.05),
        height = 350,
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
