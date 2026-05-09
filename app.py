import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ──────────────────────────────────────────
st.set_page_config(
    page_title="NBA Player Archetype Evolution",
    page_icon="🏀",
    layout="wide"
)

# ── Professional CSS Theme ────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&family=Bebas+Neue&display=swap');

:root {
    --bg-primary: #0a0e1a;
    --bg-secondary: #111827;
    --bg-card: #1a2236;
    --bg-card-hover: #1e2a42;
    --accent-gold: #f5a623;
    --accent-blue: #4f8ef7;
    --accent-green: #00d4aa;
    --accent-red: #ff4d6d;
    --text-primary: #f0f4ff;
    --text-secondary: #8892a4;
    --border: rgba(255,255,255,0.06);
    --shadow: 0 8px 32px rgba(0,0,0,0.4);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1526 50%, #0a0e1a 100%) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

.header-banner {
    background: linear-gradient(135deg, #0f1923 0%, #1a2a4a 50%, #0f1923 100%);
    border: 1px solid rgba(245,166,35,0.2);
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    animation: fadeSlideIn 0.8s ease forwards;
}

.header-banner::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle at 60% 50%, rgba(245,166,35,0.04) 0%, transparent 60%);
    animation: shimmer 8s ease-in-out infinite;
}

.header-banner::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-gold), transparent);
    animation: scanline 3s ease-in-out infinite;
}

.header-title {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 3.2rem !important;
    letter-spacing: 3px !important;
    background: linear-gradient(135deg, #f5a623, #f0c060, #f5a623);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 !important;
    line-height: 1 !important;
}

.header-subtitle {
    color: var(--text-secondary) !important;
    font-size: 0.95rem !important;
    font-weight: 300 !important;
    letter-spacing: 1px !important;
    margin-top: 0.5rem !important;
}

.header-badge {
    display: inline-block;
    background: rgba(245,166,35,0.1);
    border: 1px solid rgba(245,166,35,0.3);
    color: var(--accent-gold);
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 2px;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 1rem;
    text-transform: uppercase;
}

@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(-20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes shimmer {
    0%, 100% { transform: rotate(0deg); }
    50%       { transform: rotate(5deg); }
}
@keyframes scanline {
    0%, 100% { opacity: 0.3; }
    50%       { opacity: 1; }
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1526 0%, #111827 100%) !important;
    border-right: 1px solid var(--border) !important;
}

.sidebar-logo {
    text-align: center;
    padding: 1rem 0 1.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}

.sidebar-logo-text {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
    letter-spacing: 3px;
    color: var(--accent-gold);
}

.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-secondary) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    border: 1px solid var(--border) !important;
    gap: 4px !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px !important;
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.5px !important;
    padding: 10px 20px !important;
    transition: all 0.2s ease !important;
    border: none !important;
}

.stTabs [data-baseweb="tab"]:hover {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(245,166,35,0.15), rgba(245,166,35,0.05)) !important;
    color: var(--accent-gold) !important;
    border: 1px solid rgba(245,166,35,0.2) !important;
}

[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1rem 1.25rem !important;
    transition: all 0.2s ease !important;
}

[data-testid="metric-container"]:hover {
    background: var(--bg-card-hover) !important;
    border-color: rgba(245,166,35,0.2) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.3) !important;
}

[data-testid="stMetricValue"] {
    color: var(--accent-gold) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 1.6rem !important;
    font-weight: 500 !important;
}

[data-testid="stMetricLabel"] {
    color: var(--text-secondary) !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}

[data-testid="stMetricDelta"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
}

[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    transition: border-color 0.2s ease !important;
}

[data-testid="stSelectbox"] > div > div:hover,
[data-testid="stMultiSelect"] > div > div:hover {
    border-color: rgba(245,166,35,0.3) !important;
}

.stTextInput > div > div > input {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.6rem 1rem !important;
    transition: border-color 0.2s ease !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--accent-gold) !important;
    box-shadow: 0 0 0 3px rgba(245,166,35,0.1) !important;
}

[data-testid="stSlider"] > div > div > div {
    background: var(--accent-gold) !important;
}

[data-testid="stAlert"] {
    background: rgba(79,142,247,0.08) !important;
    border: 1px solid rgba(79,142,247,0.2) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}

hr {
    border-color: var(--border) !important;
    margin: 1.5rem 0 !important;
}

.stMarkdown h2 {
    font-family: 'Bebas Neue', sans-serif !important;
    letter-spacing: 2px !important;
    color: var(--text-primary) !important;
    font-size: 1.8rem !important;
    border-bottom: 1px solid var(--border) !important;
    padding-bottom: 0.5rem !important;
}

.stMarkdown h3 {
    color: var(--accent-gold) !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--bg-card-hover); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-gold); }
</style>
""", unsafe_allow_html=True)

# ── Data loading ──────────────────────────────────────────
@st.cache_data
def load_data():
    per_game = pd.read_csv("Player Per Game.csv")
    advanced = pd.read_csv("Advanced.csv")
    career   = pd.read_csv("Player Career Info.csv")

    per_game = per_game[(per_game["season"] >= 1980) & (per_game["season"] <= 2026)]
    advanced = advanced[(advanced["season"] >= 1980) & (advanced["season"] <= 2026)]

    df = per_game.merge(
        advanced,
        on=["player", "season", "team", "player_id", "pos", "age", "g", "gs"],
        suffixes=("_pg", "_adv")
    )
    df = df[(df["g"] >= 40) & (df["mp_per_game"] >= 20)]

    career = career[["player_id", "ht_in_in"]].dropna()
    career["height_cm"] = career["ht_in_in"] * 2.54
    df = df.merge(career[["player_id", "ht_in_in", "height_cm"]], on="player_id", how="left")
    df.dropna(subset=["ht_in_in", "bpm", "ts_percent", "x3pa_per_game", "usg_percent"], inplace=True)

    def get_era(season):
        if season <= 1999:   return "Pre-2000"
        elif season <= 2014: return "2000-2014"
        else:                return "2015-2026"

    df["era"] = df["season"].apply(get_era)
    return df

df = load_data()

# ── Header ────────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
    <div class="header-badge">CS 4379G · Spring 2026 · Data Visualization Final Project</div>
    <div class="header-title">NBA PLAYER ARCHETYPE EVOLUTION</div>
    <div class="header-subtitle">
        How height, shooting, and advanced metrics reveal the transformation of player roles from 1980 to 2026
    </div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────
st.sidebar.markdown("""
<div class="sidebar-logo">
    <div class="sidebar-logo-text">🏀 NBA ARCHETYPES</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### FILTERS")
season_range = st.sidebar.slider("Season Range", 1980, 2026, (1980, 2026))
positions = st.sidebar.multiselect(
    "Positions",
    options=["PG", "SG", "SF", "PF", "C"],
    default=["PG", "SG", "SF", "PF", "C"]
)

filtered_df = df[
    (df["season"] >= season_range[0]) &
    (df["season"] <= season_range[1]) &
    (df["pos"].isin(positions))
].copy()

def get_era(s):
    if s <= 1999:   return "Pre-2000"
    elif s <= 2014: return "2000-2014"
    else:           return "2015-2026"

filtered_df["era"] = filtered_df["season"].apply(get_era)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**{filtered_df['player'].nunique():,}** players · **{filtered_df['season'].nunique()}** seasons")
st.sidebar.markdown("**Data:** Kaggle / Basketball Reference")
st.sidebar.markdown("**Course:** CS 4379G · Spring 2026")

# ── Tabs ──────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📈  3-Point Revolution",
    "📊  Win Shares Evolution",
    "⭐  Player Profiles",
    "🔬  Archetype Clustering"
])

# TAB 1 — 3-Point Revolution
with tab1:
    st.subheader("The 3-Point Revolution")
    st.markdown("Average 3-point attempts per game by position over time. Use the sidebar to filter seasons and positions.")

    avg_3pa = (
        filtered_df.groupby(["season", "pos"])["x3pa_per_game"]
        .mean()
        .reset_index()
    )

    fig1 = px.line(
        avg_3pa,
        x="season", y="x3pa_per_game", color="pos",
        markers=True,
        title="Average 3-Point Attempts Per Game by Position",
        labels={"x3pa_per_game": "Avg 3PA Per Game", "season": "Season", "pos": "Position"},
        color_discrete_map={"PG":"#636EFA","SG":"#EF553B","SF":"#00CC96","PF":"#FFA15A","C":"#AB63FA"}
    )
    fig1.add_vline(x=2015, line_dash="dash", line_color="rgba(255,255,255,0.3)",
                   annotation_text="Analytics Era", annotation_font_color="#f5a623")
    fig1.update_layout(
        hovermode="x unified", height=500,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#f0f4ff"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.1)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.1)"),
        legend=dict(bgcolor="rgba(26,34,54,0.8)", bordercolor="rgba(255,255,255,0.1)", borderwidth=1)
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")
    st.markdown("### Height of Players Averaging 2+ Three-Point Attempts")

    shooters = filtered_df[filtered_df["x3pa_per_game"] >= 2].copy()
    avg_height = shooters.groupby("season")["ht_in_in"].mean().reset_index()
    avg_height["height_ft"] = avg_height["ht_in_in"].apply(
        lambda x: f"{int(x)//12}'{int(round(x % 12))}\""
    )

    fig2 = px.line(
        avg_height, x="season", y="ht_in_in",
        markers=True,
        title="Average Height of Players Averaging 2+ Three-Point Attempts Per Game",
        labels={"ht_in_in": "Avg Height (inches)", "season": "Season"},
        custom_data=["height_ft"]
    )
    fig2.update_traces(
        hovertemplate="Season: %{x}<br>Avg Height: %{customdata[0]}<extra></extra>",
        line_color="#FFA15A", marker=dict(color="#FFA15A")
    )
    fig2.add_vline(x=2015, line_dash="dash", line_color="rgba(255,255,255,0.3)",
                   annotation_text="Analytics Era", annotation_font_color="#f5a623")
    fig2.update_layout(
        yaxis=dict(
            tickmode="array",
            tickvals=list(range(74, 83)),
            ticktext=[f"{v//12}'{v%12}\"" for v in range(74, 83)],
            gridcolor="rgba(255,255,255,0.05)"
        ),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        height=500,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#f0f4ff"),
        legend=dict(bgcolor="rgba(26,34,54,0.8)", bordercolor="rgba(255,255,255,0.1)", borderwidth=1)
    )
    st.plotly_chart(fig2, use_container_width=True)

# TAB 2 — Win Shares Evolution
with tab2:
    st.subheader("📊 Win Shares Per 48 — The Rise of the Modern Big")
    st.markdown("""
    Win Shares Per 48 (WS/48) measures how much a player contributes to winning 
    per minute played. Watch how **Centers and Power Forwards** climb from the 
    middle of the pack to the **most efficient players on the floor** as the 
    modern era unfolds. Press **Play** to animate from 1980 to 2026.
    """)

    pos_order = ["PG", "SG", "SF", "PF", "C"]
    color_map = {
        "PG": "#636EFA", "SG": "#EF553B",
        "SF": "#00CC96", "PF": "#FFA15A", "C": "#AB63FA"
    }

    ws_df = (
        filtered_df[filtered_df["pos"].isin(pos_order)]
        .groupby(["season", "pos"])["ws_48"]
        .mean()
        .reset_index()
    )
    ws_df.columns = ["season", "pos", "ws48"]
    ws_df["ws48"] = ws_df["ws48"].round(4)
    ws_df = ws_df.sort_values("season")
    seasons = sorted(ws_df["season"].unique())

    def make_bar_frame(season):
        frame_data = (
            ws_df[ws_df["season"] == season]
            .set_index("pos").reindex(pos_order).reset_index()
        )
        return go.Bar(
            x=frame_data["ws48"],
            y=frame_data["pos"],
            orientation="h",
            marker_color=[color_map[p] for p in pos_order],
            text=[f"{v:.4f}" if pd.notna(v) else "N/A" for v in frame_data["ws48"]],
            textposition="outside",
            textfont=dict(family="DM Mono", color="#f0f4ff")
        )

    fig_ws = go.Figure(data=make_bar_frame(seasons[0]))
    frames = [
        go.Frame(
            data=make_bar_frame(s),
            name=str(s),
            layout=go.Layout(title_text=f"Avg Win Shares Per 48 by Position — Season {s}")
        )
        for s in seasons
    ]
    fig_ws.frames = frames

    fig_ws.update_layout(
        title=f"Avg Win Shares Per 48 by Position — Season {seasons[0]}",
        xaxis_title="Avg Win Shares Per 48 (WS/48)",
        yaxis_title="Position",
        xaxis=dict(range=[0, 0.20], gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        height=450,
        bargap=0.3,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#f0f4ff"),
        updatemenus=[{
            "type": "buttons",
            "showactive": False,
            "y": 1.2, "x": 0.1,
            "buttons": [
                {"label": "▶  Play", "method": "animate",
                 "args": [None, {"frame": {"duration": 350, "redraw": True},
                                 "fromcurrent": True, "transition": {"duration": 100}}]},
                {"label": "⏸  Pause", "method": "animate",
                 "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}]}
            ]
        }],
        sliders=[{
            "steps": [
                {"args": [[str(s)], {"frame": {"duration": 350, "redraw": True}, "mode": "immediate"}],
                 "label": str(s), "method": "animate"}
                for s in seasons
            ],
            "x": 0.1, "len": 0.9,
            "bgcolor": "#1a2236",
            "bordercolor": "rgba(255,255,255,0.1)",
            "font": {"color": "#f0f4ff", "family": "DM Sans"},
            "currentvalue": {"prefix": "Season: ", "visible": True, "xanchor": "center",
                             "font": {"color": "#f5a623", "family": "DM Mono"}}
        }]
    )

    st.plotly_chart(fig_ws, use_container_width=True)
    st.info("💡 **Watch the C bar** — it starts in the middle of the pack in 1980 and climbs to the longest bar by 2026, surpassing guards and wings. Centers expanded their skill sets to become the most efficient players per minute in the modern NBA.")

    st.markdown("---")
    st.markdown("### Era Summary — Avg WS/48 by Position")

    era_ws = (
        filtered_df[filtered_df["pos"].isin(pos_order)]
        .groupby(["era", "pos"])["ws_48"]
        .mean().round(4).reset_index()
    )
    era_ws["era"] = pd.Categorical(
        era_ws["era"],
        categories=["Pre-2000", "2000-2014", "2015-2026"], ordered=True
    )
    era_ws = era_ws.sort_values("era")

    fig_era = px.bar(
        era_ws, x="ws_48", y="pos", color="era",
        orientation="h", barmode="group",
        title="Avg Win Shares Per 48 by Position and Era",
        labels={"ws_48": "Avg WS/48", "pos": "Position", "era": "Era"},
        color_discrete_map={"Pre-2000": "#636EFA", "2000-2014": "#8892a4", "2015-2026": "#FFA15A"},
        height=400
    )
    fig_era.update_layout(
        xaxis=dict(range=[0, 0.20], gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#f0f4ff"),
        legend=dict(bgcolor="rgba(26,34,54,0.8)", bordercolor="rgba(255,255,255,0.1)", borderwidth=1)
    )
    st.plotly_chart(fig_era, use_container_width=True)

# TAB 3 — Player Profile Lookup
with tab3:
    st.subheader("⭐ Player Archetype Profile Lookup")
    st.markdown("""
    Search for any player to see their **stat profile radar chart**.
    Compare two players side by side — see how two players at the same position
    can have completely different shapes, proving clustering is needed.
    """)

    all_players_df = df.copy()

    radar_features = {
        "Points":   "pts_per_game",
        "Assists":  "ast_per_game",
        "Rebounds": "trb_per_game",
        "3PA":      "x3pa_per_game",
        "BPM":      "bpm",
        "Blocks":   "blk_per_game"
    }

    def normalize(series):
        mins = all_players_df[list(radar_features.values())].min()
        maxs = all_players_df[list(radar_features.values())].max()
        return (series - mins) / (maxs - mins)

    col_p1, col_p2 = st.columns(2)

    # ── Player 1 ──────────────────────────────────────────
    with col_p1:
        st.markdown("### Player 1")
        search1 = st.text_input("Search player:", placeholder="e.g. LeBron James...", key="s1")
        matches1 = [p for p in sorted(all_players_df["player"].unique())
                    if search1.lower() in p.lower()] if search1 \
                   else sorted(all_players_df["player"].unique())
        if not matches1:
            st.warning("No players found.")
            st.stop()
        p1 = st.selectbox("Select:", matches1, key="p1")
        seasons1 = sorted(all_players_df[all_players_df["player"] == p1]["season"].unique(), reverse=True)
        s1 = st.selectbox("Season:", seasons1, key="ss1")

    # ── Player 2 ──────────────────────────────────────────
    with col_p2:
        st.markdown("### Player 2")
        search2 = st.text_input("Search player:", placeholder="e.g. Shaquille O'Neal...", key="s2")
        matches2 = [p for p in sorted(all_players_df["player"].unique())
                    if search2.lower() in p.lower()] if search2 \
                   else sorted(all_players_df["player"].unique())
        if not matches2:
            st.warning("No players found.")
            st.stop()
        p2 = st.selectbox("Select:", matches2, key="p2")
        seasons2 = sorted(all_players_df[all_players_df["player"] == p2]["season"].unique(), reverse=True)
        s2 = st.selectbox("Season:", seasons2, key="ss2")

    # ── Get data ───────────────────────────────────────────
    row1 = all_players_df[(all_players_df["player"] == p1) & (all_players_df["season"] == s1)]
    row2 = all_players_df[(all_players_df["player"] == p2) & (all_players_df["season"] == s2)]

    if row1.empty or row2.empty:
        st.warning("Could not find data for one of the selected players.")
        st.stop()

    row1, row2 = row1.iloc[0], row2.iloc[0]
    vals1 = normalize(row1[list(radar_features.values())]).tolist()
    vals2 = normalize(row2[list(radar_features.values())]).tolist()
    raw1  = row1[list(radar_features.values())]
    raw2  = row2[list(radar_features.values())]
    cats  = list(radar_features.keys())

    # ── Side by side radars ────────────────────────────────
    rc1, rc2 = st.columns(2)

    with rc1:
        fig_r1 = go.Figure()
        fig_r1.add_trace(go.Scatterpolar(
            r=vals1 + [vals1[0]], theta=cats + [cats[0]],
            fill="toself", name=p1,
            line_color="#FFA15A", fillcolor="rgba(255,161,90,0.2)"
        ))
        fig_r1.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0,1],
                                gridcolor="rgba(255,255,255,0.1)",
                                linecolor="rgba(255,255,255,0.1)"),
                bgcolor="rgba(0,0,0,0)"
            ),
            showlegend=False,
            title=dict(text=f"{p1} — {s1} ({row1['pos']})",
                       font=dict(family="DM Sans", color="#f0f4ff", size=13)),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans", color="#f0f4ff"),
            height=420
        )
        st.plotly_chart(fig_r1, use_container_width=True)

    with rc2:
        fig_r2 = go.Figure()
        fig_r2.add_trace(go.Scatterpolar(
            r=vals2 + [vals2[0]], theta=cats + [cats[0]],
            fill="toself", name=p2,
            line_color="#00CC96", fillcolor="rgba(0,204,150,0.2)"
        ))
        fig_r2.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0,1],
                                gridcolor="rgba(255,255,255,0.1)",
                                linecolor="rgba(255,255,255,0.1)"),
                bgcolor="rgba(0,0,0,0)"
            ),
            showlegend=False,
            title=dict(text=f"{p2} — {s2} ({row2['pos']})",
                       font=dict(family="DM Sans", color="#f0f4ff", size=13)),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans", color="#f0f4ff"),
            height=420
        )
        st.plotly_chart(fig_r2, use_container_width=True)

    # ── Overlay comparison radar ───────────────────────────
    st.markdown("---")
    st.markdown("### Head-to-Head Overlay")

    fig_overlay = go.Figure()
    fig_overlay.add_trace(go.Scatterpolar(
        r=vals1 + [vals1[0]], theta=cats + [cats[0]],
        fill="toself", name=f"{p1} ({s1})",
        line_color="#FFA15A", fillcolor="rgba(255,161,90,0.15)"
    ))
    fig_overlay.add_trace(go.Scatterpolar(
        r=vals2 + [vals2[0]], theta=cats + [cats[0]],
        fill="toself", name=f"{p2} ({s2})",
        line_color="#00CC96", fillcolor="rgba(0,204,150,0.15)"
    ))
    fig_overlay.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0,1],
                            gridcolor="rgba(255,255,255,0.1)",
                            linecolor="rgba(255,255,255,0.1)"),
            bgcolor="rgba(0,0,0,0)"
        ),
        showlegend=True,
        legend=dict(bgcolor="rgba(26,34,54,0.8)", bordercolor="rgba(255,255,255,0.1)", borderwidth=1),
        title=dict(text=f"{p1} vs {p2} — Archetype Comparison",
                   font=dict(family="DM Sans", color="#f0f4ff", size=14)),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#f0f4ff"),
        height=520
    )
    st.plotly_chart(fig_overlay, use_container_width=True)

    # ── Stat metrics ───────────────────────────────────────
    st.markdown("---")
    st.markdown("### Raw Stats")
    mc = st.columns(len(radar_features))
    for i, (label, col_name) in enumerate(radar_features.items()):
        delta = raw1[col_name] - raw2[col_name]
        mc[i].metric(
            label,
            f"{raw1[col_name]:.2f}",
            f"{delta:+.2f} vs {p2[:10]}"
        )

    st.info("💡 **This is the clustering argument in action** — if two players at the same position have radar shapes this different, a single position label cannot describe both. K-Means clustering in Milestone 4 will formally identify these distinct archetypes.")

# TAB 4 — Archetype Clustering

with tab4:
    st.subheader("🔬 NBA Player Archetype Clustering")
    st.markdown("""
    Using **K-Means clustering (K=3)** on 10 performance features, every qualified 
    player season from 2000–2026 was assigned to one of three data-driven archetypes. 
    The optimal K was selected using the elbow method and silhouette scoring.
    """)

    # ── Run clustering ────────────────────────────────────
    @st.cache_data
    def run_clustering(dataframe):
        from sklearn.preprocessing import StandardScaler, MinMaxScaler
        from sklearn.cluster import KMeans
        from sklearn.manifold import TSNE

        features = [
            "pts_per_game", "ast_per_game", "trb_per_game",
            "x3pa_per_game", "x3p_percent", "ts_percent",
            "usg_percent", "blk_per_game", "stl_per_game", "dbpm"
        ]

        cluster_df = dataframe[
            (dataframe["season"] >= 2000) &
            (dataframe["pos"].isin(["PG", "SG", "SF", "PF", "C"]))
        ][["player", "season", "pos", "era"] + features].dropna().copy()

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(cluster_df[features])

        km = KMeans(n_clusters=3, random_state=42, n_init=10)
        cluster_df["cluster"] = km.fit_predict(X_scaled)

        cluster_names = {0: "Playmaking Scorer", 1: "3-and-D Role Player", 2: "Traditional Big"}
        cluster_df["archetype"] = cluster_df["cluster"].map(cluster_names)

        tsne = TSNE(n_components=2, random_state=42, perplexity=40, max_iter=1000)
        coords = tsne.fit_transform(X_scaled)
        cluster_df["tsne_x"] = coords[:, 0]
        cluster_df["tsne_y"] = coords[:, 1]

        # Normalized heatmap data
        cluster_means = cluster_df.groupby("archetype")[features].mean()
        norm_scaler = MinMaxScaler()
        cluster_normalized = pd.DataFrame(
            norm_scaler.fit_transform(cluster_means),
            index=cluster_means.index,
            columns=features
        )

        return cluster_df, cluster_means, cluster_normalized, features

    with st.spinner("Running K-Means clustering and t-SNE... this takes about 30 seconds ⏳"):
        cluster_df, cluster_means, cluster_normalized, features = run_clustering(df)

    # ── Metric cards ──────────────────────────────────────
    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    total = len(cluster_df)
    m1.metric("Total Players Clustered", f"{total:,}")
    m2.metric("Playmaking Scorers",
              f"{(cluster_df['archetype']=='Playmaking Scorer').sum():,}",
              f"{(cluster_df['archetype']=='Playmaking Scorer').mean()*100:.1f}%")
    m3.metric("3-and-D Role Players",
              f"{(cluster_df['archetype']=='3-and-D Role Player').sum():,}",
              f"{(cluster_df['archetype']=='3-and-D Role Player').mean()*100:.1f}%")
    m4.metric("Traditional Bigs",
              f"{(cluster_df['archetype']=='Traditional Big').sum():,}",
              f"{(cluster_df['archetype']=='Traditional Big').mean()*100:.1f}%")

    # ── t-SNE scatter ─────────────────────────────────────
    st.markdown("---")
    st.markdown("### t-SNE Visualization — Player Archetypes in 2D Space")
    st.markdown("Each dot is a player season. Colors represent K-Means assigned archetypes. Hover to see player details.")

    color_map = {
        "Playmaking Scorer": "#636EFA",
        "3-and-D Role Player": "#00CC96",
        "Traditional Big": "#FFA15A"
    }

    fig_tsne = px.scatter(
        cluster_df,
        x="tsne_x", y="tsne_y",
        color="archetype",
        hover_name="player",
        hover_data={
            "season": True, "pos": True,
            "pts_per_game": ":.1f",
            "ast_per_game": ":.1f",
            "tsne_x": False, "tsne_y": False
        },
        color_discrete_map=color_map,
        title="t-SNE — NBA Player Archetypes (2000–2026)",
        labels={"archetype": "Archetype"},
        opacity=0.7,
        height=550
    )
    fig_tsne.update_traces(marker=dict(size=5, line=dict(width=0.3, color="white")))
    fig_tsne.update_layout(
        hovermode="closest",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#f0f4ff"),
        legend=dict(bgcolor="rgba(26,34,54,0.8)",
                    bordercolor="rgba(255,255,255,0.1)", borderwidth=1),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", zeroline=False),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", zeroline=False)
    )
    st.plotly_chart(fig_tsne, use_container_width=True)

    # ── Heatmap ───────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Archetype Stat Profiles — Heatmap")

    col_labels = {
        "pts_per_game": "Points", "ast_per_game": "Assists",
        "trb_per_game": "Rebounds", "x3pa_per_game": "3PA",
        "x3p_percent": "3P%", "ts_percent": "TS%",
        "usg_percent": "Usage%", "blk_per_game": "Blocks",
        "stl_per_game": "Steals", "dbpm": "DBPM"
    }

    heatmap_display = cluster_means.copy()
    heatmap_display.columns = [col_labels[c] for c in heatmap_display.columns]
    heatmap_norm = cluster_normalized.copy()
    heatmap_norm.columns = [col_labels[c] for c in heatmap_norm.columns]

    fig_heat = go.Figure(data=go.Heatmap(
        z=heatmap_norm.values,
        x=heatmap_norm.columns.tolist(),
        y=heatmap_norm.index.tolist(),
        colorscale="YlOrRd",
        text=heatmap_display.round(2).values,
        texttemplate="%{text}",
        showscale=True,
        colorbar=dict(
            title=dict(text="Normalized", font=dict(color="#f0f4ff")),
            tickfont=dict(color="#f0f4ff")
        )
    ))
    fig_heat.update_layout(
        title="Archetype Profiles — Avg Stats per Cluster (Normalized Color)",
        height=350,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#f0f4ff"),
        xaxis=dict(tickangle=-30),
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    # ── Archetype trends over time ────────────────────────
    st.markdown("---")
    st.markdown("### Archetype Proportions Over Time")
    st.markdown("How the share of each archetype has shifted from 2000 to 2026.")

    archetype_counts = cluster_df.groupby(["season", "archetype"]).size().reset_index(name="count")
    archetype_totals = cluster_df.groupby("season").size().reset_index(name="total")
    archetype_pct = archetype_counts.merge(archetype_totals, on="season")
    archetype_pct["pct"] = (archetype_pct["count"] / archetype_pct["total"] * 100).round(1)

    fig_trend = px.line(
        archetype_pct,
        x="season", y="pct",
        color="archetype",
        markers=True,
        title="% of Qualified Players per Archetype by Season",
        labels={"pct": "% of Players", "season": "Season", "archetype": "Archetype"},
        color_discrete_map=color_map,
        height=450
    )
    fig_trend.add_vline(x=2015, line_dash="dash",
                        line_color="rgba(255,255,255,0.3)",
                        annotation_text="Analytics Era",
                        annotation_font_color="#f5a623")
    fig_trend.update_layout(
        hovermode="x unified",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#f0f4ff"),
        legend=dict(bgcolor="rgba(26,34,54,0.8)",
                    bordercolor="rgba(255,255,255,0.1)", borderwidth=1),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)")
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    st.info("💡 Traditional Bigs declined from ~26% in 2000 to under 10% by 2026. Playmaking Scorers nearly doubled post-2015. The analytics era fundamentally reshaped the distribution of player archetypes.")

    # ── Player archetype lookup ───────────────────────────
    st.markdown("---")
    st.markdown("### Look Up a Player's Archetype")

    search_c = st.text_input("Search player:", placeholder="e.g. Kevin Durant...", key="cluster_search")
    matches_c = [p for p in sorted(cluster_df["player"].unique())
                 if search_c.lower() in p.lower()] if search_c \
               else sorted(cluster_df["player"].unique())

    if matches_c:
        selected_c = st.selectbox("Select player:", matches_c, key="cluster_player")
        player_data = cluster_df[cluster_df["player"] == selected_c].sort_values("season", ascending=False)

        ac1, ac2 = st.columns(2)
        with ac1:
            st.markdown(f"**{selected_c} — Archetype History**")
            st.dataframe(
                player_data[["season", "pos", "archetype", "pts_per_game",
                              "ast_per_game", "trb_per_game", "x3pa_per_game"]].rename(columns={
                    "pts_per_game": "PTS", "ast_per_game": "AST",
                    "trb_per_game": "REB", "x3pa_per_game": "3PA"
                }),
                hide_index=True
            )
        with ac2:
            if not player_data.empty:
                latest = player_data.iloc[0]
                arch = latest["archetype"]
                arch_color = color_map.get(arch, "#ffffff")
                st.markdown(f"**Most Recent Archetype:**")
                st.markdown(f"""
                <div style='background: rgba(26,34,54,0.8); border: 1px solid {arch_color};
                border-radius: 12px; padding: 1.5rem; text-align: center;'>
                    <div style='font-size: 1.8rem; font-weight: bold; color: {arch_color};'>{arch}</div>
                    <div style='color: #8892a4; margin-top: 0.5rem;'>{latest['pos']} · {int(latest['season'])} Season</div>
                </div>
                """, unsafe_allow_html=True)