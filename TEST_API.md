# Test-only API

`crc/test_api.yml` is a second OpenAPI spec, separate from `crc/api.yml`, for
endpoints that only make sense in a test context (e.g. forcing a workflow or
study into a specific state without driving the BPMN engine through it).

## Wiring

In `crc/__init__.py`, the spec is mounted only when running under the test
config:

```python
connexion_app.add_api('api.yml', base_path='/v1.0')

if app.config['TESTING']:
    connexion_app.add_api('test_api.yml', base_path='/v1.0/test')
```

`app.config['TESTING']` is `True` whenever `config/testing.py` is loaded
(i.e. the `TESTING=true` env var is set before `crc` is imported). In any
other environment, including production, `test_api.yml` is never loaded and
none of its routes exist.

### Why `base_path='/v1.0/test'` and not `/v1.0`

Connexion derives each mounted spec's internal Flask blueprint name from its
`base_path` alone. Reusing `/v1.0` for both `api.yml` and `test_api.yml`
produced two blueprints with the same derived name and Flask refused to
register the second one (`ValueError: The name 'v1_0' is already registered
for a different blueprint`). Splitting the base path avoids the collision.
Paths inside `test_api.yml` do not repeat `/test` themselves, so the final
URLs still land under `/v1.0/test/...`.

## Endpoints

### `PUT /v1.0/test/workflow/{workflow_id}/status`

Body: `{"new_workflow_status": "<WorkflowStatus value>"}`

Looks up the `WorkflowModel` by id, validates the status against
`crc.models.workflow.WorkflowStatus`, sets it, and commits. Returns
`{"status": "<new value>"}`.

### `PUT /v1.0/test/study/{study_id}/progress-status`

Body: `{"new_status": "<ProgressStatus member name>"}`

Looks up the `StudyModel` by id, validates the name against
`crc.models.study.ProgressStatus`, sets `progress_status`, and commits.
Returns `{"progress_status": "<new value>"}`.

Both raise `ApiError` (`invalid_status`, `workflow_not_found` /
`study_not_found`) on bad input, handled by the same
`connexion_app.add_error_handler(ProblemException, render_errors)` used by
the main API.

## Handlers

`crc/api/test.py` implements the two operations above. It does **not** use
the `Script` mechanism (`crc.scripts.set_workflow_status.SetWorkflowStatus`,
`crc.scripts.set_study_progress_status.SetStudyProgressStatus`) even though
those scripts exist for the equivalent BPMN Script Tasks and share the same
names/purpose. The validate/lookup/set/commit logic is written directly in
the handlers instead, so these HTTP endpoints don't depend on the `Script`
base class or BPMN task context.

## Auth

Neither endpoint currently declares a `security` requirement, so they are
reachable without a JWT. This is intentional for now; JWT auth (matching the
rest of the API) is expected to be added later.