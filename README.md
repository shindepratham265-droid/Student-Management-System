# Student Management System

A simple web-based Student Management System built with **Flask** and **Firebase Firestore**. It allows an administrator to **add, view, edit, search, and delete** student records through a clean Bootstrap 5 interface.

---

## Features

- **Dashboard** — Displays total student count with quick-navigation cards.
- **Add Student** — Register new students with validation and duplicate-ID prevention.
- **View Students** — Browse all student records in a responsive table.
- **Edit Student** — Update an existing student's details.
- **Delete Student** — Remove a student record with a confirmation prompt.
- **Search** — Find students by Student ID or Name.

---

## Technology Stack

| Layer      | Technology              |
|------------|-------------------------|
| Language   | Python 3.12+            |
| Backend    | Flask                   |
| Database   | Firebase Cloud Firestore|
| Frontend   | HTML5, CSS3, Bootstrap 5|
| Security   | Flask-WTF (CSRF)        |

---

## Project Structure

```
student_management_system/
├── app.py                  # Main Flask application
├── firebase_config.py      # Firebase initialization module
├── requirements.txt        # Python dependencies
├── .env.example            # Example environment variables
├── .gitignore              # Git ignore rules
├── README.md               # This file
├── templates/
│   ├── base.html           # Base layout template
│   ├── dashboard.html      # Dashboard page
│   ├── students.html       # Student list + search
│   ├── add_student.html    # Add student form
│   └── edit_student.html   # Edit student form
└── static/
    └── css/
        └── style.css       # Custom styles
```

---

## Setup Instructions (Windows)

### 1. Install Python

Download and install **Python 3.12+** from [python.org](https://www.python.org/downloads/).  
During installation, check **"Add Python to PATH"**.

Verify:
```cmd
python --version
```

### 2. Clone or Download the Project

Place the project folder on your desktop or any preferred location.

### 3. Create a Virtual Environment

Open **Command Prompt** and navigate to the project folder:

```cmd
cd "C:\Users\YourUsername\Desktop\Student Management System"
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` at the beginning of your command prompt.

### 4. Install Dependencies

```cmd
pip install -r requirements.txt
```

### 5. Set Up Firebase

#### 5.1 Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/).
2. Click **"Add project"** and follow the prompts.
3. Give your project a name (e.g., `student-management-system`).
4. Disable Google Analytics (optional for this project).
5. Click **Create project**.

#### 5.2 Enable Cloud Firestore

1. In your Firebase project, click **"Build"** → **"Firestore Database"** in the left sidebar.
2. Click **"Create database"**.
3. Choose **"Start in test mode"** (for development only).
4. Select a Firestore location closest to you.
5. Click **Enable**.

#### 5.3 Generate a Service Account Key

1. In the Firebase Console, click the **gear icon** (⚙️) → **"Project settings"**.
2. Go to the **"Service accounts"** tab.
3. Click **"Generate new private key"**.
4. A JSON file will be downloaded. **Keep this file safe and never share it.**
5. Move the JSON file into your project folder (e.g., `serviceAccountKey.json`).

### 6. Configure Environment Variables

1. Copy the example environment file:
   ```cmd
   copy .env.example .env
   ```
2. Open `.env` in a text editor and update it:
   ```
   FIREBASE_CREDENTIALS=serviceAccountKey.json
   SECRET_KEY=my-super-secret-key-12345
   ```
   - Set `FIREBASE_CREDENTIALS` to the path of your downloaded JSON key file.
   - Set `SECRET_KEY` to any random string.

### 7. Run the Application

```cmd
python app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
```

### 8. Open in Browser

Open your browser and go to:
```
http://127.0.0.1:5000
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'flask'` | Activate your virtual environment: `venv\Scripts\activate`, then run `pip install -r requirements.txt`. |
| `FIREBASE_CREDENTIALS environment variable is not set` | Create a `.env` file with the correct path to your service account JSON key. |
| `Firebase service account file not found` | Double-check the file path in your `.env` file. Use a relative path (e.g., `serviceAccountKey.json`) if the file is in the project folder. |
| `Failed to initialize Firebase` | Ensure your service account JSON file is valid and not corrupted. Re-download from Firebase Console if needed. |
| `Address already in use` | Another application is using port 5000. Close it or run Flask on a different port: `flask run --port 5001`. |
| `TemplateNotFound` | Make sure the `templates/` folder exists in the project directory with all `.html` files. |
| Page styles not loading | Make sure the `static/css/style.css` file exists and your browser cache is cleared. |

---

## Security Notes

- **Never commit** your Firebase service account JSON key to GitHub.
- The `.gitignore` file is configured to exclude `.json` files and `.env`.
- CSRF protection is enabled via Flask-WTF.
- All form data is validated on the server side.
- Delete operations require POST requests to prevent accidental deletion.

---

## License

This project is intended for educational purposes as a college mini-project.
