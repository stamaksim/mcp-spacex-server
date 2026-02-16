## Setup (uv)

### 1) Install uv (one-time)

**Linux / macOS**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh


Windows (PowerShell)

irm https://astral.sh/uv/install.ps1 | iex

Verify:

uv --version

2) Install dependencies

From the project root:

uv sync

Run the server
uv run uvicorn main:app --reload


Open:

http://127.0.0.1:8000/

http://127.0.0.1:8000/docs


---
## Important

1) **`pyproject.toml` + `uv.lock` — should do via commit**  
2) If somone add dependencies  — only through:
```bash
uv add <package>


After git pull every one execute:

uv sync