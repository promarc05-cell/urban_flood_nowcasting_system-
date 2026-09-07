# dashboard.py

import streamlit as st
import pandas as pd

from rainfall import (
    get_spatial_rainfall_forecast,
    validate_rainfall_forecast
)

from runoff import calculate_spatial_runoff

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
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title(
    "🌊 Urban Flood Nowcasting System"
)

st.markdown(
    """
    ### Hyper-local 0–3 Hour Flood Risk & Safe Routing

    **External rainfall nowcast → Runoff → Terrain flow →
    Water accumulation → Drainage → Flood risk → Flood depth
    → Safe routing**
    """
)

st.info(
    "Prototype mode: rainfall is currently simulated as a "
    "radar-like spatial field. The production architecture "
    "is designed to ingest an external 0–3 hour rainfall "
    "nowcast from a weather radar/API."
)


# ============================================================
# LOAD RAINFALL
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
# PROCESS FORECAST
# ============================================================

forecast_results = {}


for hour in range(1, 4):

    rainfall_grid = rainfall_forecast[hour]

    # Spatial runoff
    runoff_grid = calculate_spatial_runoff(
        rainfall_grid
    )

    # Terrain accumulation
    accumulation_grid = calculate_accumulation(
        runoff_grid,
        DEM
    )

    # Drainage
    excess_grid = calculate_excess_water(
        accumulation_grid,
        DRAINAGE_CAPACITY_GRID
    )

    # Flood risk
    risk_grid = calculate_flood_risk(
        excess_grid
    )

    # Risk score
    risk_score_grid = calculate_risk_score(
        excess_grid
    )

    # Flood depth
    depth_grid = calculate_flood_depth(
        excess_grid,
        0.01
    )

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
    "Forecast Controls"
)

selected_hour = st.sidebar.selectbox(
    "Forecast hour",
    [1, 2, 3],
    format_func=lambda x: f"Hour +{x}"
)


# ============================================================
# ROUTING CONTROLS
# ============================================================

st.sidebar.markdown("---")

st.sidebar.header(
    "🚗 Safe Routing"
)

grid_cells = [
    (r, c)
    for r in range(4)
    for c in range(4)
]


start = st.sidebar.selectbox(
    "Start location",
    grid_cells,
    index=12
)

destination = st.sidebar.selectbox(
    "Destination",
    grid_cells,
    index=3
)


# ============================================================
# CURRENT FORECAST DATA
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
# SUMMARY METRICS
# ============================================================

total_rainfall = sum(
    sum(row)
    for row in rainfall_grid
)

total_runoff = sum(
    sum(row)
    for row in runoff_grid
)

max_depth = max(
    max(row)
    for row in depth_grid
)

max_excess = max(
    max(row)
    for row in excess_grid
)

high_cells = sum(
    1
    for row in risk_grid
    for value in row
    if value == "HIGH"
)

severe_cells = sum(
    1
    for row in risk_grid
    for value in row
    if value == "SEVERE"
)


col1, col2, col3, col4, col5 = st.columns(5)


col1.metric(
    "Forecast",
    f"+{selected_hour} hr"
)

col2.metric(
    "Total Rainfall",
    f"{total_rainfall:.1f} mm"
)

col3.metric(
    "Total Runoff",
    f"{total_runoff:.1f}"
)

col4.metric(
    "Max Flood Depth",
    f"{max_depth:.2f}"
)

col5.metric(
    "High / Severe",
    f"{high_cells} / {severe_cells}"
)


# ============================================================
# TABS
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
        f"Flood Risk — Hour +{selected_hour}"
    )

    risk_dataframe = pd.DataFrame(
        risk_grid,
        index=[
            "Row 0",
            "Row 1",
            "Row 2",
            "Row 3"
        ],
        columns=[
            "Cell 0",
            "Cell 1",
            "Cell 2",
            "Cell 3"
        ]
    )

    st.dataframe(
        risk_dataframe,
        use_container_width=True
    )

    st.subheader(
        "Numerical Risk Score"
    )

    score_dataframe = pd.DataFrame(
        risk_score_grid,
        index=[
            "Row 0",
            "Row 1",
            "Row 2",
            "Row 3"
        ],
        columns=[
            "Cell 0",
            "Cell 1",
            "Cell 2",
            "Cell 3"
        ]
    )

    st.dataframe(
        score_dataframe,
        use_container_width=True
    )

    st.markdown(
        """
        **Risk Score**

        `0 = LOW`

        `1 = MEDIUM`

        `2 = HIGH`

        `3 = SEVERE`
        """
    )


# ============================================================
# TAB 2 — RAINFALL & RUNOFF
# ============================================================

with tab2:

    left, right = st.columns(2)

    with left:

        st.subheader(
            "🌧️ Rainfall"
        )

        rainfall_dataframe = pd.DataFrame(
            rainfall_grid
        )

        st.dataframe(
            rainfall_dataframe,
            use_container_width=True
        )

    with right:

        st.subheader(
            "💧 Runoff"
        )

        runoff_dataframe = pd.DataFrame(
            runoff_grid
        )

        st.dataframe(
            runoff_dataframe,
            use_container_width=True
        )

    st.markdown(
        """
        ### Spatial runoff

        Every cell has its own runoff coefficient.

        Therefore:

        **Same rainfall ≠ same runoff**
        """
    )


# ============================================================
# TAB 3 — WATER & DRAINAGE
# ============================================================

with tab3:

    st.subheader(
        "🌊 Water Accumulation"
    )

    accumulation_dataframe = pd.DataFrame(
        accumulation_grid
    )

    st.dataframe(
        accumulation_dataframe,
        use_container_width=True
    )

    st.subheader(
        "🚰 Drainage Capacity"
    )

    drainage_dataframe = pd.DataFrame(
        DRAINAGE_CAPACITY_GRID
    )

    st.dataframe(
        drainage_dataframe,
        use_container_width=True
    )

    st.subheader(
        "💦 Excess Water"
    )

    excess_dataframe = pd.DataFrame(
        excess_grid
    )

    st.dataframe(
        excess_dataframe,
        use_container_width=True
    )


# ============================================================
# TAB 4 — SAFE ROUTING
# ============================================================

with tab4:

    st.subheader(
        f"🚗 Flood-aware Route — Hour +{selected_hour}"
    )

    st.write(
        f"**Start:** {start}"
    )

    st.write(
        f"**Destination:** {destination}"
    )

    route, route_cost = find_safest_route(
        risk_grid,
        start,
        destination
    )

    if route:

        summary = calculate_route_summary(
            route,
            risk_grid
        )

        st.success(
            "A safe route is available."
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

        # Route statistics
        route_col1, route_col2, route_col3, route_col4 = (
            st.columns(4)
        )

        route_col1.metric(
            "Route Length",
            f"{summary['route_length']} cells"
        )

        route_col2.metric(
            "Medium Risk",
            summary["medium_cells"]
        )

        route_col3.metric(
            "High Risk",
            summary["high_cells"]
        )

        route_col4.metric(
            "Severe Risk",
            summary["severe_cells"]
        )

        st.markdown(
            """
            ### Routing logic

            The routing engine:

            - Allows LOW-risk cells normally.
            - Penalizes MEDIUM-risk cells.
            - Strongly penalizes HIGH-risk cells.
            - Blocks SEVERE-risk cells.

            Therefore, the route dynamically changes
            according to the predicted flood conditions.
            """
        )

        # ----------------------------------------------------
        # ROUTE GRID
        # ----------------------------------------------------

        st.subheader(
            "Route Grid"
        )

        route_set = set(route)

        route_grid = []

        for r in range(4):

            row_values = []

            for c in range(4):

                cell = (r, c)

                if cell == start:

                    value = "START"

                elif cell == destination:

                    value = "END"

                elif cell in route_set:

                    value = "ROUTE"

                else:

                    value = risk_grid[r][c]

                row_values.append(value)

            route_grid.append(
                row_values
            )

        route_dataframe = pd.DataFrame(
            route_grid,
            columns=[
                "Cell 0",
                "Cell 1",
                "Cell 2",
                "Cell 3"
            ]
        )

        st.dataframe(
            route_dataframe,
            use_container_width=True
        )

    else:

        st.error(
            "No safe route is available between "
            "the selected locations for this forecast hour."
        )

        st.warning(
            "Try another start/destination or a "
            "different forecast hour."
        )


# ============================================================
# TAB 5 — CELL DETAILS
# ============================================================

with tab5:

    st.subheader(
        "📊 Spatial Cell Analysis"
    )

    cell_data = []

    for row in range(4):

        for col in range(4):

            cell_data.append(
                {
                    "Cell": f"({row}, {col})",
                    "Elevation": DEM[row][col],
                    "Rainfall": rainfall_grid[row][col],
                    "Runoff": runoff_grid[row][col],
                    "Accumulation": accumulation_grid[row][col],
                    "Drainage": DRAINAGE_CAPACITY_GRID[row][col],
                    "Excess Water": excess_grid[row][col],
                    "Flood Risk": risk_grid[row][col],
                    "Risk Score": risk_score_grid[row][col],
                    "Flood Depth": depth_grid[row][col]
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
# HIGH-RISK LOCATIONS
# ============================================================

st.markdown("---")

st.subheader(
    f"🚨 High-Risk Locations — Hour +{selected_hour}"
)

high_risk_cells = []

for row in range(4):

    for col in range(4):

        if risk_score_grid[row][col] >= 2:

            high_risk_cells.append(
                {
                    "Location": f"Grid ({row}, {col})",
                    "Elevation": DEM[row][col],
                    "Excess Water": round(
                        excess_grid[row][col],
                        2
                    ),
                    "Risk": risk_grid[row][col],
                    "Flood Depth": round(
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
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Urban Flood Nowcasting Prototype | "
    "Rainfall input is simulated for demonstration | "
    "Flood depth is a prototype estimate and is not "
    "a calibrated hydraulic prediction | "
    "Routing uses a simplified grid network."
)

