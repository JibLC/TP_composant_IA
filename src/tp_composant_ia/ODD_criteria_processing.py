"""ODD (Operational Design Domain) criteria verification for the Welding Quality Detection component."""

import numpy as np
from numpy.typing import NDArray

# Number of bins for the gradient orientation histogram (resolution: 180/N_BINS degrees)
_ORIENTATION_N_BINS: int = 180


# Thresholds derived from challenge ODD specification
# luminosity_level in the metadata is expressed as a percentage (0-100)
LUMINOSITY_MIN_PCT: float = 10.0
LUMINOSITY_MAX_PCT: float = 90.0


def compute_luminosity(image: np.ndarray) -> float:
    """Compute the luminosity of an image as a percentage of maximum brightness.

    Uses the ITU-R BT.601 luma formula on an RGB or grayscale image.

    Args:
        image: numpy array of shape (H, W, 3) in RGB or (H, W) in grayscale,
               with pixel values in [0, 255].

    Returns:
        Luminosity as a float in [0.0, 100.0].
    """
    if image.ndim == 3:
        luma = 0.299 * image[:, :, 0] + 0.587 * image[:, :, 1] + 0.114 * image[:, :, 2]
    elif image.ndim == 2:
        luma = image.astype(np.float64)
    else:
        raise ValueError(f"Expected 2D or 3D array, got shape {image.shape}")

    return float(np.mean(luma) / 255.0 * 100.0)


def check_luminosity_odd(
    image: np.ndarray,
    min_pct: float = LUMINOSITY_MIN_PCT,
    max_pct: float = LUMINOSITY_MAX_PCT,
) -> dict[str, float | bool | str]:
    """Check whether an image luminosity falls within ODD criteria.

    Args:
        image: numpy array (H, W, 3) RGB or (H, W) grayscale, pixel values in [0, 255].
        min_pct: minimum acceptable luminosity percentage (default: challenge ODD lower bound).
        max_pct: maximum acceptable luminosity percentage (default: challenge ODD upper bound).

    Returns:
        Dictionary with keys:
            - ``luminosity_pct``: computed luminosity in [0, 100]
            - ``within_odd``: True if luminosity is within [min_pct, max_pct]
            - ``luminosity_class``: "normal" | "too_dark" | "too_bright"
    """
    luminosity_pct = compute_luminosity(image)

    if luminosity_pct < min_pct:
        luminosity_class = "too_dark"
    elif luminosity_pct > max_pct:
        luminosity_class = "too_bright"
    else:
        luminosity_class = "normal"

    return {
        "luminosity_pct": luminosity_pct,
        "within_odd": luminosity_class == "normal",
        "luminosity_class": luminosity_class,
    }


def compute_dominant_orientation(image: np.ndarray, n_bins: int = _ORIENTATION_N_BINS) -> float:
    """Compute the dominant orientation angle of patterns in an image.

    Builds a gradient magnitude-weighted histogram of edge orientations (0-180°)
    using Sobel filters, then returns the angle of the dominant peak.
    Unsigned orientation (0-180°) is used because edges have no inherent direction.

    Args:
        image: numpy array (H, W, 3) RGB or (H, W) grayscale, pixel values in [0, 255].
        n_bins: number of histogram bins over [0°, 180°].

    Returns:
        Dominant orientation angle in degrees, in [0.0, 180.0).
    """
    if image.ndim == 3:
        gray: NDArray[np.float64] = (
            0.299 * image[:, :, 0] + 0.587 * image[:, :, 1] + 0.114 * image[:, :, 2]
        )
    else:
        gray = image.astype(np.float64)

    gx = np.gradient(gray, axis=1)
    gy = np.gradient(gray, axis=0)

    magnitude = np.sqrt(gx**2 + gy**2)
    # arctan2 returns [-π, π] → map to unsigned orientation [0, π)
    angles_rad = np.arctan2(gy, gx) % np.pi
    angles_deg = np.degrees(angles_rad)

    histogram, bin_edges = np.histogram(
        angles_deg.ravel(),
        bins=n_bins,
        range=(0.0, 180.0),
        weights=magnitude.ravel(),
    )

    dominant_bin = int(np.argmax(histogram))
    dominant_angle = float((bin_edges[dominant_bin] + bin_edges[dominant_bin + 1]) / 2.0)
    return dominant_angle


def compare_orientations(angle_a: float, angle_b: float) -> float:
    """Compute the angular difference between two dominant orientation angles.

    Handles the circular wraparound of unsigned orientations (0-180°):
    e.g. 5° and 175° differ by 10°, not 170°.

    Args:
        angle_a: orientation angle in degrees, in [0, 180).
        angle_b: orientation angle in degrees, in [0, 180).

    Returns:
        Angular difference in degrees, in [0.0, 90.0].
    """
    diff = abs(angle_a - angle_b) % 180.0
    return float(min(diff, 180.0 - diff))
