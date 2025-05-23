# -*- coding: utf-8 -*-
"""
Created on Fri May 23 18:23:30 2025

@author: Guilherme Kundlatsch
"""

import os
from redis import Redis
from rq import Queue
from sequence_generator2_6 import optimize_terminator

# 1) Read Redis URL from env (default to localhost for dev)
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_conn = Redis.from_url(redis_url)

# 2) Create (or get) the RQ queue named "default"
queue = Queue("default", connection=redis_conn)

def enqueue_optimize(*args, **kwargs):
    """
    Enqueue an optimize_terminator job.
    Returns an RQ Job instance immediately.
    """
    return queue.enqueue(optimize_terminator, *args, **kwargs)
