"""Method functions extracted verbatim; see README.md for inputs and scope."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable
import cv2
import numpy as np

GEOMETRY_COLUMNS = (
    "area_board_sq",
    "perimeter_board",
    "circularity",
    "major_axis_board",
    "minor_axis_board",
    "aspect_ratio",
    "solidity",
    "oriented_extent",
)

@dataclass(frozen=True)
class GeometryResult:
    values: np.ndarray
    calibration_variation: np.ndarray
    valid_calibrations: int

def _validated_homography(matrix: Any, label: str) -> np.ndarray:
    value = np.asarray(matrix, dtype=np.float64)
    if value.shape != (3, 3) or not np.isfinite(value).all():
        raise ValueError(f"{label} must be a finite 3x3 matrix")
    if abs(float(np.linalg.det(value))) <= 1e-12 or abs(float(value[2, 2])) <= 1e-12:
        raise ValueError(f"{label} is singular")
    return value / value[2, 2]

def _largest_contour(mask: np.ndarray) -> np.ndarray:
    binary = np.asarray(mask, dtype=np.uint8)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not contours:
        raise ValueError("instance mask contains no contour")
    return max(contours, key=cv2.contourArea).astype(np.float32)

def _geometry_from_contour(contour: np.ndarray) -> np.ndarray:
    area = abs(float(cv2.contourArea(contour)))
    perimeter = float(cv2.arcLength(contour, True))
    if area <= 0 or perimeter <= 0:
        raise ValueError("transformed contour has non-positive area or perimeter")
    (_, _), (width, height), _ = cv2.minAreaRect(contour)
    major = max(float(width), float(height))
    minor = max(min(float(width), float(height)), 1e-9)
    hull_area = abs(float(cv2.contourArea(cv2.convexHull(contour))))
    circularity = 4.0 * np.pi * area / max(perimeter * perimeter, 1e-12)
    return np.asarray(
        [
            area,
            perimeter,
            circularity,
            major,
            minor,
            major / minor,
            area / max(hull_area, area),
            area / max(major * minor, area),
        ],
        dtype=np.float64,
    )

def normalized_instance_geometry(mask: np.ndarray, matrices: Iterable[np.ndarray]) -> GeometryResult:
    """Measure one instance in checker-square units across calibration replicates."""
    contour = _largest_contour(mask)
    measurements: list[np.ndarray] = []
    for matrix in matrices:
        transformed = cv2.perspectiveTransform(contour, _validated_homography(matrix, "geometry matrix"))
        measurements.append(_geometry_from_contour(transformed))
    values = np.stack(measurements)
    return GeometryResult(
        values=np.median(values, axis=0),
        calibration_variation=np.ptp(values, axis=0),
        valid_calibrations=len(values),
    )

def replace_rgb_geometry(rgb_basic: np.ndarray, board_geometry: np.ndarray) -> np.ndarray:
    """Replace the eight pixel-geometry columns while preserving color statistics."""
    basic = np.asarray(rgb_basic)
    geometry = np.asarray(board_geometry)
    if basic.ndim != 2 or basic.shape[1] != 28:
        raise ValueError(f"rgb_basic must have shape (n, 28), got {basic.shape}")
    if geometry.shape != (len(basic), len(GEOMETRY_COLUMNS)):
        raise ValueError(f"board_geometry must have shape ({len(basic)}, 8), got {geometry.shape}")
    result = np.asarray(basic, dtype=np.float32).copy()
    result[:, : len(GEOMETRY_COLUMNS)] = geometry.astype(np.float32)
    return result
