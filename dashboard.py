import streamlit as st

from rainfall import get_rainfall_data
from forecast import forecast_next_3_hours
from runoff import calculate_runoff
from terrain import calculate_accumulation
from drainage import calculate_excess_water
from flood import calculate_flood_risk, calculate_flood_depth


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Urban Flood Nowcasting",
    page_icon="🌊",
    layout="wide"
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
        font-size: 18px;
        color: #777777;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    .risk-box {
        padding: 22px;
        border-radius: 14px;
        text-align: center;
        font-size: 30px;
        font-weight: 800;
        margin-bottom: 20px;
    }

    .risk-low {
        background-color: #d4edda;
        color: #155724;
    }

    .risk-medium {
        background-color: #fff3cd;
        color: #856404;
    }

    .risk-high {
        background-color: #ffe0b2;
        color: #8a4b08;
    }

    .risk-severe {
        background-color: #f8d7da;
        color: #721c24;
    }

    .map-cell {
        padding: 25px 5px;
        border-radius: 10px;
        text-align: center;
        font-size: 16px;
        font-weight: 800;
        margin: 4px;
    }

    .depth-cell {
        padding: 25px 5px;
        border-radius: 10px;
        text-align: center;
        font-size: 18px;
        font-weight: 800;
        margin: 4px;
        background-color: #e7f1ff;
        color: #000000 !important;
    }

    .legend-cell {
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        font-weight: 700;
    }

    .status-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #f0f2f6;
        text-align: center;
        font-weight: 600;
        color: #000000 !important;
    }

    .footer {
        text-align: center;
        color: #888888;
        padding-top: 30px;
        padding-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🌊 Urban Flood Nowcasting System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    '0–3 Hour Urban Flood Prediction • Prototype Monitoring Dashboard'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SYSTEM STATUS
# ============================================================

status_columns = st.columns(3)

with status_columns[0]:
    st.markdown(
        '<div class="status-box">🟢 MODEL STATUS<br>ONLINE</div>',
        unsafe_allow_html=True
    )

with status_columns[1]:
    st.markdown(
        '<div class="status-box">🗺️ GRID<br>4 × 4 DEM</div>',
        unsafe_allow_html=True
    )

with status_columns[2]:
    st.markdown(
        '<div class="status-box">⏱️ FORECAST<br>0–3 HOURS</div>',
        unsafe_allow_html=True
    )


# ============================================================
# LOAD RAINFALL DATA
# ============================================================

rainfall_data = get_rainfall_data()

rainfall_values = [
    row[2] for row in rainfall_data
]


# ============================================================
# RAINFALL FORECAST
# ============================================================

forecast = forecast_next_3_hours(rainfall_values)


st.markdown(
    '<div class="section-title">🌧️ Rainfall Forecast</div>',
    unsafe_allow_html=True
)

forecast_columns = st.columns(3)

for i, rainfall in enumerate(forecast):

    with forecast_columns[i]:

        st.metric(
            label=f"Hour {i + 1}",
            value=f"{rainfall:.1f} mm"
        )


# ============================================================
# PROCESS FORECAST HOURS
# ============================================================

results = []

for rainfall in forecast:

    # Current prototype runoff coefficient
    runoff = calculate_runoff(
        rainfall,
        0.8
    )

    runoff_grid = [
        [runoff, runoff, runoff, runoff],
        [runoff, runoff, runoff, runoff],
        [runoff, runoff, runoff, runoff],
        [runoff, runoff, runoff, runoff]
    ]

    accumulation = calculate_accumulation(
        runoff_grid
    )

    excess = calculate_excess_water(
        accumulation,
        100
    )

    risk = calculate_flood_risk(
        excess
    )

    depth = calculate_flood_depth(
        excess
    )

    results.append(
        {
            "rainfall": rainfall,
            "runoff": runoff,
            "accumulation": accumulation,
            "excess": excess,
            "risk": risk,
            "depth": depth
        }
    )


# ============================================================
# FORECAST TIMELINE
# ============================================================

st.markdown(
    '<div class="section-title">🕐 Forecast Timeline</div>',
    unsafe_allow_html=True
)

selected_hour = st.radio(
    "Select forecast horizon:",
    ["Hour 1", "Hour 2", "Hour 3"],
    horizontal=True
)

hour_index = int(
    selected_hour.split()[1]
) - 1

result = results[hour_index]


# ============================================================
# SUMMARY
# ============================================================

st.markdown(
    f'<div class="section-title">📊 {selected_hour} Prediction</div>',
    unsafe_allow_html=True
)

max_depth = max(
    max(row) for row in result["depth"]
)

max_excess = max(
    max(row) for row in result["excess"]
)


# ============================================================
# OVERALL RISK
# ============================================================

risk_priority = {
    "LOW": 0,
    "MEDIUM": 1,
    "HIGH": 2,
    "SEVERE": 3
}

overall_risk = "LOW"

for row in result["risk"]:

    for risk_value in row:

        if risk_priority[risk_value] > risk_priority[overall_risk]:

            overall_risk = risk_value


# ============================================================
# KPI CARDS
# ============================================================

kpi_columns = st.columns(4)

with kpi_columns[0]:

    st.metric(
        "🌧️ Rainfall",
        f"{result['rainfall']:.1f} mm"
    )

with kpi_columns[1]:

    st.metric(
        "💧 Runoff",
        f"{result['runoff']:.1f} mm"
    )

with kpi_columns[2]:

    st.metric(
        "💦 Max Excess",
        f"{max_excess:.1f} mm"
    )

with kpi_columns[3]:

    st.metric(
        "📏 Max Depth",
        f"{max_depth:.2f} m"
    )


# ============================================================
# OVERALL RISK
# ============================================================

st.markdown(
    '<div class="section-title">🚦 Overall Flood Risk</div>',
    unsafe_allow_html=True
)

risk_class = {
    "LOW": "risk-low",
    "MEDIUM": "risk-medium",
    "HIGH": "risk-high",
    "SEVERE": "risk-severe"
}

st.markdown(
    f"""
    <div class="risk-box {risk_class[overall_risk]}">
        {overall_risk}
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FLOOD RISK MAP
# ============================================================

st.markdown(
    '<div class="section-title">🗺️ Flood Risk Map</div>',
    unsafe_allow_html=True
)

risk_background = {
    "LOW": "#d4edda",
    "MEDIUM": "#fff3cd",
    "HIGH": "#ffe0b2",
    "SEVERE": "#f8d7da"
}

risk_text = {
    "LOW": "#155724",
    "MEDIUM": "#856404",
    "HIGH": "#8a4b08",
    "SEVERE": "#721c24"
}


for row in result["risk"]:

    columns = st.columns(4)

    for index, risk_value in enumerate(row):

        with columns[index]:

            st.markdown(
                f"""
                <div class="map-cell"
                     style="
                     background-color:{risk_background[risk_value]};
                     color:{risk_text[risk_value]};
                     ">
                    {risk_value}
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# LEGEND
# ============================================================

legend_columns = st.columns(4)

legend_items = [
    ("LOW", "#d4edda", "#155724"),
    ("MEDIUM", "#fff3cd", "#856404"),
    ("HIGH", "#ffe0b2", "#8a4b08"),
    ("SEVERE", "#f8d7da", "#721c24")
]

for i, item in enumerate(legend_items):

    label, background, text_color = item

    with legend_columns[i]:

        st.markdown(
            f"""
            <div class="legend-cell"
                 style="
                 background-color:{background};
                 color:{text_color};
                 ">
                {label}
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# FLOOD DEPTH MAP
# ============================================================

st.markdown(
    '<div class="section-title">📏 Flood Depth Map</div>',
    unsafe_allow_html=True
)

for row in result["depth"]:

    columns = st.columns(4)

    for index, depth_value in enumerate(row):

        with columns[index]:

            st.markdown(
                f"""
                <div class="depth-cell">
                    {depth_value:.2f} m
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# MODEL PIPELINE
# ============================================================

st.markdown(
    '<div class="section-title">🔄 Prediction Pipeline</div>',
    unsafe_allow_html=True
)

pipeline_columns = st.columns(7)

pipeline_steps = [
    "🌧️\nRainfall",
    "💧\nRunoff",
    "⛰️\nTerrain",
    "🌊\nAccumulation",
    "🚰\nDrainage",
    "🚦\nRisk",
    "📏\nDepth"
]

for i, step in enumerate(pipeline_steps):

    with pipeline_columns[i]:

        st.markdown(
            f"""
            <div class="status-box">
                {step.replace(chr(10), '<br>')}
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# MODEL ASSUMPTIONS
# ============================================================

st.markdown(
    '<div class="section-title">ℹ️ Model Assumptions</div>',
    unsafe_allow_html=True
)

info_columns = st.columns(3)

with info_columns[0]:

    st.info(
        """
        **Rainfall → Runoff**

        Runoff coefficient:
        **0.8**

        Runoff = Rainfall × 0.8
        """
    )

with info_columns[1]:

    st.info(
        """
        **Drainage**

        Prototype drainage capacity:
        **100 mm**

        Excess water occurs when
        accumulated water exceeds capacity.
        """
    )

with info_columns[2]:

    st.info(
        """
        **Forecast**

        Uses recent rainfall observations
        as a simple baseline for the
        next 3 hours.
        """
    )


# ============================================================
# PROTOTYPE NOTICE
# ============================================================

st.warning(
    """
    ⚠️ **Prototype Notice**

    This hackathon prototype uses a simplified rainfall forecast,
    artificial 4×4 DEM, prototype drainage capacity, and simplified
    flood-depth estimation. Operational deployment would require
    real-time rainfall, calibrated hydrological parameters, real DEM/GIS
    data, drainage-network information, and validation against observed
    flood events.
    """
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Urban Flood Nowcasting System • Hackathon Prototype
    </div>
    """,
    unsafe_allow_html=True
)