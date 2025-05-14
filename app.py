from flask import Flask, render_template, request
from sequence_generator2_6 import optimize_terminator

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

        # 3) Run the optimizer (captures all print()s into logs)
        predicted, features, sequences, logs = optimize_terminator(
            target_strength,
            max_hp,
            desired_threshold,
            hairpin_tol,
            seed
        )

        # 4) Render the results page with the log at the top
        return render_template(
            "results.html",
            predicted=predicted,
            features=features,
            sequences=sequences,
            logs=logs
        )

    # GET → show the form
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
