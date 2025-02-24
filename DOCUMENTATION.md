# FastAPI Snowflake Lambda Architecture

This project demonstrates a production-ready architecture for building APIs that can run both locally using FastAPI and on AWS Lambda with Snowflake database integration.

-- Project Structure

```
project/
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── application.py    # Application factory
│   │   ├── exceptions.py     # Custom exceptions
│   │   └── middleware.py     # Request middleware
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection pool
│   ├── models/             # Database models
│   ├── repositories/       # Database operations
│   │   └── user_repository.py
│   ├── routes/            # API endpoints
│   │   └── user_routes.py
│   ├── services/          # Business logic
│   │   └── user_service.py
│   └── schemas/           # Pydantic models
│       └── user_schema.py
├── lambda_handler.py      # AWS Lambda handler
├── local_app.py          # Local FastAPI application
├── requirements.txt      # Dependencies
└── README.md
```

-- Architecture Overview

The application follows a clean architecture pattern with the following layers:

1. **Presentation Layer** (routes/)
   - Handles HTTP requests/responses
   - Input validation
   - Route definitions

2. **Service Layer** (services/)
   - Business logic
   - Orchestration
   - Error handling

3. **Repository Layer** (repositories/)
   - Database operations
   - Data access patterns
   - Query handling

4. **Core Layer** (core/)
   - Application configuration
   - Middleware
   - Exception handling
   - Common utilities

-- Setup and Installation

-- 1. Local Development Environment

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:
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

-- 2. Database Setup

1. Create the required table in Snowflake:
```sql
CREATE TABLE users (
    id INTEGER AUTOINCREMENT,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);
```

-- Key Features

-- 1. Connection Pooling
- Efficient database connection management
- Configurable pool size
- Automatic connection cleanup

-- 2. Error Handling
- Custom exception classes
- Structured error responses
- Detailed error tracking

-- 3. Request Middleware
- Request ID tracking
- Performance monitoring
- Request/Response logging

-- 4. Environment-based Configuration
- Development/Staging/Production environments
- Environment-specific settings
- Cached configuration loading

-- Local Development

1. Run the FastAPI application:
```bash
python local_app.py
```

2. Access the API:
- API endpoints: `http://localhost:8000/api/v1/`
- Swagger documentation: `http://localhost:8000/docs` (disabled in production)
- ReDoc documentation: `http://localhost:8000/redoc` (disabled in production)

-- AWS Deployment

-- 1. Prepare Deployment Package

1. Create a deployment package:
```bash
pip install --target ./package -r requirements.txt
cd package
zip -r ../lambda_deployment.zip .
cd ..
zip -g lambda_deployment.zip lambda_handler.py
zip -gr lambda_deployment.zip src/
```

-- 2. AWS Lambda Setup

1. Create a new Lambda function:
   - Runtime: Python 3.9+
   - Handler: `lambda_handler.handler`
   - Memory: 256MB (minimum recommended)
   - Timeout: 30 seconds

2. Environment Variables:
   - Set all configuration variables from `.env`
   - Use AWS Secrets Manager for sensitive data
   - Set `ENVIRONMENT=production`

-- 3. API Gateway Setup

1. Create a new REST API
2. Configure proxy integration
3. Set up CORS if needed
4. Deploy to desired stage

-- Best Practices

-- 1. Error Handling
```python
try:
    result = await service.process()
except CustomHTTPException as e:
    # Already formatted for API response
    raise e
except Exception as e:
    # Unexpected errors
    raise CustomHTTPException(
        status_code=500,
        detail="Internal server error",
        error_code="INTERNAL_ERROR",
        extra={"original_error": str(e)}
    )
```

-- 2. Database Operations
```python
async with DatabasePool.get_connection() as conn:
    try:
        cursor = conn.cursor()
        await cursor.execute("SELECT * FROM users")
        return await cursor.fetchall()
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise
```

-- 3. Middleware Usage
```python
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

-- Monitoring and Maintenance

1. **CloudWatch Metrics**
   - Lambda execution duration
   - Database connection pool usage
   - API response times
   - Error rates

2. **Logging**
   - Request/Response logging
   - Error tracking
   - Performance monitoring

3. **Health Checks**
   - Database connectivity
   - External service status
   - Application health endpoints

-- Security Considerations

1. **API Security**
   - API Gateway authorization
   - Request validation
   - Rate limiting

2. **Database Security**
   - Connection pooling
   - Prepared statements
   - Minimal privilege access

3. **Environment Security**
   - Secrets management
   - Environment isolation
   - Access control
