# Project Structure Documentation

This document describes the project’s directory layout, detailing the purpose of each component and how they interrelate within the application. The structure is organized to separate configuration, documentation, application logic, static resources, and testing, ensuring clear separation of concerns and maintainability.

---

## Root Level

- **config/**  
  Contains configurations for continuous integration, containerization, and environment-specific settings.
  - **docker/**  
    - **Dockerfile**: Instructions to build the Docker container for the application.
    - **entrypoint.sh**: Script executed on container startup.

- **Makefile**  
  A collection of useful commands (such as running tests or building the project) that can be executed from the command line.

- **docs/**  
  Documentation related to the project.
  - **project_structure.md**: This document that explains the project’s organization.
  - **usage.md**: Instructions and guidelines on how to install, run, and use the application.

- **pyproject.toml**  
  Project configuration file that defines dependencies, build system, and other project metadata.

- **pytest.ini**  
  Configuration file for pytest, defining settings for running tests.

- **README.md**  
  The main entry point for project documentation. Provides an overview, installation steps, usage instructions, and other essential details.

- **resources/**  
  Contains static data files that the application may require at runtime.

- **uv.lock**  
  Lock file used by the application to ensure consistent dependency versions.

---

## [APP NAME] Folder

This folder (named after the application) contains the core application logic and is structured into several sub-components to handle different aspects of the application.

- **auth/**  
  Responsible for authentication mechanisms. Examples:
  - **jwt.py**: Logic related to JSON Web Tokens; may also contain code for OAuth if needed.
  - **oauth.py**: Logic related to OAuth authentication.

- **api/**  
  Manages client communication and exposes endpoints.
  - **graphql/** (Optional, may be deleted if GraphQL is not used):  
    Contains GraphQL-related implementation.
    - **resolvers/**: Business logic for resolving GraphQL queries.
      - **user_resolver.py**
      - **restaurant_resolver.py**
    - **schemas/**: Definition of GraphQL schemas.
    - **queries/**: Predefined GraphQL queries.
    - **mutations/**: Predefined GraphQL mutations.
    - **data_loaders/**: Optimizes data-fetching patterns with batching and caching.
  - **api_contracts/**  
    Contains Pydantic models for request validation and response generation, contributing to automatic OpenAPI documentation.
    - **responses/**:  
      - **get_user_response.py**
    - **requests/**:  
      - **save_restaurant_request.py**
  - **routers/**  
    Defines the route handlers for the API endpoints.
    - **user.py**: Endpoint definitions related to user management.
    - **restaurant.py**: Endpoint definitions related to restaurant management.
    
  - **middleware/**: 
    Contains middleware components that can be applied to the API.
    - **auth_middleware.py**: Middleware for handling authentication.
    - **logging_middleware.py**: Middleware for logging requests and responses.
  - **main.py**  
    The entry point of the FastAPI application. It is responsible for starting the server, loading the routes, and initializing middleware.

- **cli/** (Optional)  
  Contains scripts for managing various administrative and operational tasks.
  - **cli.py**: Main script handling command-line operations. Uses Click to define commands and options.  

- **dto/** (Optional)  
  Contains Data Transfer Objects that help in decoupling the data representation from the business logic.

- **infrastructure/**  
  Manages external resources and system integrations. Contains db connection instances for lifecycles in FastAPI.
  - **config.py**: Configuration logic for external resources.
  

- **services/**  
  Implements business logic using a service pattern.
  - **user_service.py**: Service layer for user-related operations.
  - **warmup_service.py**: Service for handling initialization tasks.
  

- **models/**  
  Defines data models that represent domain entities.
  - **comments.py**
  - **foodradar_api.py**
  

- **repositories/**  
  Encapsulates data access logic and the repository pattern.
  - **restaurant_repository.py**: Handles database operations for restaurant data.
  - **user_repository.py**: Handles database operations for user data.
  

- **utils/**  
  Contains helper functions and utilities used across the application.
  - **url_parser.py**: Utility for URL parsing and related logic.
  

  
  Makes the [APP NAME] folder a Python package, ensuring that modules can be imported correctly.

---

## Tests

Testing is organized into two main categories, ensuring separation between unit and integration tests.

- **tests/unit/**  
  Mimics the structure of the [APP NAME] folder to facilitate isolated testing of functions and methods.
  - **api/**  
  - **services/**  
    
- **tests/integration/**  
  Contains tests that evaluate the integration between different components of the application.
  

---

## Summary

- **Configuration & Setup:** Managed via `config/`, `Makefile`, and `pyproject.toml`, ensuring that environment-specific settings and command-line operations are streamlined.
- **Application Logic:** Centralized in the `[APP NAME]` folder, divided into sub-components for API endpoints, authentication, CLI operations, infrastructure management, and business logic.
- **Documentation & Resources:** Detailed in the `docs/` and `resources/` folders to support both developers and operational teams.
- **Testing:** Separated into unit and integration tests for robust quality assurance.

This structure facilitates development scalability and maintainability by enforcing a clear separation of concerns across configuration, application logic, documentation, static assets, and testing.