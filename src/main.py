import uvicorn
from fastapi import FastAPI
from src.api.routes import router as api_app
from src.api.webhook_routes import router as webhook_router  # Import the webhook router

app = FastAPI()

# Include existing routes from `api/routes.py`
app.include_router(api_app)

# Include the webhook route
app.include_router(webhook_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
