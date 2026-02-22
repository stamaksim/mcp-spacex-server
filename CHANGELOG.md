# Changelog

All notable changes to the MCP SpaceX Server project.

---

## [0.1.0] - 2026-02-22

**Initial Release** 🚀

### Added
- Project structure with `uv` package manager
- FastAPI server with proper lifecycle management
- SpaceXClient for async communication with SpaceX API v4
- Tool Registry for centralized tool management
- Three launch-related tools:
  - `list_launches` - Get all SpaceX launches
  - `get_latest_launch` - Get the most recent launch
  - `get_launch_by_id` - Get specific launch by ID
- MCP-compliant tool manifests with parameter schemas
- REST API endpoints:
  - `GET /` - Server status check
  - `GET /health` - Health check endpoint
  - `GET /tools` - List available tools
  - `GET /tools/manifests` - Get all tool descriptions
  - `GET /tools/{tool_name}/manifest` - Get specific tool manifest
  - `POST /execute` - Execute tools with arguments
- Pydantic schemas for type-safe validation
- Comprehensive error handling
- API documentation with Swagger UI (`/docs`)
- Full code documentation (docstrings)

### Technical Features
- Fully async architecture (async/await)
- Type-safe with Pydantic models
- Modular design (easy to extend)
- Separation of concerns (client, tools, registry, API)
- Connection pooling with shared HTTP client
- MCP protocol compliance

### Dependencies
- Python 3.12+
- FastAPI - Modern web framework
- httpx - Async HTTP client
- Pydantic - Data validation
- uvicorn - ASGI server
- ruff - Linter and formatter

---

## Future Plans

### Upcoming Tools
- [ ] `list_rockets` - List all SpaceX rockets
- [ ] `get_rocket_by_id` - Get rocket information by ID
- [ ] Launchpad tools

### Improvements
- [ ] Unit tests
- [ ] Integration tests
- [ ] Docker support
- [ ] Caching layer
- [ ] Rate limiting

---

_University project demonstrating MCP server architecture with modern Python practices._