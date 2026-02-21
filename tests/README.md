# Tests

Lightweight smoke tests for the claude-skills repository.

## Scope

These are not full unit test suites. They verify:

- **test_imports.py** - All Python scripts parse without syntax errors (no actual imports, so no dependency issues)
- **test_notify.py** - Core notification functions work correctly (Pushover API is mocked)
- **test_notion_api.py** - Notion API client initializes and builds requests correctly (API calls are mocked)

## Running

```bash
cd ~/claude-skills
pytest tests/
```

Or with verbose output:

```bash
pytest tests/ -v
```

## Dependencies

- `pytest` (installed by `setup.sh`)
