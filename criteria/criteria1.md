# criteria1 — binary rubric for idea1 builds (all must pass; slices gate independently)

An agent may not submit until every row below is green. Verification names the
exact test/demo/review that must exist — provide it or fail the row.

| ID | Statement (binary) | Verification | Owner |
|---|---|---|---|
| C1 | Graph supports catalytic edges: automating A changes B's breakthrough hazard rate, demonstrated on 1 seeded pair | test `test_catalytic_edge_changes_hazard` | human |
| C2 | Scarcity metric B_i implemented per thesis formula (induced demand × indispensability × replacement × permission / capacity+substitutes+inventory) | test `test_scarcity_formula_terms` | human |
| C3 | dB/dt tracked: severity time series in, rising-vs-falling verdict out, on 1 seeded series | test `test_bottleneck_velocity_sign` | human |
| C4 | Every event carries three clocks (capability/deployment/cashflow timestamps) | test `test_three_clocks_present` | human |
| C5 | surprise() primitive implemented (e − E[e\|W]) and used in ranking, not raw novelty | test `test_surprise_beats_novelty` | human |
| C6 | Evidence hierarchy weights verified cash-flow impact above benchmark scores (configurable weights file) | test `test_cashflow_outranks_benchmark` | human |
| C7 | Cross-world exposure scored over ≥3 explicit scenarios with sourced probabilities | test `test_cross_world_counts_scenarios` | human |
| C8 | Irreducibility metric implemented (genuine-observation cost − synthetic cost) on 1 seeded dataset | test `test_irreducibility_positive` | human |
| C9 | Technical-half-life vs valuation-duration mismatch computed on 1 seeded asset | test `test_duration_mismatch_sign` | human |
| C10 | Bottleneck-release probability tracked (capacity/supply-response inputs present) | test `test_release_inputs_present` | human |
| C11 | Geography layer present (company × geography × capability × permission on 1 seeded node) | test `test_geo_quad_present` | human |
| C12 | One worked belief-inconsistency demo: two securities with mutually exclusive implied futures, shown in `demo/inconsistency.sh` output | demo `demo/inconsistency.sh` expects `INCONSISTENT` | human |

Out of scope for v1 (logged, not gated): live data feeds, 100-company universe,
real capital deployment, biology/quantum domain packs.
