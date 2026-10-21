"""Method functions extracted verbatim; see README.md for inputs and scope."""

from __future__ import annotations

import numpy as np
import pandas as pd

def _deranged_groups(rows: pd.DataFrame, group_column: str, rng: np.random.Generator) -> np.ndarray:
    donor = np.empty(len(rows), dtype=np.int64)
    for _, block in rows.groupby(group_column, sort=False):
        indices = block.index.to_numpy(dtype=np.int64)
        if len(indices) < 2:
            raise ValueError(f"cannot derange singleton {group_column}")
        order = rng.permutation(indices)
        shift = int(rng.integers(1, len(order)))
        donor[order] = np.roll(order, shift)
    if np.any(donor == np.arange(len(rows))):
        raise AssertionError("same-group derangement retained a seed")
    return donor

def _map_group_to_other_group(
    rows: pd.DataFrame,
    *,
    outer_column: str,
    inner_column: str,
    rng: np.random.Generator,
) -> np.ndarray:
    donor = np.empty(len(rows), dtype=np.int64)
    for _, outer in rows.groupby(outer_column, sort=False):
        groups = [block.index.to_numpy(dtype=np.int64) for _, block in outer.groupby(inner_column, sort=False)]
        if len(groups) < 2:
            raise ValueError(f"{outer_column} has fewer than two {inner_column} groups")
        order = rng.permutation(len(groups))
        shuffled_groups = [rng.permutation(groups[int(index)]) for index in order]
        recipient = np.concatenate(shuffled_groups)
        shift = max(len(group) for group in shuffled_groups)
        if 2 * shift > len(recipient):
            raise ValueError(f"cannot make an exact cross-{inner_column} permutation")
        donor[recipient] = np.roll(recipient, shift)
    return donor

def _different_variety(rows: pd.DataFrame, rng: np.random.Generator) -> np.ndarray:
    groups = [block.index.to_numpy(dtype=np.int64) for _, block in rows.groupby("variety_name", sort=False)]
    order = rng.permutation(len(groups))
    shuffled_groups = [rng.permutation(groups[int(index)]) for index in order]
    recipient = np.concatenate(shuffled_groups)
    shift = max(len(group) for group in shuffled_groups)
    if 2 * shift > len(recipient):
        raise ValueError("cannot make an exact cross-variety permutation")
    donor = np.empty(len(rows), dtype=np.int64)
    donor[recipient] = np.roll(recipient, shift)
    return donor

def _different_variety_within_fold(rows: pd.DataFrame, rng: np.random.Generator) -> np.ndarray:
    donor = np.empty(len(rows), dtype=np.int64)
    for _, fold in rows.groupby("outer_fold", sort=False):
        groups = [block.index.to_numpy(dtype=np.int64) for _, block in fold.groupby("variety_name", sort=False)]
        if len(groups) < 2:
            raise ValueError("fold has fewer than two varieties")
        shuffled_groups = [rng.permutation(groups[int(index)]) for index in rng.permutation(len(groups))]
        recipient = np.concatenate(shuffled_groups)
        shift = max(len(group) for group in shuffled_groups)
        if 2 * shift > len(recipient):
            raise ValueError("cannot make exact cross-variety permutation within fold")
        donor[recipient] = np.roll(recipient, shift)
    return donor

def _balanced_fold_matched_subset(rows: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    selected = []
    for _, outer in rows.groupby(["variety_name", "outer_fold"], sort=False):
        trays = [block.index.to_numpy(dtype=np.int64) for _, block in outer.groupby("record_id", sort=False)]
        if len(trays) < 2:
            continue
        count = min(len(indices) for indices in trays)
        selected.extend(rng.choice(indices, size=count, replace=False).tolist() for indices in trays)
    flat = np.concatenate([np.asarray(indices, dtype=np.int64) for indices in selected])
    subset = rows.iloc[flat].copy().reset_index().rename(columns={"index": "_source_position"})
    subset["variety_fold"] = subset["variety_name"].astype(str) + "|" + subset["outer_fold"].astype(str)
    return subset
