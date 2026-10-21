"""Method functions extracted verbatim; see README.md for inputs and scope."""

from __future__ import annotations

import hashlib
import warnings
from typing import Iterable
import numpy as np
import pandas as pd
from sklearn.metrics import balanced_accuracy_score, f1_score

FROZEN_LABEL_SPACE = (
    "密甜糯1号",
    "昕禾323",
    "昕禾一号",
    "浙糯玉19",
    "浙糯玉22",
    "浙糯玉24",
    "澳早60",
    "澳甜糯65",
    "珍珍糯600",
    "白甜糯6号",
    "诚糯10号",
    "金辉306",
)

CLASSES = tuple(FROZEN_LABEL_SPACE)

CLASS_INDEX = {label: index for index, label in enumerate(CLASSES)}

def _balanced_accuracy(y: Iterable[int], prediction: Iterable[int]) -> float:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="y_pred contains classes not in y_true", category=UserWarning)
        return float(balanced_accuracy_score(y, prediction))

def _labels(values: Iterable[object]) -> np.ndarray:
    return np.asarray([CLASS_INDEX[str(value)] for value in values], dtype=np.int64)

def _metric_block(y: np.ndarray, probability: np.ndarray) -> tuple[float, float, float]:
    prediction = probability.argmax(axis=1)
    arange = np.arange(len(y))
    return (
        _balanced_accuracy(y, prediction),
        float(f1_score(y, prediction, labels=np.arange(len(CLASSES)), average="macro", zero_division=0)),
        float(probability[arange, y].mean()),
    )

def _gain_retention(sparse: float, d_only: float, full_sd: float) -> float:
    denominator = full_sd - d_only
    return (sparse - d_only) / denominator if abs(denominator) > 1e-12 else np.nan

def evaluate_selection(
    rows: pd.DataFrame,
    d: np.ndarray,
    s: np.ndarray,
    label_column: str,
    selections: dict[str, np.ndarray],
    *,
    scope: str,
    strategy: str,
    k: int,
    repeat: int,
) -> dict:
    remaining_positions = []
    sparse_parts = []
    d_parts = []
    full_parts = []
    y_parts = []
    tray_sparse = []
    tray_d = []
    tray_full = []
    tray_y = []
    tray_sizes = []
    selected_seed_ids = []
    seed_id_column = "seed_id" if "seed_id" in rows else "entity_seed_id"
    for record_id, block in rows.groupby("record_id", sort=False):
        indices = block.index.to_numpy(dtype=np.int64)
        if len(indices) <= k:
            continue
        local_selected = np.asarray(selections[str(record_id)], dtype=np.int64)
        if len(local_selected) != k or len(np.unique(local_selected)) != k:
            raise ValueError("invalid selected set")
        selected = indices[local_selected]
        keep = np.ones(len(indices), dtype=bool)
        keep[local_selected] = False
        remaining = indices[keep]
        if np.intersect1d(selected, remaining).size:
            raise AssertionError("selected HSI seeds leaked into evaluation")
        q_group = s[selected].mean(axis=0)
        sparse = (d[remaining] + q_group[None, :]) / 2.0
        full = (d[remaining] + s[remaining]) / 2.0
        label_values = rows.loc[remaining, label_column].astype(str).unique()
        if len(label_values) != 1:
            raise ValueError("tray contains multiple labels")
        true_index = CLASS_INDEX[label_values[0]]
        y = np.full(len(remaining), true_index, dtype=np.int64)
        remaining_positions.append(remaining)
        sparse_parts.append(sparse)
        d_parts.append(d[remaining])
        full_parts.append(full)
        y_parts.append(y)
        tray_sparse.append(sparse.mean(axis=0))
        tray_d.append(d[remaining].mean(axis=0))
        tray_full.append(full.mean(axis=0))
        tray_y.append(true_index)
        tray_sizes.append(len(indices))
        selected_seed_ids.extend(rows.loc[selected, seed_id_column].astype(str).tolist())
    if not sparse_parts:
        raise ValueError("no eligible trays")
    sparse_probability = np.concatenate(sparse_parts)
    d_probability = np.concatenate(d_parts)
    full_probability = np.concatenate(full_parts)
    y_seed = np.concatenate(y_parts)
    tray_sparse_probability = np.stack(tray_sparse)
    tray_d_probability = np.stack(tray_d)
    tray_full_probability = np.stack(tray_full)
    y_tray = np.asarray(tray_y, dtype=np.int64)
    seed_sparse = _metric_block(y_seed, sparse_probability)
    seed_d = _metric_block(y_seed, d_probability)
    seed_full = _metric_block(y_seed, full_probability)
    tray_sparse_metric = _metric_block(y_tray, tray_sparse_probability)
    tray_d_metric = _metric_block(y_tray, tray_d_probability)
    tray_full_metric = _metric_block(y_tray, tray_full_probability)
    d_prediction = d_probability.argmax(axis=1)
    sparse_prediction = sparse_probability.argmax(axis=1)
    return {
        "scope": scope, "strategy": strategy, "k": k, "repeat": repeat,
        "eligible_trays": len(tray_sizes), "eligible_total_seeds": int(sum(tray_sizes)),
        "selected_hsi_seeds": int(k * len(tray_sizes)), "unmeasured_test_seeds": len(y_seed),
        "coverage_fraction_weighted": float(k * len(tray_sizes) / sum(tray_sizes)),
        "coverage_fraction_tray_mean": float(np.mean([k / size for size in tray_sizes])),
        "coverage_fraction_tray_min": float(np.min([k / size for size in tray_sizes])),
        "coverage_fraction_tray_max": float(np.max([k / size for size in tray_sizes])),
        "seed_ba_sparse": seed_sparse[0], "seed_macro_f1_sparse": seed_sparse[1],
        "seed_true_probability_sparse": seed_sparse[2],
        "seed_ba_d_matched": seed_d[0], "seed_ba_full_sd_matched": seed_full[0],
        "seed_gain_retention": _gain_retention(seed_sparse[0], seed_d[0], seed_full[0]),
        "seed_rescue_rate": float(np.mean((d_prediction != y_seed) & (sparse_prediction == y_seed))),
        "seed_harm_rate": float(np.mean((d_prediction == y_seed) & (sparse_prediction != y_seed))),
        "tray_ba_sparse": tray_sparse_metric[0], "tray_macro_f1_sparse": tray_sparse_metric[1],
        "tray_true_probability_sparse": tray_sparse_metric[2],
        "tray_ba_d_matched": tray_d_metric[0], "tray_ba_full_sd_matched": tray_full_metric[0],
        "tray_gain_retention": _gain_retention(tray_sparse_metric[0], tray_d_metric[0], tray_full_metric[0]),
        "selected_ids_sha256": hashlib.sha256("\n".join(selected_seed_ids).encode("utf-8")).hexdigest(),
    }
