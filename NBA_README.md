# NBA Player Archetype Evolution

Data-driven analysis of how traditional NBA positional archetypes have dissolved in the modern era, using K-Means clustering, t-SNE dimensionality reduction, and 6 EDA visualizations across 35+ years of player data (1990–2026).

Built for **Data Visualization and Analysis** at Texas State University.

> **Author:** Rudy Rutiaga

---

## Project Overview

The NBA has undergone a fundamental structural shift — Centers now shoot three-pointers, point guards rebound, and the idea of a "power forward" barely exists anymore. This project uses statistical analysis and unsupervised machine learning to **quantify that shift** and identify the real player archetypes driving modern basketball.

**Key findings:**
- Centers increased 3-point attempts by **+794%** since 2015
- Power Forwards increased by **+134%** over the same period
- Traditional Bigs declined from **26% of qualified players in 2000 to under 10% by 2026**
- K-Means clustering identified **3 statistically distinct archetypes** that replace the 5 classical positions
- The 6'9"+ height group increased assists per game by **+27% since the Pre-2000 era** while maintaining the highest rebounding numbers of any group

---

## Files

```
NBA_Final_Project/
├── nba_data.ipynb              # Main analysis notebook (27 cells)
├── app.py                      # Streamlit interactive dashboard
├── Written_Narrative_gnb30.pdf # Full written narrative and findings
│
└── data/                       # Kaggle NBA dataset (multiple CSV files)
    ├── Player Per Game.csv
    ├── Advanced.csv
    ├── Player Career Info.csv
    ├── Player Totals.csv
    ├── Per 100 Poss.csv
    ├── Per 36 Minutes.csv
    ├── Player Shooting.csv
    ├── Player Play By Play.csv
    ├── Player Season Info.csv
    ├── Team Summaries.csv
    ├── Team Stats Per Game.csv
    ├── Team Totals.csv
    └── ...
```

---

## Analysis Breakdown

### Data Preparation
- Merged `Player Per Game` and `Advanced` datasets on player + season + team
- Filtered to qualified players: **40+ games played, 20+ minutes per game**
- Joined height data from `Player Career Info`
- Final dataset: **5,972 player-seasons** spanning 2000–2026

### EDA Visualizations (6 Charts)

| Chart | Type | Key Finding |
|-------|------|-------------|
| 1 | Line plot | Avg 3PA per game nearly tripled from 1.7 (2000) to 4.4+ (2026) |
| 2 | Line plot | Avg height of high-volume 3P shooters rose from 6'3" to 6'6" since 1990 |
| 3 | Multi-line plot | Centers +794% and PFs +134% in 3PA since 2015 |
| 4 | Normalized heatmap | Traditional big man stats (blocks) declining as 3PA explodes |
| 5 | Horizontal bar chart | Centers now lead all positions in Win Shares/48 in the modern era |
| 6 | Diverging bar chart | 6'9"+ group increased assists +27% while maintaining top rebounding numbers |

### K-Means Clustering

**Features used (10 total):**
`pts_per_game`, `ast_per_game`, `trb_per_game`, `x3pa_per_game`, `x3p_percent`, `ts_percent`, `usg_percent`, `blk_per_game`, `stl_per_game`, `dbpm`

**Optimal K selection:** Elbow method + silhouette scoring → **K=3**

**Archetypes identified:**

| Archetype | % of Players | Avg Pts | Avg Ast | Avg Reb | Avg 3PA | Avg Blk |
|-----------|-------------|---------|---------|---------|---------|---------|
| Playmaking Scorer | 25.2% | 19.9 | 5.1 | 4.2 | 4.8 | 0.4 |
| 3-and-D Role Player | 55.8% | 10.3 | 2.1 | 3.9 | 2.8 | 0.4 |
| Traditional Big | 18.9% | 11.2 | 1.8 | 7.96 | 0.59 | 1.20 |

### t-SNE Visualization
t-SNE compressed the 10 clustering features to 2 dimensions — the clear visual separation between all 3 archetypes confirms the K-Means clusters are statistically genuine, not arbitrary groupings.

---

## Interactive Dashboard

The project includes a full **Streamlit dashboard** (`app.py`) with interactive Plotly charts, allowing you to explore player archetypes, filter by era, and hover over individual player data points.

**Run locally:**
```bash
pip install streamlit pandas plotly
streamlit run app.py
```

---

## Notebook

**Run the full analysis:**
```bash
pip install pandas matplotlib seaborn scikit-learn plotly
jupyter notebook nba_data.ipynb
```

> **Note:** The CSV data files must be in the same directory as the notebook when running locally.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Pandas | Data loading, merging, feature engineering |
| Matplotlib / Seaborn | Static EDA visualizations |
| Scikit-learn | StandardScaler, KMeans, silhouette scoring, t-SNE |
| Plotly | Interactive t-SNE scatter plot |
| Streamlit | Interactive web dashboard |
| Jupyter Notebook | Analysis and narrative |

---

## Data Source

Dataset sourced from Kaggle — NBA Player Stats (multiple tables covering per game, advanced, shooting, play-by-play, and career info stats from 1946 to 2026).
