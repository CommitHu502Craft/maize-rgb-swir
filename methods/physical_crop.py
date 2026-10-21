"""Method functions extracted verbatim; see README.md for inputs and scope."""

from __future__ import annotations

from typing import Any
import cv2
import numpy as np

IMAGENET_MEAN_RGB = np.asarray([0.485, 0.456, 0.406], dtype=np.float32)

IMAGENET_STD_RGB = np.asarray([0.229, 0.224, 0.225], dtype=np.float32)

MEAN_FILL_RGB = np.rint(IMAGENET_MEAN_RGB * 255).astype(np.uint8)

IMAGE_SIZE = 224

PHYSICAL_FOV = 1.7

def physical_seed_crop(
    image_bgr: np.ndarray,
    labels: np.ndarray,
    label: int,
    analysis_to_board: np.ndarray,
    *,
    physical_fov: float = PHYSICAL_FOV,
    size: int = IMAGE_SIZE,
) -> tuple[np.ndarray, dict[str, Any]]:
    """Warp one seed into a square fixed-FOV checkerboard-plane crop."""
    if image_bgr.shape[:2] != labels.shape or size <= 1 or physical_fov <= 0:
        raise ValueError("invalid image/label/FOV geometry")
    mask = np.asarray(labels == int(label), dtype=np.uint8)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not contours:
        raise ValueError(f"seed label is absent: {label}")
    contour = max(contours, key=cv2.contourArea).astype(np.float32)
    board_contour = cv2.perspectiveTransform(contour, np.asarray(analysis_to_board, dtype=np.float64))
    moments = cv2.moments(board_contour)
    if abs(float(moments["m00"])) <= 1e-12:
        center = board_contour.reshape(-1, 2).mean(axis=0)
    else:
        center = np.asarray(
            [moments["m10"] / moments["m00"], moments["m01"] / moments["m00"]],
            dtype=np.float64,
        )
    pixels_per_unit = (size - 1) / float(physical_fov)
    board_to_crop = np.asarray(
        [
            [pixels_per_unit, 0.0, (size - 1) / 2.0 - pixels_per_unit * center[0]],
            [0.0, pixels_per_unit, (size - 1) / 2.0 - pixels_per_unit * center[1]],
            [0.0, 0.0, 1.0],
        ],
        dtype=np.float64,
    )
    analysis_to_crop = board_to_crop @ np.asarray(analysis_to_board, dtype=np.float64)
    rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    crop = cv2.warpPerspective(
        rgb,
        analysis_to_crop,
        (size, size),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=tuple(int(value) for value in MEAN_FILL_RGB),
    )
    crop_mask = cv2.warpPerspective(
        mask,
        analysis_to_crop,
        (size, size),
        flags=cv2.INTER_NEAREST,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    ).astype(bool)
    crop[~crop_mask] = MEAN_FILL_RGB
    touches_border = bool(
        crop_mask[0].any() or crop_mask[-1].any() or crop_mask[:, 0].any() or crop_mask[:, -1].any()
    )
    return crop.astype(np.uint8), {
        "center_board_x": float(center[0]),
        "center_board_y": float(center[1]),
        "mask_pixels": int(crop_mask.sum()),
        "touches_border": touches_border,
    }
