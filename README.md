# Maize RGB–SWIR code and result data

Article: Observation count shapes RGB–SWIR comparisons in waxy-maize seed groups.

## Contents

- data/figure_source: article figure values, intervals, diagnostic tables and variety mapping.
- data/tables: main and supplementary table text and available CSV sources.
- data/supporting_results: cited frozen summaries, grouped by scientific topic, including fold-matched composition and direct contrasts.
- replay: saved M/D/S predictions, seed/tray/fold identities, nested schedules, bootstrap draws, decisions, summaries and the standalone verification program.
- methods: unmodified geometry, physical-crop, donor-assignment and group-sharing definitions extracted from the research implementation. See methods/README.md.
- FILE_CATALOG.csv and DATA_DICTIONARY.md: file checksums, schemas, units and identity conventions.
- REPLAY_VERIFICATION.json: the actual saved-output verification result.

## Verify the primary analyses

With uv installed, run from this folder:

    uv run --project replay python replay/replay_portable.py --package replay/probabilities

Only NumPy and Pandas are required for this command. It uses the included fixed outputs, schedules and bootstrap draws; it performs no fitting, model inference or new sampling. Add --output verification.json to save a new record; use a new filename if one exists. Initial installation may download dependencies. Dependency installation and replay were verified in an isolated Windows environment.

The method functions have a separate optional environment and are not needed by the replay. Raw image processing and model fitting are outside the standalone replay's scope. COVERAGE_AND_RELEASE.md identifies exactly what can be reproduced from this folder.

## Distribution

Repository: https://github.com/CommitHu502Craft/maize-rgb-swir

This repository provides the article's code and result data. Article submission files, private author records, review correspondence, historical manuscripts, raw imagery and model weights are excluded. Original batch IDs in data files remain stable; reader-facing cohort names are explained in DATA_DICTIONARY.md.

Licenses have not yet been assigned by the authors.

FILE_CATALOG.csv identifies the exact contents of each revision; cite a specific commit when referring to this repository.
