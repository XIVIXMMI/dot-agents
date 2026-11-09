## Stack: Python
- Lint / format: `ruff check .` / `ruff format .`
- Test, all: `pytest -q`
- Test, one: `pytest -q path/to/test_file.py::test_name`; by requirement: `pytest -q -k AUTH_3`
- JUnit XML (for the RTM): `pytest -q --junitxml=.agents/logs/junit/pytest.xml`. RTM glob: `.agents/logs/junit/*.xml`
- Requirement IDs go in the test function name: `def test_AUTH_3_rejects_empty_title():`
