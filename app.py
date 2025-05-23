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
        max_hp = int(max_hp_raw) if max_hp_raw else 48

        thresh_raw = request.form.get("desired_threshold", "").strip()
        desired_threshold = float(thresh_raw) if thresh_raw else 0.2
        
        tol_raw = request.form.get("hairpin_tol", "").strip()
        hairpin_tol = float(tol_raw) if tol_raw else 0.05

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
    # 1) Connect to Redis (same URL you used in tasks.py)
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    redis_conn = Redis.from_url(redis_url)
    q = Queue("default", connection=redis_conn)

    # 2) Fetch the job
    job = q.fetch_job(job_id)
    if job is None:
        return f"Unknown job ID: {job_id}", 404

    # 3) If finished, unpack results and render your results page
    if job.is_finished:
        predicted, features, sequences, logs = job.result
        return render_template(
            "results.html",
            predicted=predicted,
            features=features,
            sequences=sequences,
            logs=logs,
        )

    # 4) Otherwise, show a status page (we’ll create this template next)
    return render_template(
        "status.html",
        job_id=job_id,
        status=job.get_status(),  # e.g. "queued" or "started"
    )

if __name__ == "__main__":
    app.run(debug=True)
