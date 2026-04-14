import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from celery.result import AsyncResult

from app.celery_app import celery
from app.tasks import compute_sum_parallel
from app.models import JobRequest

logger = logging.getLogger(__name__)

app = FastAPI(title="Mini App - FastAPI + Celery")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/jobs")
def start_job(payload: JobRequest):
    if payload.number < 0:
        raise HTTPException(status_code=400, detail="Number must be non-negative")

    logger.info(f"Creating parallel job for number={payload.number}")

    task = compute_sum_parallel(payload.number)

    return {
        "job_id": task.id,
        "status": "PENDING",
        "message": "Parallel job created successfully",
    }


@app.get("/jobs/{job_id}")
def get_job_status(job_id: str):
    logger.info(f"Checking job status for job_id={job_id}")

    result = AsyncResult(job_id, app=celery)

    response = {
        "job_id": job_id,
        "status": result.status,
    }

    if result.status == "PENDING":
        response["message"] = "Job is waiting to be processed"

    elif result.status == "STARTED":
        response["message"] = "Job has started"

    elif result.status == "PROGRESS":
        response["message"] = "Job is in progress"
        response["progress"] = result.info

    elif result.status == "SUCCESS":
        response["message"] = "Job completed successfully"
        response["result"] = result.result

    elif result.status == "FAILURE":
        response["message"] = "Job failed"
        response["error"] = str(result.result)

    else:
        response["message"] = f"Job is in {result.status} state"

    return response