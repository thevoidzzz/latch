# Latch

Operations agent with a human latch. It can read a manual and query a warehouse, draft the next step, and it does not commit that step until a person approves the same run.

## Evaluation

`python -m latch` scores the stand-in on the fixed set. It exits with an error when `unapproved_actions` is not 0, and then it names the task id.

```
assistant: stand-in
tasks: 5
trajectory_pass_rate: 0.667
unapproved_actions: 0
completed_tasks: 3
cost_per_completed_task: 2.000
```

## Tests

GitHub Actions runs `pytest` on pull requests and on pushes to `main`. The job installs no model client and uses no API key.

```bash
pip install -e ".[dev]"
pytest
```

## Image

The image runs the same suite and uses no API key. Compose publishes port 8000 and does not publish a database.

```bash
docker compose run --rm --build tests
```

## Try it

Create a codespace on the 2-core machine. It uses the default image and installs the package. Delete the codespace when you finish.

```bash
python -m latch
python -m latch.api
```

`python -m latch` prints the report above. With the API running, copy the `id` into the second request from another terminal:

```bash
curl -s -X POST localhost:8000/v1/runs \
  -H 'content-type: application/json' \
  -d '{"question":"Where is the handoff logged?","role":"operator"}'
curl -s -X POST localhost:8000/v1/runs/ID/approval \
  -H 'content-type: application/json' \
  -d '{"approved":true}'
```

The first body has `"status": "waiting"`. The second, after a yes, has `"status": "committed"`.

## Contributing

Open a pull request against `main`. The `test` check has to pass before merge.

Architecture and decisions live in `docs/architecture/` and `docs/adr/`.
