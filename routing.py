# routing.py

import heapq


# ============================================================
# ROUTING COSTS
# ============================================================
#
# Lower cost = safer / easier to travel through.
#
# LOW       -> normal movement
# MEDIUM    -> moderate penalty
# HIGH      -> very high penalty
# SEVERE    -> blocked
# ============================================================

RISK_COST = {
    "LOW": 1,
    "MEDIUM": 5,
    "HIGH": 25,
    "SEVERE": float("inf")
}


# ============================================================
# GRID NEIGHBORS
# ============================================================

def get_route_neighbors(row, col, rows, cols):
    """
    Return the four directly connected neighboring cells.

    Routing uses:
        Up
        Down
        Left
        Right

    Diagonal movement is not allowed.
    """

    directions = [
        (-1, 0),   # Up
        (1, 0),    # Down
        (0, -1),   # Left
        (0, 1)     # Right
    ]

    neighbors = []

    for dr, dc in directions:

        nr = row + dr
        nc = col + dc

        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))

    return neighbors


# ============================================================
# SAFEST ROUTE
# ============================================================

def find_safest_route(
    risk_grid,
    start,
    destination
):
    """
    Find the safest route between two grid cells.

    Uses Dijkstra's shortest-path algorithm.

    Risk costs:

        LOW       = 1
        MEDIUM    = 5
        HIGH      = 25
        SEVERE    = blocked

    Parameters:
        risk_grid:
            2D grid containing risk categories.

        start:
            Tuple (row, col).

        destination:
            Tuple (row, col).

    Returns:
        route, total_cost

        route:
            List of cells from start to destination.

        total_cost:
            Total route cost.

        If no route exists:
            returns [], infinity
    """

    rows = len(risk_grid)
    cols = len(risk_grid[0])

    # Validate start
    if not (
        0 <= start[0] < rows
        and 0 <= start[1] < cols
    ):
        raise ValueError("Invalid start location.")

    # Validate destination
    if not (
        0 <= destination[0] < rows
        and 0 <= destination[1] < cols
    ):
        raise ValueError("Invalid destination location.")

    # Severe start/destination cannot be used
    if risk_grid[start[0]][start[1]] == "SEVERE":
        return [], float("inf")

    if risk_grid[destination[0]][destination[1]] == "SEVERE":
        return [], float("inf")

    # Priority queue
    queue = []

    heapq.heappush(
        queue,
        (0, start)
    )

    # Best known cost to each cell
    distances = {
        start: 0
    }

    # Previous cell for reconstructing route
    previous = {}

    while queue:

        current_cost, current = heapq.heappop(queue)

        # Ignore outdated queue entries
        if current_cost > distances.get(
            current,
            float("inf")
        ):
            continue

        # Destination reached
        if current == destination:
            break

        row, col = current

        neighbors = get_route_neighbors(
            row,
            col,
            rows,
            cols
        )

        for neighbor in neighbors:

            nr, nc = neighbor

            risk = risk_grid[nr][nc]

            movement_cost = RISK_COST.get(
                risk,
                float("inf")
            )

            # Cannot travel through SEVERE cells
            if movement_cost == float("inf"):
                continue

            new_cost = (
                current_cost
                + movement_cost
            )

            if new_cost < distances.get(
                neighbor,
                float("inf")
            ):

                distances[neighbor] = new_cost

                previous[neighbor] = current

                heapq.heappush(
                    queue,
                    (new_cost, neighbor)
                )

    # No route found
    if destination not in distances:
        return [], float("inf")

    # --------------------------------------------------------
    # Reconstruct route
    # --------------------------------------------------------

    route = []

    current = destination

    while current != start:

        route.append(current)

        current = previous[current]

    route.append(start)

    route.reverse()

    return route, distances[destination]


# ============================================================
# ROUTE SUMMARY
# ============================================================

def calculate_route_summary(
    route,
    risk_grid
):
    """
    Calculate useful information about a route.

    Returns:
        dictionary containing:
            route length
            low cells
            medium cells
            high cells
            severe cells
    """

    summary = {
        "route_length": len(route),
        "low_cells": 0,
        "medium_cells": 0,
        "high_cells": 0,
        "severe_cells": 0
    }

    for row, col in route:

        risk = risk_grid[row][col]

        if risk == "LOW":
            summary["low_cells"] += 1

        elif risk == "MEDIUM":
            summary["medium_cells"] += 1

        elif risk == "HIGH":
            summary["high_cells"] += 1

        elif risk == "SEVERE":
            summary["severe_cells"] += 1

    return summary


# ============================================================
# PRINT ROUTE
# ============================================================

def print_route(route, total_cost):
    """
    Print the calculated route.
    """

    print("\nSafe Route:")

    if not route:

        print("No safe route available.")

        return

    route_text = " → ".join(
        f"({row},{col})"
        for row, col in route
    )

    print(route_text)

    print(
        f"Route Cost: {total_cost}"
    )

