
import sqlite3
from pathlib import Path

from flask import Flask, redirect, render_template_string, request, url_for

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "comments.db"

PAGE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Laboratorio Stored XSS</title>
</head>
<body>
    <h1>Laboratorio de comentarios</h1>

    <form method="POST" action="/comments">
        <label for="comment">Escribe un comentario:</label>
        <input id="comment" name="comment" required>
        <button type="submit">Publicar</button>
    </form>

    <h2>Comentarios publicados</h2>
    <ul>
        {% for comment in comments %}
            <li>{{ comment }}</li>
        {% else %}
            <li>Aún no hay comentarios.</li>
        {% endfor %}
    </ul>
</body>
</html>
"""


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL
            )
            """
        )


@app.route("/", methods=["GET"])
def index():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT content FROM comments ORDER BY id"
        ).fetchall()

    comments = [row["content"] for row in rows]
    return render_template_string(PAGE, comments=comments)


@app.route("/comments", methods=["POST"])
def add_comment():
    comment = request.form.get("comment", "")

    with get_connection() as connection:
        connection.execute(
            "INSERT INTO comments (content) VALUES (?)",
            (comment,),
        )

    return redirect(url_for("index"))


init_db()


if __name__ == "__main__":
    app.run(debug=False)
