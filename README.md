# FastAPI Snowflake Lambda Architecture

A production-ready FastAPI application that can run both locally and on AWS Lambda with Snowflake database integration.

## Project Structure

```
project/
├── src/
│   ├── modules/                # Feature modules
│   │   ├── users/             # User module
│   │   │   ├── controller.py  # API routes
│   │   │   ├── model.py      # Database models
│   │   │   ├── schema.py     # Pydantic schemas
│   │   │   ├── service.py    # Business logic
│   │   │   ├── repository.py # Database operations
│   │   │   └── queries.py    # SQL queries
│   │   └── auth/             # Auth module (similar structure)
│   ├── core/
│   │   ├── application.py    # App factory
│   │   ├── exceptions.py     # Custom exceptions
│   │   └── middleware.py     # Middleware
│   ├── utils/
│   │   ├── logger.py         # Logging utilities
│   │   └── validators.py     # Validation utilities
│   ├── config.py             # Configuration
│   └── database.py           # Database connection
├── lambda_handler.py         # AWS Lambda handler
├── local_app.py             # Local FastAPI application
└── requirements.txt         # Dependencies
```

## Features

- **Modular Architecture**: Clean separation of concerns with feature modules
- **Type Safety**: Full type hinting with Pydantic models
- **Database Integration**: Snowflake connection pooling and query management
- **Error Handling**: Centralized error handling with custom exceptions
- **Logging**: Structured JSON logging with request tracking
- **Validation**: Custom validators for data integrity
- **Documentation**: Auto-generated OpenAPI documentation

## Quick Start

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```plaintext
ENVIRONMENT=development
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
SNOWFLAKE_WAREHOUSE=your_warehouse
DB_POOL_MIN_CONNECTIONS=1
DB_POOL_MAX_CONNECTIONS=10
```

4. Run locally:
```bash
python local_app.py
```

## API Endpoints

### Users Module

```bash
# Create user
POST /api/v1/users/
{
    "email": "user@example.com",
    "name": "Test User"
}

# Get user by ID
GET /api/v1/users/{user_id}

# List users
GET /api/v1/users/?skip=0&limit=10
```

## Module Structure

Each feature module follows a consistent structure:

### 1. Controller (controller.py)
- API route definitions
- Request/Response handling
- Input validation
- Dependency injection

### 2. Model (model.py)
- Database model definitions
- Data structure definitions
- Type hints

### 3. Schema (schema.py)
- Pydantic models for request/response
- Data validation
- Type conversion

### 4. Service (service.py)
- Business logic
- Error handling
- Data processing

### 5. Repository (repository.py)
- Database operations
- Query execution
- Data mapping

### 6. Queries (queries.py)
- SQL query definitions
- Query parameters
- Database operations

## Development

### Adding a New Module

1. Create a new module directory:
```bash
mkdir src/modules/new_module
```

2. Create module files:
```bash
touch src/modules/new_module/{__init__,controller,model,schema,service,repository,queries}.py
```

3. Register routes in application.py:
```python
from src.modules.new_module.controller import router as new_module_router
app.include_router(new_module_router, prefix="/api/v1/new-module")
```

### Testing

Run tests with pytest:
```bash
pytest tests/
```

## Deployment

### AWS Lambda

1. Create deployment package:
```bash
pip install --target ./package -r requirements.txt
cd package
zip -r ../lambda_deployment.zip .
cd ..
zip -g lambda_deployment.zip lambda_handler.py
zip -gr lambda_deployment.zip src/
```

2. Configure Lambda:
- Runtime: Python 3.9+
- Handler: lambda_handler.handler
- Memory: 256MB (minimum)
- Timeout: 30 seconds

3. Set up API Gateway:
- Create REST API
- Configure proxy integration
- Deploy to stage

## Best Practices

- Use dependency injection for services
- Implement proper error handling
- Add logging for debugging
- Use type hints everywhere
- Keep modules independent
- Follow SOLID principles

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit a pull request

## License

MIT
