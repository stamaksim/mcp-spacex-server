## 1. Project Overview

This project is an MCP (Model Context Protocol) SpaceX Server that exposes a set of tools for retrieving SpaceX data such as launches and rockets using a clean and modular architecture.  
The system is designed for educational purposes to demonstrate API integration, clean separation of concerns, and structured tool-based business logic using FastAPI and Pydantic.

---

## 2. Goals & Objectives

- **Core Goal:**  
  Build a server that provides MCP tools for accessing SpaceX public API data in a clean and maintainable way.

- **Secondary Goals:**  
  - Implement a SpaceX API client using a single shared asynchronous HTTP client.  
  - Define clear Pydantic schemas for tool input and output validation.  
  - Document architecture and design decisions.  
  - Ensure the project structure is reproducible for team collaboration.

---

## 3. The User Journey

- **The Experience:**  
  Users interact with the MCP server by calling tools that retrieve SpaceX information. Each tool processes the request, communicates with the SpaceX API, and returns structured, validated responses.

- **Inputs:**  
  Tool arguments passed as JSON dictionaries.

- **Outputs:**  
  Structured responses using Pydantic schemas such as `LaunchResponse` and `RocketResponse`.

---

## 4. Program Logic (Step-by-Step)

1. **Initialization:**  
   The FastAPI application starts and creates a shared `AsyncClient` instance for the SpaceXClient.

2. **Input Phase:**  
   A user invokes an MCP tool with input arguments.

3. **Processing Phase:**  
   The tool calls the SpaceXClient to fetch data from the SpaceX public API and applies the required business logic.

4. **Output Phase:**  
   The tool returns validated Pydantic response objects.

5. **Loop/Cleanup:**  
   The server continues handling requests until shutdown, where the HTTP client is properly closed.

---

## 5. Team Responsibility Breakdown

- **Member 1:** SpaceXClient implementation and infrastructure layer.  
- **Member 2:** MCP tools implementation (launch and rocket tools).  
- **Member 3:** Pydantic schemas and ToolRegistry.  
- **Member 4:** Testing, cleanup, and documentation (README, DESIGN.md, CHANGELOG.md).

---

## 6. Module & Function Breakdown

- **`src/main.py`** – FastAPI entry point and application lifecycle management.  
- **`src/infrastructure/spacex/client.py`** – SpaceXClient responsible for communication with the SpaceX public API only.  
- **`src/tools/launch_tool.py`** – Tool for listing SpaceX launches.  
- **`src/tools/latest_launch_tool.py`** – Tool for retrieving the most recent SpaceX launch.  
- **`src/tools/rocket_list_tool.py`** – Tool for listing SpaceX rockets.  
- **`src/tools/registry.py`** – ToolRegistry that maintains the final list of MCP tools.  
- **`src/schemas/tools/`** – Pydantic input and output schemas for all tools.

---

## 7. Data Storage & Structures

- **Variables/Collections:**  
  Lists and dictionaries are used to store and process SpaceX data retrieved from the API.

- **Persistence:**  
  No local database is used. Data is retrieved live from the SpaceX public API.

---

## 8. Development Timeline (Milestones)

1. **Milestone 1:**  
   Project structure and base architecture setup completed.

2. **Milestone 2:**  
   SpaceXClient and MCP tools implemented with validated schemas.

3. **Milestone 3:**  
   Final testing, cleanup, and documentation completed.

---

## MCP Tools List

The MCP SpaceX Server exposes the following tools:

- **`list_launches`** – Returns a list of SpaceX launches.  
- **`get_latest_launch`** – Returns the most recent SpaceX launch.  
- **`list_rockets`** – Returns a list of SpaceX rockets.

Each tool:
- Uses the SpaceXClient for external API calls.  
- Has Pydantic input and output schemas.  
- Contains only business logic.  
- Is independent from FastAPI routes.

---

## Project Structure
src/
main.py
infrastructure/
spacex/
client.py
tools/
launch_tool.py
latest_launch_tool.py
rocket_list_tool.py
registry.py
schemas/
tools/
docs/
images/
architecture.png
README.md
DESIGN.md
CHANGELOG.md
pyproject.toml
uv.lock
.gitignore

---

## Architecture

![Architecture Diagram](docs/images/architecture.png)

The system follows a layered architecture:

- **API Layer:** FastAPI routes  
- **Tool Layer:** MCP tools containing business logic  
- **Infrastructure Layer:** SpaceXClient for external API communication  

Dependencies flow downward only: API → Tools → Infrastructure.

---

## Team Checklist

- **Consistency:** All code uses `snake_case` naming conventions.  
- **Communication:** Discord / Teams / WhatsApp.  
- **Integration:** All tools are tested together through the ToolRegistry.  
- **Testing:** Manual testing for valid and invalid inputs.  
- **Documentation:** README.md, DESIGN.md, and CHANGELOG.md are up to date.

---

## How to Run the Project

1. Install dependencies:

2. Run the server:

3. Access the API and test MCP tools.

---

## Future Improvements

- Add more MCP tools (payloads, missions, crew data).  
- Add caching and retry logic for API requests.  
- Improve error handling and logging.  
- Add automated tests.

---

## License

This project is developed as a university group project for learning and educational purposes.