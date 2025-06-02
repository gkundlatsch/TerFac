
from redis import Redis
from rq import Queue
import os
from sequence_generator2_8 import optimize_terminator

# Connect with a high default for jobs enqueued without explicit timeout
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_conn = Redis.from_url(redis_url)
queue = Queue("default", connection=redis_conn)

def enqueue_optimize(*args, **kwargs):
    """
    Enqueue optimize_terminator with a 1-hour timeout.
    """
    return queue.enqueue(
        optimize_terminator,
        *args,
        **kwargs,
        job_timeout=3600   # allow up to 3600 seconds (1 hour)
    )

