# Cluedogpt Backend

A FastAPI application generated from the company template.

## Features

- FastAPI application with built-in documentation
- Configurable API settings via environment variables
- PostgreSQL integration with Tortoise ORM
- Ruff linting configuration
- CORS middleware
- Project structure based on company standards

## Getting Started

### Prerequisites

- Python 3.12+
- uv (recommended for dependency management)

### Installation

1. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   uv pip install -e .
   ```

### Running the Application

```
python -m cluedogpt_backend.api.main
```

The API will be available at http://localhost:8000.



## Configuration

Create a `.env` file in the root directory with the following variables:

```
API_HOST=0.0.0.0
API_PORT=8000
ENABLE_DOCS=true

POSTGRES_DSN=postgres://postgres:postgres@localhost:5432/cluedogpt_backend


```

## Development

### Running Linting

```
ruff check .
ruff format .
```

### Running Tests

```
pytest
```