# Reproducibility coverage

| Evidence | Included and verified |
| --- | --- |
| Observation-count comparisons, RGB comparators and spectral-weight sensitivity | M/D/S outputs, seed/tray/fold mappings, saved nested schedules, decisions, bootstrap draws and results; standalone replay verifies the archived endpoints |
| Donor hierarchy and fold-matched sensitivity | Figure/table data, cited summaries, direct contrasts, 50-repeat composition and exact donor-rule functions; randomization analyses were not rerun |
| SGSEF and RGB group/broadcast controls | Figure/table data, cited summaries and exact selected-group evaluation functions; simulations were not rerun |
| Secondary robustness, residual-error and cross-count evidence | Figure/table source data and cited supporting tables; not all secondary analyses are covered by the portable replay |
| RGB preprocessing | Exact geometry/crop functions; raw images, calibration inputs, complete feature extraction and training pipelines are outside this standalone release |

This is a saved-result reproduction package, not a raw-image-to-trained-model reproduction package. Raw RGB/CR3/SWIR, calibration images, masks and model checkpoints are not included. Their access must be specified separately if the authors release them.

Code and result data are distributed at https://github.com/CommitHu502Craft/maize-rgb-swir. Code and software configuration use MIT; result data, protocol metadata and documentation use CC BY 4.0. See LICENSE.md for scope. This access information applies to the included files; it does not specify access to the excluded raw acquisition data.
