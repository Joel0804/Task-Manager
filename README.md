# Task Manager

A full stack web application that allows user to Create read update delete task

## Tech Stack

Backend — Python, Flask
Database — SQLite (via Python's built-in sqlite3)
Frontend — HTML, CSS, JavaScript (vanilla)

## What it does

Register and log in with a username and password
Add, complete, and delete tasks
Each user only sees their own tasks
Priority levels (low, medium, high) with colour coding
Fully responsive — works on mobile and desktop

## How to run
1. Clone or download the project

2. Create a virtual environment

python -m venv .venv

3. Activate it

Windows:
bash.venv\Scripts\activate

Mac/Linux:
bashsource .venv/bin/activate

4. Install dependencies

bashpip install flask

5. Run the app

python app.py

6. Open your browser

http://localhost:5000

The database file tasks.db is created automatically on first run.