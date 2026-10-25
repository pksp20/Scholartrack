# ScholarTrack Student Management System

**ScholarTrack** is a mini project web application for managing student records. It uses **Python Flask** for the web server, **SQLite** for data storage, and **HTML/CSS** for the interface.

## Features

- Add, view, search, edit, and delete student records
- Search by student name, roll number, or class
- Show total students and average marks
- Validate required fields, unique roll numbers, contact numbers, and marks from 0 to 100
- Create the SQLite database automatically when the app starts

## Requirements

- Windows 10 or 11
- Python 3.9 or newer
- Internet connection for the first Flask installation

## Run the app on Windows

1. Download or clone this project and extract it if it is a ZIP file.
2. In File Explorer, open the `student-management-system` folder. It must contain `app.py` and `requirements.txt`.
3. Click the File Explorer address bar, type `powershell`, and press Enter. PowerShell will open in the project folder.
4. Create a virtual environment:

   ```powershell
   py -m venv .venv
   ```

5. Install Flask into that environment:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

6. Start the application:

   ```powershell
   .\.venv\Scripts\python.exe app.py
   ```

7. Open <http://127.0.0.1:5000> in a web browser. Keep the PowerShell window open while using the app. Press **Ctrl+C** in that window to stop it.

These instructions call the virtual environment's Python directly, so you do not need to run `Activate.ps1`.

### If PowerShell opens in the wrong folder

Use `Set-Location` with the path to the extracted project folder. For example:

```powershell
Set-Location "C:\path\to\student-management-system"
Get-ChildItem
```

Confirm the file list includes `app.py` and `requirements.txt` before continuing with the setup commands above. Replace the example path with the location where you extracted the project.

### If `py` is not recognized

Use `python` instead. For example:

```powershell
python -m venv .venv
```

Then continue with the `.venv\Scripts\python.exe` commands.

## Database

The app uses SQLite. On first start, it creates `students.db` in the project folder, including a `students` table. The database file is local runtime data and is excluded from Git by `.gitignore`; each person running the project gets their own database.

## Load the sample dataset

`students_seed.csv` contains 200 synthetic student records with placeholder contact numbers. To load them into the local SQLite database, run this from the project folder:

```powershell
.\.venv\Scripts\python.exe seed_students.py
```

The import is safe to repeat: rows with roll numbers already in the database are skipped. The app creates the database automatically if it does not exist.

## Project files

```text
student-management-system/
├── app.py                 # Flask routes, validation, and database operations
├── requirements.txt       # Python dependencies
├── PROJECT_REPORT.md      # Mini project report template
├── README.md              # Setup and project guide
├── static/
│   └── style.css          # Interface styling
└── templates/
    ├── form.html          # Add and edit student form
    └── index.html         # Student list and search page
```

## Main routes

| URL | Purpose |
|---|---|
| `/` | View and search student records |
| `/students/new` | Add a student |
| `/students/<id>/edit` | Edit a student |
| `/students/<id>/delete` | Delete a student using a POST request |
| `/health` | Return a basic application health response |

## Deploy to Render

This project includes `render.yaml` for a Render web service. To deploy it:

1. Push the latest project files, including `render.yaml` and the updated `requirements.txt`, to your GitHub repository.
2. Create or sign in to a Render account and connect your GitHub account.
3. In Render, choose **New → Blueprint**, select the GitHub repository, and apply the Blueprint. You can also create a **Web Service** manually with Python runtime, build command `pip install -r requirements.txt`, and start command `gunicorn --bind 0.0.0.0:$PORT app:app`.
4. In the Render service settings, add the environment variable `FLASK_SECRET_KEY` with a long random value. Keep that value private.
5. Wait for the deploy to finish, then open the `onrender.com` URL shown in the service dashboard. The `/health` route is configured as the health check.

Render's free web services use temporary local storage. This app's SQLite database is stored locally, so records may be lost when the service restarts, spins down, or redeploys. Use this deployment for a classroom demo with sample data only. For records that must persist, move the app to a persistent database such as PostgreSQL or use hosting with persistent disk storage.

## Deploy to PythonAnywhere

PythonAnywhere supports Flask apps and SQLite files. These steps use a free PythonAnywhere account; free accounts have limited CPU, storage, and a one-month web app expiry/renewal period.

1. Create or sign in to your PythonAnywhere account. Upload this ZIP to your account's home folder using the **Files** page.
2. Open **Consoles → Bash** and run the commands below. Replace `3.13` with the Python version you select for the web app if it differs.

   ```bash
   mkdir -p ~/mysite
   unzip ~/ScholarTrack_PythonAnywhere.zip -d ~/mysite
   cd ~/mysite/ScholarTrack
   python3.13 -m venv ~/.virtualenvs/scholartrack
   source ~/.virtualenvs/scholartrack/bin/activate
   pip install -r requirements.txt
   python seed_students.py
   ```

3. Open **Web → Add a new web app → Next → Manual configuration**, then choose the same Python version used for the virtual environment.
4. In the web app's **Virtualenv** field, enter `/home/YOUR_USERNAME/.virtualenvs/scholartrack`, replacing `YOUR_USERNAME` with your PythonAnywhere username.
5. Open the web app's **WSGI configuration file** and set the project path and Flask application import as follows, replacing the username:

   ```python
   import sys
   path = "/home/YOUR_USERNAME/mysite/ScholarTrack"
   if path not in sys.path:
       sys.path.insert(0, path)
   from app import app as application
   ```

6. Save the WSGI file, return to the **Web** tab, and click **Reload**. Open `https://YOUR_USERNAME.pythonanywhere.com` to check the app.

The SQLite database is created in the project folder. Run `python seed_students.py` from the project directory to load the bundled sample dataset; duplicate roll numbers are skipped.

## Uploading to GitHub

Include `app.py`, `requirements.txt`, `README.md`, `PROJECT_REPORT.md`, `.gitignore`, `static/`, and `templates/`. Do not upload `.venv/`, `students.db`, or `__pycache__/`.

## Before submitting

- Fill in your name, roll number, class, institution, and submission date in `PROJECT_REPORT.md`.
- Run the app and demonstrate adding, searching, editing, and deleting a record.
- The built-in Flask development server is for local classroom demonstration, not public production hosting.
