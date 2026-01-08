from fastapi import FastAPI
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Test API")

@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "Test API"}

@app.get("/health")
async def health():
    logger.info("Health endpoint called")
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
