import re
import sqlite3
from contextlib import closing

from flask import Flask, abort, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash

from db import DB_PATH, init_db

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024
app.config["TRUSTED_HOSTS"] = ["127.0.0.1", "192.168.1.195", "192.168.253.133"]
ALLOWED_ORIGINS = {"https://192.168.1.195", "https://192.168.253.133"}

init_db()


@app.before_request
def check_origin():
    if request.method == "POST":
        if request.headers.get("Origin") not in ALLOWED_ORIGINS:
            abort(403, description="Invalid request origin. Use the HTTPS site.")


@app.after_request
def security_headers(response):
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; frame-ancestors 'none'; form-action 'self'"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/")
def home():
    return redirect(url_for("register"))


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    username = ""
    status = 200

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not re.fullmatch(r"[A-Za-z0-9_]{3,32}", username):
            error = "Username: 3-32 English letters, digits or underscores."
            status = 400
        elif not 15 <= len(password) <= 128:
            error = "Password must contain 15-128 characters."
            status = 400
        else:
            password_hash = generate_password_hash(password, method="scrypt")
            try:
                with closing(sqlite3.connect(DB_PATH)) as connection:
                    with connection:
                        connection.execute(
                            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                            (username, password_hash),
                        )
            except sqlite3.IntegrityError:
                error = "That username is already taken."
                status = 409
            else:
                return redirect(url_for("register", created="1"), code=303)

    return render_template(
        "register.html",
        error=error,
        username=username,
        created=request.args.get("created") == "1",
    ), status
from auth import auth
app.register_blueprint(auth)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["5 per minute"],
    default_limits_exempt_when=lambda: (
        request.method != "POST"
        or request.endpoint not in {"auth.login", "register"}
    ),
    storage_uri="memory://",
    strategy="moving-window",
    headers_enabled=True,
)
