import rasterio
import numpy as np

from config import STUDY_AREA, GRID_ROWS, GRID_COLS, DEM_FILE


def load_dem():
    """
    Read the real DEM, crop it to the study area,
    and aggregate it into the model grid.
    """

    with rasterio.open(DEM_FILE) as src:

        print("\n======================================")
        print("       REAL DEM PROCESSING")
        print("======================================")

        print(f"DEM file: {DEM_FILE}")
        print(f"CRS: {src.crs}")
        print(f"Original size: {src.width} × {src.height}")
        print(f"Resolution: {src.res}")
        print(f"NoData value: {src.nodata}")

        # Study area
        lat_min = STUDY_AREA["lat_min"]
        lat_max = STUDY_AREA["lat_max"]
        lon_min = STUDY_AREA["lon_min"]
        lon_max = STUDY_AREA["lon_max"]

        # Convert geographic coordinates to pixel coordinates
        row_min, col_min = src.index(lon_min, lat_max)
        row_max, col_max = src.index(lon_max, lat_min)

        # Make sure indices are valid
        row_min = max(0, row_min)
        col_min = max(0, col_min)

        row_max = min(src.height, row_max)
        col_max = min(src.width, col_max)

        # Read only the required area
        window = rasterio.windows.Window(
            col_min,
            row_min,
            col_max - col_min,
            row_max - row_min
        )

        dem = src.read(1, window=window).astype(float)

        # Replace NoData values
        if src.nodata is not None:
            dem[dem == src.nodata] = np.nan

        print(f"Cropped DEM size: {dem.shape[1]} × {dem.shape[0]}")

        # Remove invalid values if present
        valid_values = dem[~np.isnan(dem)]

        if len(valid_values) == 0:
            raise ValueError("No valid elevation data found in study area.")

        print(f"Minimum elevation: {np.min(valid_values):.2f} m")
        print(f"Maximum elevation: {np.max(valid_values):.2f} m")
        print(f"Mean elevation: {np.mean(valid_values):.2f} m")

        # Aggregate into model grid
        model_grid = aggregate_dem(
            dem,
            GRID_ROWS,
            GRID_COLS
        )

        print(f"\nModel grid: {GRID_ROWS} × {GRID_COLS}")
        print("\nReal elevation grid:")
        print(np.round(model_grid, 2))

        return model_grid


def aggregate_dem(dem, rows, cols):
    """
    Convert the cropped high-resolution DEM
    into a smaller rows × cols model grid.

    Each model cell contains the mean elevation
    of the DEM pixels falling inside it.
    """

    height, width = dem.shape

    result = np.zeros((rows, cols), dtype=float)

    for r in range(rows):
        for c in range(cols):

            row_start = int(r * height / rows)
            row_end = int((r + 1) * height / rows)

            col_start = int(c * width / cols)
            col_end = int((c + 1) * width / cols)

            cell = dem[row_start:row_end, col_start:col_end]

            valid = cell[~np.isnan(cell)]

            if len(valid) > 0:
                result[r, c] = np.mean(valid)
            else:
                result[r, c] = np.nan

    return result


if __name__ == "__main__":
    load_dem()