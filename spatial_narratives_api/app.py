from flask import Flask, request, render_template, jsonify
import sqlite3 as db
import psycopg2

app = Flask(__name__)

def db_connection():
    # conn = None
    # while True:
    try:
        conn = psycopg2.connect(host="0.0.0.0",
                                database="lakedistrict",
                                user="root",
                                password="root1!")
        # if conn:
        #     break
        
    except BaseException as e:
        print(e)
        # exit(0)
    print(conn)    
    return conn
        

@app.route("/")
def home():
    return render_template("home.html", name="")


@app.route('/search', methods=['GET'])
def search():
    conn = db_connection()
    cur = conn.cursor()
    term = request.args.get("search")

    statement = f"""
            select text,
            ts_rank(search, websearch_to_tsquery('english', '{term}')) +
            ts_rank(search, websearch_to_tsquery('simple', '{term}'))
            as rank
            from public.data_paragraphs 
            where search @@ websearch_to_tsquery('english', '{term}')
            or search @@ websearch_to_tsquery('simple', '{term}')
            order by rank desc;
            """

    cur.execute(statement)

    paragraphs = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('home.html', paragraphs=paragraphs, term=term)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8100, debug=True)