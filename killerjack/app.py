from flask import Flask, request, render_template, jsonify
import pandas as pd
import joblib
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.getenv("DATA_FILE", os.path.join(BASE_DIR, "data.csv"))
MODEL_DIR = os.getenv("MODEL_DIR", os.path.join(BASE_DIR, "model/saved"))
MODEL_PATH = os.path.join(MODEL_DIR, "stock_predictor.pkl")
PREPROCESSOR_PATH = os.path.join(MODEL_DIR, "preprocessor.pkl")
PORT = int(os.getenv("PORT", "5000"))


def load_pickle(path):
    if os.path.exists(path):
        try:
            return joblib.load(path)
        except Exception:
            return None
    return None


model = load_pickle(MODEL_PATH)
preprocessor = load_pickle(PREPROCESSOR_PATH)


def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["name", "age", "salary", "position", "yoe", "bonus_percent", "investment_expert"])


def save_data(df):
    df.to_csv(DATA_FILE, index=False)


def is_ajax():
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"


def get_table_html():
    df = load_data()
    if df.empty:
        return "<p>No data yet.</p>"
    df = df.copy()
    if "salary" in df.columns:
        df["salary"] = df["salary"].apply(lambda x: f"{x:,.2f}" if pd.notna(x) else "")
    return df.to_html(classes="data-table", index=False, border=0, justify="left")


def make_entry(form):
    return {
        "name": form["name"].strip(),
        "age": int(form["age"]),
        "salary": float(form["salary"]),
        "position": form["position"].strip(),
        "yoe": int(form["yoe"]),
        "bonus_percent": float(form["bonus_percent"]),
        "investment_expert": form["investment_expert"].strip()
    }


@app.route("/")
def home():
    return render_template("index.html", table=get_table_html())


@app.route("/submit", methods=["POST"])
def submit():
    try:
        entry = make_entry(request.form)
    except Exception as exc:
        return get_table_html(), 400

    df = load_data()
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    save_data(df)
    return get_table_html()


@app.route("/analyze", methods=["POST"])
def analyze():
    df = load_data()
    if df.empty:
        return render_template("index.html", error="No data to analyze.", table=get_table_html())

    if model is None or preprocessor is None:
        return render_template(
            "index.html",
            error="Model files are missing or could not be loaded.",
            table=get_table_html(),
        )

    X = preprocessor.transform(df.drop(columns=["name"]))
    preds = model.predict(X)
    inc = int((preds == "increase").sum())
    dec = int((preds == "decrease").sum())
    count = len(preds)
    summary = f"Suggest increasing stock for {inc} out of {count} entries."

    return render_template(
        "index.html",
        prediction=summary,
        inc=inc,
        dec=dec,
        count=count,
        table=get_table_html(),
    )


@app.route("/fetch_person", methods=["POST"])
def fetch_person():
    name_to_fetch = request.form.get("fetch_name", "").strip()
    df = load_data()

    if df.empty:
        return render_template("index.html", error="No data available.", table=get_table_html())

    person = df[df["name"].str.lower() == name_to_fetch.lower()]
    if person.empty:
        return render_template("index.html", error="Person not found.", table=get_table_html())

    person_info = person.iloc[-1].to_dict()
    return render_template("index.html", person_info=person_info, table=get_table_html())


@app.route("/update_person", methods=["POST"])
def update_person():
    name_to_update = request.form.get("update_name", "").strip()
    df = load_data()

    if df.empty:
        return render_template("index.html", error="No data available to update.", table=get_table_html())

    mask = df["name"].str.lower() == name_to_update.lower()
    if not mask.any():
        return render_template("index.html", error="No matching record found.", table=get_table_html())

    updates = {}
    if request.form.get("update_age"):
        updates["age"] = int(request.form["update_age"])
    if request.form.get("update_salary"):
        updates["salary"] = float(request.form["update_salary"])
    if request.form.get("update_position"):
        updates["position"] = request.form["update_position"].strip()
    if request.form.get("update_yoe"):
        updates["yoe"] = int(request.form["update_yoe"])
    if request.form.get("update_bonus_percent"):
        updates["bonus_percent"] = float(request.form["update_bonus_percent"])
    if request.form.get("update_investment_expert"):
        updates["investment_expert"] = request.form["update_investment_expert"].strip()

    for key, value in updates.items():
        df.loc[mask, key] = value

    save_data(df)
    response = {
        "success": True,
        "message": f"Updated {mask.sum()} record(s) for '{name_to_update}'.",
        "table_html": get_table_html(),
    }
    if is_ajax():
        return jsonify(response)

    return render_template(
        "index.html",
        message=response["message"],
        table=response["table_html"],
    )


@app.route("/delete_person", methods=["POST"])
def delete_person():
    name_to_delete = request.form.get("delete_name", "").strip()
    df = load_data()

    if df.empty:
        return render_template("index.html", error="No data available to delete.", table=get_table_html())

    mask = df["name"].str.lower() == name_to_delete.lower()
    if not mask.any():
        return render_template("index.html", error="No matching record found.", table=get_table_html())

    deleted_count = int(mask.sum())
    df = df[~mask]
    save_data(df)
    response = {
        "success": True,
        "message": f"Deleted {deleted_count} record(s) for '{name_to_delete}'.",
        "table_html": get_table_html(),
    }
    if is_ajax():
        return jsonify(response)

    return render_template(
        "index.html",
        message=response["message"],
        table=response["table_html"],
    )


@app.route("/compare", methods=["POST"])
def compare():
    raw_names = request.form.get("compare_names", "")
    names = [name.strip() for name in raw_names.replace(";", ",").split(",") if name.strip()]
    if len(names) < 2:
        parts = raw_names.strip().split()
        if len(parts) >= 2:
            names = [name.strip() for name in parts if name.strip()]

    unique_names = []
    for name in names:
        lower_name = name.lower()
        if lower_name not in [n.lower() for n in unique_names]:
            unique_names.append(name)

    df = load_data()

    if df.empty:
        return jsonify({"success": False, "error": "No data available."})

    if len(unique_names) < 2:
        return jsonify({"success": False, "error": "Please provide at least two different names to compare."})

    selected = []
    missing = []
    for name in unique_names:
        person = df[df["name"].str.lower() == name.lower()]
        if person.empty:
            missing.append(name)
        else:
            p_dict = person.iloc[-1].to_dict()
            p_dict = {k: (None if pd.isna(v) else v) for k, v in p_dict.items()}
            selected.append(p_dict)

    if not selected:
        return jsonify({"success": False, "error": "No matching investors found."})

    chart_data = {
        "labels": [person["name"] for person in selected],
        "metrics": {
            "Age": [person["age"] for person in selected],
            "Salary": [person["salary"] for person in selected],
            "YOE": [person["yoe"] for person in selected],
            "BonusPercent": [person["bonus_percent"] for person in selected]
        },
        "expertise": {
            "yes": sum(1 for person in selected if str(person.get("investment_expert", "")).lower() == "yes"),
            "no": sum(1 for person in selected if str(person.get("investment_expert", "")).lower() == "no")
        },
        "positions": {}
    }

    for person in selected:
        position = person.get("position", "Unknown")
        chart_data["positions"][position] = chart_data["positions"].get(position, 0) + 1

    return jsonify({
        "success": True,
        "selected": selected,
        "chart_data": chart_data,
        "missing": missing,
    })


@app.route("/table")
def table():
    return get_table_html()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=os.getenv("FLASK_DEBUG", "1") == "1")
