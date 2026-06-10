# python -m venv venv → 가상환경 만들기
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser → 파워쉘에서 실행 권한 설정
# .\venv\Scripts\Activate.ps1
# python app.py
# http://localhost:5000

import os

from flask import Flask, render_template, request
import psycopg2
import psycopg2.extras
import pandas as pd


app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = os.environ.get("DATABASE_URL")


def get_db_connection():
    if DATABASE_URL:
        conn = psycopg2.connect(DATABASE_URL)
    else:
        conn = psycopg2.connect(
            host="localhost",
            database="db_project",
            user="postgres",
            password="darkk0729",
            port=5432
        )
    return conn


def import_csv_data():
    works_path = os.path.join(BASE_DIR, "data", "works.csv")
    articles_path = os.path.join(BASE_DIR, "data", "articles.csv")

    print("현재 작업 폴더:", os.getcwd())
    print("works.csv 실제 경로:", works_path)
    print("articles.csv 실제 경로:", articles_path)

    works_df = pd.read_csv(works_path)
    articles_df = pd.read_csv(articles_path)

    print("articles.csv 컬럼:", articles_df.columns.tolist())
    print("articles.csv 첫 행 published_at:", articles_df.loc[0, "published_at"])
    print("articles.csv 첫 행 summary:", articles_df.loc[0, "summary"])

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # 기존 데이터 삭제
        cur.execute("DELETE FROM bookmarks;")
        cur.execute("DELETE FROM notes;")
        cur.execute("DELETE FROM article_tags;")
        cur.execute("DELETE FROM work_articles;")
        cur.execute("DELETE FROM articles;")
        cur.execute("DELETE FROM works;")
        cur.execute("DELETE FROM users;")

        # 기본 사용자 추가
        cur.execute("INSERT INTO users (username) VALUES (%s);", ("test_user",))

        # works.csv import
        for _, row in works_df.iterrows():
            cur.execute("""
                INSERT INTO works (
                    title,
                    type,
                    release_date,
                    status,
                    description,
                    source_url,
                    franchise
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (
                row["title"],
                row["type"],
                row["release_date"],
                row["status"],
                row["description"],
                row["source_url"],
                row.get("franchise", "Star Wars")
            ))

        # articles.csv import
        for _, row in articles_df.iterrows():
            cur.execute("""
                INSERT INTO articles (
                    title,
                    title_ko,
                    source_name,
                    source_url,
                    image_url,
                    published_at,
                    summary,
                    summary_ko,
                    category,
                    franchise
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                row["title"],
                row["title_ko"],
                row["source_name"],
                row["source_url"],
                row.get("image_url", ""),
                row["published_at"],
                row["summary"],
                row["summary_ko"],
                row["category"],
                row.get("franchise", "Star Wars")
            ))

        conn.commit()

    except Exception as e:
        conn.rollback()
        print("IMPORT 실패:", e)
        raise

    finally:
        cur.close()
        conn.close()


@app.route("/")
def index():
    keyword = request.args.get("keyword", "")
    category = request.args.get("category", "")
    franchise = request.args.get("franchise", "starwars")

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    query = """
        SELECT
            article_id,
            title,
            title_ko,
            source_name,
            source_url,
            image_url,
            published_at,
            summary,
            summary_ko,
            category,
            franchise
        FROM articles
        WHERE 1=1
    """
    params = []

    if franchise == "marvel":
        query += " AND franchise = %s"
        params.append("Marvel")
    else:
        query += " AND franchise = %s"
        params.append("Star Wars")

    if keyword:
        query += """
            AND (
                title ILIKE %s
                OR title_ko ILIKE %s
                OR summary ILIKE %s
                OR summary_ko ILIKE %s
                OR source_name ILIKE %s
            )
        """
        search_keyword = f"%{keyword}%"
        params.extend([
            search_keyword,
            search_keyword,
            search_keyword,
            search_keyword,
            search_keyword
        ])

    if category:
        query += " AND category = %s"
        params.append(category)

    query += " ORDER BY published_at DESC;"

    cur.execute(query, params)
    articles = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "index.html",
        articles=articles,
        keyword=keyword,
        selected_category=category,
        selected_franchise=franchise
    )

@app.route("/works")
def works():
    franchise = request.args.get("franchise", "starwars")
    selected_franchise_name = "Marvel" if franchise == "marvel" else "Star Wars"

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT
            work_id,
            title,
            type,
            release_date,
            status,
            description,
            source_url,
            franchise
        FROM works
        WHERE franchise = %s
        ORDER BY release_date DESC;
    """, (selected_franchise_name,))

    works = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "works.html",
        works=works,
        selected_franchise=franchise
    )


@app.route("/import")
def import_data():
    import_csv_data()
    return "CSV 데이터가 PostgreSQL DB에 import 되었습니다."


if __name__ == "__main__":
    app.run(debug=True)