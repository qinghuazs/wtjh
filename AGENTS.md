# Repository Guidelines

## 对话和思考时使用中文
## python 命令不可用，如果你后续运行脚本请用 python3
## Project Structure & Module Organization

- `__init__.py`: ComfyUI entry point that exposes node mappings.
- `config.py`: Base URL and timeout configuration, backed by environment variables.
- `api/`: HTTP client wrapper for the WYJH API.
- `nodes/`: ComfyUI node implementations, grouped by model type:
  - `session.py` (chat), `text2img.py`, `img2img.py`, `video.py`
- `utils/`: Error types, HTTP helpers, and image conversion placeholders.
- `requirements.txt`: Python dependencies for the client runtime.
- `README.md`: Project overview and setup notes.

## Build, Test, and Development Commands

This repo is a lightweight Python plugin; there is no build step.

Common commands:

- `python -m pip install -r requirements.txt` — install runtime dependencies.
- `python -m pip install -e .` — optional editable install if you want to import locally.

If you add tests later, document the exact command here.

## Coding Style & Naming Conventions

- Language: Python 3.
- Indentation: 4 spaces; keep lines reasonably short (≈100 chars).
- Naming:
  - Classes: `PascalCase` (e.g., `WyjhText2Image`)
  - Functions/variables: `snake_case`
  - ComfyUI node keys: human-readable strings in `NODE_CLASS_MAPPINGS`.
- Prefer explicit, small helpers in `utils/` and keep node classes thin.

## Testing Guidelines

There are currently no tests or test framework configured. If you introduce tests:

- Place them under a `tests/` directory.
- Use `pytest` naming (`test_*.py`, `Test*` classes).
- Add the test command to the section above.

## Commit & Pull Request Guidelines

There is no established commit message convention in this repository yet. Use clear,
imperative messages (e.g., "Add text2img endpoint call").

For pull requests:

- Provide a short summary and list any API changes.
- Link related issues if applicable.
- Include screenshots only if you modify UI or node metadata.

## Configuration Tips

- `WYJH_BASE_URL` overrides the default API base URL.
- `WYJH_TIMEOUT` sets the request timeout (seconds).

Keep secrets out of source control; use environment variables for tokens or keys.
