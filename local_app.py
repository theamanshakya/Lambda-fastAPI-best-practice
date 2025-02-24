import uvicorn
from src.core.application import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "local_app:app",
        host="localhost",
        port=8000,
        reload=True
    ) 