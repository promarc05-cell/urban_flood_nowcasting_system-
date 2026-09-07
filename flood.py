# flood.py


# ============================================================
# FLOOD RISK THRESHOLDS
# ============================================================

# These are prototype thresholds.
# They should be calibrated later using real flood observations.

MEDIUM_THRESHOLD = 25
HIGH_THRESHOLD = 75


# ============================================================
# FLOOD RISK
# ============================================================

def calculate_flood_risk(excess_water_grid):
    """
    Convert excess water into flood-risk categories.

    Risk levels:

        0              -> LOW
        > 0 to 25      -> MEDIUM
        > 25 to 75     -> HIGH
        > 75           -> SEVERE

    Parameters:
        excess_water_grid:
            2D grid containing excess water.

    Returns:
        2D grid containing risk categories.
    """

    risk_grid = []

    for row in excess_water_grid:

        risk_row = []

        for excess_water in row:

            if excess_water <= 0:
                risk = "LOW"

            elif excess_water <= MEDIUM_THRESHOLD:
                risk = "MEDIUM"

            elif excess_water <= HIGH_THRESHOLD:
                risk = "HIGH"

            else:
                risk = "SEVERE"

            risk_row.append(risk)

        risk_grid.append(risk_row)

    return risk_grid


# ============================================================
# FLOOD DEPTH
# ============================================================

def calculate_flood_depth(
    excess_water_grid,
    depth_factor=0.01
):
    """
    Estimate flood depth from excess water.

    Prototype relationship:

        Flood Depth = Excess Water × Depth Factor

    Example:

        Excess Water = 50
        Depth Factor = 0.01

        Depth = 0.50

    IMPORTANT:
        This is a prototype estimate, not a physically
        calibrated hydraulic depth model.
    """

    depth_grid = []

    for row in excess_water_grid:

        depth_row = []

        for excess_water in row:

            depth = max(
                excess_water * depth_factor,
                0
            )

            depth_row.append(depth)

        depth_grid.append(depth_row)

    return depth_grid


# ============================================================
# FLOOD RISK SCORE
# ============================================================

def calculate_risk_score(excess_water_grid):
    """
    Convert excess water into a simple numerical risk score.

    Score range:

        0   -> No flood risk
        1   -> Medium
        2   -> High
        3   -> Severe

    This can be useful later for the dashboard and routing.
    """

    score_grid = []

    for row in excess_water_grid:

        score_row = []

        for excess_water in row:

            if excess_water <= 0:
                score = 0

            elif excess_water <= MEDIUM_THRESHOLD:
                score = 1

            elif excess_water <= HIGH_THRESHOLD:
                score = 2

            else:
                score = 3

            score_row.append(score)

        score_grid.append(score_row)

    return score_grid


# ============================================================
# PRINT FUNCTIONS
# ============================================================

def print_risk_grid(risk_grid):
    """
    Print flood risk categories.
    """

    print("\nFlood Risk:")

    for row in risk_grid:

        print(
            "  ".join(
                f"{value:8}"
                for value in row
            )
        )


def print_depth_grid(depth_grid):
    """
    Print estimated flood depth.
    """

    print("\nEstimated Flood Depth:")

    for row in depth_grid:

        print(
            "  ".join(
                f"{value:8.2f}"
                for value in row
            )
        )


def print_risk_score_grid(score_grid):
    """
    Print numerical flood risk scores.
    """

    print("\nFlood Risk Score:")

    for row in score_grid:

        print(
            "  ".join(
                f"{value:8}"
                for value in row
            )
        )

