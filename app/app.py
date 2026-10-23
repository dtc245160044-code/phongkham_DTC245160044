import os
import psycopg2
import psycopg2.extras
from flask import Flask, request, redirect, render_template, abort

app = Flask(__name__)
STATUSES = ["pending", "confirmed", "done", "cancelled"]

DELETE_SQL = {
    "patients": "DELETE FROM patients WHERE id = %s",
    "doctors": "DELETE FROM doctors WHERE id = %s",
    "appointments": "DELETE FROM appointments WHERE id = %s",
}


def run(sql, params=(), fetch=False):
    """Chạy 1 câu SQL. Dữ liệu luôn đi qua params (%s) để chống SQL Injection."""
    conn = psycopg2.connect(
        host=os.environ["DB_HOST"], port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ["DB_NAME"], user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )
    try:
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(sql, params)
                return cur.fetchall() if fetch else None
    finally:
        conn.close()


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/health")
def health():
    run("SELECT 1", fetch=True)
    return {"status": "ok"}


@app.route("/patients", methods=["GET", "POST"])
def patients():
    if request.method == "POST":
        f = request.form
        run("INSERT INTO patients(full_name, birth_date, gender, phone, address) VALUES (%s,%s,%s,%s,%s)",
            (f["full_name"], f.get("birth_date") or None, f.get("gender"), f.get("phone"), f.get("address")))
        return redirect("/patients")
    rows = run("SELECT * FROM patients ORDER BY id", fetch=True)
    return render_template("patients.html", rows=rows)


@app.route("/doctors", methods=["GET", "POST"])
def doctors():
    if request.method == "POST":
        f = request.form
        run("INSERT INTO doctors(full_name, specialty, phone) VALUES (%s,%s,%s)",
            (f["full_name"], f["specialty"], f.get("phone")))
        return redirect("/doctors")
    rows = run("SELECT * FROM doctors ORDER BY id", fetch=True)
    return render_template("doctors.html", rows=rows)


@app.route("/appointments", methods=["GET", "POST"])
def appointments():
    if request.method == "POST":
        f = request.form
        run("INSERT INTO appointments(patient_id, doctor_id, appointment_time, reason) VALUES (%s,%s,%s,%s)",
            (f["patient_id"], f["doctor_id"], f["appointment_time"], f.get("reason")))
        return redirect("/appointments")
    rows = run("""SELECT a.id, p.full_name AS patient, d.full_name AS doctor,
                         a.appointment_time, a.reason, a.status
                  FROM appointments a
                  JOIN patients p ON p.id = a.patient_id
                  JOIN doctors  d ON d.id = a.doctor_id
                  ORDER BY a.appointment_time""", fetch=True)
    return render_template(
        "appointments.html", rows=rows, statuses=STATUSES,
        patients=run("SELECT id, full_name FROM patients ORDER BY full_name", fetch=True),
        doctors=run("SELECT id, full_name FROM doctors ORDER BY full_name", fetch=True))


@app.post("/appointments/<int:rid>/status")
def set_status(rid):
    status = request.form["status"]
    if status not in STATUSES:
        abort(400)
    run("UPDATE appointments SET status = %s WHERE id = %s", (status, rid))
    return redirect("/appointments")


@app.post("/<table>/<int:rid>/delete")
def delete(table, rid):
    if table not in DELETE_SQL:
        abort(404)
    run(DELETE_SQL[table], (rid,))
    return redirect("/" + table)
