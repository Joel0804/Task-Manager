import sqlite3
from flask import Flask, request, jsonify, session
import hashlib
DB_PATH = "database.db" # this is file name

# function allows you talk to database
def get_db():
    conn = sqlite3.connect(DB_PATH) # this open file and create if doesnt exist
    conn.row_factory = sqlite3.Row # changes row[0] --> row[id] easier to read
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                pw_hash TEXT NOT NULL
                );
            CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0,
                priority TEXT NOT NULL DEFAULT 'medium',
                created_at TEXT NOT NULL DEFAULT(datetime('now')),
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
            """)
    conn.commit() #save changes without this written wont get saved
    conn.close() 
    print("Database ready")
    
app = Flask(__name__) # tells flask to start  web application
app.secret_key = 'devkey'

@app.route("/register", methods=["POST"]) # post to submit
def register(): 
    data = request.get_json()# gets data in json format it converts into dictionary
    username = data["username"] 
    password = data["password"]
    
    pw_hash = hashlib.sha256(password.encode()).hexdigest() 
    # .encode() — converts the string to bytes (sha256 needs bytes, not a string)
    #hashlib.sha256(...) — runs the hashing algorithm 
    #.hexdigest() — converts the result to a readable string
    conn = get_db()
    try:
        conn.execute(
        """INSERT INTO users(username, pw_hash) VALUES (?, ?)""" , 
        (username, pw_hash)
        )
        conn.commit()
        jsonify({"message": "Account created!"})
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already taken"}), 409
    finally:
        conn.close()
        
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    
    pw_hash = hashlib.sha256(password.encode()).hexdigest()

    conn = get_db()
    try:
        user = conn.execute("SELECT * FROM users WHERE username = ?", 
                     (username, )).fetchone()
    finally:
        conn.close()
    if user is None:
         return jsonify({"error": "User not found"}), 401
    
    if user["pw_hash"] != pw_hash:
        return jsonify({"error": "Wrong password"}), 401
    
    session["user_id"] = user["id"]
    session["username"] = user["username"]

    return jsonify({"message": f"Welcome {username}!"})


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})
  
   
@app.route('/me', methods=["GET"])
def me():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401
    return jsonify({"username": session["username"]})
    

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
    




