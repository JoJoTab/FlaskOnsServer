from flask import Flask, request, jsonify
import pymysql
import json

app = Flask(__name__)

con = pymysql.connect(host='localhost', user='root', password='a980911', db='react', charset='utf8',
                          autocommit=True, cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def home():
    return "Hello Flask Server!"

@app.route('/api/get', methods=["GET", "POST"])
def DB_get():
    # DB 연결
    conn = pymysql.connect(host='localhost', user='root', password='a980911', db='react', charset='utf8',
                           autocommit=True, cursorclass=pymysql.cursors.DictCursor)
    # SQL 쿼리 작성
    sql = 'SELECT * FROM table1'
    # 데이터베이스에 insert
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            conn.commit()
            data = {"data": cursor.fetchall()}
            json_data = json.dumps(data, default=str, ensure_ascii=False)
    except Exception as e:
        conn.rollback()
        json_data = {"status": "error", "message": str(e)}
    finally:
        conn.close()
    # 결과 반환
    return json_data

@app.route('/api/insert', methods=["GET", "POST"])
def DB_insert():
    # 요청받은 JSON 데이터 파싱
    data = request.get_json()
    title = data['title']
    content = data['content']
    writer = data['writer']
    ndate = data['ndate']
    # SQL 쿼리 작성
    sql = "INSERT INTO table1 (title, content, writer, ndate) VALUES (%s, %s, %s, %s)"
    val = (title, content, writer, ndate)
    # DB 연결
    conn = pymysql.connect(host='localhost', user='root', password='a980911', db='react', charset='utf8',
                          autocommit=True, cursorclass=pymysql.cursors.DictCursor)
    # 데이터베이스에 insert
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, val)
            conn.commit()
            result = {"status": "success", "message": "Data inserted"}
    except Exception as e:
        conn.rollback()
        result = {"status": "error", "message": str(e)}
    finally:
        conn.close()

    # 결과 반환
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
    # debug=True, host="localhost", port=4000

