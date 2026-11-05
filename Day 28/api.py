
import os

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

from graph import run_workflow
from knowledge_base import load_articles
from logging_config import setup_logging, get_logger


# Initialize logging and load environment configuration
setup_logging()
logger = get_logger(__name__)

APP_NAME = os.getenv("APP_NAME", "ShopEase Customer Support API")
APP_ENV = os.getenv("APP_ENV", "development")


app = FastAPI(
    title=APP_NAME,
    description="AI-powered customer support using LangGraph",
    version="1.0.0"
)


# Request model
class ChatRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Customer support question"
    )

    @field_validator("query")
    @classmethod
    def validate_query(cls, value):
        if not value.strip():
            raise ValueError(
                "Query cannot be empty or contain only whitespace."
            )

        return value.strip()


# Response model
class ChatResponse(BaseModel):
    answer: str
    status: str
    revision_count: int


# Home endpoint
@app.get("/")
def home():
    logger.info("Home endpoint accessed")

    return {
        "message": f"Welcome to {APP_NAME}",
        "status": "running"
    }


# Liveness check
@app.get("/health")
def health_check():
    logger.info("Liveness check requested")

    return {
        "status": "healthy",
        "service": APP_NAME,
        "environment": APP_ENV
    }


# Readiness check
@app.get("/ready")
def readiness_check():
    logger.info("Readiness check requested")

    try:
        articles = load_articles()

        if not articles:
            raise ValueError("Knowledge base contains no articles.")

        logger.info(
            "Readiness check passed: %d articles available",
            len(articles)
        )

        return {
            "status": "ready",
            "knowledge_base": "available",
            "article_count": len(articles)
        }

    except Exception:
        logger.exception("Readiness check failed")

        raise HTTPException(
            status_code=503,
            detail="Service is not ready. Knowledge base is unavailable."
        )


# Customer support endpoint
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    logger.info("Customer support request received")

    try:
        result = run_workflow(request.query)

        if result["status"] != "completed":
            logger.error(
                "Customer support workflow did not complete"
            )

            raise HTTPException(
                status_code=500,
                detail="Unable to process the customer query."
            )

        logger.info(
            "Customer support request completed successfully"
        )

        return ChatResponse(
            answer=result["answer"],
            status=result["status"],
            revision_count=result["revision_count"]
        )

    except ValueError as error:
        logger.warning("Invalid workflow input: %s", error)

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except HTTPException:
        raise

    except Exception:
        logger.exception(
            "Unexpected error while processing customer request"
        )

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred."
        )


# Run the application using environment configuration
if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))

    logger.info(
        "Starting %s in %s mode",
        APP_NAME,
        APP_ENV
    )

    uvicorn.run(
        "api:app",
        host=host,
        port=port,
        reload=APP_ENV.lower() == "development"
    )
