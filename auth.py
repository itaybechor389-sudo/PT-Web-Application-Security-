import hashlib
import hmac
import re
import secrets
import sqlite3
import time
from contextlib import closing

from flask import Blueprint, abort, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from db import DB_PATH

auth = Blueprint("auth", __name__)
COOKIE_NAME = "pt_session"
SESSION_SECONDS = 30 * 60
DUMMY_HASH = generate_password_hash(secrets.token_urlsafe(32), method="scrypt")


def open_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def token_hash(token):
    return hashlib.sha256(token.encode()).hexdigest()


def logout_csrf(token):
    return hmac.new(token.encode(), b"logout", hashlib.sha256).hexdigest()


def current_user():
    token = request.cookies.get(COOKIE_NAME, "")
    if not re.fullmatch(r"[A-Za-z0-9_-]{43}", token):
        return None

    with closing(open_db()) as connection:
        return connection.execute(
            """
            SELECT users.id, users.username
            FROM sessions
            JOIN users ON users.id = sessions.user_id
            WHERE sessions.token_hash = ? AND sessions.expires_at > ?
            """,
            (token_hash(token), int(time.time())),
        ).fetchone()


@auth.route("/login", methods=["GET", "POST"])
def login():
    error = None
    status = 200

    if request.method == "GET" and current_user() is not None:
        return redirect(url_for("auth.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = None

        if re.fullmatch(r"[A-Za-z0-9_]{3,32}", username):
            with closing(open_db()) as connection:
                user = connection.execute(
                    "SELECT id, password_hash FROM users WHERE username = ?",
                    (username,),
                ).fetchone()

        stored_hash = user["password_hash"] if user is not None else DUMMY_HASH
        valid = 15 <= len(password) <= 128 and check_password_hash(
            stored_hash, password
        )

        if user is not None and valid:
            token = secrets.token_urlsafe(32)
            old_token = request.cookies.get(COOKIE_NAME, "")
            now = int(time.time())

            with closing(open_db()) as connection:
                with connection:
                    connection.execute(
                        "DELETE FROM sessions WHERE expires_at <= ? OR token_hash = ?",
                        (now, token_hash(old_token)),
                    )
                    connection.execute(
                        "INSERT INTO sessions (token_hash, user_id, expires_at) "
                        "VALUES (?, ?, ?)",
                        (token_hash(token), user["id"], now + SESSION_SECONDS),
                    )

            response = redirect(url_for("auth.dashboard"), code=303)
            response.set_cookie(
                COOKIE_NAME,
                token,
                max_age=SESSION_SECONDS,
                httponly=True,
                samesite="Lax",
                secure=True,  # Local HTTP; enable Secure when we add HTTPS.
                path="/",
            )
            return response

        error = "Incorrect username or password."
        status = 401

    return render_template("login.html", error=error), status


@auth.get("/dashboard")
def dashboard():
    user = current_user()
    if user is None:
        response = redirect(url_for("auth.login"))
        response.delete_cookie(COOKIE_NAME, path="/")
        return response

    token = request.cookies[COOKIE_NAME]
    return render_template(
        "dashboard.html",
        username=user["username"],
        csrf_token=logout_csrf(token),
    )


@auth.post("/logout")
def logout():
    token = request.cookies.get(COOKIE_NAME, "")

    if current_user() is not None:
        supplied = request.form.get("csrf_token", "")
        if not re.fullmatch(r"[0-9a-f]{64}", supplied):
            abort(403)
        if not hmac.compare_digest(supplied, logout_csrf(token)):
            abort(403)

    if token:
        with closing(open_db()) as connection:
            with connection:
                connection.execute(
                    "DELETE FROM sessions WHERE token_hash = ?",
                    (token_hash(token),),
                )

    response = redirect(url_for("auth.login"), code=303)
    response.delete_cookie(COOKIE_NAME, path="/", httponly=True, samesite="Lax")
    return response
