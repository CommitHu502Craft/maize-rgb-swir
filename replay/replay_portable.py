"""Portable archived-decision replay, with optional locally generated probabilities."""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from pathlib import Path
sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
from replay_core import RECIPES, KS, ALPHAS, probability_check, close, replay, public_result, require


def verify_package(package, cohorts, checks):
    manifest = json.loads((package / "manifest.json").read_text(encoding="utf-8"))
    require(manifest["schema"] == "seed-probability-replay-1" and manifest["alphas"] == ALPHAS and manifest["ks"] == KS,
            "Portable package protocol/schema mismatch")
    require(manifest["branches"] == ["M", "D", "S"], "Portable branch order mismatch")
    require(set(manifest["files"]) == {"batch2.npz", "batch3.npz"}, "Unexpected package file/path")
    for cohort, c in cohorts.items():
        path = package / f"{cohort}.npz"
        require(hashlib.sha256(path.read_bytes()).hexdigest() == manifest["files"][path.name]["sha256"], "Portable input hash mismatch")
        with np.load(path, allow_pickle=False) as archive:
            require(set(archive.files) == {"row_id", "tray_index", "truth", "outer_fold", "class_order", "probabilities"}, "Portable input columns mismatch")
            p = archive["probabilities"]
            probability_check(p, len(c["rows"]), 12)
            require(list(archive["class_order"]) == [f"C{i:02d}" for i in range(12)], "Anonymous class order mismatch")
            close(archive["row_id"], np.arange(len(c["rows"])), f"{cohort}_package_row_order", checks)
            tray_indices = np.array([list(c["meta"].record_id).index(v) for v in c["rows"].record_id])
            close(archive["tray_index"], tray_indices, f"{cohort}_package_tray_order", checks)
            close(archive["truth"], c["truth"][tray_indices], f"{cohort}_package_truth", checks)
            close(archive["outer_fold"], c["meta"].fold.to_numpy()[tray_indices], f"{cohort}_package_fold", checks)
        m, d, s = p
        md = (m + d) / 2
        raw = np.stack([m, d, s, (m + s) / 2, (d + s) / 2, md, (m + d + s) / 3,
                        *((1 - a) * md + a * s for a in ALPHAS)])
        calculated = np.empty_like(c["prediction"])
        gap = float("inf")
        for ti, tray in c["meta"].iterrows():
            idx = np.flatnonzero(tray_indices == ti)
            ordered = c["schedules"][:, ti, :tray.seeds]
            for ki, k in enumerate(KS):
                mean = raw[:, idx].mean(axis=1)[:, None] if k == "all" else raw[:, ordered[:, :int(k)]].mean(axis=2)
                calculated[:, ki, :, ti] = mean.argmax(axis=-1)
                top = np.sort(mean, axis=-1)[..., -2:]
                gap = min(gap, float(np.min(top[..., 1] - top[..., 0])))
        close(calculated, c["prediction"], f"{cohort}_package_all_seed_probability_decisions", checks)
        require(np.array_equal(calculated, c["prediction"]), "Portable decision equality failed")
        checks.append({"check": f"{cohort}_minimum_top_gap", "values": 1, "max_abs_error": 0., "gap": gap})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--package", type=Path, help="Optional approved/generated compact probabilities; never inferred from local upstream files")
    parser.add_argument("--output", type=Path, help="New JSON audit path; historical output paths are rejected")
    args = parser.parse_args()
    if args.output and any(args.output.resolve().is_relative_to((args.root / p).resolve()) for p in ("audit", "data", "figures")):
        parser.error("Historical audit/data/figures are read-only")
    result = replay(args.root)
    if args.package:
        verify_package(args.package, result["cohorts"], result["checks"])
        result["mode"] = "compact-seed-probability-replay"
        result["package_manifest_sha256"] = hashlib.sha256((args.package / "manifest.json").read_bytes()).hexdigest()
    result["max_numeric_error"] = max(c["max_abs_error"] for c in result["checks"])
    result = public_result(result)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        require(not args.output.exists(), "Replay audit exists; select a new output path")
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(f"PASS: {result['mode']}; {result['decisions_checked']:,} archived decisions; "
          f"{result['bootstrap_values_checked']:,} paired values; max error {result['max_numeric_error']:.3g}")


if __name__ == "__main__":
    main()
