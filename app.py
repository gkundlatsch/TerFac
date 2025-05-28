from flask import Flask, render_template, request, redirect, url_for
from tasks import enqueue_optimize
from redis import Redis
from rq import Queue
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # 1) Read required field
        target_strength = float(request.form["target_strength"])

        # 2) Read optional advanced fields (with defaults)
        max_hp_raw = request.form.get("max_hp", "").strip()
        max_hp = int(max_hp_raw) if max_hp_raw else 24

        thresh_raw = request.form.get("desired_threshold", "").strip()
        desired_threshold = float(thresh_raw) if thresh_raw else 1
        
        tol_raw = request.form.get("hairpin_tol", "").strip()
        hairpin_tol = float(tol_raw) if tol_raw else 0.1

        seed_raw = request.form.get("seed", "").strip()
        seed = int(seed_raw) if seed_raw else 1

        # 3) Enqueue the optimize_terminator job
        job = enqueue_optimize(
            target_strength,
            max_hp,
            desired_threshold,
            hairpin_tol,
            seed
        )

        # 4) Immediately redirect to a status page to poll for completion
        return redirect(url_for("job_status", job_id=job.get_id()))

    # GET → show the form
    return render_template("index.html")

@app.route("/status/<job_id>")
def job_status(job_id):
    # 1) Connect to Redis
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    redis_conn = Redis.from_url(redis_url)
    q = Queue("default", connection=redis_conn)

    # 2) Fetch the job
    job = q.fetch_job(job_id)
    if job is None:
        return f"Unknown job ID: {job_id}", 404

    # 3) Always load live logs from metadata (may be empty)
    logs = job.meta.get("logs", [])

    # 4) If finished, unpack the *result* logs instead
    if job.is_finished:
        predicted, features, sequences, result_logs = job.result
        return render_template(
            "results.html",
            predicted=predicted,
            features=features,
            sequences=sequences,
            logs=result_logs,   # use the logs returned with result
        )

    # 5) Otherwise, we’re still queued or running
    status = job.get_status()  # "queued" or "started"
    position = None
    if status == "queued":
        # compute position in queue
        waiting_ids = q.job_ids
        if job_id in waiting_ids:
            position = waiting_ids.index(job_id) + 1

    # 6) Render the status page with the live logs
    return render_template(
        "status.html",
        job_id=job_id,
        status=status,
        position=position,
        logs=logs,  
    )

    
@app.route("/cancel/<job_id>")
def cancel_job(job_id):
    """Remove a pending job from the queue, then send the user back home."""
    # 1) Connect to Redis
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    conn = Redis.from_url(redis_url)
    q = Queue("default", connection=conn)

    # 2) Fetch and delete the job if it’s still queued
    job = q.fetch_job(job_id)
    if job and job.get_status() == "queued":
        job.cancel()  # unschedule if it was scheduled
        job.delete()  # remove it from Redis entirely

    # 3) Redirect back to the home page
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
