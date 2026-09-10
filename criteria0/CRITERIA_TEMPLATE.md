# CRITERIA TEMPLATE (criteria0) — copy to criteria/criteriaN.md and fill

An agent may not submit until every row is green. Verification names the exact
mechanism — provide it or fail the row. Methods: test | demo | review | kanban
| pyeval. See HERMES_HANDBOOK.md §3 and Pydantic evals docs
(`docs/vendor/pydantic/evals_getting-started_core-concepts_md`).

| ID | Statement (binary) | Verification | Owner |
|---|---|---|---|
| C1 | [Falsifiable, true-or-false] | test `test_name_here` | human |
| C2 | [Falsifiable, true-or-false] | demo `demo/script.sh` expects `OUTPUT` | human |
| C3 | [Multi-agent or survival work] | kanban `board/task-slug` done per completion contract | human |
| C4 | [Model-behavior claim] | pyeval `dataset.case` passing with named evaluator | human |

Run it: `OPENCODE_GO_API_KEY=... python3 pyeval.py run datasets/<name>.json`
(rule + judge evaluators; key via env only, cheap model default).
