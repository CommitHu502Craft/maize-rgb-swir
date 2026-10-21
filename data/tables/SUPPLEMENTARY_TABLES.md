# Supplementary tables

## Table S1. Full recorded primary-cohort provenance

| variety | seeds | trays | acquisition_date | sessions | commercial_source | package_records | recorded_packaging | production_lot_status | outer_fold_trays_0_1_2_3 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V01 | 215 | 4 | 2026-07-21 | S2_after_battery | Online retail channel; seller not recorded | PKG-007 | unspecified | Supplier production-lot identifier unavailable; internal grouping confidence low | 1/1/1/1 |
| V02 | 296 | 6 | 2026-07-21 | S2_after_battery | Online retail channel; seller not recorded | PKG-013 | unspecified | Supplier production-lot identifier unavailable; internal grouping confidence low | 1/1/2/2 |
| V03 | 292 | 5 | 2026-07-21 | S1_before_battery;S2_after_battery | Online retail channel; seller not recorded | PKG-018 | unspecified | Supplier production-lot identifier unavailable; internal grouping confidence low | 2/1/1/1 |
| V04 | 393 | 8 | 2026-07-21 | S1_before_battery | Online retail channel; seller not recorded | PKG-016;PKG-017 | large_200g | Supplier production-lot identifier unavailable; packages author-reported as the same lot | 2/2/2/2 |
| V05 | 384 | 6 | 2026-07-21 | S1_before_battery | Online retail channel; seller not recorded | PKG-014;PKG-015 | large_200g | Supplier production-lot identifier unavailable; packages author-reported as the same lot | 2/1/1/2 |
| V06 | 294 | 6 | 2026-07-21 | S1_before_battery | Online retail channel; seller not recorded | PKG-010;PKG-011 | large_200g | Supplier production-lot identifier unavailable; packages author-reported as the same lot | 1/1/2/2 |
| V07 | 258 | 5 | 2026-07-21 | S2_after_battery | Online retail channel; seller not recorded | PKG-009 | unspecified | Supplier production-lot identifier unavailable; internal grouping confidence low | 2/1/1/1 |
| V08 | 302 | 5 | 2026-07-21 | S2_after_battery | Online retail channel; seller not recorded | PKG-005 | unspecified | Supplier production-lot identifier unavailable; internal grouping confidence low | 1/1/2/1 |
| V09 | 276 | 5 | 2026-07-21 | S2_after_battery | Online retail channel; seller not recorded | PKG-004 | unspecified | Supplier production-lot identifier unavailable; internal grouping confidence low | 1/2/1/1 |
| V10 | 254 | 5 | 2026-07-21 | S2_after_battery | Online retail channel; seller not recorded | PKG-019 | unspecified | Supplier production-lot identifier unavailable; internal grouping confidence low | 1/1/2/1 |
| V11 | 515 | 8 | 2026-07-21 | S1_before_battery | Online retail channel; seller not recorded | PKG-001;PKG-002 | large_200g | Supplier production-lot identifier unavailable; packages author-reported as the same lot | 2/2/2/2 |
| V12 | 148 | 4 | 2026-07-21 | S2_after_battery | Online retail channel; seller not recorded | PKG-008 | unspecified | Supplier production-lot identifier unavailable; internal grouping confidence low | 1/1/1/1 |

Entries reproduce recorded metadata. Unavailable lot identifiers must not be interpreted as independent lots. Recorded cultivar names corresponding to V01–V12 are listed in Supplementary Table S3.

## Table S2. All-seed residual balanced-error ratios

| pair | residual_error_reduction | ratio_ci_2_5 | ratio_ci_97_5 | ratio_invalid_bootstraps |
| --- | --- | --- | --- | --- |
| M_to_MS | -20.0% | -260.0% | 100.0% | 639 |
| D_to_SD | 51.8% | 0.0% | 100.0% | 0 |
| MD_to_MSD | 63.6% | 0.0% | 100.0% | 57 |

Post hoc ratios divide the mean BA difference by remaining RGB balanced error. Bounds are existing conditional 95% bootstrap limits; invalid-bootstrap counts are out of 2,000 draws and indicate zero denominators. Near-zero denominators make these ratios unstable. They are retained for transparency, not used as headline results.

## Table S3. Variety identifiers and recorded Chinese cultivar names

| Variety ID | Recorded cultivar name (Chinese) |
| --- | --- |
| V01 | 密甜糯1号 |
| V02 | 昕禾323 |
| V03 | 昕禾一号 |
| V04 | 浙糯玉19 |
| V05 | 浙糯玉22 |
| V06 | 浙糯玉24 |
| V07 | 澳早60 |
| V08 | 澳甜糯65 |
| V09 | 珍珍糯600 |
| V10 | 白甜糯6号 |
| V11 | 诚糯10号 |
| V12 | 金辉306 |

These identifiers are used consistently in the main text, tables, and figures. Names reproduce the recorded Chinese cultivar labels.

## Table S4. Paired SGSEF contrasts against RGB and spectral controls

| Endpoint | Donors k | Comparator | SGSEF minus comparator | Conditional 95% interval |
| --- | --- | --- | --- | --- |
| Recipient-seed BA | 3 | Individual D | +0.1091 | [+0.0977, +0.1200] |
| Recipient-seed BA | 3 | Group S only | +0.0770 | [+0.0493, +0.1040] |
| Recipient-seed BA | 3 | Seed-paired SD | +0.0446 | [+0.0368, +0.0523] |
| Group BA | 3 | Dense D aggregation | -0.0095 | [-0.0441, +0.0289] |
| Group BA | 3 | Group S only | +0.3976 | [+0.3651, +0.4283] |
| Group BA | 3 | Seed-paired SD | -0.0554 | [-0.0746, -0.0368] |
| Recipient-seed BA | 5 | Individual D | +0.1143 | [+0.1024, +0.1258] |
| Recipient-seed BA | 5 | Group S only | -0.0095 | [-0.0409, +0.0213] |
| Recipient-seed BA | 5 | Seed-paired SD | +0.0498 | [+0.0416, +0.0579] |
| Group BA | 5 | Dense D aggregation | +0.0187 | [-0.0140, +0.0542] |
| Group BA | 5 | Group S only | +0.3357 | [+0.2981, +0.3718] |
| Group BA | 5 | Seed-paired SD | -0.0252 | [-0.0411, -0.0108] |

Contrasts are evaluated on donor-excluded recipients at the stated endpoint and summarize 500 donor selections. Intervals use 2,000 paired, variety-stratified whole-tray bootstrap samples. Recipient-seed BA and group BA use different weighting. The RGB group broadcast comparison appears in Table 3.
