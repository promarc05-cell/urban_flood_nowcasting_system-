# ============================================================
# dashboard.py
# URBAN FLOOD NOWCASTING SYSTEM
# Presentation-ready Streamlit Dashboard
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium

from streamlit_folium import st_folium


# ============================================================
# FLOOD ENGINE IMPORTS
# ============================================================

from rainfall import (
    get_spatial_rainfall_forecast,
    validate_rainfall_forecast
)

from runoff import (
    calculate_spatial_runoff
)

from terrain import (
    DEM,
    calculate_accumulation
)

from drainage import (
    DRAINAGE_CAPACITY_GRID,
    calculate_excess_water
)

from flood import (
    calculate_flood_risk,
    calculate_flood_depth,
    calculate_risk_score
)

from routing import (
    find_safest_route,
    calculate_route_summary
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Urban Flood Nowcasting",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 20px;
        color: #777;
        margin-top: 0px;
    }

    .section-title {
        font-size: 27px;
        font-weight: 700;
        margin-top: 15px;
        margin-bottom: 10px;
    }

    .small-text {
        font-size: 14px;
        color: #777;
    }

    div[data-testid="stDataFrame"] {
        font-size: 13px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# STUDY AREA
# ============================================================

MIN_LAT = 22.5500
MAX_LAT = 22.5850

MIN_LON = 88.3400
MAX_LON = 88.3800

STUDY_CENTER = [
    (MIN_LAT + MAX_LAT) / 2,
    (MIN_LON + MAX_LON) / 2
]


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🌊 Urban Flood Nowcasting</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Central Kolkata • Hyper-local 0–3 Hour Flood Prediction'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("")

st.markdown(
    """
    **Rainfall → Runoff → Terrain → Water Accumulation
    → Drainage → Excess Water → Flood Risk → Flood Depth
    → Safer Routing**
    """
)

st.info(
    "Prototype rainfall input: a deterministic spatial rainfall "
    "field is currently used to demonstrate the complete 0–3 hour "
    "flood prediction pipeline. The architecture is designed to "
    "ingest an external weather/radar nowcast in the future."
)


# ============================================================
# STUDY AREA INFORMATION
# ============================================================

with st.expander(
    "📍 Study Area — Central Kolkata",
    expanded=False
):

    area_col1, area_col2, area_col3 = st.columns(3)

    area_col1.metric(
        "Study Area",
        "Central Kolkata"
    )

    area_col2.metric(
        "Model Grid",
        "20 × 20"
    )

    area_col3.metric(
        "Model Cells",
        "400"
    )

    st.markdown(
        """
        **Approximate study area**

        Latitude: `22.5500 → 22.5850`

        Longitude: `88.3400 → 88.3800`

        The prototype uses a real Digital Elevation Model (DEM)
        aggregated into the 20 × 20 model grid.
        """
    )


# ============================================================
# LOAD DEM
# ============================================================

DEM = np.array(
    DEM,
    dtype=float
)

grid_rows = DEM.shape[0]
grid_cols = DEM.shape[1]

total_cells = grid_rows * grid_cols


# ============================================================
# LOAD RAINFALL FORECAST
# ============================================================

rainfall_forecast = get_spatial_rainfall_forecast()

if not validate_rainfall_forecast(
    rainfall_forecast
):

    st.error(
        "Invalid rainfall forecast."
    )

    st.stop()


# ============================================================
# PROCESS 3-HOUR FORECAST
# ============================================================

forecast_results = {}


for hour in range(1, 4):

    rainfall_grid = np.array(
        rainfall_forecast[hour],
        dtype=float
    )

    # --------------------------------------------------------
    # RUNOFF
    # --------------------------------------------------------

    runoff_grid = calculate_spatial_runoff(
        rainfall_grid
    )

    runoff_grid = np.array(
        runoff_grid,
        dtype=float
    )

    # --------------------------------------------------------
    # TERRAIN ACCUMULATION
    # --------------------------------------------------------

    accumulation_grid = calculate_accumulation(
        runoff_grid,
        DEM
    )

    accumulation_grid = np.array(
        accumulation_grid,
        dtype=float
    )

    # --------------------------------------------------------
    # DRAINAGE
    # --------------------------------------------------------

    excess_grid = calculate_excess_water(
        accumulation_grid,
        DRAINAGE_CAPACITY_GRID
    )

    excess_grid = np.array(
        excess_grid,
        dtype=float
    )

    # --------------------------------------------------------
    # FLOOD RISK
    # --------------------------------------------------------

    risk_grid = calculate_flood_risk(
        excess_grid
    )

    # --------------------------------------------------------
    # RISK SCORE
    # --------------------------------------------------------

    risk_score_grid = calculate_risk_score(
        excess_grid
    )

    risk_score_grid = np.array(
        risk_score_grid,
        dtype=int
    )

    # --------------------------------------------------------
    # FLOOD DEPTH
    # --------------------------------------------------------

    depth_grid = calculate_flood_depth(
        excess_grid,
        0.01
    )

    depth_grid = np.array(
        depth_grid,
        dtype=float
    )

    # --------------------------------------------------------
    # STORE RESULTS
    # --------------------------------------------------------

    forecast_results[hour] = {

        "rainfall": rainfall_grid,

        "runoff": runoff_grid,

        "accumulation": accumulation_grid,

        "excess": excess_grid,

        "risk": risk_grid,

        "risk_score": risk_score_grid,

        "depth": depth_grid
    }


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header(
    "🎛️ Forecast Controls"
)

selected_hour = st.sidebar.selectbox(
    "Forecast hour",
    [1, 2, 3],
    format_func=lambda x: f"Hour +{x}"
)


# ============================================================
# CURRENT FORECAST
# ============================================================

result = forecast_results[
    selected_hour
]

rainfall_grid = result["rainfall"]

runoff_grid = result["runoff"]

accumulation_grid = result["accumulation"]

excess_grid = result["excess"]

risk_grid = result["risk"]

risk_score_grid = result["risk_score"]

depth_grid = result["depth"]


# ============================================================
# SIDEBAR ROUTING
# ============================================================

st.sidebar.markdown("---")

st.sidebar.header(
    "🚗 Safer Route"
)


# Create all valid model cells

grid_cells = [

    (r, c)

    for r in range(grid_rows)

    for c in range(grid_cols)
]


# ------------------------------------------------------------
# Default start and destination
# ------------------------------------------------------------

default_start = (
    grid_rows - 1,
    0
)

default_destination = (
    0,
    grid_cols - 1
)


# ------------------------------------------------------------
# Find default indices safely
# ------------------------------------------------------------

if default_start in grid_cells:

    start_index = grid_cells.index(
        default_start
    )

else:

    start_index = 0


if default_destination in grid_cells:

    destination_index = grid_cells.index(
        default_destination
    )

else:

    destination_index = len(grid_cells) - 1


# ------------------------------------------------------------
# Sidebar Start
# ------------------------------------------------------------

start = st.sidebar.selectbox(
    "Start cell",
    grid_cells,
    index=start_index
)


# ------------------------------------------------------------
# Sidebar Destination
# ------------------------------------------------------------

destination = st.sidebar.selectbox(
    "Destination cell",
    grid_cells,
    index=destination_index
)


# ============================================================
# SUMMARY CALCULATIONS
# ============================================================

rainfall_array = np.array(
    rainfall_grid,
    dtype=float
)

runoff_array = np.array(
    runoff_grid,
    dtype=float
)

excess_array = np.array(
    excess_grid,
    dtype=float
)

depth_array = np.array(
    depth_grid,
    dtype=float
)


# ------------------------------------------------------------
# Rainfall
# ------------------------------------------------------------

total_rainfall = rainfall_array.sum()

max_rainfall = rainfall_array.max()


# ------------------------------------------------------------
# Runoff
# ------------------------------------------------------------

total_runoff = runoff_array.sum()

max_runoff = runoff_array.max()


# ------------------------------------------------------------
# Flood depth
# ------------------------------------------------------------

max_depth = depth_array.max()


# ------------------------------------------------------------
# Excess water
# ------------------------------------------------------------

max_excess = excess_array.max()


# ============================================================
# RISK COUNTS
# ============================================================

low_cells = 0

medium_cells = 0

high_cells = 0

severe_cells = 0


for row in range(grid_rows):

    for col in range(grid_cols):

        risk_value = risk_grid[row][col]

        if risk_value == "LOW":

            low_cells += 1

        elif risk_value == "MEDIUM":

            medium_cells += 1

        elif risk_value == "HIGH":

            high_cells += 1

        elif risk_value == "SEVERE":

            severe_cells += 1


# ============================================================
# HEADER SUMMARY
# ============================================================

st.markdown("---")

st.subheader(
    f"⏱️ Flood Forecast — Hour +{selected_hour}"
)


metric1, metric2, metric3, metric4, metric5 = st.columns(5)


metric1.metric(
    "🌧️ Max Rainfall",
    f"{max_rainfall:.1f} mm"
)


metric2.metric(
    "💧 Max Runoff",
    f"{max_runoff:.2f}"
)


metric3.metric(
    "📏 Max Flood Depth",
    f"{max_depth:.2f}"
)


metric4.metric(
    "🟠 High Risk",
    high_cells
)


metric5.metric(
    "🔴 Severe Risk",
    severe_cells
)


# ============================================================
# REAL MAP FLOOD VISUALIZATION
# ============================================================

st.markdown("---")

st.subheader(
    f"🗺️ Flood Risk Map — Central Kolkata — Hour +{selected_hour}"
)

st.caption(
    "Colored cells represent predicted flood risk across "
    "the 20 × 20 model grid. The underlying OpenStreetMap "
    "provides geographical context."
)


# ============================================================
# RISK COLOR FUNCTION
# ============================================================

def get_risk_color(score):

    if score == 0:

        return "#7B2CBF"

    elif score == 1:

        return "#2196F3"

    elif score == 2:

        return "#4CAF50"

    elif score == 3:

        return "#FFD600"

    return "#808080"


# ============================================================
# CREATE FOLIUM MAP
# ============================================================

flood_map = folium.Map(

    location=STUDY_CENTER,

    zoom_start=13,

    tiles="OpenStreetMap",

    control_scale=True
)


# ============================================================
# GRID CELL SIZE
# ============================================================

lat_step = (
    MAX_LAT - MIN_LAT
) / grid_rows


lon_step = (
    MAX_LON - MIN_LON
) / grid_cols


# ============================================================
# DRAW FLOOD GRID
# ============================================================

for row in range(grid_rows):

    for col in range(grid_cols):

        score = int(
            risk_score_grid[row][col]
        )

        risk_name = risk_grid[row][col]

        cell_color = get_risk_color(
            score
        )


        # ----------------------------------------------------
        # Geographic boundaries
        # ----------------------------------------------------

        north = (
            MAX_LAT
            - row * lat_step
        )

        south = (
            MAX_LAT
            - (row + 1) * lat_step
        )

        west = (
            MIN_LON
            + col * lon_step
        )

        east = (
            MIN_LON
            + (col + 1) * lon_step
        )


        cell_coordinates = [

            [north, west],

            [north, east],

            [south, east],

            [south, west]
        ]


        # ----------------------------------------------------
        # Flood cell
        # ----------------------------------------------------

        folium.Polygon(

            locations=cell_coordinates,

            color=cell_color,

            weight=0.5,

            fill=True,

            fill_color=cell_color,

            fill_opacity=0.48,

            popup=(
                f"<b>Flood Risk:</b> {risk_name}<br>"
                f"<b>Risk Score:</b> {score}<br>"
                f"<b>Flood Depth:</b> "
                f"{depth_grid[row][col]:.2f}<br>"
                f"<b>Elevation:</b> "
                f"{DEM[row][col]:.2f}"
            )

        ).add_to(
            flood_map
        )


# ============================================================
# CELL → LAT/LON
# ============================================================

def cell_to_latlon(cell):

    row, col = cell


    latitude = (
        MAX_LAT
        - (row + 0.5) * lat_step
    )


    longitude = (
        MIN_LON
        + (col + 0.5) * lon_step
    )


    return latitude, longitude


# ============================================================
# CALCULATE SAFER ROUTE
# ============================================================

route, route_cost = find_safest_route(

    risk_grid,

    start,

    destination
)


# ============================================================
# ROUTE SUMMARY
# ============================================================

route_summary = None


if route:

    route_summary = calculate_route_summary(

        route,

        risk_grid
    )


# ============================================================
# DRAW ROUTE ON MAP
# ============================================================

if route:

    route_coordinates = []


    for cell in route:

        lat, lon = cell_to_latlon(
            cell
        )

        route_coordinates.append(
            [lat, lon]
        )


    # --------------------------------------------------------
    # SAFER ROUTE
    # --------------------------------------------------------

    folium.PolyLine(

        locations=route_coordinates,

        color="#000000",

        weight=6,

        opacity=1.0,

        tooltip="Dijkstra Safer Route"

    ).add_to(
        flood_map
    )


    # --------------------------------------------------------
    # START MARKER
    # --------------------------------------------------------

    start_lat, start_lon = cell_to_latlon(
        start
    )


    folium.Marker(

        location=[
            start_lat,
            start_lon
        ],

        popup=f"Start: {start}",

        tooltip="START",

        icon=folium.Icon(

            color="blue",

            icon="play"
        )

    ).add_to(
        flood_map
    )


    # --------------------------------------------------------
    # DESTINATION MARKER
    # --------------------------------------------------------

    dest_lat, dest_lon = cell_to_latlon(
        destination
    )


    folium.Marker(

        location=[
            dest_lat,
            dest_lon
        ],

        popup=f"Destination: {destination}",

        tooltip="DESTINATION",

        icon=folium.Icon(

            color="red",

            icon="flag"
        )

    ).add_to(
        flood_map
    )


# ============================================================
# MAP LEGEND
# ============================================================

legend_html = """

<div style="

    position: fixed;

    bottom: 35px;

    left: 35px;

    width: 180px;

    background-color: white;

    border: 2px solid #777;

    z-index: 9999;

    font-size: 14px;

    padding: 12px;

    border-radius: 8px;

    box-shadow: 0 2px 8px rgba(0,0,0,0.25);

    color: #222222;

">

<div style="

    font-weight: bold;

    font-size: 16px;

    margin-bottom: 8px;

    color: #222222;

">

FLOOD RISK

</div>


<div style="

    margin: 6px;

    color: #222222;

">

<span style="

    display:inline-block;

    width:18px;

    height:18px;

    background:#7B2CBF;

    margin-right:7px;

    vertical-align:middle;

    border-radius:3px;

"></span>

LOW

</div>


<div style="

    margin: 6px;

    color: #222222;

">

<span style="

    display:inline-block;

    width:18px;

    height:18px;

    background:#2196F3;

    margin-right:7px;

    vertical-align:middle;

    border-radius:3px;

"></span>

MEDIUM

</div>


<div style="

    margin: 6px;

    color: #222222;

">

<span style="

    display:inline-block;

    width:18px;

    height:18px;

    background:#4CAF50;

    margin-right:7px;

    vertical-align:middle;

    border-radius:3px;

"></span>

HIGH

</div>


<div style="

    margin: 6px;

    color: #222222;

">

<span style="

    display:inline-block;

    width:18px;

    height:18px;

    background:#FFD600;

    margin-right:7px;

    vertical-align:middle;

    border-radius:3px;

"></span>

SEVERE

</div>


</div>

"""


flood_map.get_root().html.add_child(

    folium.Element(
        legend_html
    )
)


# ============================================================
# DISPLAY MAP
# ============================================================

st_folium(

    flood_map,

    width=None,

    height=650,

    returned_objects=[]
)


# ============================================================
# MAP INTERPRETATION
# ============================================================

st.markdown("")


map_col1, map_col2, map_col3 = st.columns(3)


with map_col1:

    st.markdown(
        """
        **🟣 Low Risk**

        Normal or relatively low
        flood exposure.
        """
    )


with map_col2:

    st.markdown(
        """
        **🟢 High Risk**

        Significant excess water
        is predicted.
        """
    )


with map_col3:

    st.markdown(
        """
        **🟡 Severe Risk**

        Extreme predicted excess
        water; routing treats these
        cells as blocked.
        """
    )


# ============================================================
# ROUTING SUMMARY
# ============================================================

st.markdown("---")

st.subheader(
    "🚗 Safer Route"
)


if route:

    route_col1, route_col2, route_col3, route_col4 = (
        st.columns(4)
    )


    route_col1.metric(
        "Route Length",
        f"{route_summary['route_length']} cells"
    )


    route_col2.metric(
        "Medium Risk",
        route_summary["medium_cells"]
    )


    route_col3.metric(
        "High Risk",
        route_summary["high_cells"]
    )


    route_col4.metric(
        "Severe Risk",
        route_summary["severe_cells"]
    )


    st.success(
        f"Safer route found from "
        f"{start} → {destination}"
    )


    with st.expander(
        "View route grid coordinates"
    ):

        route_text = " → ".join(

            f"({row},{col})"

            for row, col in route
        )


        st.code(
            route_text
        )


    st.caption(
        "The routing demonstration uses the 20 × 20 model grid "
        "rather than a real road network. The Dijkstra algorithm "
        "penalizes high-risk cells and blocks severe-risk cells."
    )


else:

    st.error(
        "No safe route is available between the selected "
        "locations for this forecast hour."
    )


    st.warning(
        "Try another start/destination or another forecast hour."
    )


# ============================================================
# MAIN TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(

    [
        "🚦 Flood Risk",

        "🌧️ Rainfall & Runoff",

        "🌊 Water & Drainage",

        "🚗 Safe Routing",

        "📊 Cell Details"
    ]
)


# ============================================================
# TAB 1 — FLOOD RISK
# ============================================================

with tab1:

    st.subheader(
        "Flood Risk Overview"
    )


    risk_col1, risk_col2, risk_col3, risk_col4 = (
        st.columns(4)
    )


    risk_col1.metric(
        "🟣 LOW",
        low_cells
    )


    risk_col2.metric(
        "🔵 MEDIUM",
        medium_cells
    )


    risk_col3.metric(
        "🟢 HIGH",
        high_cells
    )


    risk_col4.metric(
        "🟡 SEVERE",
        severe_cells
    )


    st.markdown(
        "### How the system determines flood risk"
    )


    st.markdown(
        """
        🌧️ **Spatial Rainfall**

        ↓

        💧 **Surface Runoff**

        ↓

        ⛰️ **Terrain determines water flow**

        ↓

        🌊 **Water Accumulation**

        ↓

        🚰 **Drainage Capacity**

        ↓

        💦 **Excess Water**

        ↓

        🚦 **Flood Risk**
        """
    )


    with st.expander(
        "View detailed risk grid"
    ):

        risk_dataframe = pd.DataFrame(
            risk_grid
        )


        st.dataframe(

            risk_dataframe,

            use_container_width=True,

            hide_index=True
        )


    with st.expander(
        "View numerical risk scores"
    ):

        score_dataframe = pd.DataFrame(
            risk_score_grid
        )


        st.dataframe(

            score_dataframe,

            use_container_width=True,

            hide_index=True
        )


# ============================================================
# TAB 2 — RAINFALL & RUNOFF
# ============================================================

with tab2:

    st.subheader(
        f"🌧️ Rainfall & Runoff — Hour +{selected_hour}"
    )


    rainfall_col, runoff_col = st.columns(2)


    # ========================================================
    # RAINFALL
    # ========================================================

    with rainfall_col:

        st.markdown(
            "### 🌧️ Spatial Rainfall"
        )


        fig, ax = plt.subplots(
            figsize=(7, 6)
        )


        rainfall_image = ax.imshow(

            rainfall_grid,

            interpolation="nearest"
        )


        ax.set_title(
            f"Rainfall — Hour +{selected_hour}"
        )


        ax.set_xlabel(
            "Grid Column"
        )


        ax.set_ylabel(
            "Grid Row"
        )


        plt.colorbar(

            rainfall_image,

            ax=ax,

            label="Rainfall"
        )


        st.pyplot(

            fig,

            use_container_width=True
        )


        plt.close(fig)


        st.metric(

            "Maximum Rainfall",

            f"{max_rainfall:.1f} mm"
        )


    # ========================================================
    # RUNOFF
    # ========================================================

    with runoff_col:

        st.markdown(
            "### 💧 Surface Runoff"
        )


        fig, ax = plt.subplots(
            figsize=(7, 6)
        )


        runoff_image = ax.imshow(

            runoff_grid,

            interpolation="nearest"
        )


        ax.set_title(
            f"Runoff — Hour +{selected_hour}"
        )


        ax.set_xlabel(
            "Grid Column"
        )


        ax.set_ylabel(
            "Grid Row"
        )


        plt.colorbar(

            runoff_image,

            ax=ax,

            label="Runoff"
        )


        st.pyplot(

            fig,

            use_container_width=True
        )


        plt.close(fig)


        st.metric(

            "Maximum Runoff",

            f"{max_runoff:.2f}"
        )


    st.info(
        "The current prototype uses a runoff coefficient of 0.80. "
        "Future versions can use land-cover and imperviousness "
        "data for spatially varying runoff coefficients."
    )


    with st.expander(
        "View rainfall matrix"
    ):

        st.dataframe(

            pd.DataFrame(
                rainfall_grid
            ),

            use_container_width=True,

            hide_index=True
        )


    with st.expander(
        "View runoff matrix"
    ):

        st.dataframe(

            pd.DataFrame(
                runoff_grid
            ),

            use_container_width=True,

            hide_index=True
        )


# ============================================================
# TAB 3 — WATER & DRAINAGE
# ============================================================

with tab3:

    st.subheader(
        f"🌊 Water Movement & Drainage — Hour +{selected_hour}"
    )


    # ========================================================
    # ACCUMULATION
    # ========================================================

    st.markdown(
        "### 🌊 Terrain-driven Water Accumulation"
    )


    fig, ax = plt.subplots(
        figsize=(10, 6)
    )


    accumulation_image = ax.imshow(

        accumulation_grid,

        interpolation="nearest"
    )


    ax.set_title(
        f"Water Accumulation — Hour +{selected_hour}"
    )


    ax.set_xlabel(
        "Grid Column"
    )


    ax.set_ylabel(
        "Grid Row"
    )


    plt.colorbar(

        accumulation_image,

        ax=ax,

        label="Accumulated Water"
    )


    st.pyplot(

        fig,

        use_container_width=True
    )


    plt.close(fig)


    # ========================================================
    # DRAINAGE + EXCESS
    # ========================================================

    drainage_col, excess_col = st.columns(2)


    # ========================================================
    # DRAINAGE
    # ========================================================

    with drainage_col:

        st.markdown(
            "### 🚰 Drainage Capacity"
        )


        drainage_array = np.array(

            DRAINAGE_CAPACITY_GRID,

            dtype=float
        )


        fig, ax = plt.subplots(
            figsize=(7, 5)
        )


        drainage_image = ax.imshow(

            drainage_array,

            interpolation="nearest"
        )


        ax.set_title(
            "Drainage Capacity"
        )


        ax.set_xlabel(
            "Grid Column"
        )


        ax.set_ylabel(
            "Grid Row"
        )


        plt.colorbar(

            drainage_image,

            ax=ax,

            label="Capacity"
        )


        st.pyplot(

            fig,

            use_container_width=True
        )


        plt.close(fig)


        st.caption(
            f"Drainage grid: "
            f"{drainage_array.shape[0]} × "
            f"{drainage_array.shape[1]}"
        )


    # ========================================================
    # EXCESS WATER
    # ========================================================

    with excess_col:

        st.markdown(
            "### 💦 Excess Water"
        )


        fig, ax = plt.subplots(
            figsize=(7, 5)
        )


        excess_image = ax.imshow(

            excess_grid,

            interpolation="nearest"
        )


        ax.set_title(
            "Water Remaining After Drainage"
        )


        ax.set_xlabel(
            "Grid Column"
        )


        ax.set_ylabel(
            "Grid Row"
        )


        plt.colorbar(

            excess_image,

            ax=ax,

            label="Excess Water"
        )


        st.pyplot(

            fig,

            use_container_width=True
        )


        plt.close(fig)


    st.info(
        "Excess water represents the water remaining after "
        "available drainage capacity is accounted for."
    )


    with st.expander(
        "View accumulation matrix"
    ):

        st.dataframe(

            pd.DataFrame(
                accumulation_grid
            ),

            use_container_width=True,

            hide_index=True
        )


    with st.expander(
        "View drainage matrix"
    ):

        st.dataframe(

            pd.DataFrame(
                DRAINAGE_CAPACITY_GRID
            ),

            use_container_width=True,

            hide_index=True
        )


    with st.expander(
        "View excess-water matrix"
    ):

        st.dataframe(

            pd.DataFrame(
                excess_grid
            ),

            use_container_width=True,

            hide_index=True
        )


# ============================================================
# TAB 4 — SAFE ROUTING
# ============================================================

with tab4:

    st.subheader(
        f"🚗 Flood-aware Routing — Hour +{selected_hour}"
    )


    st.markdown(
        """
        ### Routing Strategy

        The prototype uses **Dijkstra's shortest-path algorithm**
        with flood-risk-based movement costs.

        🟣 **LOW** → Normal movement cost

        🔵 **MEDIUM** → Increased cost

        🟢 **HIGH** → Strongly penalized

        🟡 **SEVERE** → Blocked
        """
    )


    st.write(
        f"**Start:** `{start}`"
    )


    st.write(
        f"**Destination:** `{destination}`"
    )


    if route:

        st.success(
            "A safer route is available for the selected "
            "flood forecast."
        )


        st.markdown(
            "### Recommended Route"
        )


        route_text = " → ".join(

            f"({row},{col})"

            for row, col in route
        )


        st.code(
            route_text
        )


        route_col1, route_col2, route_col3, route_col4 = (
            st.columns(4)
        )


        route_col1.metric(
            "Route Length",
            f"{route_summary['route_length']} cells"
        )


        route_col2.metric(
            "Medium Risk",
            route_summary["medium_cells"]
        )


        route_col3.metric(
            "High Risk",
            route_summary["high_cells"]
        )


        route_col4.metric(
            "Severe Risk",
            route_summary["severe_cells"]
        )


        st.info(
            "The main map above shows this route directly "
            "over the geographical map."
        )


    else:

        st.error(
            "No safe route is available between the selected "
            "locations for this forecast hour."
        )


# ============================================================
# CELL DETAILS
# ============================================================

# The drainage grid may have a different size from the
# 20 × 20 model grid. Therefore all drainage accesses
# below are bounds-checked.


# ============================================================
# HIGH-RISK LOCATIONS
# ============================================================

st.markdown("---")


st.subheader(
    f"🚨 High-Risk Locations — Hour +{selected_hour}"
)


high_risk_cells = []


for row in range(grid_rows):

    for col in range(grid_cols):

        if risk_score_grid[row][col] >= 2:

            high_risk_cells.append(

                {

                    "Location":
                        f"Grid ({row}, {col})",


                    "Elevation":
                        round(
                            DEM[row][col],
                            2
                        ),


                    "Excess Water":
                        round(
                            excess_grid[row][col],
                            2
                        ),


                    "Risk":
                        risk_grid[row][col],


                    "Flood Depth":
                        round(
                            depth_grid[row][col],
                            2
                        )

                }

            )


if high_risk_cells:

    high_risk_dataframe = pd.DataFrame(

        high_risk_cells
    )


    st.dataframe(

        high_risk_dataframe,

        use_container_width=True,

        hide_index=True
    )


else:

    st.success(
        "No HIGH or SEVERE flood-risk cells "
        "for this forecast hour."
    )


# ============================================================
# CELL DETAILS TAB
# ============================================================

with tab5:

    st.subheader(
        "📊 Spatial Cell Analysis"
    )


    st.caption(
        f"Showing detailed information for "
        f"{total_cells} model cells."
    )


    cell_data = []


    # --------------------------------------------------------
    # SAFE DRAINAGE ARRAY
    # --------------------------------------------------------

    drainage_array = np.array(

        DRAINAGE_CAPACITY_GRID,

        dtype=float
    )


    drainage_rows, drainage_cols = (
        drainage_array.shape
    )


    # --------------------------------------------------------
    # CREATE CELL DATA
    # --------------------------------------------------------

    for row in range(grid_rows):

        for col in range(grid_cols):

            # ------------------------------------------------
            # SAFE DRAINAGE ACCESS
            # ------------------------------------------------

            if (

                row < drainage_rows

                and col < drainage_cols

            ):

                drainage_value = (
                    drainage_array[row, col]
                )

            else:

                drainage_value = np.nan


            # ------------------------------------------------
            # CELL RECORD
            # ------------------------------------------------

            cell_data.append(

                {

                    "Cell":
                        f"({row}, {col})",


                    "Elevation":
                        round(
                            DEM[row][col],
                            2
                        ),


                    "Rainfall":
                        round(
                            rainfall_grid[row][col],
                            2
                        ),


                    "Runoff":
                        round(
                            runoff_grid[row][col],
                            2
                        ),


                    "Accumulation":
                        round(
                            accumulation_grid[row][col],
                            2
                        ),


                    "Drainage":
                        drainage_value,


                    "Excess Water":
                        round(
                            excess_grid[row][col],
                            2
                        ),


                    "Flood Risk":
                        risk_grid[row][col],


                    "Risk Score":
                        risk_score_grid[row][col],


                    "Flood Depth":
                        round(
                            depth_grid[row][col],
                            2
                        )

                }

            )


    cell_dataframe = pd.DataFrame(
        cell_data
    )


    st.dataframe(

        cell_dataframe,

        use_container_width=True,

        hide_index=True
    )


# ============================================================
# FINAL PRESENTATION MESSAGE
# ============================================================

st.markdown("---")


st.subheader(
    "💡 What This Prototype Demonstrates"
)


story_col1, story_col2, story_col3 = st.columns(3)


with story_col1:

    st.markdown(
        """
        ### 🌧️ Predict

        Forecast spatial rainfall for
        the next 1–3 hours.
        """
    )


with story_col2:

    st.markdown(
        """
        ### 🌊 Understand

        Combine rainfall, runoff, terrain,
        accumulation and drainage to estimate
        where flooding may occur.
        """
    )


with story_col3:

    st.markdown(
        """
        ### 🚗 Respond

        Use predicted flood risk to identify
        safer routes around hazardous cells.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")


st.caption(
    "Urban Flood Nowcasting Prototype | "
    "Central Kolkata | "
    "20 × 20 model grid | "
    "Real DEM | "
    "Prototype rainfall input | "
    "Flood depth is a prototype estimate and is not a calibrated "
    "hydraulic prediction | "
    "Routing uses a simplified grid network."
)