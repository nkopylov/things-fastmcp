# Things FastMCP Development Guide

## Build Commands
- Build package: `python -m build`
- Run linting: `ruff check .`
- Format code: `ruff format .`
- Run tests: `pytest tests`
- Run single test: `pytest tests/test_name.py::test_function`
- Start dev server: `mcp dev things_fast_server.py`
- Start in CLI mode: `python things_fast_server.py`

## Code Style Guidelines
- Type annotations for all function parameters and return values
- Use docstrings with Args/Returns sections (Google style)
- PEP 8 compliant (enforced by ruff)
- Imports order: standard lib, third-party, local imports
- Prefer explicit error handling with try/except blocks
- Naming: snake_case for variables/functions, PascalCase for classes
- Use FastMCP pattern with decorators for tool registration
- Error handling: log errors, provide clear error messages to users
- Keep tool functions focused on a single responsibility