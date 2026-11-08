# Latch

Operations agent with a human latch. It can read a manual and query a warehouse, draft the next step, and it does not commit that step until a person approves the same run.

## Tests

GitHub Actions runs `pytest` on pull requests and on pushes to `main`. The job installs no model client and uses no API key.

```bash
pip install -e ".[dev]"
pytest
```

## Contributing

Open a pull request against `main`. The `test` check has to pass before merge.

Architecture and decisions live in `docs/architecture/` and `docs/adr/`.
