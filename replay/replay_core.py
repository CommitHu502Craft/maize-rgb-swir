"""Sign-agnostic replay from archived decisions; NumPy/Pandas only.

No model, original project loader, local absolute path, training or new resampling.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
import numpy as np
import pandas as pd

KS = ["1", "3", "5", "10", "20", "all"]
ALPHAS = [0., .1, .2, 1 / 3, .5]
F_NAMES = ["F0", "F0.1", "F0.2", "F1_3", "F0.5"]
RECIPES = ["M", "D", "S", "MS", "SD", "MD", "MSD", *F_NAMES]
TOL = 1e-12


def require(condition, message):
    if not condition:
        raise ValueError(message)


def close(actual, expected, name, checks):
    a, b = np.asarray(actual), np.asarray(expected)
    require(a.shape == b.shape, f"{name}: shape mismatch {a.shape} / {b.shape}")
    require(np.isfinite(a).all() and np.isfinite(b).all(), f"{name}: nonfinite number")
    error = float(np.max(np.abs(a - b))) if a.size else 0.
    require(error <= TOL, f"{name}: numerical mismatch {error}")
    checks.append({"check": name, "values": int(a.size), "max_abs_error": error})


def probability_check(values, rows, classes):
    require(values.shape == (3, rows, classes), "Probability shape/order mismatch")
    require(np.isfinite(values).all(), "Nonfinite probability")
    require(values.min() >= 0 and values.max() <= 1 + 1e-8, "Probability outside [0,1]")
    require(np.max(np.abs(values.sum(axis=-1) - 1)) <= 1e-5, "Probability row sum differs from one")


def class_mean(values, truth):
    """Explicit mean of within-class tray recalls, independent of signs."""
    return np.stack([values[..., truth == c].mean(axis=-1) for c in np.unique(truth)], axis=-1).mean(axis=-1)


def table(root, filename, keys, expected_count=None):
    value = pd.read_csv(root / "data" / filename, dtype={"k": str, "start": str, "end": str, "record_id": str})
    require(set(keys).issubset(value.columns), f"{filename}: missing columns")
    require(not value[keys].isna().any().any(), f"{filename}: missing key")
    require(not value.duplicated(keys).any(), f"{filename}: duplicate key")
    if expected_count is not None:
        require(len(value) == expected_count, f"{filename}: incomplete grid")
    return value


def validate_decisions(prediction, truth, weights):
    require(prediction.ndim == 4 and prediction.shape[:3] == (12, 6, 500), "Decision schema mismatch")
    require(np.issubdtype(prediction.dtype, np.integer), "Noninteger class decision")
    require(prediction.min() >= 0 and prediction.max() < 12, "Class decision outside fixed class space")
    require(prediction.shape[-1] == len(truth) == len(weights), "Tray dimension mismatch")
    require(np.array_equal(prediction[7], prediction[5]), "F0 != MD")
    require(np.array_equal(prediction[10], prediction[6]), "F1/3 != MSD")
    require(np.all(prediction[:, -1] == prediction[:, -1, :1]), "All decisions vary with schedule")


def load_archived(root, cohort, checks):
    run = json.loads((root / "audit/run.json").read_text(encoding="utf-8"))
    require(run["ks"] == KS and run["alphas"] == ALPHAS, "Protocol grid/order changed")
    classes = run["classes"]
    require(len(classes) == len(set(classes)) == 12, "Class order invalid")
    rows = table(root, f"{cohort}_rows.csv", ["row_index"])
    meta = table(root, f"{cohort}_trays.csv", ["tray_index", "record_id"])
    label, identity = ("variety_name", "seed_id") if cohort == "batch2" else ("variety", "entity_seed_id")
    require(not rows[identity].isna().any() and not rows[identity].duplicated().any(), "Missing/duplicate seed identity")
    require(not meta.record_id.duplicated().any(), "Duplicate tray identity")
    require(np.array_equal(rows.row_index, np.arange(len(rows))), "Row order mismatch")
    require(np.array_equal(meta.tray_index, np.arange(len(meta))), "Tray order mismatch")
    require(set(rows[label]).issubset(classes) and set(meta.variety).issubset(classes), "Unknown truth class")
    require(list(rows.record_id.drop_duplicates()) == list(meta.record_id), "Tray encounter order mismatch")
    require(len(rows) == run["cohorts"][cohort]["seeds"] and len(meta) == run["cohorts"][cohort]["trays"], "Cohort dimensions changed")
    if cohort == "batch2":
        require(set(rows.outer_fold).issubset({0, 1, 2, 3}), "Invalid outer fold")
    else:
        require(rows.condition.eq("BASE").all() and meta.fold.eq(-1).all(), "Batch-3 BASE/fold mismatch")
    truth = np.asarray([classes.index(v) for v in meta.variety])
    weights = np.asarray([1 / (len(np.unique(truth)) * np.sum(truth == t)) for t in truth])
    with np.load(root / "data" / f"{cohort}_decisions.npz", allow_pickle=False) as archive:
        require(set(archive.files) == {"predictions", "truth", "tray_weights", "recipes", "ks"}, "Decision archive keys invalid")
        require(list(archive["recipes"]) == RECIPES and list(archive["ks"]) == KS, "Recipe/k order mismatch")
        prediction = archive["predictions"]
        close(truth, archive["truth"], f"{cohort}_truth_order", checks)
        close(weights, archive["tray_weights"], f"{cohort}_balanced_tray_weights", checks)
    validate_decisions(prediction, truth, weights)
    with np.load(root / "data" / f"{cohort}_schedules.npz", allow_pickle=False) as archive:
        require(set(archive.files) == {"permutations", "tray_sizes", "seed"}, "Schedule archive keys invalid")
        require(int(archive["seed"]) == run["sampling_seed"], "Schedule seed mismatch")
        close(meta.seeds, archive["tray_sizes"], f"{cohort}_tray_sizes", checks)
        schedules = archive["permutations"]
    require(schedules.shape == (500, len(meta), int(meta.seeds.max())), "Schedule dimensions invalid")
    require(np.issubdtype(schedules.dtype, np.integer), "Schedule indices not integers")
    for ti, tray in meta.iterrows():
        idx = np.flatnonzero(rows.record_id.eq(tray.record_id))
        require(len(idx) == tray.seeds and tray.seeds >= 20, "Tray membership/size mismatch")
        require(rows.loc[idx, label].eq(tray.variety).all(), "Mixed truth in tray")
        if cohort == "batch2":
            require(rows.loc[idx, "outer_fold"].eq(tray.fold).all(), "Tray fold mismatch")
        require(np.all(np.sort(schedules[:, ti, :len(idx)], axis=-1) == idx), "Schedule omits/duplicates seeds")
        require(np.all(schedules[:, ti, len(idx):] == -1), "Invalid schedule padding")
    hashes = table(root, f"{cohort}_schedule_hashes.csv", ["k", "repeat"], 3000)
    for row in hashes.itertuples():
        require(row.k in KS and 0 <= row.repeat < 500, "Invalid schedule-hash key")
        selected = [schedules[row.repeat, ti, :int(n) if row.k == "all" else int(row.k)] for ti, n in enumerate(meta.seeds)]
        joined = "\n".join(",".join(str(int(x)) for x in part) for part in selected)
        require(hashlib.sha256(joined.encode()).hexdigest() == row.indices_sha256, "Schedule prefix hash mismatch")
    correct = prediction == truth[None, None, None, :]
    ba = class_mean(correct, truth)
    close(ba, correct @ weights, f"{cohort}_BA_equals_explicit_class_recall", checks)
    return {"prediction": prediction, "correct": correct, "ba": ba, "truth": truth, "weights": weights,
            "meta": meta, "rows": rows, "schedules": schedules, "classes": classes}


def bootstrap(root, cohort, checks):
    with np.load(root / "data/batch2_bootstrap.npz", allow_pickle=False) as archive:
        require(set(archive.files) == {"draws", "weights", "seed"}, "Bootstrap schema mismatch")
        require(int(archive["seed"]) == 20260914, "Bootstrap seed mismatch")
        draws, weights = archive["draws"], archive["weights"]
    truth = cohort["truth"]
    require(draws.shape == weights.shape == (2000, len(truth)), "Bootstrap dimensions invalid")
    require(np.issubdtype(draws.dtype, np.integer) and draws.min() >= 0 and draws.max() < len(truth), "Invalid bootstrap tray index")
    expected_weights = np.zeros_like(weights)
    for c in np.unique(truth):
        require(np.all(np.sum(truth[draws] == c, axis=1) == np.sum(truth == c)), "Bootstrap class count changed")
    for repeat, indices in enumerate(draws):
        np.add.at(expected_weights[repeat], indices, cohort["weights"][indices])
    close(expected_weights, weights, "paired_bootstrap_weights_from_draws", checks)
    averaged = cohort["correct"].mean(axis=2)
    values = {}
    for a, name in zip(ALPHAS, F_NAMES):
        for comp in ("MD", "M"):
            delta = averaged[RECIPES.index(name)] - averaged[RECIPES.index(comp)]
            direct = np.mean([delta[:, draws[truth[draws] == c].reshape(2000, -1)].mean(axis=-1).T for c in np.unique(truth)], axis=0)
            close(direct, weights @ delta.T, f"paired_bootstrap_arithmetic_{a}_{comp}", checks)
            values[(a, comp)] = direct
    return values


def replay(root):
    checks, output_contrasts, output_states, output_endpoints = [], [], [], []
    cohorts = {name: load_archived(root, name, checks) for name in ("batch2", "batch3")}
    boot = bootstrap(root, cohorts["batch2"], checks)
    saved_contrasts = table(root, "weight_contrasts.csv", ["cohort", "alpha", "comparator", "k"], 120)
    saved_states = table(root, "error_states.csv", ["cohort", "alpha", "comparator", "k"], 120)
    repeats = table(root, "sampling_repeats.csv", ["cohort", "recipe", "k", "repeat"], 72000)
    summary = table(root, "curve_summary.csv", ["cohort", "recipe", "k"], 144)
    endpoints = table(root, "endpoint_changes.csv", ["cohort", "alpha", "comparator", "start", "end"], 60)
    all_seed = table(root, "all_seed_decisions.csv", ["cohort", "recipe", "record_id"], 924)
    for name, c in cohorts.items():
        for a, recipe in zip(ALPHAS, F_NAMES):
            for comp in ("MD", "M"):
                fi, ci = RECIPES.index(recipe), RECIPES.index(comp)
                deltas = c["ba"][fi] - c["ba"][ci]
                for ki, k in enumerate(KS):
                    aok, bok = c["correct"][ci, ki], c["correct"][fi, ki]
                    rates = [float(class_mean(mask, c["truth"]).mean()) for mask in (aok & bok, ~aok & bok, aok & ~bok, ~aok & ~bok)]
                    diff = float(deltas[ki].mean())
                    close([sum(rates), rates[1] - rates[2]], [1., diff], f"{name}_{recipe}_{comp}_{k}_state_identity", checks)
                    interval = list(np.quantile(boot[(a, comp)][:, ki], [.025, .975])) if name == "batch2" else [None, None]
                    output_contrasts.append(dict(cohort=name, alpha=a, recipe=recipe, comparator=comp, k=k, difference=diff,
                                                 sampling_sd=float(deltas[ki].std(ddof=1)), comparator_ba=float(c["ba"][ci, ki].mean()),
                                                 f_ba=float(c["ba"][fi, ki].mean()), ci025=interval[0], ci975=interval[1]))
                    output_states.append(dict(cohort=name, alpha=a, comparator=comp, k=k, both_correct=rates[0], rescue=rates[1],
                                              harm=rates[2], both_wrong=rates[3], net=diff))
                for start, end in (("1", "20"), ("3", "20"), ("1", "all")):
                    si, ei = KS.index(start), KS.index(end)
                    interval = list(np.quantile(boot[(a, comp)][:, ei] - boot[(a, comp)][:, si], [.025, .975])) if name == "batch2" else [None, None]
                    output_endpoints.append(dict(cohort=name, alpha=a, comparator=comp, start=start, end=end,
                                                endpoint_change=float((deltas[ei] - deltas[si]).mean()), ci025=interval[0], ci975=interval[1]))
        sub = repeats[repeats.cohort.eq(name)]
        close([c["ba"][RECIPES.index(r.recipe), KS.index(r.k), int(r.repeat)] for r in sub.itertuples()], sub.ba, f"{name}_all_repeat_BAs", checks)
        sub = summary[summary.cohort.eq(name)]
        calculated = []
        for row in sub.itertuples():
            v = c["ba"][RECIPES.index(row.recipe), KS.index(row.k)]
            calculated.append([v.mean(), v.std(ddof=1), *np.quantile(v, [.025, .975])])
        close(calculated, sub[["ba", "sampling_sd", "sampling_q025", "sampling_q975"]], f"{name}_curve_statistics", checks)
        for r in all_seed[all_seed.cohort.eq(name)].itertuples():
            ti = list(c["meta"].record_id).index(r.record_id)
            pred = int(c["prediction"][RECIPES.index(r.recipe), -1, 0, ti])
            require(c["classes"][pred] == r.prediction and int(pred == c["truth"][ti]) == r.correct,
                    f"{name}: all-seed identity/decision mismatch")
            require(r.variety == c["meta"].iloc[ti].variety and r.seeds == c["meta"].iloc[ti].seeds, "All-seed metadata mismatch")
    def compare_frame(actual, saved, keys, cols, title):
        actual = pd.DataFrame(actual).set_index(keys).sort_index()
        expected = saved.set_index(keys).sort_index()
        require(actual.index.equals(expected.index), f"{title}: key coverage mismatch")
        for col in cols:
            require(actual[col].isna().equals(expected[col].isna()), f"{title}/{col}: missing-value pattern changed")
            valid = actual[col].notna()
            close(actual.loc[valid, col], expected.loc[valid, col], f"{title}/{col}", checks)
    compare_frame(output_contrasts, saved_contrasts, ["cohort", "alpha", "comparator", "k"],
                  ["difference", "sampling_sd", "comparator_ba", "f_ba", "ci025", "ci975"], "weight_contrasts")
    compare_frame(output_states, saved_states, ["cohort", "alpha", "comparator", "k"],
                  ["both_correct", "rescue", "harm", "both_wrong", "net"], "error_states")
    compare_frame(output_endpoints, endpoints, ["cohort", "alpha", "comparator", "start", "end"],
                  ["endpoint_change", "ci025", "ci975"], "endpoint_changes")
    saved_boot = table(root, "paired_bootstrap_values.csv", ["cohort", "alpha", "comparator", "k", "repeat"], 180000)
    actual = []
    for r in saved_boot.itertuples():
        require(r.cohort == "batch2" and 0 <= r.repeat < 2000, "Invalid bootstrap key")
        alpha = ALPHAS[int(np.argmin(np.abs(np.asarray(ALPHAS) - r.alpha)))]
        values = boot[(alpha, r.comparator)]
        if r.k.startswith("change_"):
            _, start, end = r.k.split("_")
            actual.append(values[r.repeat, KS.index(end)] - values[r.repeat, KS.index(start)])
        else:
            actual.append(values[r.repeat, KS.index(r.k)])
    close(actual, saved_boot.difference, "all_saved_paired_bootstrap_values", checks)
    return {"pass": True, "mode": "tracked-decision-replay", "checks": checks,
            "max_numeric_error": max(v["max_abs_error"] for v in checks),
            "decisions_checked": sum(c["prediction"].size for c in cohorts.values()),
            "bootstrap_values_checked": len(saved_boot), "cohorts": cohorts,
            "weight_contrasts": output_contrasts, "error_states": output_states, "endpoint_changes": output_endpoints}


def public_result(result):
    return {k: v for k, v in result.items() if k != "cohorts"}
