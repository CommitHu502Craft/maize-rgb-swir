# Data dictionary and identity conventions

- batch2 / original Batch 2 = primary cohort (21 July 2026; 3,627 seeds, 67 trays, 12 varieties). batch3 / original Batch 3 = descriptive later-date BASE cohort (4 August 2026; 280 seeds, 10 trays, 10 represented varieties). Original IDs remain stable.
- M = M_phys; D = D_phys; S = fitted SWIR classifier. MD=(M+D)/2; MSD=(M+D+S)/3; MS=(M+S)/2; SD=(D+S)/2. F_alpha=(1-alpha)MD+alpha*S.
- replay/audit/run.json fixes the 12-class probability order. C00–C11 are zero-based positions in that list, not direct equivalents of V01–V12. Join the original variety names through data/figure_source/variety_id_mapping.csv for the article's labels.
- row_index / row_id is the zero-based row position. seed_id (primary), entity_seed_id (later-date), and record_id identify seeds and trays. tray_index follows first encounter order, matching the tray CSV.
- outer_fold is 0–3 for the primary cohort and -1 for compact later-date outputs (four fitted-model predictions averaged). Primary M/S/D arrays are aligned by seed identity.
- Compact probabilities: shape [branch, seed, class], branch order [M,D,S], float64; fitted outputs, not spectra or weights.
- k is seeds per tray decision; all uses the complete tray. Saved schedules comprise 500 nested repetitions (seed 20260913); the primary archive includes 2,000 variety-stratified whole-tray bootstrap draws.
- BA uses the 0–1 scale unless explicitly marked percent or percentage points. Group BA averages within-variety tray recalls, then varieties; seed endpoints use seed-level class recalls. Differences precede rounding.
- Primary intervals are conditional whole-tray bootstrap intervals for fixed predictions/schedules. Later-date curves are descriptive. Donor randomization quantiles are not confidence intervals. Each CSV's interval_type, endpoint, filter_description and unit_multiplier govern its interpretation.
- Figure_2_A/B/C/D are source layers: visible Figure 2A combines primary layers A/B, and visible Figure 2B combines later-date layers C/D.
- upstream_path / source_path point to included files relative to this release folder. Only these provenance-path cells are relabeled; every other CSV cell and all saved arrays retain their source values. source_row keeps the original generator's convention.
- FILE_CATALOG.csv records all files in this folder except itself, including documentation and the actual replay record.

## File-level schemas

### data/figure_source/Figure_2_A.csv

12 data rows. Columns: scope, schedule, recipe, k, repetitions, balanced_accuracy_mean, balanced_accuracy_std, balanced_accuracy_min, balanced_accuracy_max, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_2_B.csv

6 data rows. Columns: k, schedule, contrast, point_estimate, sampling_repeat_mean, sampling_repeat_std, bootstrap_ci_2_5, bootstrap_ci_97_5, varieties_positive, varieties_zero, varieties_nonnegative, loo_min, loo_max, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_2_C.csv

12 data rows. Columns: scope, recipe, k, repetitions, balanced_accuracy_mean, balanced_accuracy_std, balanced_accuracy_min, balanced_accuracy_max, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_2_D.csv

6 data rows. Columns: k, scope, schedule, contrast, repetitions, difference_mean, difference_std, difference_min, difference_max, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_3_B.csv

6 data rows. Columns: recipe, k, repetitions, balanced_accuracy_mean, balanced_accuracy_std, balanced_accuracy_min, balanced_accuracy_max, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_3_absolute_D_to_SD.csv

6 data rows. Columns: k, pair, rgb_recipe, multimodal_recipe, rgb_ba, multimodal_ba, absolute_increment, absolute_ci_2_5, absolute_ci_97_5, residual_error_reduction, ratio_ci_2_5, ratio_ci_97_5, ratio_invalid_bootstraps, sampling_increment_mean, sampling_ratio_mean, varieties_positive, varieties_nonnegative, loo_variety_min, loo_variety_max, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_3_absolute_MD_to_MSD.csv

6 data rows. Columns: k, pair, rgb_recipe, multimodal_recipe, rgb_ba, multimodal_ba, absolute_increment, absolute_ci_2_5, absolute_ci_97_5, residual_error_reduction, ratio_ci_2_5, ratio_ci_97_5, ratio_invalid_bootstraps, sampling_increment_mean, sampling_ratio_mean, varieties_positive, varieties_nonnegative, loo_variety_min, loo_variety_max, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_3_absolute_M_to_MS.csv

6 data rows. Columns: k, pair, rgb_recipe, multimodal_recipe, rgb_ba, multimodal_ba, absolute_increment, absolute_ci_2_5, absolute_ci_97_5, residual_error_reduction, ratio_ci_2_5, ratio_ci_97_5, ratio_invalid_bootstraps, sampling_increment_mean, sampling_ratio_mean, varieties_positive, varieties_nonnegative, loo_variety_min, loo_variety_max, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_4_A_means.csv

4 data rows. Columns: hierarchy, recipe, repeats, balanced_accuracy_mean, balanced_accuracy_std, balanced_accuracy_min, balanced_accuracy_max, macro_f1_mean, true_class_probability_mean, prediction_change_from_rgb_mean, prediction_change_from_true_pair_mean, rescue_rate_mean, harm_rate_mean, loss_from_true_pair_mean, gain_retention_mean, gain_retention_std, donor_unique_fraction_mean, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_4_B.csv

3 data rows. Columns: contrast, analysis, recipe, bootstrap_repeats, point_estimate, bootstrap_mean, bootstrap_std, ci_2_5, ci_97_5, fraction_above_zero, ci_contains_zero, ci_strictly_above_zero, ci_strictly_below_zero, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_4_C.csv

2 data rows. Columns: recipe, repeats, true_seed_ba_mean, same_variety_other_tray_ba_mean, difference_mean, difference_std, randomization_q2_5, randomization_q97_5, difference_min, difference_max, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_S1_ratio_D_to_SD.csv

5 data rows. Columns: k, pair, rgb_recipe, multimodal_recipe, rgb_ba, multimodal_ba, absolute_increment, absolute_ci_2_5, absolute_ci_97_5, residual_error_reduction, ratio_ci_2_5, ratio_ci_97_5, ratio_invalid_bootstraps, sampling_increment_mean, sampling_ratio_mean, varieties_positive, varieties_nonnegative, loo_variety_min, loo_variety_max, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_S1_ratio_MD_to_MSD.csv

5 data rows. Columns: k, pair, rgb_recipe, multimodal_recipe, rgb_ba, multimodal_ba, absolute_increment, absolute_ci_2_5, absolute_ci_97_5, residual_error_reduction, ratio_ci_2_5, ratio_ci_97_5, ratio_invalid_bootstraps, sampling_increment_mean, sampling_ratio_mean, varieties_positive, varieties_nonnegative, loo_variety_min, loo_variety_max, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_S1_ratio_M_to_MS.csv

5 data rows. Columns: k, pair, rgb_recipe, multimodal_recipe, rgb_ba, multimodal_ba, absolute_increment, absolute_ci_2_5, absolute_ci_97_5, residual_error_reduction, ratio_ci_2_5, ratio_ci_97_5, ratio_invalid_bootstraps, sampling_increment_mean, sampling_ratio_mean, varieties_positive, varieties_nonnegative, loo_variety_min, loo_variety_max, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_S2_A.csv

72 data rows. Columns: schedule, k, contrast, variety, difference, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_S2_B_full.csv

6 data rows. Columns: k, schedule, contrast, point_estimate, sampling_repeat_mean, sampling_repeat_std, bootstrap_ci_2_5, bootstrap_ci_97_5, varieties_positive, varieties_zero, varieties_nonnegative, loo_min, loo_max, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_S2_B_omissions.csv

72 data rows. Columns: schedule, k, contrast, omitted_variety, difference, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_S3_A.csv

3 data rows. Columns: contrast, left, right, point_estimate, sampling_mean, sampling_q2_5, sampling_q97_5, bootstrap_ci_2_5, bootstrap_ci_97_5, varieties_positive, varieties_nonnegative, loo_variety_min, loo_variety_max, loo_tray_min, loo_tray_max, formally_supported_under_protocol, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_S3_B.csv

1500 data rows. Columns: contrast, repeat, difference, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_S3_B_ranges.csv

3 data rows. Columns: contrast, left, right, point_estimate, sampling_mean, sampling_q2_5, sampling_q97_5, bootstrap_ci_2_5, bootstrap_ci_97_5, varieties_positive, varieties_nonnegative, loo_variety_min, loo_variety_max, loo_tray_min, loo_tray_max, formally_supported_under_protocol, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_S3_C_tray.csv

3 data rows. Columns: contrast, left, right, point_estimate, sampling_mean, sampling_q2_5, sampling_q97_5, bootstrap_ci_2_5, bootstrap_ci_97_5, varieties_positive, varieties_nonnegative, loo_variety_min, loo_variety_max, loo_tray_min, loo_tray_max, formally_supported_under_protocol, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_S3_C_variety.csv

3 data rows. Columns: contrast, left, right, point_estimate, sampling_mean, sampling_q2_5, sampling_q97_5, bootstrap_ci_2_5, bootstrap_ci_97_5, varieties_positive, varieties_nonnegative, loo_variety_min, loo_variety_max, loo_tray_min, loo_tray_max, formally_supported_under_protocol, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_S4_A.csv

48 data rows. Columns: variety_id, variety, hierarchy, seeds, trays, repeats, recall_mean, recall_std, recall_q025, recall_q975, recall_min, recall_max, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_S4_B.csv

12 data rows. Columns: variety_id, variety, different_variety, same_tray_other_seed, same_variety_other_tray, true_seed, same_variety_minus_matched, same_variety_minus_cross_variety, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_S4_C.csv

12 data rows. Columns: variety_id, variety, different_variety, same_tray_other_seed, same_variety_other_tray, true_seed, same_variety_minus_matched, same_variety_minus_cross_variety, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_S5_B_Group_S_only.csv

2 data rows. Columns: scope, k, coverage_percent, unmeasured_seeds, seed_BA_D_only, seed_BA_Group_S_only, seed_BA_Sparse_D_Group_S, seed_BA_Full_SD, seed_RGB_increment, tray_BA_D_only, tray_BA_Group_S_only, tray_BA_Sparse_D_Group_S, tray_BA_Full_SD, tray_RGB_increment, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_S5_B_Individual_D.csv

2 data rows. Columns: scope, k, coverage_percent, unmeasured_seeds, seed_BA_D_only, seed_BA_Group_S_only, seed_BA_Sparse_D_Group_S, seed_BA_Full_SD, seed_RGB_increment, tray_BA_D_only, tray_BA_Group_S_only, tray_BA_Sparse_D_Group_S, tray_BA_Full_SD, tray_RGB_increment, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_S5_B_SGSEF.csv

2 data rows. Columns: scope, k, coverage_percent, unmeasured_seeds, seed_BA_D_only, seed_BA_Group_S_only, seed_BA_Sparse_D_Group_S, seed_BA_Full_SD, seed_RGB_increment, tray_BA_D_only, tray_BA_Group_S_only, tray_BA_Sparse_D_Group_S, tray_BA_Full_SD, tray_RGB_increment, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_S5_B_broadcast.csv

2 data rows. Columns: scope, k, repeats, eligible_trays, recipient_seeds, seed_ba_D_only_mean, seed_ba_Group_D_broadcast_mean, seed_ba_Group_D_broadcast_min, seed_ba_Group_D_broadcast_max, seed_ba_SGSEF_mean, SGSEF_minus_Group_D_broadcast_mean, SGSEF_minus_Group_D_broadcast_min, SGSEF_minus_Group_D_broadcast_max, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_S5_C_Dense_D.csv

2 data rows. Columns: scope, k, coverage_percent, unmeasured_seeds, seed_BA_D_only, seed_BA_Group_S_only, seed_BA_Sparse_D_Group_S, seed_BA_Full_SD, seed_RGB_increment, tray_BA_D_only, tray_BA_Group_S_only, tray_BA_Sparse_D_Group_S, tray_BA_Full_SD, tray_RGB_increment, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_S5_C_Group_S_only.csv

2 data rows. Columns: scope, k, coverage_percent, unmeasured_seeds, seed_BA_D_only, seed_BA_Group_S_only, seed_BA_Sparse_D_Group_S, seed_BA_Full_SD, seed_RGB_increment, tray_BA_D_only, tray_BA_Group_S_only, tray_BA_Sparse_D_Group_S, tray_BA_Full_SD, tray_RGB_increment, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_S5_C_SGSEF.csv

2 data rows. Columns: scope, k, coverage_percent, unmeasured_seeds, seed_BA_D_only, seed_BA_Group_S_only, seed_BA_Sparse_D_Group_S, seed_BA_Full_SD, seed_RGB_increment, tray_BA_D_only, tray_BA_Group_S_only, tray_BA_Sparse_D_Group_S, tray_BA_Full_SD, tray_RGB_increment, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_S5_D.csv

2 data rows. Columns: analysis, k, contrast, bootstrap_repeats, point_estimate, bootstrap_mean, bootstrap_std, ci_2_5, ci_97_5, fraction_above_zero, ci_contains_zero, ci_strictly_above_zero, ci_strictly_below_zero, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_S5_E.csv

2 data rows. Columns: analysis, k, level, contrast, bootstrap_repeats, point_estimate, bootstrap_mean, bootstrap_std, ci_2_5, ci_97_5, fraction_above_zero, ci_contains_zero, ci_strictly_above_zero, ci_strictly_below_zero, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_S6_A.csv

24 data rows. Columns: scope, condition, level, recipe, n, n_trays, accuracy, balanced_accuracy, macro_f1, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_S6_label_agreement.csv

20 data rows. Columns: condition, recipe, n_pairs_total, n_pairs_true_class_scored, mean_delta_true_class_probability, median_delta_true_class_probability, mean_js_divergence, mean_probability_l1, label_agreement, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_S6_mean_delta_true_class_probability.csv

20 data rows. Columns: condition, recipe, n_pairs_total, n_pairs_true_class_scored, mean_delta_true_class_probability, median_delta_true_class_probability, mean_js_divergence, mean_probability_l1, label_agreement, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_S6_mean_js_divergence.csv

20 data rows. Columns: condition, recipe, n_pairs_total, n_pairs_true_class_scored, mean_delta_true_class_probability, median_delta_true_class_probability, mean_js_divergence, mean_probability_l1, label_agreement, upstream_path, source_row, estimate, lower, upper, estimate_field, lower_field, upper_field, interval_type, endpoint, cohort, filter_description, unit_multiplier, panel.

### data/figure_source/Figure_S7_endpoint_changes.csv

60 data rows. Columns: cohort, alpha, comparator, start, end, endpoint_change, ci025, ci975, loo_min, loo_max.

### data/figure_source/Figure_S7_error_states.csv

120 data rows. Columns: cohort, alpha, comparator, k, both_correct, rescue, harm, both_wrong, net.

### data/figure_source/Figure_S7_weight_contrasts.csv

120 data rows. Columns: cohort, alpha, recipe, comparator, k, difference, sampling_sd, comparator_ba, f_ba, comparator_error, residual_error_reduction, ci025, ci975.

### data/figure_source/all_seed_verification/tray_decisions.csv

77 data rows. Columns: cohort, record_id, variety_id, seeds, M_prediction, M_correct, D_prediction, D_correct, MS_prediction, MS_correct, MD_prediction, MD_correct, SD_prediction, SD_correct, MSD_prediction, MSD_correct.

### data/figure_source/endpoint_diagnostics/paired_endpoint_changes.csv

2000 data rows. Columns: schedule, contrast, repeat, endpoint_change.

### data/figure_source/endpoint_diagnostics/variety_equal_rescue_harm.csv

3 data rows. Columns: k, rescue, harm, net_difference, original_difference, absolute_error.

### data/figure_source/perturbation_group_results.csv

50 data rows. Columns: condition, source_recipe, entity_tray_id, variety_id, base_record_id, condition_record_id, n_pairs, mean_delta_true_class_probability, mean_js_divergence, base_seed_accuracy, condition_seed_accuracy, recipe.

### data/figure_source/variety_id_mapping.csv

12 data rows. Columns: variety_id, variety.

### data/supporting_results/donor_and_group_controls/batch2_rgb_broadcast_bootstrap_summary.csv

4 data rows. Columns: analysis, k, contrast, bootstrap_repeats, point_estimate, bootstrap_mean, bootstrap_std, ci_2_5, ci_97_5, fraction_above_zero, ci_contains_zero, ci_strictly_above_zero, ci_strictly_below_zero.

### data/supporting_results/donor_and_group_controls/batch2_rgb_broadcast_summary.csv

2 data rows. Columns: scope, k, repeats, eligible_trays, recipient_seeds, seed_ba_D_only_mean, seed_ba_Group_D_broadcast_mean, seed_ba_Group_D_broadcast_min, seed_ba_Group_D_broadcast_max, seed_ba_SGSEF_mean, SGSEF_minus_Group_D_broadcast_mean, SGSEF_minus_Group_D_broadcast_min, SGSEF_minus_Group_D_broadcast_max.

### data/supporting_results/donor_and_group_controls/fold_matched_composition_by_repeat.csv

950 data rows. Columns: repeat, variety, outer_fold, trays, seeds.

### data/supporting_results/donor_and_group_controls/fold_matched_direct_contrast_summary.csv

2 data rows. Columns: recipe, repeats, true_seed_ba_mean, same_variety_other_tray_ba_mean, difference_mean, difference_std, randomization_q2_5, randomization_q97_5, difference_min, difference_max.

### data/supporting_results/donor_and_group_controls/fold_matched_direct_contrasts.csv

100 data rows. Columns: recipe, repeat, different_variety, same_tray_other_seed, same_variety_other_tray, true_seed, same_variety_other_tray_minus_true_seed, same_tray_other_seed_minus_true_seed.

### data/supporting_results/figure_summaries/donor_hierarchy_bootstrap.csv

6 data rows. Columns: analysis, recipe, contrast, bootstrap_repeats, point_estimate, bootstrap_mean, bootstrap_std, ci_2_5, ci_97_5, fraction_above_zero, ci_contains_zero, ci_strictly_above_zero, ci_strictly_below_zero.

### data/supporting_results/figure_summaries/donor_hierarchy_summary.csv

8 data rows. Columns: recipe, hierarchy, repeats, balanced_accuracy_mean, balanced_accuracy_std, balanced_accuracy_min, balanced_accuracy_max, macro_f1_mean, true_class_probability_mean, prediction_change_from_rgb_mean, prediction_change_from_true_pair_mean, rescue_rate_mean, harm_rate_mean, loss_from_true_pair_mean, gain_retention_mean, gain_retention_std, donor_unique_fraction_mean.

### data/supporting_results/figure_summaries/paired_perturbation_effects.csv

20 data rows. Columns: condition, recipe, n_pairs_total, n_pairs_true_class_scored, mean_delta_true_class_probability, median_delta_true_class_probability, mean_js_divergence, mean_probability_l1, label_agreement.

### data/supporting_results/figure_summaries/per_variety_donor_deltas.csv

12 data rows. Columns: variety_id, variety, different_variety, same_tray_other_seed, same_variety_other_tray, true_seed, same_variety_minus_matched, same_variety_minus_cross_variety.

### data/supporting_results/figure_summaries/per_variety_donor_reassignment.csv

48 data rows. Columns: variety_id, variety, hierarchy, seeds, trays, repeats, recall_mean, recall_std, recall_q025, recall_q975, recall_min, recall_max.

### data/supporting_results/figure_summaries/perturbation_robustness.csv

24 data rows. Columns: scope, condition, level, recipe, n, n_trays, accuracy, balanced_accuracy, macro_f1.

### data/supporting_results/figure_summaries/sgsef_coverage_and_rgb_control.csv

8 data rows. Columns: scope, k, coverage_percent, unmeasured_seeds, seed_BA_D_only, seed_BA_Group_S_only, seed_BA_Sparse_D_Group_S, seed_BA_Full_SD, seed_RGB_increment, tray_BA_D_only, tray_BA_Group_S_only, tray_BA_Sparse_D_Group_S, tray_BA_Full_SD, tray_RGB_increment.

### data/supporting_results/figure_summaries/sgsef_rgb_contrast_bootstrap.csv

12 data rows. Columns: analysis, k, level, contrast, bootstrap_repeats, point_estimate, bootstrap_mean, bootstrap_std, ci_2_5, ci_97_5, fraction_above_zero, ci_contains_zero, ci_strictly_above_zero, ci_strictly_below_zero.

### data/supporting_results/observation_count/batch3_nested_curve_summary.csv

24 data rows. Columns: scope, recipe, k, repetitions, balanced_accuracy_mean, balanced_accuracy_std, balanced_accuracy_min, balanced_accuracy_max.

### data/supporting_results/observation_count/batch3_same_k_contrast_summary.csv

12 data rows. Columns: scope, schedule, contrast, k, repetitions, difference_mean, difference_std, difference_min, difference_max.

### data/supporting_results/observation_count/nested_curve_summary.csv

24 data rows. Columns: scope, schedule, recipe, k, repetitions, balanced_accuracy_mean, balanced_accuracy_std, balanced_accuracy_min, balanced_accuracy_max.

### data/supporting_results/observation_count/nested_leave_one_variety_out.csv

144 data rows. Columns: schedule, k, contrast, omitted_variety, difference.

### data/supporting_results/observation_count/nested_per_variety_contrasts.csv

144 data rows. Columns: schedule, k, contrast, variety, difference.

### data/supporting_results/observation_count/nested_same_k_contrast_summary.csv

12 data rows. Columns: schedule, k, contrast, point_estimate, sampling_repeat_mean, sampling_repeat_std, bootstrap_ci_2_5, bootstrap_ci_97_5, varieties_positive, varieties_zero, varieties_nonnegative, loo_min, loo_max.

### data/supporting_results/robustness/cross_k_frontier_summary.csv

3 data rows. Columns: contrast, left, right, point_estimate, sampling_mean, sampling_q2_5, sampling_q97_5, bootstrap_ci_2_5, bootstrap_ci_97_5, varieties_positive, varieties_nonnegative, loo_variety_min, loo_variety_max, loo_tray_min, loo_tray_max, formally_supported_under_protocol.

### data/supporting_results/robustness/cross_k_sampling_repeats.csv

1500 data rows. Columns: contrast, repeat, difference.

### data/supporting_results/robustness/fixed_pair_ceiling_summary.csv

18 data rows. Columns: pair, rgb_recipe, multimodal_recipe, k, rgb_ba, multimodal_ba, absolute_increment, absolute_ci_2_5, absolute_ci_97_5, residual_error_reduction, ratio_ci_2_5, ratio_ci_97_5, ratio_invalid_bootstraps, sampling_increment_mean, sampling_ratio_mean, varieties_positive, varieties_nonnegative, loo_variety_min, loo_variety_max.

### data/supporting_results/robustness/recipe_curve_summary.csv

36 data rows. Columns: recipe, k, repetitions, balanced_accuracy_mean, balanced_accuracy_std, balanced_accuracy_min, balanced_accuracy_max.

### data/tables/table_1_compact_provenance.csv

12 data rows. Columns: Variety, Seeds, Trays, Session(s), Trays in folds 0/1/2/3.

### data/tables/table_1_variety_provenance.csv

12 data rows. Columns: variety, seeds, trays, acquisition_date, sessions, commercial_source, package_records, batch2_packaging, production_lot_status, outer_fold_trays_0_1_2_3.

### data/tables/table_2_observation_scale.csv

6 data rows. Columns: k, MD_BA, MSD_BA, MSD_minus_MD, ci_lower, ci_upper.

### data/tables/table_3_donor_sharing_controls.csv

4 data rows. Columns: endpoint, k_donors, evaluation_units, SGSEF_BA, comparator, comparator_BA, difference, ci_lower, ci_upper.

### data/tables/table_s2_all_seed_ratios.csv

3 data rows. Columns: pair, residual_error_reduction, ratio_ci_2_5, ratio_ci_97_5, ratio_invalid_bootstraps.

### replay/data/all_seed_branch_margins.csv

231 data rows. Columns: cohort, record_id, variety, branch, top_prediction, true_probability, true_vs_best_wrong_margin.

### replay/data/all_seed_decisions.csv

924 data rows. Columns: cohort, record_id, variety, seeds, recipe, prediction, correct.

### replay/data/batch2_bootstrap.npz

draws: (2000, 67) int64; weights: (2000, 67) float64; seed: () int64.

### replay/data/batch2_decisions.npz

predictions: (12, 6, 500, 67) int8; truth: (67,) int64; tray_weights: (67,) float64; recipes: (12,) <U4; ks: (6,) <U3.

### replay/data/batch2_rows.csv

3627 data rows. Columns: row_index, seed_id, record_id, variety_name, outer_fold.

### replay/data/batch2_schedule_hashes.csv

3000 data rows. Columns: k, repeat, indices_sha256.

### replay/data/batch2_schedules.npz

permutations: (500, 67, 72) int32; tray_sizes: (67,) int64; seed: () int64.

### replay/data/batch2_trays.csv

67 data rows. Columns: tray_index, record_id, variety, seeds, fold.

### replay/data/batch3_decisions.npz

predictions: (12, 6, 500, 10) int8; truth: (10,) int64; tray_weights: (10,) float64; recipes: (12,) <U4; ks: (6,) <U3.

### replay/data/batch3_rows.csv

280 data rows. Columns: row_index, entity_seed_id, record_id, variety, condition.

### replay/data/batch3_schedule_hashes.csv

3000 data rows. Columns: k, repeat, indices_sha256.

### replay/data/batch3_schedules.npz

permutations: (500, 10, 36) int32; tray_sizes: (10,) int64; seed: () int64.

### replay/data/batch3_trays.csv

10 data rows. Columns: tray_index, record_id, variety, seeds, fold.

### replay/data/curve_summary.csv

144 data rows. Columns: cohort, recipe, k, ba, sampling_sd, sampling_q025, sampling_q975, distinct_sampling_decisions.

### replay/data/endpoint_changes.csv

60 data rows. Columns: cohort, alpha, comparator, start, end, endpoint_change, ci025, ci975, loo_min, loo_max.

### replay/data/error_states.csv

120 data rows. Columns: cohort, alpha, comparator, k, both_correct, rescue, harm, both_wrong, net.

### replay/data/leave_one_variety_out.csv

1320 data rows. Columns: cohort, alpha, comparator, k, omitted_variety, difference.

### replay/data/paired_bootstrap_values.csv

180000 data rows. Columns: cohort, alpha, comparator, k, repeat, difference.

### replay/data/per_variety.csv

1320 data rows. Columns: cohort, alpha, comparator, k, variety, difference, rescue, harm.

### replay/data/sampling_repeats.csv

72000 data rows. Columns: cohort, recipe, k, repeat, ba.

### replay/data/tray_error_states.csv

4620 data rows. Columns: cohort, alpha, comparator, k, record_id, variety, both_correct, rescue, harm, both_wrong, difference.

### replay/data/weight_contrasts.csv

120 data rows. Columns: cohort, alpha, recipe, comparator, k, difference, sampling_sd, comparator_ba, f_ba, comparator_error, residual_error_reduction, ci025, ci975.

### replay/probabilities/batch2.npz

row_id: (3627,) int32; tray_index: (3627,) int32; truth: (3627,) int8; outer_fold: (3627,) int8; class_order: (12,) <U3; probabilities: (3, 3627, 12) float64.

### replay/probabilities/batch3.npz

row_id: (280,) int32; tray_index: (280,) int32; truth: (280,) int8; outer_fold: (280,) int8; class_order: (12,) <U3; probabilities: (3, 280, 12) float64.
