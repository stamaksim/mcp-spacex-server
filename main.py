from fastapi import FastAPI

app = FastAPI(title="MCP SpaceX Server")

@app.get("/tools")
def tools():
    return [
        {"name": "list_launches"},
        {"name": "get_rocket"}
    ]