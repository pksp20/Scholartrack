"""Import the bundled synthetic sample dataset into the local SQLite database."""
import csv
from app import BASE_DIR, get_db, init_db

init_db()
with (BASE_DIR / "students_seed.csv").open(newline="", encoding="utf-8") as csv_file:
    records = list(csv.DictReader(csv_file))
with get_db() as conn:
    before = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    conn.executemany(
        "INSERT OR IGNORE INTO students (name, roll_no, class_name, marks, contact) VALUES (?, ?, ?, ?, ?)",
        [(r["name"], r["roll_no"], r["class_name"], float(r["marks"]), r["contact"]) for r in records],
    )
    added = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0] - before
print(f"Imported {added} sample students; {len(records) - added} were already present.")
