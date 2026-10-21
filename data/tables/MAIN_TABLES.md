# Tables

## Table 1. Primary-cohort variety composition and tray allocation

| Variety | Seeds | Trays | Acquisition segment(s) | Trays in folds 0/1/2/3 |
| --- | --- | --- | --- | --- |
| V01 | 215 | 4 | S2 | 1/1/1/1 |
| V02 | 296 | 6 | S2 | 1/1/2/2 |
| V03 | 292 | 5 | S1;S2 | 2/1/1/1 |
| V04 | 393 | 8 | S1 | 2/2/2/2 |
| V05 | 384 | 6 | S1 | 2/1/1/2 |
| V06 | 294 | 6 | S1 | 1/1/2/2 |
| V07 | 258 | 5 | S2 | 2/1/1/1 |
| V08 | 302 | 5 | S2 | 1/1/2/1 |
| V09 | 276 | 5 | S2 | 1/2/1/1 |
| V10 | 254 | 5 | S2 | 1/1/2/1 |
| V11 | 515 | 8 | S1 | 2/2/2/2 |
| V12 | 148 | 4 | S2 | 1/1/1/1 |

All samples were acquired on 21 July 2026. S1 and S2 denote the acquisition segments before and after the battery change that day. Seeds were purchased through an online retail channel; seller identity and supplier production-lot identifiers were unavailable. Package records do not establish independent production lots. Full recorded provenance is provided in Supplementary Table S1.

## Table 2. Observation-count comparison of the fixed MD and MSD recipes in the primary cohort

| k | MD | MSD | MSD − MD | Conditional 95% interval |
| --- | --- | --- | --- | --- |
| 1 | 0.5260 | 0.5848 | +0.0588 | [0.0468, 0.0714] |
| 3 | 0.7472 | 0.8151 | +0.0678 | [0.0577, 0.0787] |
| 5 | 0.8386 | 0.8935 | +0.0548 | [0.0439, 0.0665] |
| 10 | 0.9130 | 0.9488 | +0.0357 | [0.0240, 0.0481] |
| 20 | 0.9442 | 0.9693 | +0.0251 | [0.0105, 0.0410] |
| all | 0.9618 | 0.9861 | +0.0243 | [0.0000, 0.0590] |

Values are mean group balanced accuracy over 500 shared nested sampling schedules. Intervals are conditional 95% variety-stratified whole-tray bootstrap intervals for MSD minus MD from the primary analysis. All 67 trays and 12 varieties contribute at every k. Differences are calculated before rounding.

## Table 3. Secondary donor sharing compared with RGB group decisions

| Endpoint | Donors k | n | SGSEF | RGB comparator | RGB BA | Difference | Conditional 95% interval |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Recipient-seed BA | 3 | 3426 | 0.5856 | RGB group broadcast | 0.9184 | -0.3328 | [-0.3711, -0.2901] |
| Recipient-seed BA | 5 | 3292 | 0.5908 | RGB group broadcast | 0.9200 | -0.3292 | [-0.3660, -0.2876] |
| Group BA | 3 | 67 | 0.9036 | Dense D group decision | 0.9132 | -0.0095 | [-0.0441, 0.0289] |
| Group BA | 5 | 67 | 0.9335 | Dense D group decision | 0.9147 | +0.0187 | [-0.0140, 0.0542] |

Here k is the number of spectral donors, not the observation count in Table 2. Recipient-seed BA is evaluated on the same donor-excluded recipient sets for both rules (n seeds); group BA uses all 67 tray decisions (n trays). Recipient-seed BA weights seeds within variety, whereas group BA weights tray decisions within variety. Differences are SGSEF minus the stated comparator; intervals are paired conditional 95% tray-bootstrap intervals. Complete controls appear in Figure S5.
