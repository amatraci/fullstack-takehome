import logging
import math
import time

from celery import chord

from app.celery_app import celery

logger = logging.getLogger(__name__)


@celery.task(bind=True)
def sum_range(self, start: int, end: int):
    logger.info(f"Processing chunk from {start} to {end}")

    partial_sum = 0

    for i in range(start, end + 1):
        partial_sum += i
        time.sleep(0.1)

    return {
        "start": start,
        "end": end,
        "partial_sum": partial_sum,
    }


@celery.task
def aggregate_results(results: list, original_input: int, started_at: float = None):
    logger.info(f"Aggregating {len(results)} chunk results for input={original_input}")

    total = sum(item["partial_sum"] for item in results)
    duration = round(time.time() - started_at, 2) if started_at else None

    return {
        "input": original_input,
        "result": total,
        "chunks": results,
        "chunk_count": len(results),
        "duration": duration,
        "message": f"Completed parallel sum from 1 to {original_input}",
    }


def build_chunks(n: int, num_chunks: int = 4):
    if n <= 0:
        return []

    chunk_size = max(1, math.ceil(n / num_chunks))
    chunks = []

    start = 1
    while start <= n:
        end = min(start + chunk_size - 1, n)
        chunks.append((start, end))
        start = end + 1

    return chunks


def compute_sum_parallel(n: int):
    if n < 0:
        raise ValueError("Number must be non-negative")

    if n == 0:
        started_at = time.time()
        return aggregate_results.delay([], 0, started_at)

    chunks = build_chunks(n, num_chunks=4)
    logger.info(f"Created {len(chunks)} chunks for input={n}: {chunks}")

    header = [sum_range.s(start, end) for start, end in chunks]
    started_at = time.time()
    callback = aggregate_results.s(n, started_at)

    workflow = chord(header)(callback)
    return workflow